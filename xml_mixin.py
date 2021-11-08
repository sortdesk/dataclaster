from common import Config, BaseMixin
from exceptions import TooManyMatchesError


class XMLConfig(Config):
    def __init__(self, xpath, attrib=None) -> None:
        self.xpath = xpath
        self.attrib = attrib


class XMLMixin(BaseMixin):

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
    def process_field(cls, field, xml_tree):

        cls.raise_for_types_not_supported(field.type)

        if hasattr(field, "config"):
            if not isinstance(field.config, XMLConfig):
                raise ValueError(
                    f"You must pass a valid instance of XMLConfig to the `config` parameter on {field.name}"
                )
            return cls.process_field_with_config(field, xml_tree)
        else:
            return cls.process_field_without_config(field, xml_tree)

    @classmethod
    def process_field_with_config(cls, field, xml_tree):
        base_type = cls.get_base_type(field.type)
        config = field.config

        elements = xml_tree.xpath(config.xpath)
        if base_type == list:
            value = cls.get_text_values(elements, config)
        else:
            if len(elements) > 1:
                # TODO: improve message + maybe DRY this check with JSON mixin
                raise TooManyMatchesError(f"There are two many matches for {field.name}.")
            value = cls.get_text_value(elements[0], config)

        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def process_field_without_config(cls, field, xml_tree):
        value = xml_tree.findtext(field.name)
        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def from_xml(cls, xml_tree):
        dc = cls.to_dataclass(xml_tree)
        return dc
