import unittest
from .mock import MagicMock, Mock
from .util import TrelloElementMock, CommandMock, OperationMock

from operations import *

class BaseOperationTests(unittest.TestCase):
    def setUp(self):
        self.base_operation, self.trello_element = OperationMock.create(BaseOperation)
        self.class_mock, self.instance_mock = OperationMock.instance(self.base_operation)

    def test_names_sets_the_collection(self):
        self.base_operation.set_collection = MagicMock()
        self.base_operation.names()
        self.base_operation.set_collection.assert_called_with()

    def test_names_returns_every_name_from_the_collection_with_back_and_exit(self):
        self.assertEqual(self.base_operation.names(), ["..", "first", "second", "Exit"])

    def test_set_collection_gets_the_property_from_the_trello_element(self):
        self.base_operation.trello_element_property = MagicMock(return_value = "name")
        self.base_operation.set_collection()
        self.assertEqual(self.base_operation.collection, self.trello_element.name)

    def test_find_gets_an_element_from_the_collection_by_index(self):
        self.assertEqual(self.base_operation.find(1), self.base_operation.collection[1])

    def test_callback_uses_find_to_instantiate_the_operation_if_the_index_is_in_the_collection(self):
        self.base_operation.callback(1)
        self.class_mock.assert_called_with(self.base_operation.collection[0], self.base_operation)

    def test_callback_doesnt_call_find__if_the_index_is_bigger_than_the_collection_length(self):
        self.base_operation.callback(55)
        assert not self.class_mock.called

    def test_callback_calls_execute_on_the_operation(self):
        self.base_operation.callback(1)
        self.instance_mock.execute.assert_called_with(self.base_operation.command)

    def test_callback_calls_execute_on_the_previous_operation_if_index_is_0(self):
        self.base_operation.callback(0)
        self.base_operation.previous_operation.execute.assert_called_with()

class BoardOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = OperationMock.create(BoardOperation)

    def test_names_returns_every_name_from_the_collection_without_goback(self):
        self.assertEqual(self.operation.names(), ["first", "second", "Exit"])

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "boards")

    def test_callback_calls_execute_command_with_the_index(self):
        self.operation.execute_command = MagicMock()
        self.operation.callback(5)
        self.operation.execute_command.assert_called_with(5)

    def test_next_operation_class(self):
        self.assertEqual(self.operation.next_operation_class(), ListOperation)

class ListOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = OperationMock.create(ListOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "lists")

    def test_next_operation_class(self):
        self.assertEqual(self.operation.next_operation_class(), CardOperation)

class CardOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = OperationMock.create(CardOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "cards")

    def test_next_operation_class(self):
        self.assertEqual(self.operation.next_operation_class(), CardOptions)


if __name__ == '__main__':
    unittest.main()