from dataclasses import fields, field as dcfield
from typing import Type
from datetime import datetime
from distutils.util import strtobool

from dateutil.parser import parse


CONF_KEY_NAME = "_config"  # TODO: maybe UID?


class Config:
    pass


class XMLConfig(Config):
    def __init__(self, xpath, attrib=None) -> None:
        self.xpath = xpath
        self.attrib = attrib


class XMLMixin:
    SIMPLE_TYPES = [str, int, float]
    SPECIAL_TYPES = [bool, datetime]
    SUPPORTED_TYPES = SIMPLE_TYPES + SPECIAL_TYPES

    @classmethod
    def cast_data_type(cls, value, data_type=str):
        if data_type not in cls.SUPPORTED_TYPES:
            raise NotImplementedError(f"Data type {data_type} is not supported yet.")

        if data_type in cls.SIMPLE_TYPES:
            return data_type(value)
        elif data_type == bool:
            return bool(strtobool(value))
        elif data_type == datetime:
            return parse(value)

    @classmethod
    def process_field(cls, field, xml_tree):
        if isinstance(field.metadata.get(CONF_KEY_NAME), XMLConfig):
            return cls.process_field_with_config(field, xml_tree)
        else:
            return cls.process_field_without_config(field, xml_tree)

    @classmethod
    def process_field_with_config(cls, field, xml_tree):
        config = field.metadata[CONF_KEY_NAME]
        element = xml_tree.find(config.xpath)

        if config.attrib:
            attrib_text = element.get(config.attrib)
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


def fieldwrapper(config: Type[Config], *args, **kwargs):
    # TODO: this will break if `field()` is called with args only
    metadata = kwargs.setdefault("metadata", {})
    metadata[CONF_KEY_NAME] = config
    return dcfield(*args, **kwargs)
