from dataclasses import fields

from base_mixin import BaseMixin


class JSONMixin(BaseMixin):

    @classmethod
    def process_field(cls, field, json_dict):

        cls.raise_for_types_not_supported(field.type)

        value = json_dict[field.name]
        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def from_dict(cls, json_dict):
        dc = cls(**{field.name: cls.process_field(field, json_dict) for field in fields(cls)})
        return dc
