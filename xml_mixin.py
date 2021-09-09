from dataclasses import fields, field as dcfield
from typing import Type
import inspect


class XMLMixin:
    @classmethod
    def process_standard_field(cls, field, xml_tree):
        return xml_tree.findtext(field.name)

    @classmethod
    def process_complex_field(cls, field, xml_tree):
        xpath = field.metadata["xpath"]
        attrib = field.metadata["attrib"]
        element = xml_tree.find(xpath)
        print(element)
        if attrib:
            return element.get(attrib)
        else:
            return element.text

    @classmethod
    def process_field(cls, field, xml_tree):
        print(inspect.getmro(type(field.metadata)))
        if isinstance(field.metadata, Config):
            print("hello")
            return cls.process_complex_field(field, xml_tree)
        else:
            # TODO: maybe don't process at all?
            return cls.process_standard_field(field, xml_tree)

    @classmethod
    def from_xml(cls, xml_tree):
        dc = cls(**{field.name: cls.process_field(field, xml_tree) for field in fields(cls)})
        # print(dc)
        return dc


class Config:
    pass


def fieldwrapper(config: Type[Config], *args, **kwargs):
    # TODO: this will break if `field()` is called with args only
    kwargs["metadata"]["_config"] = config
    return dcfield(*args, **kwargs)
