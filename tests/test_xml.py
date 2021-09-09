from unittest.case import TestCase

import xml.etree.ElementTree as ET
from dataclasses import dataclass


from xml_mixin import XMLMixin, Config, fieldwrapper


class TestXMLMixin(TestCase):

    def setUp(self) -> None:
        @dataclass
        class Note(XMLMixin):
            recipient: str
            sender: str
            heading: str
            body: str

        self.Note = Note
        self.note_tree = ET.parse("./tests/data/flat_document.xml")

    def test_instantiation(self):
        try:
            XMLMixin()
        except Exception as e:
            self.fail(e)

    def test_from_xml(self):

        try:
            self.Note.from_xml(self.note_tree)
        except Exception as e:
            self.fail(e)

    def test_from_xml_tags(self):
        note_dc = self.Note.from_xml(self.note_tree)

        all_tags_match = all([
            self.note_tree.findtext("recipient") == note_dc.recipient,
            self.note_tree.findtext("sender") == note_dc.sender,
            self.note_tree.findtext("heading") == note_dc.heading,
            self.note_tree.findtext("body") == note_dc.body
        ])

        self.assertTrue(all_tags_match)

    # def test_from_xml_attributes(self):
    #     @dataclass
    #     class NoteWithAttributes(self.Note):
    #         recipient_gender: str = field(metadata=XMLConfig({"xpath": "./recipient", "attrib": "gender"}))
    #         sender_gender: str = field(metadata=XMLConfig({"xpath": "./sender", "attrib": "gender"}))
    #         body_lang: str = field(metadata=XMLConfig({"xpath": "./body", "attrib": "lang"}))

    #     note_dc = NoteWithAttributes.from_xml(self.note_tree)

    #     all_attributes_match = all([
    #         self.note_tree.find("recipient").get("gender") == note_dc.recipient_gender,
    #         self.note_tree.find("sender").get("gender") == note_dc.sender_gender,
    #         self.note_tree.find("body").get("lang") == note_dc.body_lang
    #     ])

    #     self.assertTrue(all_attributes_match)


class TestFieldConfig(TestCase):

    def test_fieldwrapper_preserves_metadata(self):
        config = Config()

        @dataclass
        class Something:
            name: str = fieldwrapper(config=config, metadata={"hello": "world"})

        something = Something(name="Pierre")

        self.assertTrue(something.__dataclass_fields__["name"].metadata["hello"] == "world")

    def test_fieldwrapper_passes_config(self):
        config = Config()

        @dataclass
        class Something:
            name: str = fieldwrapper(config=config, metadata={"hello": "world"})

        something = Something(name="Pierre")

        self.assertTrue(isinstance(something.__dataclass_fields__["name"].metadata["_config"], Config))
