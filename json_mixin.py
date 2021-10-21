from dataclasses import fields


class JSONMixin:

    @classmethod
    def process_field(cls, field, json_dict):
        return json_dict[field.name]

    @classmethod
    def from_dict(cls, json_dict):
        dc = cls(**{field.name: cls.process_field(field, json_dict) for field in fields(cls)})
        return dc
