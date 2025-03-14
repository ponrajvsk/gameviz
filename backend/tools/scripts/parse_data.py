import asyncio
import json
import typing

from db import collection_structures as coll
from shared.models import cricket


async def parse():
    with open('/opt/projects/gameviz/backend/tools/ipl.json', 'r') as file:
        data = json.load(file)

        match_info = data.get("info")

        series = await _get_series(match_info["event"]["name"],
                                   match_info["season"],
                                   match_info['gender'],
                                   match_info['match_type'])

        for team in match_info["teams"]:
            team_data = await _get_teams(team,
                                         match_info['team_type'])
            if team_data.id not in series.teams:
                series.teams.append(team_data.id)

        print(f"Final series teams: {series.teams}")
        await series.update_in_db()


async def _get_series(name: str,
                      season: str,
                      gender: str,
                      match_type: str) -> typing.Optional[cricket.Series]:
    query = {
        coll.Series.NAME: name,
        coll.Series.SEASON: season,
        coll.Series.GENDER: gender,
        coll.Series.MATCH_TYPE: match_type,
    }

    series = await cricket.Series.read_from_db(query)

    if not series:
        series = cricket.Series(name=name,
                                season=season,
                                gender=gender,
                                match_type=match_type)
        await series.save_to_db()

    return series


async def _get_teams(name: str,
                     team_type: str):
    query = {
        coll.Teams.NAME: name,
        coll.Teams.TEAM_TYPE: team_type
    }

    team = await cricket.Team.read_from_db(query)
    if not team:
        team = cricket.Team(
            name=name,
            team_type=team_type
        )
        await team.save_to_db()

    return team


asyncio.run(parse())
