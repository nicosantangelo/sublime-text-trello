import unittest
from .mock import MagicMock

from navigator import Navigator

class CommandMock(object):
    def execute():
        pass

class TrelloNavigatorCommandTests(unittest.TestCase):
    def setUp(self):
        self.commandMock = self.create_command_mock()
        self.navigator = Navigator(self.commandMock)

    def create_command_mock(self):
        mock = CommandMock()
        mock.execute = MagicMock()
        return mock

    def test_start_calls_show_boards_with_the_value_supplied(self):
        value = "not important"
        self.navigator.show_boards = MagicMock()
        self.navigator.start(value)

        self.navigator.show_boards.assert_called_with(value)


if __name__ == '__main__':
    unittest.main()