from datetime import date
from datetime import datetime

from bson import ObjectId


class BaseField:

    def __init__(self, desc="", mandatory=False, default=None):
        self.desc = desc
        self.mandatory = mandatory
        self.default = None if mandatory else default  # Default is only applied if mandatory=False

    def validate(self, value):
        raise NotImplementedError("Subclasses must implement validate method")


class StringField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default)

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected string, got {type(value).__name__}")


class IntegerField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default)

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected integer, got {type(value).__name__}")


class FloatField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default)

    def validate(self, value):
        if not isinstance(value, float):
            raise ValueError(f"Expected float, got {type(value).__name__}")


class BooleanField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default)

    def validate(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Expected boolean, got {type(value).__name__}")


class ListField(BaseField):
    def __init__(self, item_type, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default if not mandatory else None)
        self.item_type = item_type

    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected list, got {type(value).__name__}")

        for item in value:
            if not isinstance(item, self.item_type):
                raise ValueError(f"Expected list of {self.item_type.__name__}, got {type(item).__name__}")


class DictField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default)

    def validate(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict, got {type(value).__name__}")


class NestedField(BaseField):

    def __init__(self, model_class, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default if not mandatory else None)
        self.model_class = model_class

    def validate(self, value):
        if not isinstance(value, self.model_class):
            raise ValueError(f"Expected {self.model_class.__name__} instance, got {type(value).__name__}")


class DateTimeField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default if not mandatory else None)

    def validate(self, value):
        if not isinstance(value, datetime):
            raise ValueError(f"Expected datetime, got {type(value).__name__}")


class DateField(BaseField):

    def __init__(self, desc="", mandatory=False, default=None):
        super().__init__(desc, mandatory, default if not mandatory else None)

    def validate(self, value):
        if not isinstance(value, date):
            raise ValueError(f"Expected date, got {type(value).__name__}")


class ObjectIdField(BaseField):
    def validate(self, value):
        if value is not None and not isinstance(value, ObjectId):
            raise ValueError(f"Expected valid ObjectId, got {type(value).__name__}")
