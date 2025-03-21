from enum import Enum


class WicketType(str, Enum):
    BOWLED = "bowled"
    CAUGHT = "caught"
    LBW = "lbw"
    RUN_OUT = "run_out"
    STUMPED = "stumped"
    HIT_WICKET = "hit_wicket"
    HANDLED_BALL = "handled_ball"
    HIT_BALL_TWICE = "hit_ball_twice"
    OBSTRUCTING_FIELD = "obstructing_field"
    TIMED_OUT = "timed_out"
    RETIRED_OUT = "retired_out"
