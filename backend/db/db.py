from shared import db_adapters


class CricketDatabaseAdapterBuilder(db_adapters.DatabaseAdapterBuilder):

    def __init__(self):
        super().__init__("mongodb://localhost:27017", "cricket")


class DatabaseAdapter:
    CRICKET = db_adapters.DatabaseAdapter(CricketDatabaseAdapterBuilder)


class Collections:
    TEAMS: str = "teams"
    PLAYERS: str = "players"
    UMPIRES: str = "umpires"
    SERIES: str = "series"
    STADIUM: str = "stadium"
    MATCHES: str = "matches"
    INNINGS: str = "innings"
    DELIVERIES: str = "deliveries"
    PLAYER_SCORECARD: str = "player_scorecard"


class CollectionAdapters:
    TEAMS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.TEAMS)

    PLAYERS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.PLAYERS)

    UMPIRES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.UMPIRES)

    SERIES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.SERIES)

    STADIUM: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.STADIUM)

    MATCHES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.MATCHES)

    INNINGS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.INNINGS)

    DELIVERIES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.DELIVERIES)

    PLAYER_SCORECARD: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.PLAYER_SCORECARD)
