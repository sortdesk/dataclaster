import unittest

import xml.etree.ElementTree as ET
from dataclasses import dataclass


from xml_mixin import XMLMixin


class TestXMLMixin(unittest.TestCase):

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

    def test_from_xml_attributes(self):
        note_dc = self.Note.from_xml(self.note_tree)

        all_attributes_match = all([
            self.note_tree.findtext("recipient") == note_dc.recipient,
            self.note_tree.findtext("sender") == note_dc.sender,
            self.note_tree.findtext("heading") == note_dc.heading,
            self.note_tree.findtext("body") == note_dc.body
        ])

        self.assertTrue(all_attributes_match)
