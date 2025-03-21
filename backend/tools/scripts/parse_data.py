import asyncio
import json
from collections import defaultdict
from datetime import datetime

from db import collection_structures as coll
from shared.models import cricket


async def parse():
    with open('/opt/projects/gameviz/backend/tools/ipl.json', 'r') as file:
        data = json.load(file)

        match_meta_data = {
            "venue": None,
            "series": None,
            "teams": {},
            "umpires": {},
            "players": {},
        }
        match_info = data.get("info")

        venue = await _get_stadium(match_info["venue"], match_info['city'])
        match_meta_data["venue"] = venue

        series = await _get_series(match_info["event"]["name"],
                                   match_info["season"],
                                   match_info['gender'],
                                   match_info['match_type'])

        team_players = []
        for team in match_info["teams"]:
            team_data = await _get_teams(team, match_info['team_type'])
            if team_data.id not in series.teams:
                series.teams.append(team_data.id)

            match_meta_data["teams"][team] = team_data

            players = []
            for player in match_info["players"][team_data.name]:
                player_data = await _get_players(player,
                    match_info["registry"]["people"].get(player, {}),
                    team_data.id)
                match_meta_data["players"][player] = player_data
                players.append(player_data.id)

            team_player = cricket.TeamPlayers(players=players, team_id=team_data.id)
            team_players.append(team_player)

        await series.update_in_db()
        match_meta_data["series"] = series

        query = {
            coll.Matches.SERIES_ID: series.id,
            coll.Matches.MATCH_NUMBER: match_info["event"]["match_number"]
        }

        match_data = await cricket.Match.read_one_from_db(query)

        if match_data:
            delete_query = {
                coll.Innings.MATCH_ID: match_data.id
            }

            innings = await cricket.Innings.read_many_from_db(delete_query)
            for inning in innings:
                await cricket.Delivery.delete_many_from_db({
                    coll.Delivery.INNINGS_ID: inning.id
                })

            await cricket.Innings.delete_many_from_db(delete_query)
            await cricket.PlayerScorecard.delete_many_from_db(delete_query)
            await cricket.Match.delete_many_from_db(query)

        officials = {}
        for key, umpires in match_info["officials"].items():
            umpires_data = [await _get_umpires(umpire) for umpire in umpires]
            match_meta_data["umpires"].update({umpire.name: umpire for umpire in umpires_data})
            officials[key] = [umpire.id for umpire in umpires_data]

        officials_model = cricket.Officials(
            match_referees=officials.get("match_referees"),
            umpires=officials.get("umpires"),
            tv_umpires=officials.get("tv_umpires"),
            reserve_umpires=officials.get("reserve_umpires"),
        )

        outcome = match_info["outcome"]
        outcome_model = cricket.Outcome(
            winner=match_meta_data["teams"][outcome["winner"]].id,
            by_runs=outcome.get("by", {}).get("runs", 0),
            by_wickets=outcome.get("by", {}).get("wickets", 0),
        )

        toss = cricket.Toss(
            decision=match_info["toss"]["decision"],
            team=match_meta_data["teams"].get(match_info["toss"]["winner"]).id
        )

        match = cricket.Match(
            dates=[datetime.strptime(date, "%Y-%m-%d") for date in match_info["dates"]],
            match_number=match_info["event"]["match_number"],
            outcome=outcome_model,
            player_of_match=match_meta_data["players"].get(match_info.get("player_of_match", [None])[0]).id,
            series=series.id,
            team_1=team_players[0],
            team_2=team_players[1],
            umpires=officials_model,
            venue=venue.id,
            toss=toss
        )
        await match.save_to_db()

        # Process Innings
        await _process_innings(data["innings"], match.id, match_meta_data)

        print("Match and Stats stored successfully!")


async def _get_stadium(name: str,
                       city: str) -> cricket.Stadium:
    split_name = name.split(',')

    query = {
        coll.Stadiums.NAME: split_name[0],
        coll.Stadiums.CITY: city
    }

    stadium = await cricket.Stadium.read_one_from_db(query)
    if not stadium:
        stadium = cricket.Stadium(
            name=split_name[0],
            locality=split_name[1] if len(split_name) > 1 else "",
            city=city
        )
        await stadium.save_to_db()

    return stadium


async def _get_series(name: str,
                      season: str,
                      gender: str,
                      match_type: str) -> cricket.Series:
    query = {
        coll.Series.NAME: name,
        coll.Series.SEASON: season,
        coll.Series.GENDER: gender,
        coll.Series.MATCH_TYPE: match_type,
    }

    series = await cricket.Series.read_one_from_db(query)

    if not series:
        series = cricket.Series(name=name,
                                season=season,
                                gender=gender,
                                match_type=match_type)
        await series.save_to_db()

    return series


async def _get_teams(name: str,
                     team_type: str) -> cricket.Team:
    query = {
        coll.Teams.NAME: name,
        coll.Teams.TEAM_TYPE: team_type
    }

    team = await cricket.Team.read_one_from_db(query)
    if not team:
        team = cricket.Team(
            name=name,
            team_type=team_type
        )
        await team.save_to_db()

    return team


async def _get_players(name: str,
                       cric_sheet_id: dict,
                       team_id: str) -> cricket.Player:
    query = {
        coll.Players.NAME: name,
        coll.Players.CRIC_SHEET_ID: cric_sheet_id
    }

    player = await cricket.Player.read_one_from_db(query)
    if not player:
        player = cricket.Player(
            name=name,
            team_id=[team_id],
            cric_sheet_id=cric_sheet_id
        )
        await player.save_to_db()
    else:
        if team_id not in player.teams:
            player.teams.append(team_id)
            await player.update_in_db()

    return player


async def _get_umpires(name: str) -> cricket.Umpire:
    query = {
        coll.Umpires.NAME: name,
    }

    umpire = await cricket.Umpire.read_one_from_db(query)
    if not umpire:
        umpire = cricket.Umpire(
            name=name
        )
        await umpire.save_to_db()

    return umpire


async def _process_innings(innings_data, match_id, match_meta_data):
    """Processes innings, deliveries, and player scorecards"""

    player_stats = defaultdict(lambda: {
        "batting": {
            "runs": 0,
            "balls": 0,
            "fours": 0,
            "sixes": 0,
            "dot_balls": 0,
            "is_out": False,
            "dismissal_type": "",
            "fielders_involved": []
        },
        "bowling": {
            "overs": 0.0,
            "balls_bowled": 0,
            "wickets": 0,
            "runs": 0,
            "maidens": 0,
            "dot_balls": 0,
            "fours": 0,
            "sixes": 0,
            "economy": 0.0
        },
        "fielding": {
            "catches": 0,
            "run_outs": 0,
            "stumping": 0
        }
    })

    for innings in innings_data:
        innings_team = innings["team"]

        innings_model = cricket.Innings(
            match_id=match_id,
            batting_team=match_meta_data["teams"][innings_team].id
        )
        await innings_model.save_to_db()

        total_runs, total_wickets, overs_played_balls = 0, 0, 0  # Track balls bowled

        overs_played = 0

        for over_index, over in enumerate(innings.get("overs", [])):
            balls_in_over = 0  # Track balls per over for maidens

            for delivery_num, delivery in enumerate(over.get("deliveries", []), start=1):
                batter, bowler = delivery["batter"], delivery["bowler"]
                runs_scored = delivery["runs"]["batter"]
                total_runs += delivery["runs"]["total"]

                is_wide = "extras" in delivery and "wides" in delivery["extras"]
                is_no_ball = "extras" in delivery and "noballs" in delivery["extras"]
                is_leg_bye = "extras" in delivery and "legbyes" in delivery["extras"]
                is_byes = "extras" in delivery and "byes" in delivery["extras"]

                batter_stats = player_stats[batter]["batting"]
                bowler_stats = player_stats[bowler]["bowling"]

                if not is_wide and not is_no_ball:
                    batter_stats["balls"] += 1
                    bowler_stats["balls_bowled"] += 1
                    bowler_stats["dot_balls"] += (1 if runs_scored == 0 else 0)

                if not is_byes and not is_leg_bye:
                    batter_stats["runs"] += runs_scored
                    bowler_stats["runs"] += delivery["runs"]["total"]

                batter_stats["fours"] += (1 if runs_scored == 4 else 0)
                batter_stats["sixes"] += (1 if runs_scored == 6 else 0)
                batter_stats["dot_balls"] += (1 if runs_scored == 0 else 0)

                bowler_stats["wickets"] += len(delivery["wickets"]) if "wickets" in delivery else 0
                bowler_stats["fours"] += (1 if runs_scored == 4 else 0)
                bowler_stats["sixes"] += (1 if runs_scored == 6 else 0)

                # Check if batter got out
                if "wickets" in delivery:
                    total_wickets += len(delivery["wickets"])
                    dismissal = delivery["wickets"][0]
                    batter_stats["is_out"] = True
                    batter_stats["dismissal_type"] = dismissal["kind"]

                    # Extract fielders involved in dismissal
                    fielders_involved = [
                        match_meta_data["players"][fielder["name"]].id
                        for fielder in dismissal.get("fielders", []) if "name" in fielder
                    ]
                    batter_stats["fielders_involved"] = fielders_involved

                    dismissal_type = dismissal["kind"]
                    for fielder in dismissal.get("fielders", []):
                        fielder_name = fielder.get("name")
                        if not fielder_name:
                            continue  # Skip if fielder name is missing

                        fielder_stats = player_stats[fielder_name]["fielding"]
                        if dismissal_type == "caught":
                            fielder_stats["catches"] += 1
                        elif dismissal_type == "run out":
                            fielder_stats["run_outs"] += 1
                        elif dismissal_type == "stumped":
                            fielder_stats["stumping"] += 1

                # Update bowling stats
                # Track balls per over for maidens
                balls_in_over += 1

                # ✅ Update bowler's overs in decimal format (e.g., 2.3 for 2 overs, 3 balls)
                bowler_stats["overs"] = (bowler_stats["balls_bowled"] // 6) + (bowler_stats["balls_bowled"] % 6) / 10.0

                # ✅ Calculate Economy Rate
                if bowler_stats["overs"] > 0:
                    bowler_stats["economy"] = round(bowler_stats["runs"] / bowler_stats["overs"], 2)

                # Store delivery
                await _store_delivery(delivery, innings_model.id, over["over"], delivery_num, match_meta_data)

                # ✅ Check for Maiden Over (zero runs in the over)
                if balls_in_over == 6 and sum(delivery["runs"]["total"] for delivery in over.get("deliveries", [])) == 0:
                    bowler_stats["maidens"] += 1  # Mark it as a maiden over

            if balls_in_over == 6:
                overs_played = over_index + 1.0  # Move to next over
            else:
                overs_played = over_index + (balls_in_over / 10)  # Keep decimal format

        # Step 5: Update Innings record with calculated values
        innings_model.total_runs = total_runs
        innings_model.wickets_lost = total_wickets
        innings_model.overs_played = overs_played
        await innings_model.update_in_db()

    # Step 6: Store player scorecards
    await _store_player_scorecards(player_stats, match_id, match_meta_data)


async def _store_player_scorecards(player_stats, match_id, match_meta_data):
    """Stores player scorecards based on dynamically calculated stats"""
    for player_name, stats in player_stats.items():
        player_id = match_meta_data["players"][player_name].id

        batting_stats = cricket.BattingStats(
            runs_scored=stats["batting"]["runs"],
            balls_faced=stats["batting"]["balls"],
            fours=stats["batting"]["fours"],
            sixes=stats["batting"]["sixes"],
            strike_rate=(stats["batting"]["runs"] / stats["batting"]["balls"] * 100) if stats["batting"]["balls"] > 0 else 0.0,
            dot_balls=stats["batting"]["dot_balls"],
            is_out=stats["batting"]["is_out"],
            dismissal_type=stats["batting"]["dismissal_type"],
            fielders_involved=stats["batting"]["fielders_involved"]
        ) if "batting" in stats else None

        bowling_stats = cricket.BowlingStats(
            overs_bowled=stats["bowling"]["overs"],
            wickets_taken=stats["bowling"]["wickets"],
            runs_conceded=stats["bowling"]["runs"],
            maidens=stats["bowling"]["maidens"],
            economy=(stats["bowling"]["runs"] / stats["bowling"]["overs"]) if stats["bowling"]["overs"] > 0 else 0.0,
            dot_balls=stats["bowling"]["dot_balls"],
            boundaries_conceded={
                "fours": stats["bowling"]["fours"],
                "sixes": stats["bowling"]["sixes"]
            }
        ) if "bowling" in stats else None

        fielding_stats = cricket.FieldingStats(
            catches_taken=stats["fielding"]["catches"],
            run_outs=stats["fielding"]["run_outs"],
            stumping=stats["fielding"]["stumping"]
        ) if "fielding" in stats else None

        player_scorecard = cricket.PlayerScorecard(
            player_id=player_id,
            match_id=match_id,
            team=" ",
            batting_stats=batting_stats,
            bowling_stats=bowling_stats,
            fielding_stats=fielding_stats
        )
        await player_scorecard.save_to_db()


async def _store_delivery(delivery, innings_id, over_number, delivery_number, match_meta_data):
    batter_id = match_meta_data["players"][delivery["batter"]].id
    bowler_id = match_meta_data["players"][delivery["bowler"]].id
    non_striker_id = match_meta_data["players"][delivery["non_striker"]].id
    delivery_model = cricket.Delivery(
        innings_id=innings_id,
        over_number=over_number,
        delivery_number=delivery_number,
        batter=batter_id,
        bowler=bowler_id,
        non_striker=non_striker_id,
        runs_by_batter=delivery["runs"]["batter"],
        extras=delivery["runs"].get("extras", 0),
        total_runs=delivery["runs"]["total"],
        is_wicket="wickets" in delivery,
        wicket_type=delivery.get("wickets", [{}])[0].get("kind", ""),
        fielders_involved=[match_meta_data["players"].get(fielder["name"], {}).id for fielder in delivery.get("wickets", [{}])[0].get("fielders", [])],
        is_wide=delivery.get("extras", {}).get("wides", 0) > 0,
        is_no_ball=delivery.get("extras", {}).get("noballs", 0) > 0,
        is_leg_bye=delivery.get("extras", {}).get("legbyes", 0) > 0,
        is_bye=delivery.get("extras", {}).get("byes", 0) > 0,
        penalty_runs=delivery.get("extras", {}).get("penalty", 0)
    )
    await delivery_model.save_to_db()






asyncio.run(parse())
