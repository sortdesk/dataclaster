import unittest

import xml.etree.ElementTree as ET
from dataclasses import dataclass


from xml_mixin import XMLMixin


class TestXMLMixin(unittest.TestCase):

    def test_instantiation(self):
        try:
            XMLMixin()
        except Exception as e:
            self.fail(e)

    def test_from_xml_with_flat_document(self):

        @dataclass
        class Note(XMLMixin):
            to: str
            from_: str
            heading: str
            body: str

        note_xml = ET.parse("./tests/data/flat_document.xml")

        Note.from_xml(note_xml)
