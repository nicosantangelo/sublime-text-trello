import unittest
from .mock import MagicMock, patch
from .util import *

from navigator import Navigator

default_value = "default"

def create_navigator_instance():
    commandMock = CommandMock.create()
    return Navigator(commandMock)

# Test cases
class TrelloNavigatorCommandTests(unittest.TestCase):
    def setUp(self):
        self.navigator = create_navigator_instance()

    def test_start_calls_show_boards_with_the_value_supplied(self):
        self.navigator.show_boards = MagicMock()
        self.navigator.start(default_value)

        self.navigator.show_boards.assert_called_with(default_value)


class TrelloNavigatorShowMethodChainTests(unittest.TestCase):
    def setUp(self):
        self.navigator = create_navigator_instance()
        self.navigator.show = MagicMock()
        self.navigator.last_trello_element = MagicMock(return_value = default_value)

    @patch('navigator.BoardOperation')
    def test_show_boards_calls_show_with_a_board_operation_and_show_lists_as_callback(self, MockClass):
        self.navigator.show_boards(default_value)
        self.generic_asserts(self.navigator.show_lists, MockClass)

    @patch('navigator.ListOperation')
    def test_show_lists_calls_show_with_a_list_operation_and_show_cards_as_callback(self, MockClass):
        self.navigator.show_lists(default_value)
        self.generic_asserts(self.navigator.show_cards, MockClass)

    @patch('navigator.CardOperation')
    def test_show_cards_calls_show_with_a_card_operation_and_show_card_options_as_callback(self, MockClass):
        self.navigator.show_cards(default_value)
        self.generic_asserts(self.navigator.show_card_options, MockClass)

    def generic_asserts(self, callback, MockClass):
        self.navigator.show.assert_called_with(MockClass.return_value, callback)
        MockClass.assert_called_with(default_value)


if __name__ == '__main__':
    unittest.main()