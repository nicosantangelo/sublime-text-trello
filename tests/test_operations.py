import unittest
from .mock import MagicMock, Mock
from .util import TrelloElementMock, CommandMock, OperationMock

from operations import *

class BaseOperationTests(unittest.TestCase):
    def setUp(self):
        self.base_operation, self.trello_element = OperationMock.create(BaseOperation)
        self.class_mock, self.instance_mock = OperationMock.instance(self.base_operation)
        self.collection = TrelloElementMock.collection()
        self.base_operation.collection = TrelloCollection(self.collection)

    def test_items_sets_the_collection(self):
        self.base_operation.set_collection = MagicMock()
        self.base_operation.items()
        self.base_operation.set_collection.assert_called_with()

    def test_items_returns_every_name_from_the_collection_with_the_added_options(self):
        self.base_operation.set_collection = MagicMock()
        self.assertEqual(self.base_operation.items(), ["..", "Create Base", "first", "second", "Exit"])

    def test_callback_uses_find_to_instantiate_the_operation_if_the_index_is_in_the_collection(self):
        self.base_operation.callback(2)
        self.class_mock.assert_called_with(self.collection[0], self.base_operation)

    def test_callback_calls_execute_on_the_operation(self):
        self.base_operation.callback(2)
        self.instance_mock.execute.assert_called_with(self.base_operation.command)

    def test_callback_doesnt_call_find_if_the_index_is_bigger_than_the_collection_length(self):
        big_index = 55
        self.base_operation.callback(big_index)
        assert not self.class_mock.called

    def test_callback_calls_execute_on_the_previous_operation_if_index_is_0(self):
        self.base_operation.callback(0)
        self.base_operation.previous_operation.execute.assert_called_with()

    def test_callback_calls_the_input_method_on_the_command_with_deferred_add_as_callback_if_index_is_1(self):
        self.base_operation.callback(1)
        self.base_operation.command.input.assert_called_with("Name", self.base_operation.deferred_add)

class BoardOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = OperationMock.create(BoardOperation)
        self.operation.collection = TrelloCollection(TrelloElementMock.collection())

    def test_items_returns_every_name_from_the_collection_without_goback(self):
        self.operation.set_collection = MagicMock()
        self.assertEqual(self.operation.items(), ["Create Board", "first", "second", "Exit"])

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "boards")

    def test_callback_calls_execute_command_with_the_index(self):
        self.operation.execute_command = MagicMock()
        self.operation.callback(5)
        self.operation.execute_command.assert_called_with(4)

    def test_callback_calls_the_input_method_on_the_command_with_deferred_add_as_callback_if_index_is_0(self):
        self.operation.callback(0)
        self.operation.command.input.assert_called_with("Name", self.operation.deferred_add)

    def test_next_operation_class(self):
        self.assertEqual(self.operation.next_operation_class(), ListOperation)

    def test_add_creates_a_board_with_the_text(self):
        text = "Some Text"
        self.trello_element.add_board = MagicMock()
        self.operation.add(text)
        self.trello_element.add_board.assert_called_with(text)

class ListOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = OperationMock.create(ListOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "lists")

    def test_next_operation_class(self):
        self.assertEqual(self.operation.next_operation_class(), CardOperation)

    def test_add_creates_a_list_with_the_text(self):
        text = "Some Text"
        self.trello_element.add_list = MagicMock()
        self.operation.add(text)
        self.trello_element.add_list.assert_called_with(text)

class CardOperationTests(unittest.TestCase):
    def setUp(self):
        self.operation, self.trello_element = OperationMock.create(CardOperation)

    def test_trello_element_property(self):
        self.assertEqual(self.operation.trello_element_property(), "cards")

    def test_next_operation_class(self):
        self.assertEqual(self.operation.next_operation_class(), CardOptions)

    def test_add_creates_a_card_with_the_text(self):
        text = "Some Text"
        self.trello_element.add_card = MagicMock()
        self.operation.add(text)
        self.trello_element.add_card.assert_called_with(text)


if __name__ == '__main__':
    unittest.main()