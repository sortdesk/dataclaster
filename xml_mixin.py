from dataclasses import fields, field as dcfield
from typing import Type
# from xml.etree.ElementTree import XML


CONF_KEY_NAME = "_config"  # TODO: maybe UID?


class Config:
    pass


class XMLConfig(Config):
    def __init__(self, xpath, attrib=None) -> None:
        self.xpath = xpath
        self.attrib = attrib


class XMLMixin:
    @classmethod
    def process_field(cls, field, xml_tree):
        if isinstance(field.metadata.get(CONF_KEY_NAME), XMLConfig):
            config = field.metadata[CONF_KEY_NAME]
            return cls.process_field_with_config(config, xml_tree)
        else:
            return cls.process_field_without_config(field, xml_tree)

    @classmethod
    def process_field_with_config(cls, config, xml_tree):
        element = xml_tree.find(config.xpath)
        if config.attrib:
            return element.get(config.attrib)
        else:
            return element.text

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
