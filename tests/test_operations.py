import unittest
from .mock import MagicMock
from .util import *

from operations import *

class BaseOperationTests(unittest.TestCase):
    def setUp(self):
        self.base_operation, self.trello_element = create_operation(BaseOperation)

    def test_names_sets_the_collection(self):
        self.base_operation.set_collection = MagicMock()
        self.base_operation.names()
        self.base_operation.set_collection.assert_called_with()

    def test_names_returns_every_name_from_the_collection(self):
        self.assertEqual(self.base_operation.names(), ["first", "second"])

    def test_find_gets_an_element_from_the_collection_by_index(self):
        self.assertEqual(self.base_operation.find(1), self.base_operation.collection[1])

    def test_set_collection_gets_the_property_from_the_trello_element(self):
        self.base_operation.trello_element_property = MagicMock(return_value = "name")
        self.base_operation.set_collection()
        self.assertEqual(self.base_operation.collection, self.trello_element.name)

class BoardOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = create_operation(BoardOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "boards")

class ListOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = create_operation(ListOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "lists")

class CardOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = create_operation(CardOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "cards")


# Helper
def create_operation(Operation):
    trello_element = TrelloElementMock("Element name")
    operation = Operation(trello_element)
    operation.collection = TrelloElementMock.collection()
    return (operation, trello_element)


if __name__ == '__main__':
    unittest.main()