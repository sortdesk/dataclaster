import unittest

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime


from xml_mixin import XMLMixin, Config, XMLConfig, fieldwrapper


class TestXMLMixinWithFlatDocument(unittest.TestCase):

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

    def test_from_xml_attributes(self):
        @dataclass
        class NoteWithAttributes(self.Note):
            recipient_gender: str = fieldwrapper(config=XMLConfig(xpath="./recipient", attrib="gender"))
            sender_gender: str = fieldwrapper(config=XMLConfig(xpath="./sender", attrib="gender"))
            body_lang: str = fieldwrapper(config=XMLConfig(xpath="./body", attrib="lang"))

        note_dc = NoteWithAttributes.from_xml(self.note_tree)

        all_attributes_match = all([
            self.note_tree.find("recipient").get("gender") == note_dc.recipient_gender,
            self.note_tree.find("sender").get("gender") == note_dc.sender_gender,
            self.note_tree.find("body").get("lang") == note_dc.body_lang
        ])

        self.assertTrue(all_attributes_match)

    def test_field_without_config(self):
        pass  # TODO


class TestXMLMixinWithNestedDocument(unittest.TestCase):
    def setUp(self) -> None:
        @dataclass
        class FoodItem(XMLMixin):
            name: str = fieldwrapper(config=XMLConfig(xpath="./name"))
            ppu: float = fieldwrapper(config=XMLConfig(xpath="./ppu"))
            regular_batter: str = fieldwrapper(config=XMLConfig(xpath="./batters/batter[@id='1001']"))
            chocolate_batter: str = fieldwrapper(config=XMLConfig(xpath="./batters/batter[@id='1002']"))
            blueberry_batter: str = fieldwrapper(config=XMLConfig(xpath="./batters/batter[@id='1003']"))
            no_topping: str = fieldwrapper(config=XMLConfig(xpath="./topping[@id='5001']"))
            glazed_topping: str = fieldwrapper(config=XMLConfig(xpath="./topping[@id='5002']"))
            sugar_topping: str = fieldwrapper(config=XMLConfig(xpath="./topping[@id='5005']"))
            sprinkles_topping: str = fieldwrapper(config=XMLConfig(xpath="./topping[@id='5006']"))
            chocolate_topping: str = fieldwrapper(config=XMLConfig(xpath="./topping[@id='5003']"))
            maple_topping: str = fieldwrapper(config=XMLConfig(xpath="./topping[@id='5004']"))

        self.FoodItem = FoodItem
        self.fooditem_tree = ET.parse("./tests/data/nested_document.xml")

    def test_nested_elements_are_found(self):
        fooditem_dc = self.FoodItem.from_xml(self.fooditem_tree)

        all_nested_elements_match = all([
            self.fooditem_tree.findtext("./batters/batter[@id='1001']") == fooditem_dc.regular_batter,
            self.fooditem_tree.findtext("./batters/batter[@id='1002']") == fooditem_dc.chocolate_batter,
            self.fooditem_tree.findtext("./batters/batter[@id='1003']") == fooditem_dc.blueberry_batter,
        ])

        self.assertTrue(all_nested_elements_match)

    def test_elements_are_found_by_attribute(self):
        fooditem_dc = self.FoodItem.from_xml(self.fooditem_tree)

        all_attrib_elements_match = all([
            self.fooditem_tree.findtext("./topping[@id='5001']") == fooditem_dc.no_topping,
            self.fooditem_tree.findtext("./topping[@id='5002']") == fooditem_dc.glazed_topping,
            self.fooditem_tree.findtext("./topping[@id='5005']") == fooditem_dc.sugar_topping,
            self.fooditem_tree.findtext("./topping[@id='5006']") == fooditem_dc.sprinkles_topping,
            self.fooditem_tree.findtext("./topping[@id='5003']") == fooditem_dc.chocolate_topping,
            self.fooditem_tree.findtext("./topping[@id='5004']") == fooditem_dc.maple_topping,
        ])

        self.assertTrue(all_attrib_elements_match)


class TestFieldSimpleAndSpecialConfig(unittest.TestCase):

    def setUp(self) -> None:
        @dataclass
        class Biscuit(XMLMixin):
            name: str = fieldwrapper(config=XMLConfig(xpath="./name"))
            weight: float = fieldwrapper(config=XMLConfig(xpath="./weight"))
            baked_on: datetime = fieldwrapper(config=XMLConfig(xpath="./baked_on"))
            is_delicious: bool = fieldwrapper(config=XMLConfig(xpath="./is_delicious"))
            rating: int = fieldwrapper(config=XMLConfig(xpath="./rating"))

        self.Biscuit = Biscuit
        self.biscuit_tree = ET.parse("./tests/data/datatype_document.xml")

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

        self.assertTrue(isinstance(something.__dataclass_fields__["name"].config, Config))

    def test_datatype_casting_for_simple_types(self):
        biscuit_dc = self.Biscuit.from_xml(self.biscuit_tree)

        all_types_are_correct = all([
            type(biscuit_dc.name) == str,
            type(biscuit_dc.weight) == float,
            type(biscuit_dc.rating) == int,
        ])

        self.assertTrue(all_types_are_correct)

    def test_datatype_casting_for_special_types(self):
        biscuit_dc = self.Biscuit.from_xml(self.biscuit_tree)

        all_types_are_correct = all([
            type(biscuit_dc.baked_on) == datetime,
            type(biscuit_dc.is_delicious) == bool,
        ])

        self.assertTrue(all_types_are_correct)


class TestFieldComplexConfig(unittest.TestCase):

    def test_datatype_casting_for_list_type_text(self):

        @dataclass
        class Cake(XMLMixin):
            batters: list = fieldwrapper(config=XMLConfig(xpath="./batters/batter"))

        cake_tree = ET.parse("./tests/data/nested_document.xml")
        cake_dc = Cake.from_xml(cake_tree)

        batters = [batter.text for batter in cake_tree.findall("./batters/batter")]

        self.assertTrue(cake_dc.batters == batters)

    def test_datatype_casting_for_list_type_attrib(self):
        @dataclass
        class Cake(XMLMixin):
            batters: list = fieldwrapper(config=XMLConfig(xpath="./batters/batter", attrib="id"))

        cake_tree = ET.parse("./tests/data/nested_document.xml")
        cake_dc = Cake.from_xml(cake_tree)

        batters = [batter.get("id") for batter in cake_tree.findall("./batters/batter")]

        self.assertTrue(cake_dc.batters == batters)

    def test_datatype_casting_for_list_type_attrib_with_element_type(self):

        @dataclass
        class Cake(XMLMixin):
            batters: list[int] = fieldwrapper(config=XMLConfig(xpath="./batters/batter"))

        cake_tree = ET.parse("./tests/data/nested_document.xml")
        cake_dc = Cake.from_xml(cake_tree)

        batters = [int(batter.get("id")) for batter in cake_tree.findall("./batters/batter")]

        self.assertTrue(cake_dc.batters == batters)


if __name__ == '__main__':
    unittest.main()
