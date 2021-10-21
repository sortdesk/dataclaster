import unittest

import json
from dataclasses import dataclass

from json_mixin import JSONMixin


class TestJSONMixinWithFlatDocument(unittest.TestCase):
    def setUp(self) -> None:
        @dataclass
        class Note(JSONMixin):
            recipient: str
            sender: str
            heading: str
            body: str
            priority: int

        self.Note = Note
        with open("./tests/data/flat_document.json") as json_file:
            self.note_dict = json.load(json_file)

    def test_instantiation(self):
        try:
            JSONMixin()
        except Exception as e:
            self.fail(e)

    def test_from_dict(self):
        try:
            self.Note.from_dict(self.note_dict)
        except Exception as e:
            self.fail(e)

    def test_from_dict_properties(self):
        note_dc = self.Note.from_dict(self.note_dict)

        all_properties_match = all([
            self.note_dict["recipient"] == note_dc.recipient,
            self.note_dict["sender"] == note_dc.sender,
            self.note_dict["heading"] == note_dc.heading,
            self.note_dict["body"] == note_dc.body,
            self.note_dict["priority"] == note_dc.priority
        ])

        self.assertTrue(all_properties_match)
