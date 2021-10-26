from dataclasses import fields

from common import Config, BaseMixin


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

        if base_type == list:
            elements = xml_tree.findall(config.xpath)
            value = cls.get_text_values(elements, config)
        else:
            element = xml_tree.find(config.xpath)
            value = cls.get_text_value(element, config)

        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def process_field_without_config(cls, field, xml_tree):
        value = xml_tree.findtext(field.name)
        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def from_xml(cls, xml_tree):
        dc = cls(**{field.name: cls.process_field(field, xml_tree) for field in fields(cls)})
        return dc
