import unittest

from datetime import datetime
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
            created_on: datetime

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


class TestJSONMixinDataTypes(unittest.TestCase):
    def setUp(self) -> None:
        @dataclass
        class Note(JSONMixin):
            recipient: str
            sender: str
            heading: str
            body: str
            priority: int
            created_on: datetime

        self.Note = Note
        with open("./tests/data/flat_document.json") as json_file:
            self.note_dict = json.load(json_file)

    def test_datetime(self):
        note_dc = self.Note.from_dict(self.note_dict)

        self.assertIsInstance(
            note_dc.created_on,
            datetime
        )


class TestJSONMixinWithNestedDocument(unittest.TestCase):
    def setUp(self) -> None:
        @dataclass
        class Donut(JSONMixin):
            id: int
            type: str
            name: str
            ppu: float
            rating_average: float
            rating_count: int
            # batter_types: list[str]
            # topping_ids: list[int]  # str (json) -> int (dc) casting

        self.Donut = Donut
        with open("./tests/data/nested_document.json") as json_file:
            self.donut_dict = json.load(json_file)

    def test_one_level_simple_type_nesting(self):
        donut_dc = self.Donut.from_dict(self.donut_dict)
        ratings_are_found = all([
            float(self.donut_dict["ratings"]["average"]) == donut_dc.rating_average,
            int(self.donut_dict["ratings"]["count"]) == donut_dc.rating_count
        ])
        self.assertTrue(ratings_are_found)


if __name__ == '__main__':
    unittest.main()
