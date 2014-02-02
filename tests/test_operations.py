import unittest
from .mock import MagicMock
from .util import *

from operations import *

class BaseOperationTests(unittest.TestCase):
    def setUp(self):
        self.base_operation = BaseOperation()
        self.base_operation.set_collection = MagicMock()
        self.base_operation.collection = TrelloElementMock.collection()

    def test_element_names_sets_the_collection(self):
        self.base_operation.element_names()
        self.base_operation.set_collection.assert_called_with()

    def test_element_names_returns_every_name_from_the_collection(self):
        self.assertEqual(self.base_operation.element_names(), ["first", "second"])

    def test_find_gets_an_element_from_the_collection_by_index(self):
        self.assertEqual(self.base_operation.find(1), self.base_operation.collection[1])

class SpecificOperationTests(unittest.TestCase):
    def test_set_collection_calls_boards_on_the_element(self):
        self.assert_property_called(BoardOperation, "boards")

    def test_set_collection_calls_lists_on_the_element(self):
        self.assert_property_called(ListOperation, "lists")

    def test_set_collection_calls_cards_on_the_element(self):
        self.assert_property_called(CardOperation, "cards")

    def assert_property_called(self, Operation, property_name):
        element, property_mock = TrelloElementMock.mock_property(property_name)
        Operation(element).set_collection()
        property_mock.assert_called_with()

if __name__ == '__main__':
    unittest.main()