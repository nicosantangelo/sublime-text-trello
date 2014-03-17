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

    def test_reexecute_calls_execute_only_if_renavigate_is_set_on_the_comand(self):
        self.executable.execute = MagicMock()
        self.executable.command = self.command_mock
        self.executable.reexecute()
        self.executable.command.renavigate = False
        self.executable.reexecute()
        self.assertEqual(self.executable.execute.call_count, 1)


if __name__ == '__main__':
    unittest.main()