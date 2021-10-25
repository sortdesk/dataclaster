import typing
from datetime import datetime

from distutils.util import strtobool
from dateutil.parser import parse


class BaseMixin:
    SIMPLE_TYPES = [str, int, float]
    SPECIAL_TYPES = [bool, datetime]
    COMPLEX_TYPES = [list]

    SUPPORTED_TYPES = SIMPLE_TYPES + SPECIAL_TYPES + COMPLEX_TYPES

    @classmethod
    def cast_value_to_type(cls, value, data_type):

        if data_type not in cls.SUPPORTED_TYPES:
            raise NotImplementedError(f"Data type {data_type} is not supported yet.")

        if data_type in cls.SIMPLE_TYPES:
            return data_type(value)

        if data_type in cls.SPECIAL_TYPES:
            return cls.cast_special_type(value, data_type)

        if data_type in cls.COMPLEX_TYPES:
            return cls.cast_complex_type(value, data_type)

    @classmethod
    def cast_special_type(cls, value, data_type):
        if data_type == bool:
            return bool(strtobool(value))
        if data_type == datetime:
            return parse(value)
        raise NotImplementedError()

    @classmethod
    def cast_complex_type(cls, values: list, data_type: type):
        base_type = typing.get_origin(data_type) or data_type  # handle e.g. list[str]

        if base_type == list:  # only `list` support for now
            element_type = typing.get_args(data_type)[0] if typing.get_args(data_type) else str
            return [cls.cast_value_to_type(value, element_type) for value in values]

        raise NotImplementedError()
