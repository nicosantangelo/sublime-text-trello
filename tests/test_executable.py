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

    def test_execute_calls_display_on_the_command(self):
        self.executable.execute(self.command_mock)
        self.command_mock.display.assert_called_with(self.executable.names(), self.executable.callback)


if __name__ == '__main__':
    unittest.main()