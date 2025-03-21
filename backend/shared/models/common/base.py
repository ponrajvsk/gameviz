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
        """Converts the instance to a dictionary, handling nested models and ObjectId fields."""
        data = {}

        for field, value in self.__dict__.items():
            if isinstance(value, BaseModel):
                data[field] = value.to_dict()  # Recursively convert nested models
            elif isinstance(value, list):
                data[field] = [
                    v.to_dict() if isinstance(v, BaseModel) else v for v in value
                ]
            else:
                data[field] = value

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
    async def read_one_from_db(cls, query: dict):
        """Fetches a single document from the database and returns an instance of the model."""
        collection = getattr(CollectionAdapters, cls.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {cls.__name__}")

        data = await collection.find_one(query)

        if data:
            data["id"] = data.pop("_id")

            return cls._construct_from_dict(data)

        return None

    @classmethod
    async def read_many_from_db(cls, query: dict):
        """Fetches a single document from the database and returns an instance of the model."""
        collection = getattr(CollectionAdapters, cls.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {cls.__name__}")

        records = await collection.find_documents(query)

        result = []
        if records:
            async for record in records:
                record["id"] = record.pop("_id")

                result.append(cls._construct_from_dict(record))

            return result

        return None

    @classmethod
    def _construct_from_dict(cls, data: dict):
        """Recursively constructs the model from a dictionary."""
        model_data = {
            "id": data.get("id")
        }

        for field_name, field_type in cls.__annotations__.items():
            if field_name not in data:
                continue  # Skip missing fields

            value = data[field_name]

            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                # ✅ If it's a nested model, construct it recursively
                model_data[field_name] = field_type._construct_from_dict(value) if isinstance(value, dict) else value

            elif typing.get_origin(field_type) == list:
                # ✅ If it's a list of nested models, handle each item
                inner_type = typing.get_args(field_type)[0]
                if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                    model_data[field_name] = [inner_type._construct_from_dict(item) if isinstance(item, dict) else item for item in value]
                else:
                    model_data[field_name] = value

            else:
                model_data[field_name] = value

        return cls(**model_data)


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

    async def delete_one_from_db(self):
        """Deletes the document from the database."""
        collection = getattr(CollectionAdapters, self.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {self.__class__.__name__}")

        if not self.id:
            raise ValueError("Cannot delete an unsaved document")

        await collection.delete_one({"_id": self.id})

    @classmethod
    async def delete_many_from_db(cls, query: dict):
        """Deletes multiple documents from the database."""
        collection = getattr(CollectionAdapters, cls.collection_name, None)
        if not collection:
            raise ValueError(f"Collection name not set for {cls.__name__}")

        await collection.delete_many(query)
