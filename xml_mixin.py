from dataclasses import fields


class XMLMixin:
    @classmethod
    def from_xml(cls, xml_tree):
        parameters = {
            field.name: xml_tree.findtext(field.name)
            for field in fields(cls)
        }
        return cls(**parameters)
