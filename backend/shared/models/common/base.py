import typing
from bson import ObjectId
from db.db import CollectionAdapters
from shared.models.common.fields import BaseField


class BaseModel:
    collection_name: typing.ClassVar[str]

    def __init__(self, **kwargs):
        """Initializes the model and assigns values dynamically."""
        self.id = kwargs.get("id")  # Ensure id is optional

        for field_name, field in self._get_fields().items():
            if field.mandatory and field_name not in kwargs:
                raise ValueError(f"Missing required field: {field_name}")

            value = kwargs.get(field_name, field.default)
            field.validate(value)
            setattr(self, field_name, value)  # Store values as attributes

    def to_dict(self):
        """Converts the instance to a dictionary, handling ObjectId fields."""
        data = {field: getattr(self, field) for field in self._get_fields()}

        # Remove `None` id to avoid inserting it
        if self.id:
            data["_id"] = self.id if isinstance(self.id, ObjectId) else ObjectId(self.id)
        else:
            data.pop("id", None)

        return data

    @classmethod
    def _get_fields(cls):
        """Returns a dictionary of fields for the model."""
        return {
            attr: value for attr, value in cls.__dict__.items()
            if isinstance(value, BaseField)
        }

    @classmethod
    async def read_from_db(cls, query: dict):
        """Fetches a single document from the database and returns an instance of the model."""
        collection = getattr(CollectionAdapters, cls.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {cls.__name__}")

        data = await collection.find_one(query)
        if data:
            data["id"] = data["_id"]  # Assign MongoDB `_id` to `id`
        return cls(**data) if data else None

    async def save_to_db(self):
        """Inserts the current instance into the database and assigns an ID."""
        collection = getattr(CollectionAdapters, self.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {self.__class__.__name__}")

        data = self.to_dict()
        data.pop("_id", None)

        inserted_id = await collection.insert_one(data)
        self.id = inserted_id

    async def update_in_db(self):
        """Updates the existing document in the database."""
        collection = getattr(CollectionAdapters, self.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {self.__class__.__name__}")

        if not self.id:
            raise ValueError("Cannot update an unsaved document")

        data = self.to_dict()
        query = {"_id": data.pop("id")}
        update_data = {"$set": data}

        await collection.update_one(query, update_data)

    async def delete_from_db(self):
        """Deletes the document from the database."""
        collection = getattr(CollectionAdapters, self.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {self.__class__.__name__}")

        if not self.id:
            raise ValueError("Cannot delete an unsaved document")

        await collection.delete_one({"_id": self.id})
