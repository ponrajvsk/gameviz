import typing
from datetime import datetime

from bson import ObjectId

from db.db import Collections
from shared.models import cricket_enum
from shared.models.common import fields
from shared.models.common.base import BaseModel


class Team(BaseModel):
    collection_name = Collections.TEAMS.upper()

    country: typing.Optional[str]
    name: str
    team_type: str

    id = fields.ObjectIdField(desc="Id of the series")
    country = fields.StringField(desc="Country of the team", default="")
    name = fields.StringField(desc="Team name", mandatory=True)
    team_type = fields.StringField(desc="Type of the team.", mandatory=True)


class Player(BaseModel):
    collection_name = Collections.PLAYERS.upper()

    age: typing.Optional[str]
    batting_style: typing.Optional[str]
    bowling_style: typing.Optional[str]
    cric_sheet_id: str
    date_of_birth: typing.Optional[datetime]
    full_name: str
    name: str
    role: typing.Optional[str]
    teams: typing.List[str]

    id = fields.ObjectIdField(desc="Id of the series")
    age = fields.IntegerField(desc="Age of the player in year and days format", default=0)
    batting_style = fields.StringField(desc="Batting style (Right-hand, Left-hand)", default="")
    bowling_style = fields.StringField(desc="Bowling style (Off-spin, Leg-spin, etc.)", default="")
    cric_sheet_id = fields.StringField(desc="Id of the player in cricsheet", mandatory=True)
    date_of_birth = fields.DateTimeField(desc="Date of birth of the player", default=datetime.now())
    full_name = fields.StringField(desc="Full name of the player", default="")
    name = fields.StringField(desc="Full name of the player", mandatory=True)
    role = fields.StringField(desc="Player's role in the team", default="")
    teams = fields.ListField(ObjectId, desc="Associated team IDs", default=[])


class Umpire(BaseModel):
    collection_name = Collections.UMPIRES.upper()

    full_name: str
    name: str

    id = fields.ObjectIdField(desc="Id of the umpire")
    full_name = fields.StringField(desc="Full name of the umpire", default="")
    name = fields.StringField(desc="Role of the umpire (TV, Reserve, Field)", mandatory=True)


class Stadium(BaseModel):
    collection_name = Collections.STADIUM.upper()

    capacity: typing.Optional[int]
    city: str
    country: str
    locality: str
    name: str

    id = fields.ObjectIdField(desc="Id of the stadium")
    capacity = fields.IntegerField(desc="Capacity of the stadium", default=0)
    city = fields.StringField(desc="City where the stadium is located", mandatory=True)
    country = fields.StringField(desc="Country where the stadium is located", default="")
    locality = fields.StringField(desc="Locality or area where the stadium is situated", default="")
    name = fields.StringField(desc="Full name of the stadium", mandatory=True)


class Series(BaseModel):
    collection_name = Collections.SERIES.upper()

    gender: str

    match_type: str
    name: str
    season: str
    teams: typing.List[str]

    id = fields.ObjectIdField(desc="Id of the series")
    gender = fields.StringField(desc="Gender category (male/female)", mandatory=True)
    match_type = fields.StringField(desc="Type of match (T20, ODI, Test)", mandatory=True)
    name = fields.StringField(desc="Name of the series", mandatory=True)
    season = fields.StringField(desc="Season or year of the series", mandatory=True)
    teams = fields.ListField(ObjectId, desc="List of participating teams", default=[])


class Officials(BaseModel):
    match_referees: typing.List[ObjectId]
    reserve_umpires: typing.List[ObjectId]
    tv_umpires: typing.List[ObjectId]
    umpires: typing.List[ObjectId]

    match_referees = fields.ListField(ObjectId, desc="List of match referees", default=[])
    reserve_umpires = fields.ListField(ObjectId, desc="List of reserve umpires", default=[])
    tv_umpires = fields.ListField(ObjectId, desc="List of TV umpires", default=[])
    umpires = fields.ListField(ObjectId, desc="List of field umpires", mandatory=True)


class Outcome(BaseModel):
    by_runs: typing.Optional[int]
    by_wickets: typing.Optional[int]
    is_draw: bool
    winner: str

    by_runs = fields.IntegerField(desc="Margin of victory in runs", default=0)
    by_wickets = fields.IntegerField(desc="Margin of victory in wickets", default=0)
    is_draw = fields.BooleanField(desc="Indicates if the match ended in a draw", default=False)
    winner = fields.ObjectIdField(desc="Winning team id", mandatory=True)


class TeamPlayers(BaseModel):
    players: typing.List[str]
    team_id: str

    players = fields.ListField(ObjectId, desc="List of player IDs", mandatory=True)
    team_id = fields.ObjectIdField(desc="ID of the team", mandatory=True)


class Toss(BaseModel):
    decision: str
    team: str

    decision = fields.StringField(desc="Decision made by the toss winner (bat/field)", mandatory=True)
    team = fields.ObjectIdField(desc="ID of the team that won the toss", mandatory=True)


class Match(BaseModel):
    collection_name = Collections.MATCHES.upper()

    dates: typing.List[datetime]
    match_number: int
    outcome: Outcome
    player_of_match: typing.Optional[str]
    series: str
    team_1: TeamPlayers
    team_2: TeamPlayers
    umpires: Officials
    venue: str
    toss: Toss

    dates = fields.ListField(datetime, desc="List of match dates", mandatory=True)
    match_number = fields.IntegerField(desc="Number of the match", mandatory=True)
    outcome = fields.NestedField(Outcome, desc="Match outcome details")
    player_of_match = fields.ObjectIdField(desc="Id of the player")
    series = fields.ObjectIdField(desc="Id of the series", mandatory=True)
    team_1 = fields.NestedField(TeamPlayers, desc="Id of the team one", mandatory=True)
    team_2 = fields.NestedField(TeamPlayers, desc="Id of the team two", mandatory=True)
    toss = fields.NestedField(Toss, desc="Toss details", mandatory=True)
    umpires = fields.NestedField(Officials, desc="Match officials", mandatory=True)
    venue = fields.ObjectIdField(desc="Id of the match venue", mandatory=True)


class Innings(BaseModel):
    collection_name = Collections.INNINGS.upper()

    match_id: ObjectId
    batting_team: ObjectId
    total_runs: int
    wickets_lost: int
    overs_played: float

    match_id = fields.ObjectIdField(desc="Id of the match")
    batting_team = fields.ObjectIdField(desc="Id of the batting team")
    total_runs = fields.IntegerField(desc="Total runs scored in the innings", default=0)
    wickets_lost = fields.IntegerField(desc="Number of wickets lost in the innings", default=0)
    overs_played = fields.FloatField(desc="Number of overs played in the innings", default=0.0)


class Delivery(BaseModel):
    collection_name = Collections.DELIVERIES.upper()

    innings_id: ObjectId
    over_number: int
    delivery_number: int
    batter: ObjectId
    bowler: ObjectId
    non_striker: str
    runs_by_batter: int
    extras: int
    total_runs: int

    # Wicket Information
    is_wicket: bool
    wicket_type: typing.Optional[cricket_enum.WicketType]
    fielder_involved: typing.Optional[list[ObjectId]]

    # Extra tracking
    is_wide: bool
    is_no_ball: bool
    is_leg_bye: bool
    is_bye: bool
    penalty_runs: int

    innings_id = fields.ObjectIdField(desc="Id of the innings")
    over_number = fields.IntegerField(desc="Over number in the innings")
    delivery_number = fields.IntegerField(desc="Delivery number in the over")
    batter = fields.ObjectIdField(desc="Id of the batter")
    bowler = fields.ObjectIdField(desc="Id of the bowler")
    non_striker = fields.ObjectIdField(desc="Id of the non-striker")
    runs_by_batter = fields.IntegerField(desc="Runs scored by the batter")
    extras = fields.IntegerField(desc="Extra runs in the delivery")
    is_wicket = fields.BooleanField(desc="Indicates if the delivery resulted in a wicket", default=False)
    wicket_type = fields.StringField(desc="Type of the wicket", default="")
    fielder_involved = fields.ListField(ObjectId, desc="Ids of fielders involved in the wicket", default=[])
    is_wide = fields.BooleanField(desc="Indicates if the delivery is a wide", default=False)
    is_no_ball = fields.BooleanField(desc="Indicates if the delivery is a no-ball", default=False)
    is_leg_bye = fields.BooleanField(desc="Indicates if the delivery is a leg bye", default=False)
    is_bye = fields.BooleanField(desc="Indicates if the delivery is a bye", default=False)
    penalty_runs = fields.IntegerField(desc="Penalty runs awarded in the delivery", default=0)


class BattingStats(BaseModel):
    runs_scored: int
    balls_faced: int
    fours: int
    sixes: int
    strike_rate: float
    dot_balls: int
    is_out: bool
    dismissal_type: typing.Optional[cricket_enum.WicketType]
    fielders_involved: typing.Optional[list[ObjectId]]

    runs_scored = fields.IntegerField(desc="Runs scored by the batter")
    balls_faced = fields.IntegerField(desc="Balls faced by the batter")
    fours = fields.IntegerField(desc="Number of fours hit by the batter")
    sixes = fields.IntegerField(desc="Number of sixes hit by the batter")
    strike_rate = fields.FloatField(desc="Strike rate of the batter")
    dot_balls = fields.IntegerField(desc="Number of dot balls faced by the batter")
    is_out = fields.BooleanField(desc="Indicates if the batter is out")
    dismissal_type = fields.StringField(desc="Type of dismissal", default="")
    fielders_involved = fields.ListField(ObjectId, desc="Fielders involved in the dismissal", default=[])


class BowlingStats(BaseModel):
    overs_bowled: float
    wickets_taken: int
    runs_conceded: int
    maidens: int
    economy: float
    dot_balls: int
    boundaries_conceded: dict[str, int]

    overs_bowled = fields.FloatField(desc="Overs bowled by the player")
    wickets_taken = fields.IntegerField(desc="Wickets taken by the player")
    runs_conceded = fields.IntegerField(desc="Runs conceded by the player")
    maidens = fields.IntegerField(desc="Maiden overs bowled by the player")
    economy = fields.FloatField(desc="Economy rate of the player")
    dot_balls = fields.IntegerField(desc="Dot balls bowled by the player")
    boundaries_conceded = fields.DictField(desc="Boundaries conceded by the player")


class FieldingStats(BaseModel):
    catches_taken: int
    run_outs: int
    stumping: int

    catches_taken = fields.IntegerField(desc="Catches taken by the player")
    run_outs = fields.IntegerField(desc="Run outs by the player")
    stumping = fields.IntegerField(desc="Stumping by the player")


class PlayerScorecard(BaseModel):
    collection_name = Collections.PLAYER_SCORECARD.upper()

    player_id: ObjectId
    match_id: ObjectId
    batting_stats: typing.Optional[BattingStats]
    bowling_stats: typing.Optional[BowlingStats]
    fielding_stats: typing.Optional[FieldingStats]

    player_id = fields.ObjectIdField(desc="Id of the player")
    match_id = fields.ObjectIdField(desc="Id of the match")
    batting_stats = fields.NestedField(BattingStats, desc="Batting statistics of the player", default={})
    bowling_stats = fields.NestedField(BowlingStats, desc="Bowling statistics of the player", default={})
    fielding_stats = fields.NestedField(FieldingStats, desc="Fielding statistics of the player", default={})
