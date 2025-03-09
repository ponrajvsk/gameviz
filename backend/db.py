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


class CollectionAdapters:
    TEAMS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.TEAMS)

    PLAYERS: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.PLAYERS)

    SERIES: db_adapters.CollectionAdapter = db_adapters.CollectionAdapter(DatabaseAdapter.CRICKET, Collections.SERIES)
