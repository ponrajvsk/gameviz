from datetime import datetime

from shared.models.common import fields
from shared.models.common.base import BaseModel


class Team(BaseModel):
    name = fields.StringField(desc="Team name", mandatory=True)
    country = fields.StringField(desc="Country of the team", mandatory=True)
    type = fields.StringField(desc="Full name of the player", mandatory=True)


class Player(BaseModel):
    cric_sheet_id = fields.StringField(desc="Id of the player in cricsheet", mandatory=True)
    name = fields.StringField(desc="Full name of the player", mandatory=True)
    full_name = fields.StringField(desc="Full name of the player", mandatory=True)
    batting_style = fields.StringField(desc="Batting style (Right-hand, Left-hand)")
    bowling_style = fields.StringField(desc="Bowling style (Off-spin, Leg-spin, etc.)")
    teams = fields.ListField(fields.ObjectIdField, desc="Associated team IDs")
    role = fields.StringField(desc="Bowling style (Off-spin, Leg-spin, etc.)")
    date_of_birth = fields.DateTimeField(desc="Date of the birth for the player")
    age = fields.StringField(desc="Age of the player in year and days format")


class Stadium(BaseModel):
    name = fields.StringField(desc="Full name of the player", mandatory=True)
    city = fields.StringField(desc="Full name of the player", mandatory=True)
    capacity = fields.IntegerField(desc="Full name of the player")


class Series(BaseModel):
    name = fields.StringField(desc="Name of the series", mandatory=True)
    season = fields.StringField(desc="Season or year of the series", mandatory=True)
    match_type = fields.StringField(desc="Type of match (T20, ODI, Test)", mandatory=True)
    gender = fields.StringField(desc="Gender category (male/female)", mandatory=True)
    teams = fields.ListField(fields.ObjectIdField, desc="List of participating teams", mandatory=True)


class Officials(BaseModel):
    umpires = fields.ListField(fields.ObjectIdField, desc="List of field umpires", mandatory=True)
    tv_umpires = fields.ListField(fields.ObjectIdField, desc="List of TV umpires")
    match_referees = fields.ListField(fields.ObjectIdField, desc="List of match referees")
    reserve_umpires = fields.ListField(fields.ObjectIdField, desc="List of reserve umpires")


class Outcome(BaseModel):
    winner = fields.StringField(desc="Winning team name", mandatory=True)
    by_runs = fields.IntegerField(desc="Margin of victory in runs")
    by_wickets = fields.IntegerField(desc="Margin of victory in wickets")
    is_draw = fields.BooleanField(desc="Indicates if the match ended in a draw", default=False)


class TeamPlayers(BaseModel):
    team_id = fields.ObjectIdField(desc="Id of the team one", mandatory=True)
    players = fields.ListField(fields.ObjectIdField, desc="Id of the team one", mandatory=True)


class Match(BaseModel):
    series = fields.ObjectIdField(desc="Id of the series", mandatory=True)
    team_1 = fields.NestedField(TeamPlayers, desc="Id of the team one", mandatory=True)
    team_2 = fields.NestedField(TeamPlayers, desc="Id of the team one", mandatory=True)
    match_number = fields.IntegerField(desc="Number of the match", mandatory=True)
    dates = fields.ListField(datetime, desc="List of match dates", mandatory=True)
    umpires = fields.NestedField(Officials, desc="Match officials", mandatory=True)
    venue = fields.ObjectIdField(desc="Id of the match venue", mandatory=True)
    outcome = fields.NestedField("OutcomeModel", desc="Match outcome details")
    player_of_match = fields.ObjectIdField(desc="Id of the player")


class BattingPerformance(BaseModel):
    player = fields.StringField(desc="Batsman's name", mandatory=True)
    runs = fields.IntegerField(desc="Runs scored", mandatory=True, default=0)
    balls_faced = fields.IntegerField(desc="Balls faced", mandatory=True, default=0)
    fours = fields.IntegerField(desc="Number of boundaries (4s)", mandatory=True, default=0)
    sixes = fields.IntegerField(desc="Number of sixes", mandatory=True, default=0)
    strike_rate = fields.FloatField(desc="Strike rate", mandatory=True, default=0.0)
    dismissal = fields.StringField(desc="How the batsman got out", mandatory=False)
    bowler = fields.StringField(desc="Bowler who dismissed the batsman", mandatory=False)
    fielder = fields.StringField(desc="Fielder involved in dismissal", mandatory=False)


class BowlingPerformance(BaseModel):
    player = fields.StringField(desc="Bowler's name", mandatory=True)
    overs = fields.FloatField(desc="Overs bowled", mandatory=True, default=0.0)
    maidens = fields.IntegerField(desc="Maiden overs bowled", mandatory=True, default=0)
    runs_conceded = fields.IntegerField(desc="Runs conceded", mandatory=True, default=0)
    wickets = fields.IntegerField(desc="Wickets taken", mandatory=True, default=0)
    economy = fields.FloatField(desc="Bowling economy rate", mandatory=True, default=0.0)
    wides = fields.IntegerField(desc="Wides bowled", mandatory=True, default=0)
    no_balls = fields.IntegerField(desc="No-balls bowled", mandatory=True, default=0)


class Extras(BaseModel):
    wides = fields.IntegerField(desc="Wides conceded", mandatory=True, default=0)
    no_balls = fields.IntegerField(desc="No-balls conceded", mandatory=True, default=0)
    byes = fields.IntegerField(desc="Byes conceded", mandatory=True, default=0)
    leg_byes = fields.IntegerField(desc="Leg byes conceded", mandatory=True, default=0)
    penalty_runs = fields.IntegerField(desc="Penalty runs conceded", mandatory=True, default=0)


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
