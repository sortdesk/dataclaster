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

    def test_from_json(self):
        try:
            self.Note.from_dict(self.note_dict)
        except Exception as e:
            self.fail(e)
