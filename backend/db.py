from shared import db_adapters


class CricketDatabaseAdapterBuilder(db_adapters.DatabaseAdapterBuilder):

    def __init__(self):
        super().__init__("mongodb://localhost:27017", "cricket")


class DatabaseAdapter:
    CRICKET = db_adapters.DatabaseAdapter(CricketDatabaseAdapterBuilder)


class Collections:
    TEAMS: str = "teams"
    PLAYERS: str = "players"
    SERIES: str = "series"
    STADIUM: str = "stadium"
    MATCHES: str = "matches"
    INNINGS: str = "innings"
    OVERS: str = "overs"
    DELIVERIES: str = "deliveries"


class CollectionAdapters:
    TEAMS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.TEAMS)

    PLAYERS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.PLAYERS)

    SERIES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.SERIES)

    STADIUM: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.STADIUM)

    MATCHES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.MATCHES)

    INNINGS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.INNINGS)

    OVERS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.OVERS)

    DELIVERIES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET,
                                                                              Collections.DELIVERIES)
