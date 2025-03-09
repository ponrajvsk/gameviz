from shared.models.common.fields import BaseField


class BaseModel:
    def __init__(self, **kwargs):
        self.data = {}
        for field_name, field in self._get_fields().items():
            if field.mandatory and field_name not in kwargs:
                raise ValueError(f"Missing required field: {field_name}")
            if field_name in kwargs:
                field.validate(kwargs[field_name])
                self.data[field_name] = kwargs[field_name]
            else:
                self.data[field_name] = None

    def to_dict(self):
        return self.data

    @classmethod
    def _get_fields(cls):
        return {
            attr: value for attr, value in cls.__dict__.items()
            if isinstance(value, BaseField)
        }
