import unittest

import lxml.etree as ET
from dataclasses import dataclass
from datetime import datetime


from common import field as dcfield
from xmlclasses import XMLCasting, Config, XMLConfig


FLAT_DOCUMENT_PATH = "./tests/data/flat_document.xml"
DATATYPE_DOCUMENT_PATH = "./tests/data/datatype_document.xml"
NESTED_DOCUMENT_PATH = "./tests/data/nested_document.xml"


class TestXMLMixinWithFlatDocument(unittest.TestCase):

    def setUp(self) -> None:
        @dataclass
        class Note(XMLCasting):
            recipient: str
            sender: str
            heading: str
            body: str

        self.Note = Note
        self.note_tree = ET.parse(FLAT_DOCUMENT_PATH)

    def test_instantiation(self):
        try:
            XMLCasting()
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
            recipient_gender: str = dcfield(config=XMLConfig(xpath="./recipient/@gender"))
            sender_gender: str = dcfield(config=XMLConfig(xpath="./sender/@gender"))
            body_lang: str = dcfield(config=XMLConfig(xpath="./body/@lang"))

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
        class FoodItem(XMLCasting):
            name: str = dcfield(config=XMLConfig(xpath="./name"))
            ppu: float = dcfield(config=XMLConfig(xpath="./ppu"))
            regular_batter: str = dcfield(config=XMLConfig(xpath="./batters/batter[@id='1001']"))
            chocolate_batter: str = dcfield(config=XMLConfig(xpath="./batters/batter[@id='1002']"))
            blueberry_batter: str = dcfield(config=XMLConfig(xpath="./batters/batter[@id='1003']"))
            no_topping: str = dcfield(config=XMLConfig(xpath="./topping[@id='5001']"))
            glazed_topping: str = dcfield(config=XMLConfig(xpath="./topping[@id='5002']"))
            sugar_topping: str = dcfield(config=XMLConfig(xpath="./topping[@id='5005']"))
            sprinkles_topping: str = dcfield(config=XMLConfig(xpath="./topping[@id='5006']"))
            chocolate_topping: str = dcfield(config=XMLConfig(xpath="./topping[@id='5003']"))
            maple_topping: str = dcfield(config=XMLConfig(xpath="./topping[@id='5004']"))

        self.FoodItem = FoodItem
        self.fooditem_tree = ET.parse(NESTED_DOCUMENT_PATH)

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
        class Biscuit(XMLCasting):
            name: str = dcfield(config=XMLConfig(xpath="./name"))
            weight: float = dcfield(config=XMLConfig(xpath="./weight"))
            baked_on: datetime = dcfield(config=XMLConfig(xpath="./baked_on"))
            is_delicious: bool = dcfield(config=XMLConfig(xpath="./is_delicious"))
            rating: int = dcfield(config=XMLConfig(xpath="./rating"))

        self.Biscuit = Biscuit
        self.biscuit_tree = ET.parse(DATATYPE_DOCUMENT_PATH)

    def test_fieldwrapper_preserves_metadata(self):
        config = Config()

        @dataclass
        class Something:
            name: str = dcfield(config=config, metadata={"hello": "world"})

        something = Something(name="Pierre")

        self.assertTrue(something.__dataclass_fields__["name"].metadata["hello"] == "world")

    def test_fieldwrapper_passes_config(self):
        config = Config()

        @dataclass
        class Something:
            name: str = dcfield(config=config, metadata={"hello": "world"})

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
        class Cake(XMLCasting):
            batters: list = dcfield(config=XMLConfig(xpath="./batters/batter"))

        cake_tree = ET.parse(NESTED_DOCUMENT_PATH)
        cake_dc = Cake.from_xml(cake_tree)

        batters = [batter.text for batter in cake_tree.findall("./batters/batter")]

        self.assertTrue(cake_dc.batters == batters)

    def test_datatype_casting_for_list_type_attrib(self):
        @dataclass
        class Cake(XMLCasting):
            batters: list = dcfield(config=XMLConfig(xpath="./batters/batter/@id"))

        cake_tree = ET.parse(NESTED_DOCUMENT_PATH)
        cake_dc = Cake.from_xml(cake_tree)

        batters = [batter.get("id") for batter in cake_tree.findall("./batters/batter")]

        self.assertTrue(cake_dc.batters == batters)

    def test_datatype_casting_for_list_type_attrib_with_simple_element_type(self):
        @dataclass
        class Cake(XMLCasting):
            batters: list[int] = dcfield(config=XMLConfig(xpath="./batters/batter/@id"))

        cake_tree = ET.parse(NESTED_DOCUMENT_PATH)
        cake_dc = Cake.from_xml(cake_tree)

        batters = [int(batter.get("id")) for batter in cake_tree.findall("./batters/batter")]

        self.assertTrue(cake_dc.batters == batters)


class TestDeserialization(unittest.TestCase):

    def test_deserialization(self):
        with open(DATATYPE_DOCUMENT_PATH) as xml_file:
            @dataclass
            class Biscuit(XMLCasting):
                id: str = dcfield(config=XMLConfig(xpath="./@id"))

            donut_dc = Biscuit.from_xml(xml_file.read(), deserialize=True)

        tree = ET.parse(DATATYPE_DOCUMENT_PATH).getroot()

        self.assertTrue(donut_dc.id, tree.get("id"))


if __name__ == '__main__':
    unittest.main()
