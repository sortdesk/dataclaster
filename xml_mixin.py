from dataclasses import field as fieldtype, dataclass
from typing import List, Any, Union

import lxml.etree as ET
from lxml.etree import Element

from common import Config, BaseMixin
from exceptions import TooManyMatchesError


class XMLConfig(Config):
    def __init__(self, xpath: str) -> None:
        self.xpath = xpath


class XMLMixin(BaseMixin):

    @classmethod
    def _get_text_values(cls, elements: List[Element]) -> List[str]:
        text_values = []

        for element in elements:
            text_values.append(cls._get_text_value(element))

        return text_values

    @classmethod
    def _get_text_value(cls, element: Element) -> str:
        # TODO: this try/except is a mess
        try:
            return element.text
        except Exception:
            return str(element)

    @classmethod
    def _process_field(cls, field: fieldtype, xml_tree: Element) -> Any:

        cls.raise_for_types_not_supported(field.type)

        if hasattr(field, "config"):
            if not isinstance(field.config, XMLConfig):
                raise ValueError(
                    f"You must pass a valid instance of XMLConfig to the `config` parameter on {field.name}"
                )
            return cls._process_field_with_config(field, xml_tree)
        else:
            return cls._process_field_without_config(field, xml_tree)

    @classmethod
    def _process_field_with_config(cls, field: fieldtype, xml_tree: Element) -> Any:
        base_type = cls.get_base_type(field.type)
        config = field.config

        elements = xml_tree.xpath(config.xpath)
        if base_type == list:
            value = cls._get_text_values(elements)
        else:
            if len(elements) > 1:
                # TODO: improve message + maybe DRY this check with JSON mixin
                raise TooManyMatchesError(f"There are two many matches for {field.name}.")
            value = cls._get_text_value(elements[0])

        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def _process_field_without_config(cls, field: fieldtype, xml_tree: Element) -> Any:
        value = xml_tree.findtext(field.name)
        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def from_xml(cls, xml_tree: Union[Element, str], deserialize=False) -> dataclass:
        if deserialize:
            xml_tree = ET.fromstring(xml_tree)

        dc = cls.to_dataclass(xml_tree)
        return dc
