from dataclasses import fields
from datetime import datetime

from distutils.util import strtobool

from dateutil.parser import parse


class JSONMixin:
    SIMPLE_TYPES = [str, int, float]
    SPECIAL_TYPES = [datetime]
    SUPPORTED_TYPES = SIMPLE_TYPES + SPECIAL_TYPES

    @classmethod
    def cast_special_type(cls, value, data_type):
        if data_type == bool:
            return bool(strtobool(value))
        elif data_type == datetime:
            return parse(value)

    @classmethod
    def cast_data_type(cls, field, json_dict):
        data_type = field.type

        if data_type not in cls.SUPPORTED_TYPES:
            raise NotImplementedError(f"Data type {data_type} is not supported yet.")

        if data_type in cls.SIMPLE_TYPES:
            return data_type(json_dict[field.name])

        if data_type in cls.SPECIAL_TYPES:
            return cls.cast_special_type(json_dict[field.name], data_type)

    @classmethod
    def process_field(cls, field, json_dict):
        return cls.cast_data_type(field, json_dict)

    @classmethod
    def from_dict(cls, json_dict):
        dc = cls(**{field.name: cls.process_field(field, json_dict) for field in fields(cls)})
        return dc
