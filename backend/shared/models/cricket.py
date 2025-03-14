import typing
from datetime import datetime

from db.db import Collections
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
    age = fields.StringField(desc="Age of the player in year and days format")
    batting_style = fields.StringField(desc="Batting style (Right-hand, Left-hand)")
    bowling_style = fields.StringField(desc="Bowling style (Off-spin, Leg-spin, etc.)")
    cric_sheet_id = fields.StringField(desc="Id of the player in cricsheet", mandatory=True)
    date_of_birth = fields.DateTimeField(desc="Date of birth of the player")
    full_name = fields.StringField(desc="Full name of the player", mandatory=True)
    name = fields.StringField(desc="Full name of the player", mandatory=True)
    role = fields.StringField(desc="Player's role in the team")
    teams = fields.ListField(fields.ObjectIdField, desc="Associated team IDs")


class Stadium(BaseModel):
    collection_name = Collections.STADIUM.upper()

    capacity: typing.Optional[int]
    city: str
    name: str

    id = fields.ObjectIdField(desc="Id of the series")
    capacity = fields.IntegerField(desc="Capacity of the stadium")
    city = fields.StringField(desc="City where the stadium is located", mandatory=True)
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
    teams = fields.ListField(fields.ObjectIdField, desc="List of participating teams", default=[])


class Officials(BaseModel):
    match_referees: typing.List[str]
    reserve_umpires: typing.List[str]
    tv_umpires: typing.List[str]
    umpires: typing.List[str]

    match_referees = fields.ListField(fields.ObjectIdField, desc="List of match referees")
    reserve_umpires = fields.ListField(fields.ObjectIdField, desc="List of reserve umpires")
    tv_umpires = fields.ListField(fields.ObjectIdField, desc="List of TV umpires")
    umpires = fields.ListField(fields.ObjectIdField, desc="List of field umpires", mandatory=True)


class Outcome(BaseModel):
    by_runs: typing.Optional[int]
    by_wickets: typing.Optional[int]
    is_draw: bool
    winner: str

    by_runs = fields.IntegerField(desc="Margin of victory in runs")
    by_wickets = fields.IntegerField(desc="Margin of victory in wickets")
    is_draw = fields.BooleanField(desc="Indicates if the match ended in a draw", default=False)
    winner = fields.StringField(desc="Winning team name", mandatory=True)


class TeamPlayers(BaseModel):
    players: typing.List[str]
    team_id: str

    players = fields.ListField(fields.ObjectIdField, desc="List of player IDs", mandatory=True)
    team_id = fields.ObjectIdField(desc="ID of the team", mandatory=True)


class Match(BaseModel):
    dates: typing.List[datetime]
    match_number: int
    outcome: typing.Optional[Outcome]
    player_of_match: typing.Optional[str]
    series: str
    team_1: TeamPlayers
    team_2: TeamPlayers
    umpires: Officials
    venue: str

    dates = fields.ListField(datetime, desc="List of match dates", mandatory=True)
    match_number = fields.IntegerField(desc="Number of the match", mandatory=True)
    outcome = fields.NestedField(Outcome, desc="Match outcome details")
    player_of_match = fields.ObjectIdField(desc="Id of the player")
    series = fields.ObjectIdField(desc="Id of the series", mandatory=True)
    team_1 = fields.NestedField(TeamPlayers, desc="Id of the team one", mandatory=True)
    team_2 = fields.NestedField(TeamPlayers, desc="Id of the team two", mandatory=True)
    umpires = fields.NestedField(Officials, desc="Match officials", mandatory=True)
    venue = fields.ObjectIdField(desc="Id of the match venue", mandatory=True)


class BattingPerformance(BaseModel):
    balls_faced: int
    bowler: typing.Optional[str]
    dismissal: typing.Optional[str]
    fielder: typing.Optional[str]
    fours: int
    player: str
    runs: int
    sixes: int
    strike_rate: float

    balls_faced = fields.IntegerField(desc="Balls faced", mandatory=True, default=0)
    bowler = fields.StringField(desc="Bowler who dismissed the batsman", mandatory=False)
    dismissal = fields.StringField(desc="How the batsman got out", mandatory=False)
    fielder = fields.StringField(desc="Fielder involved in dismissal", mandatory=False)
    fours = fields.IntegerField(desc="Number of boundaries (4s)", mandatory=True, default=0)
    player = fields.StringField(desc="Batsman's name", mandatory=True)
    runs = fields.IntegerField(desc="Runs scored", mandatory=True, default=0)
    sixes = fields.IntegerField(desc="Number of sixes", mandatory=True, default=0)
    strike_rate = fields.FloatField(desc="Strike rate", mandatory=True, default=0.0)


class BowlingPerformance(BaseModel):
    economy: float
    maidens: int
    no_balls: int
    overs: float
    player: str
    runs_conceded: int
    wides: int
    wickets: int

    economy = fields.FloatField(desc="Bowling economy rate", mandatory=True, default=0.0)
    maidens = fields.IntegerField(desc="Maiden overs bowled", mandatory=True, default=0)
    no_balls = fields.IntegerField(desc="No-balls bowled", mandatory=True, default=0)
    overs = fields.FloatField(desc="Overs bowled", mandatory=True, default=0.0)
    player = fields.StringField(desc="Bowler's name", mandatory=True)
    runs_conceded = fields.IntegerField(desc="Runs conceded", mandatory=True, default=0)
    wides = fields.IntegerField(desc="Wides bowled", mandatory=True, default=0)
    wickets = fields.IntegerField(desc="Wickets taken", mandatory=True, default=0)


class Extras(BaseModel):
    byes: int
    leg_byes: int
    no_balls: int
    penalty_runs: int
    wides: int

    byes = fields.IntegerField(desc="Byes conceded", mandatory=True, default=0)
    leg_byes = fields.IntegerField(desc="Leg byes conceded", mandatory=True, default=0)
    no_balls = fields.IntegerField(desc="No-balls conceded", mandatory=True, default=0)
    penalty_runs = fields.IntegerField(desc="Penalty runs conceded", mandatory=True, default=0)
    wides = fields.IntegerField(desc="Wides conceded", mandatory=True, default=0)


class FallOfWickets(BaseModel):
    wicket_number = fields.IntegerField(desc="Wicket number", mandatory=True)
    runs_at_fall = fields.IntegerField(desc="Team score when the wicket fell", mandatory=True)
    over_at_fall = fields.FloatField(desc="Over number when the wicket fell", mandatory=True)
    batsman = fields.StringField(desc="Batsman dismissed", mandatory=True)


class Partnership(BaseModel):
    batsmen = fields.ListField(str, desc="Batsmen involved in partnership", mandatory=True)
    runs = fields.IntegerField(desc="Runs scored in partnership", mandatory=True, default=0)
    balls = fields.IntegerField(desc="Balls faced in partnership", mandatory=True, default=0)


class TeamScore(BaseModel):
    team = fields.StringField(desc="Team name", mandatory=True)
    total_runs = fields.IntegerField(desc="Total runs scored", mandatory=True, default=0)
    wickets_lost = fields.IntegerField(desc="Total wickets lost", mandatory=True, default=0)
    overs_played = fields.FloatField(desc="Total overs played", mandatory=True, default=0.0)


class Scorecard(BaseModel):
    team = fields.StringField(desc="Team name", mandatory=True)
    batting_performance = fields.ListField(BattingPerformance, desc="Batting statistics", mandatory=True)
    bowling_performance = fields.ListField(BowlingPerformance, desc="Bowling statistics", mandatory=True)
    extras = fields.NestedField(Extras, desc="Extras conceded", mandatory=True)
    fall_of_wickets = fields.ListField(FallOfWickets, desc="Fall of wickets details", mandatory=True)
    partnerships = fields.ListField(Partnership, desc="Partnership details", mandatory=True)
    final_score = fields.NestedField(TeamScore, desc="Final team score", mandatory=True)
    player_of_match = fields.StringField(desc="Player of the match", mandatory=False)


class PowerplayModel(BaseModel):
    from_over = fields.FloatField(desc="Start over of powerplay", mandatory=True)
    to_over = fields.FloatField(desc="End over of powerplay", mandatory=True)
    type = fields.StringField(desc="Type of powerplay (e.g., mandatory, batting, bowling)", mandatory=True)


class TargetModel(BaseModel):
    overs = fields.IntegerField(desc="Total overs allocated for the chase", mandatory=True)
    runs = fields.IntegerField(desc="Target runs to be chased", mandatory=True)


class InningsModel(BaseModel):
    innings_id = fields.ObjectIdField(desc="Unique innings identifier", mandatory=True)
    match_id = fields.ObjectIdField(desc="Reference to the match", mandatory=True)
    team = fields.ObjectIdField(desc="Team playing the innings", mandatory=True)
    overs = fields.ListField(fields.ObjectIdField, desc="References to over documents", mandatory=True)
    power_play = fields.NestedField(PowerplayModel, desc="Powerplay details", mandatory=False)
    target = fields.NestedField(TargetModel, desc="Target details if applicable", mandatory=False)
    scoreboard = fields.NestedField(Scorecard, desc="Details of first innings", mandatory=True)


class OverModel(BaseModel):
    over_id = fields.ObjectIdField(desc="Unique over identifier", mandatory=True)
    innings_id = fields.ObjectIdField(desc="Reference to innings", mandatory=True)
    over_number = fields.IntegerField(desc="Over number", mandatory=True)
    deliveries = fields.ListField(fields.ObjectIdField, desc="References to delivery documents", mandatory=True)


class RunsModel(BaseModel):
    runs_by_batter = fields.IntegerField(desc="Runs scored by the batter", mandatory=True)
    extras = fields.IntegerField(desc="Extra runs in the delivery", mandatory=True)
    total = fields.IntegerField(desc="Total runs scored on the delivery", mandatory=True)


class DeliveryModel(BaseModel):
    delivery_id = fields.ObjectIdField(desc="Unique delivery identifier", mandatory=True)
    over_id = fields.ObjectIdField(desc="Reference to over", mandatory=True)
    delivery_number = fields.IntegerField(desc="Sequence number of the delivery within the over", mandatory=True)
    batter = fields.ObjectIdField(desc="Batter on strike", mandatory=True)
    bowler = fields.ObjectIdField(desc="Bowler delivering the ball", mandatory=True)
    non_striker = fields.ObjectIdField(desc="Non-striker batter", mandatory=True)
    runs = fields.NestedField(RunsModel, desc="Runs details for this delivery", mandatory=True)
