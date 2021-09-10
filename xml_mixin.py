from dataclasses import fields, Field, MISSING
from datetime import datetime
from distutils.util import strtobool

from dateutil.parser import parse


class Config:
    pass


class XMLConfig(Config):
    def __init__(self, xpath, attrib=None) -> None:
        self.xpath = xpath
        self.attrib = attrib


class XMLMixin:
    SIMPLE_TYPES = [str, int, float]
    SPECIAL_TYPES = [bool, datetime]
    COMPLEX_TYPES = [list]
    SUPPORTED_TYPES = SIMPLE_TYPES + SPECIAL_TYPES

    @classmethod
    def cast_special_type(self, value, data_type):
        if data_type == bool:
            return bool(strtobool(value))
        elif data_type == datetime:
            return parse(value)

    @classmethod
    def cast_complex_type(self, value, data_type):
        if data_type == list:
            pass

    @classmethod
    def cast_data_type(cls, value, data_type=str):
        if data_type not in cls.SUPPORTED_TYPES:
            raise NotImplementedError(f"Data type {data_type} is not supported yet.")

        if data_type in cls.SIMPLE_TYPES:
            return data_type(value)
        elif data_type in cls.SPECIAL_TYPES:
            return cls.cast_special_type(value, data_type)
        elif data_type in cls.COMPLEX_TYPES:
            return cls.cast_complex_type(value, data_type)

    @classmethod
    def process_field(cls, field, xml_tree):
        if hasattr(field, "config"):
            if not isinstance(field.config, XMLConfig):
                raise ValueError("You must pass a valid instance of XMLConfig to the `config` parameter.")
            return cls.process_field_with_config(field, xml_tree)
        else:
            return cls.process_field_without_config(field, xml_tree)

    @classmethod
    def process_field_with_config(cls, field, xml_tree):
        element = xml_tree.find(field.config.xpath)

        if field.config.attrib:
            attrib_text = element.get(field.config.attrib)
            return cls.cast_data_type(attrib_text, field.type)
        else:
            element_text = element.text
            return cls.cast_data_type(element_text, field.type)

    @classmethod
    def process_field_without_config(cls, field, xml_tree):
        return xml_tree.findtext(field.name)

    @classmethod
    def from_xml(cls, xml_tree):
        dc = cls(**{field.name: cls.process_field(field, xml_tree) for field in fields(cls)})
        return dc


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
        raise ValueError('cannot specify both default and default_factory')
    return FieldWithConfig(config, default, default_factory, init, repr, hash, compare, metadata)
