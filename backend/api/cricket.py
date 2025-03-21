from collections import defaultdict

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from shared.models import cricket

router = APIRouter()


@router.get("/scoreboard/{innings_id}", response_model=dict)
async def get_scoreboard(innings_id: str):
  try:
    innings_obj_id = ObjectId(innings_id)
  except:
    raise HTTPException(status_code=400, detail="Invalid innings_id")

  innings = await cricket.Innings.read_one_from_db({
    "_id": innings_obj_id
  })
  match = await cricket.Match.read_one_from_db({
    "_id": innings.match_id
  })

  players = await cricket.Player.read_many_from_db({
    "_id": {
      "$in": [*match.team_1.players, *match.team_2.players]
    }
  })

  player_data = {player.id: player for player in players}

  deliveries = await cricket.Delivery.read_many_from_db({
    "innings_id": innings_obj_id
  })
  if not deliveries:
    raise HTTPException(status_code=404, detail="No deliveries found for this innings")

  scoreboard = {
    "total_runs": 0,
    "total_wickets": 0,
    "batters": defaultdict(lambda: {
      "runs": 0,
      "balls": 0,
      "fours": 0,
      "sixes": 0,
      "dot_balls": 0,
      "strike_rate": 0.0,
      "player_id": ""
    }),
    "bowlers": defaultdict(lambda: {
      "runs_conceded": 0,
      "wickets": 0,
      "balls": 0,
      "overs": 0.0,
      "dot_balls": 0,
      "economy_rate": 0.0,
      "maiden_overs": 0,
      "player_id": ""
    }),
    "extras": {
      "wides": 0,
      "no_balls": 0,
      "leg_byes": 0,
      "byes": 0,
      "penalties": 0
    },
    "fall_of_wickets": [],
    "partnerships": []
  }

  current_partnership = 0
  partnership_batters = set()
  current_runs = 0

  bowler_over_runs = defaultdict(lambda: [])  # Tracks runs in each over per bowler

  for delivery in deliveries:
    batter_id = player_data[delivery.batter].name
    non_striker_id = player_data[delivery.non_striker].name
    bowler_id = player_data[delivery.bowler].name
    fielder_ids = [player_data[fielder].name for fielder in delivery.fielders_involved]

    scoreboard["batters"][batter_id]["player_id"] = str(delivery.batter)
    scoreboard["bowlers"][bowler_id]["player_id"] = str(delivery.bowler)

    total_runs_in_delivery = delivery.runs_by_batter + delivery.extras + delivery.penalty_runs
    current_runs += total_runs_in_delivery
    current_partnership += total_runs_in_delivery
    if batter_id not in partnership_batters:
      partnership_batters.add(batter_id)
    if non_striker_id not in partnership_batters:
      partnership_batters.add(non_striker_id)

    if not delivery.is_wide and not delivery.is_no_ball:
      scoreboard["batters"][batter_id]["balls"] += 1
      scoreboard["bowlers"][bowler_id]["dot_balls"] += (1 if not delivery.runs_by_batter else 0)
      scoreboard["batters"][batter_id]["dot_balls"] += (1 if not delivery.runs_by_batter else 0)

    if not delivery.is_leg_bye and not delivery.is_bye:
      scoreboard["bowlers"][bowler_id]["runs_conceded"] += total_runs_in_delivery

    scoreboard["batters"][batter_id]["runs"] += delivery.runs_by_batter

    if delivery.runs_by_batter == 4:
      scoreboard["batters"][batter_id]["fours"] += 1
    if delivery.runs_by_batter == 6:
      scoreboard["batters"][batter_id]["sixes"] += 1

    scoreboard["total_runs"] += total_runs_in_delivery

    # Track runs per over for maiden over calculation
    bowler_over_runs[bowler_id].append(total_runs_in_delivery)

    if delivery.is_wicket:
      scoreboard["total_wickets"] += 1
      scoreboard["bowlers"][bowler_id]["wickets"] += 1
      scoreboard["fall_of_wickets"].append({
        "runs_at_wicket": current_runs,
        "batter_out": batter_id
      })
      scoreboard["batters"][batter_id]["wicket"] = {
        "bowler": bowler_id,
        "wicket_type": delivery.wicket_type,
        "fielder_involved": fielder_ids
      }

      if len(partnership_batters) == 2:
        scoreboard["partnerships"].append({
          "batters": list(partnership_batters),
          "runs": current_partnership
        })

      current_partnership = 0
      partnership_batters = set()

    if delivery.is_wide:
      scoreboard["extras"]["wides"] += delivery.extras
    if delivery.is_no_ball:
      scoreboard["extras"]["no_balls"] += delivery.extras
    if delivery.is_leg_bye:
      scoreboard["extras"]["leg_byes"] += delivery.extras
    if delivery.is_bye:
      scoreboard["extras"]["byes"] += delivery.extras
    if delivery.penalty_runs > 0:
      scoreboard["extras"]["penalties"] += delivery.penalty_runs

    if not delivery.is_wide and not delivery.is_no_ball:
      scoreboard["bowlers"][bowler_id]["balls"] += 1

  if len(partnership_batters) == 2 and current_partnership > 0:
    scoreboard["partnerships"].append({
      "batters": list(partnership_batters),
      "runs": current_partnership
    })

  # Calculate bowling statistics (Economy, Overs, Maidens)
  for bowler_id in scoreboard["bowlers"]:
    balls_bowled = scoreboard["bowlers"][bowler_id]["balls"]
    overs = (balls_bowled // 6) + (balls_bowled % 6) / 6.0
    scoreboard["bowlers"][bowler_id]["overs"] = overs

    if overs > 0:
      scoreboard["bowlers"][bowler_id]["economy_rate"] = round(
        float(scoreboard["bowlers"][bowler_id]['runs_conceded']) / overs, 2
      )
    else:
      scoreboard["bowlers"][bowler_id]["economy_rate"] = 0.0

    # Calculate maiden overs
    maiden_overs = sum(1 for over in range(len(bowler_over_runs[bowler_id]) // 6)
                       if sum(bowler_over_runs[bowler_id][over * 6:(over + 1) * 6]) == 0)

    scoreboard["bowlers"][bowler_id]["maiden_overs"] = maiden_overs

  # Calculate batting strike rate
  for batter_id in scoreboard["batters"]:
    balls_faced = scoreboard["batters"][batter_id]["balls"]
    runs_scored = scoreboard["batters"][batter_id]["runs"]
    if balls_faced > 0:
      scoreboard["batters"][batter_id]["strike_rate"] = round(
        (runs_scored / balls_faced) * 100, 2
      )

  return scoreboard


@router.get("/series", response_model=list)
async def get_series():
  series = await cricket.Series.read_many_from_db({})
  a = []
  for serie in series:
    a.append({
      "id": str(serie.id),
      "name": serie.name,
      "season": serie.season
    })
  return a


@router.get("/series/{series_id}/matches", response_model=list)
async def get_matches(series_id: str):
  try:
    series_obj_id = ObjectId(series_id)
  except:
    raise HTTPException(status_code=400, detail="Invalid series_id")

  matches = await cricket.Match.read_many_from_db({
    "series": series_obj_id
  })
  a = []

  for match in matches:
    teams = await cricket.Team.read_many_from_db({
      "_id": {
        "$in": [match.team_1.team_id, match.team_2.team_id]
      }
    })
    venue = await cricket.Stadium.read_one_from_db({
      "_id": match.venue
    })

    innings = await cricket.Innings.read_many_from_db({
      "match_id": match.id
    })
    toss = {
      "winner": "",
      "decision": match.toss.decision
    }

    for team in teams:
      if team.id == match.toss.team:
        toss["winner"] = team.name
        break

    readable_date = match.dates[0].strftime("%B %d, %Y")
    inng = [str(inn.id) for inn in innings]
    a.append({
      "id": str(match.id),
      "match_number": match.match_number,
      "cric_sheet_id": match.cric_sheet_id,
      "name": " vs ".join([team.name for team in teams]),
      "innings": inng,
      "toss": toss,
      "date": readable_date,
      "venue": venue.name
    })
  return a


@router.get("/player/{player_id}", response_model=dict)
async def get_player(player_id: str):
  try:
    player_obj_id = ObjectId(player_id)
  except:
    raise HTTPException(status_code=400, detail="Invalid player_id")

  player = await cricket.Player.read_one_from_db({
    "_id": player_obj_id
  })

  if not player:
    raise HTTPException(status_code=404, detail="Player not found")

  return {
  "player_id": str(player.id),
  "personal_info": {
    "full_name": player.full_name or  player.name   ,
    "date_of_birth": player.date_of_birth.strftime("%B %d, %Y"),
    "role": "Batsman",
    "batting_style": "Right-handed",
    "bowling_style": "Right-arm medium"
  },
  "career_stats": {
    "matches": 500,
    "runs": 25000,
    "wickets": 50,
    "batting": [
      {
        "format": "Test",
        "matches": 111,
        "runs": 8676,
        "average": 49.95,
        "strikeRate": 55.70,
        "hundreds": 29,
        "fifties": 29,
        "highest": 254
      },
      {
        "format": "ODI",
        "matches": 275,
        "runs": 13027,
        "average": 57.38,
        "strikeRate": 93.62,
        "hundreds": 46,
        "fifties": 65,
        "highest": 183
      },
      {
        "format": "T20I",
        "matches": 115,
        "runs": 4008,
        "average": 52.73,
        "strikeRate": 137.96,
        "hundreds": 1,
        "fifties": 37,
        "highest": 122
      }
    ]
  },
  "recent_performances": [
    {
      "matchDate": "2024-01-15",
      "runs": 85,
      "wickets": 0
    },
    {
      "matchDate": "2024-01-10",
      "runs": 45,
      "wickets": 1
    }
  ]
}
