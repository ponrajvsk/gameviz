from shared.models.common import fields
from shared.models.common.base import BaseModel


class TeamModel(BaseModel):
    name = fields.StringField(desc="Team name", mandatory=True)
    country = fields.StringField(desc="Country of the team", mandatory=True)


class PlayerModel(BaseModel):
    name = fields.StringField(desc="Full name of the player", mandatory=True)
    batting_style = fields.StringField(desc="Batting style (Right-hand, Left-hand)", mandatory=True)
    bowling_style = fields.StringField(desc="Bowling style (Off-spin, Leg-spin, etc.)", mandatory=False)
    team_id = fields.StringField(desc="Associated team ID", mandatory=True)
    stats = fields.DictField(desc="Player statistics", mandatory=False)
    achievements = fields.ListField(str, desc="List of achievements", mandatory=False)
    team = fields.NestedField(TeamModel, desc="Associated team", mandatory=False)
