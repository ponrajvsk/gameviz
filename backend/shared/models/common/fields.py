class BaseField:
    def __init__(self, desc="", mandatory=False):
        self.desc = desc
        self.mandatory = mandatory

    def validate(self, value):
        raise NotImplementedError("Subclasses must implement validate method")


class StringField(BaseField):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected string, got {type(value).__name__}")


class IntegerField(BaseField):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected integer, got {type(value).__name__}")


class ListField(BaseField):
    def __init__(self, item_type, desc="", mandatory=False):
        super().__init__(desc, mandatory)
        self.item_type = item_type

    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected list, got {type(value).__name__}")
        for item in value:
            if not isinstance(item, self.item_type):
                raise ValueError(f"Expected list of {self.item_type.__name__}, got {type(item).__name__}")


class DictField(BaseField):
    def validate(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict, got {type(value).__name__}")


class NestedField(BaseField):
    def __init__(self, model_class, desc="", mandatory=False):
        super().__init__(desc, mandatory)
        self.model_class = model_class

    def validate(self, value):
        if not isinstance(value, self.model_class):
            raise ValueError(f"Expected {self.model_class.__name__} instance, got {type(value).__name__}")



