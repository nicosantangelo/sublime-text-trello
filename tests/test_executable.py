import unittest
from .mock import MagicMock

from .util import CommandMock

from executable import Executable

class ExecutableTests(unittest.TestCase):
    def setUp(self):
        self.command_mock = CommandMock.create()
        self.executable = Executable()

    def test_execute_stores_the_command(self):
        self.executable.execute(self.command_mock)
        self.assertEqual(self.executable.command, self.command_mock)

    def test_execute_calls_display_on_the_command_supplied_as_argument(self):
        self.executable.execute(self.command_mock)
        self.command_mock.display.assert_called_with(self.executable.items(), self.executable.callback)

    def test_execute_calls_display_on_the_stored_command_if_None_is_passed(self):
        self.executable.command = self.command_mock
        self.executable.execute()
        self.command_mock.display.assert_called_with(self.executable.items(), self.executable.callback)


if __name__ == '__main__':
    unittest.main()