class Series:
    NAME = "name"
    SEASON = "season"
    MATCH_TYPE = "match_type"
    GENDER = "gender"
    TEAMS = "teams"


class Teams:
    NAME = "name"
    COUNTRY = "country"
    TEAM_TYPE = "team_type"


class Players:
    NAME = "name"
    TEAM_ID = "team_id"
    CRIC_SHEET_ID = "cric_sheet_id"
    ROLE = "role"
    BATTING_STYLE = "batting_style"
    BOWLING_STYLE = "bowling_style"
    DOB = "dob"


class Umpires:
    NAME = "name"
    FULL_NAME = "full_name"


class Stadiums:
    NAME = "name"
    CITY = "city"
    COUNTRY = "country"
    CAPACITY = "capacity"
    LOCALITY = "locality"


class Matches:
    SERIES_ID = "series"
    MATCH_NUMBER = "match_number"


class Innings:
    MATCH_ID = "match_id"
    INNINGS_NUMBER = "innings_number"
    TEAM_ID = "team_id"
    BATTING_TEAM_ID = "batting_team_id"
    BOWLING_TEAM_ID = "bowling_team_id"
    TOTAL_RUNS = "total_runs"
    TOTAL_WICKETS = "total_wickets"
    TOTAL_OVERS = "total_overs"
    TOTAL_OVERS_BOWLED = "total_overs_bowled"
    TOTAL_OVERS_BATTED = "total_overs_batted"


class Delivery:
    INNINGS_ID = "innings_id"
