from dataclasses import fields

from common import Config, BaseMixin
from jsontree import JSONTree


class JSONConfig(Config):
    def __init__(self, path: str) -> None:
        self.path = path


class JSONMixin(BaseMixin):

    @classmethod
    def process_field(cls, field, json_dict):

        cls.raise_for_types_not_supported(field.type)

        if hasattr(field, "config"):
            if not isinstance(field.config, JSONConfig):
                raise ValueError(
                    f"You must pass a valid instance of JSONConfig to the `config` parameter on {field.name}"
                )
            return cls.process_field_with_config(field, json_dict)
        else:
            return cls.process_field_without_config(field, json_dict)

    @classmethod
    def process_field_with_config(cls, field, json_dict):

        json_tree = JSONTree(json_dict)
        value = json_tree.get_value(field.config.path)

        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def process_field_without_config(cls, field, json_dict):
        value = json_dict[field.name]
        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def from_dict(cls, json_dict):
        dc = cls(**{field.name: cls.process_field(field, json_dict) for field in fields(cls)})
        return dc
