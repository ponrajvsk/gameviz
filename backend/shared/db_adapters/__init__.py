from typing import Dict, Any, Optional
from typing import Type

from bson import ObjectId
from motor.core import AgnosticCollection
from motor.core import AgnosticCursor
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseAdapterBuilder:
    _database_name: str
    _uri: str

    def __init__(self,
                 uri: str,
                 database_name: str,
                 /) -> None:
        self._database_name = database_name
        self._uri = uri

    def build(self) -> AgnosticDatabase:
        client = AsyncIOMotorClient(self._uri)
        return client.get_database(self._database_name)


class DatabaseAdapter:
    _builder: Type[DatabaseAdapterBuilder]
    _db: Optional[AgnosticDatabase]

    def __init__(self,
                 builder: Type[DatabaseAdapterBuilder],
                 /) -> None:
        self._builder = builder
        self._db = None

    def connect_db(self) -> AgnosticDatabase:
        if self._db is None:
            # noinspection PyArgumentList
            self._db = self._builder().build()

        return self._db


class CollectionAdapter:
    _db_adapter: DatabaseAdapter
    _collection_name: str

    def __init__(self,
                 db_adapter: DatabaseAdapter,
                 collection_name: str,
                 /) -> None:
        self._db_adapter = db_adapter
        self._collection_name = collection_name

    @property
    def db_adapter(self) -> DatabaseAdapter:
        return self._db_adapter

    @property
    def collection_name(self) -> str:
        return self._collection_name

    def get_collection(self,
                       /) -> AgnosticCollection:
        db = self._db_adapter.connect_db()
        coll = db.get_collection(self._collection_name)
        return coll

    async def insert_one(self,
                         data: Dict[str, Any],
                         /) -> ObjectId:
        result = await self.get_collection().insert_one(data)
        return result.inserted_id

    async def find_one(self,
                       query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.get_collection().find_one(query)

    async def find_documents(self,
                             query: Dict[str, Any],
                             /) -> AgnosticCursor:
        cursor = self.get_collection().find(query)
        return cursor

    async def update_one(self, query: dict, update: dict):
        """Updates a single document in the collection."""
        return await self.get_collection().update_one(query, update)

    async def update_many(self,
                          query: Dict[str, Any],
                          update_data: Dict[str, Any],
                          /) -> int:
        result = await self.get_collection().update_many(query, {"$set": update_data})
        return result.modified_count

    async def delete_one(self,
                         query: Dict[str, Any]) -> int:
        result = await self.get_collection().delete_one(query)
        return result.deleted_count

    async def delete_many(self,
                          query: Dict[str, Any]) -> int:
        result = await self.get_collection().delete_many(query)
        return result.deleted_count
