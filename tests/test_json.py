import unittest

from datetime import datetime
import json
from dataclasses import dataclass

from json_mixin import JSONMixin, JSONConfig
from common import field as dcfield


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
            self.Note.from_json(self.note_dict)
        except Exception as e:
            self.fail(e)

    def test_from_dict_properties(self):
        note_dc = self.Note.from_json(self.note_dict)

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
        note_dc = self.Note.from_json(self.note_dict)

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
            tags: list[str]
            batter_types: list[str] = dcfield(config=JSONConfig(path="batters[*].type"))
            # topping_ids: list[int]  # str (json) -> int (dc) casting
            rating_count: int = dcfield(config=JSONConfig(path="rating.count"))
            rating_average: float = dcfield(config=JSONConfig(path="rating.average"))

        self.Donut = Donut
        with open("./tests/data/nested_document.json") as json_file:
            self.donut_dict = json.load(json_file)

    def test_one_level_simple_type_nesting(self):
        donut_dc = self.Donut.from_json(self.donut_dict)
        ratings_are_found = all([
            float(self.donut_dict["rating"]["average"]) == donut_dc.rating_average,
            int(self.donut_dict["rating"]["count"]) == donut_dc.rating_count
        ])
        self.assertTrue(ratings_are_found)

    def test_one_level_complex_type_nesting(self):
        donut_dc = self.Donut.from_json(self.donut_dict)
        self.assertEqual(
            self.donut_dict["tags"],
            donut_dc.tags
        )

    def test_one_level_complex_type_nesting_with_dict_value(self):
        donut_dc = self.Donut.from_json(self.donut_dict)

        self.assertEqual(
            [batter["type"] for batter in self.donut_dict["batters"]],
            donut_dc.batter_types
        )


class TestDeserialization(unittest.TestCase):

    def test_deserialization(self):
        with open("./tests/data/nested_document.json") as json_file:
            @dataclass
            class Donut(JSONMixin):
                id: int

            donut_dc = Donut.from_json(json_file.read(), deserialize=True)

        with open("./tests/data/nested_document.json") as json_file:
            donut_dict = json.load(json_file)

        self.assertTrue(donut_dc.id, donut_dict["id"])

# class TestJSONMixinDecorator(unittest.TestCase):
#     def test_decorator(self):
#         @jsonmixin
#         @dataclass
#         class Person:
#             first_name: str

#         taja = Person(first_name="Taja")
#         self.assertTrue(isinstance(taja, JSONMixin))


# if __name__ == '__main__':
#     unittest.main()
