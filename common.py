from dataclasses import Field, fields, MISSING
from datetime import datetime
from distutils.util import strtobool
import typing
from dateutil.parser import parse


class Config:
    pass


class FieldWithConfig(Field):
    def __init__(self, config, *args, **kwargs) -> None:
        self.config = config
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        repr = super().__repr__()
        return f"{repr[:-1]},config={self.config!r})"


def fieldwrapper(*, config, default=MISSING, default_factory=MISSING, init=True,
                 repr=True, hash=None, compare=True, metadata=None):

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    return FieldWithConfig(config, default, default_factory, init, repr, hash, compare, metadata)


class BaseMixin:
    SIMPLE_TYPES = [str, int, float]
    SPECIAL_TYPES = [bool, datetime]
    COMPLEX_TYPES = [list]

    SUPPORTED_TYPES = SIMPLE_TYPES + SPECIAL_TYPES + COMPLEX_TYPES

    @classmethod
    def raise_for_types_not_supported(cls, data_type):
        base_type = cls.get_base_type(data_type)

        if base_type not in cls.SUPPORTED_TYPES:
            raise NotImplementedError(f"Data type {data_type} is not supported yet.")

    @classmethod
    def get_base_type(cls, data_type):
        return typing.get_origin(data_type) or data_type  # handle e.g. list[str]

    @classmethod
    def cast_value_to_type(cls, value, data_type):

        cls.raise_for_types_not_supported(data_type)
        base_type = cls.get_base_type(data_type)

        if base_type in cls.SIMPLE_TYPES:
            return data_type(value)

        if base_type in cls.SPECIAL_TYPES:
            return cls.cast_special_type(value, data_type)

        if base_type in cls.COMPLEX_TYPES:
            return cls.cast_complex_type(value, data_type)

    @classmethod
    def cast_special_type(cls, value, data_type):
        if data_type == bool:
            return bool(strtobool(value))
        if data_type == datetime:
            return parse(value)
        raise NotImplementedError()

    @classmethod
    def cast_complex_type(cls, value: list, data_type: type):
        base_type = cls.get_base_type(data_type)

        if base_type == list:  # only `list` support for no
            element_type = typing.get_args(data_type)[0] if typing.get_args(data_type) else str
            return [cls.cast_value_to_type(element, element_type) for element in value]

        raise NotImplementedError()

    @classmethod
    def to_dataclass(cls, raw_data):
        dc = cls(**{field.name: cls._process_field(field, raw_data) for field in fields(cls)})
        return dc
