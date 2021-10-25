from dataclasses import fields
from datetime import datetime
from distutils.util import strtobool
import typing

from dateutil.parser import parse


class Config:
    pass


class XMLConfig(Config):
    def __init__(self, xpath, attrib=None, data_type=str) -> None:
        self.xpath = xpath
        self.attrib = attrib
        self.data_type = data_type


class XMLMixin:
    SIMPLE_TYPES = [str, int, float]
    SPECIAL_TYPES = [bool, datetime]
    COMPLEX_TYPES = [list]
    SUPPORTED_TYPES = SIMPLE_TYPES + SPECIAL_TYPES + COMPLEX_TYPES

    @classmethod
    def cast_special_type(cls, value, data_type):
        if data_type == bool:
            return bool(strtobool(value))
        elif data_type == datetime:
            return parse(value)

    @classmethod
    def get_text_values(cls, elements, config):
        text_values = []

        for element in elements:
            text_values.append(cls.get_text_value(element, config))

        return text_values

    @classmethod
    def get_text_value(cls, element, config):
        if config.attrib:
            return element.get(config.attrib)
        else:
            return element.text

    @classmethod
    def cast_data_type(cls, config, data_type, xml_tree):
        base_type = typing.get_origin(data_type) or data_type  # handle e.g. list[str]

        if base_type not in cls.SUPPORTED_TYPES:
            raise NotImplementedError(f"Data type {base_type} is not supported yet.")

        # TODO: optimize conditionals below

        if base_type in cls.SIMPLE_TYPES:
            element = xml_tree.find(config.xpath)
            text_value = cls.get_text_value(element, config)
            return base_type(text_value)

        if base_type in cls.SPECIAL_TYPES:
            element = xml_tree.find(config.xpath)
            text_value = cls.get_text_value(element, config)
            return cls.cast_special_type(text_value, base_type)

        if base_type in cls.COMPLEX_TYPES:
            if base_type == list:
                element_type = typing.get_args(data_type)[0] if typing.get_args(data_type) else str

                elements = xml_tree.findall(config.xpath)
                text_values = cls.get_text_values(elements, config)

                cast_fn = cls.cast_special_type if element_type in cls.SPECIAL_TYPES else element_type

                return [cast_fn(text_value) for text_value in text_values]

    @classmethod
    def process_field(cls, field, xml_tree):
        if hasattr(field, "config"):
            if not isinstance(field.config, XMLConfig):
                raise ValueError(
                    f"You must pass a valid instance of XMLConfig to the `config` parameter on {field.name}"
                )
            # TODO: validation of data_type + config should probably happen here

            return cls.process_field_with_config(field.config, field.type, xml_tree)
        else:
            return cls.process_field_without_config(field, xml_tree)

    @classmethod
    def process_field_with_config(cls, config, data_type, xml_tree):
        return cls.cast_data_type(config, data_type, xml_tree)

    @classmethod
    def process_field_without_config(cls, field, xml_tree):
        # TODO: this is not casting the type !!
        return xml_tree.findtext(field.name)

    @classmethod
    def from_xml(cls, xml_tree):
        dc = cls(**{field.name: cls.process_field(field, xml_tree) for field in fields(cls)})
        return dc
