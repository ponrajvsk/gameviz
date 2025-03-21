import asyncio
import json
import re
import time
from datetime import datetime

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from shared import encryption
from shared.models import cricket


def extract_json(response_text):
  """
  Extracts the first valid JSON object from a text response.
  """
  try:
    match = re.search(r"\{[\s\S]*}", response_text)
    if match:
      json_str = match.group(0)
      return json.loads(json_str)
    else:
      raise ValueError("No valid JSON found in response")

  except json.JSONDecodeError as e:
    print(f"JSON Parsing Error: {e}")
    return {}


def fetch_player_info(player_name, team_name):
  """
  Fetches detailed cricket player information using Google's Gemini API.
  """
  api_key = "gAAAAABn3vI5tjHO4q0zmU02Ncee8t7U-732khmoY6TDpl55Fq_XD1_O96YcnaHXNVMxLeJx7mYfyfj9SVHJlvyTR3aXap8bfmu3iGpybmz4MZAek6GmAxJz80HNgPjhHATYsDMbI_bS"
  decrypted_key = encryption.decrypt_password(api_key)

  genai.configure(api_key=decrypted_key)

  model = genai.GenerativeModel("gemini-1.5-pro-latest")  # ✅ Use the latest available model

  prompt = f"""
    Provide detailed cricket information for {player_name.lower()} played in team {team_name} in JSON format.
    Include:
    - full_name
    - date_of_birth (YYYY-MM-DD)
    - batting_style
    - bowling_style
    - role (Batsman, Bowler, All-rounder, Wicketkeeper)
    - birth_place
    - playing role
    - nationality
    - age
    - education
    - nick names

    Example JSON Output:
    {{
        "full_name": "Sachin Tendulkar",
        "date_of_birth": "1973-04-24",
        "batting_style": "Right handed batsman",
        "bowling_style": "Right arm leg spin",
        "role": "Batsman",
        "birth_place": "Mumbai, Maharashtra, India"
        "playing_role": "Top order batsman"
        "nationality": "Indian
        "age": 48
        "education": "Bachelor of Commerce"
        "nick_names": ["Master Blaster", "Little Master"]
    }}
    """

  time.sleep(15)

  for attempt in range(3):
    try:
      response = model.generate_content(prompt)
      return extract_json(response.text)
    except ResourceExhausted:
      print(f"Quota exceeded! Retrying in {5 * (attempt + 1)} seconds...")
      time.sleep(5 * (attempt + 1))

  return {}


async def update_player_details():
  players = await cricket.Player.read_many_from_db({
    "age": 0
  })

  for player in players:
    print("Fetching for player:", player.name)
    teams = await cricket.Team.read_many_from_db({
      "_id": {
        "$in": player.teams
      }
    })
    team_names = ",".join([team.name for team in teams])

    player_info = fetch_player_info(player.name, team_names)
    player.age = int(player_info.get("age", 0))
    player.full_name = player_info.get("full_name", "")
    player.date_of_birth = datetime.strptime(player_info.get("date_of_birth"), "%Y-%m-%d") if player_info.get("date_of_birth") else datetime.now()
    player.batting_style = player_info.get("batting_style", "") if player_info.get("batting_style", "") else ""
    player.bowling_style = player_info.get("bowling_style", "") if player_info.get("bowling_style", "") else ""
    player.birth_place = player_info.get("birth_place", "") if player_info.get("birth_place", "") else ""
    player.playing_role = player_info.get("role", "") if player_info.get("role", "") else ""
    player.nationality = player_info.get("nationality", "") if player_info.get("nationality", "") else ""
    player.education = player_info.get("education", "") if player_info.get("education", "") else ""
    player.nick_names = player_info.get("nick_names", []) if player_info.get("nick_names", []) else []

    await player.update_in_db()


asyncio.run(update_player_details())
