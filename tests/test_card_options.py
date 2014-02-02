import unittest
from .mock import MagicMock

from card_options import CardOptions

class CardOptionsTests(unittest.TestCase):
    def setUp(self):
        fake_card = {}
        fake_command = {}
        self.card_options = CardOptions(fake_card, fake_command)

    def test_names_returns_the_card_operations(self):
        self.assertEqual(["Comment", "Archive", "Exit"], self.card_options.names())

    def test_call_action_calls_the_method_at_the_given_index(self):
        first_option = self.card_options.options[1]
        first_option["action"] = MagicMock()

        self.card_options.call_action(1)
        first_option["action"].assert_called_with()


if __name__ == '__main__':
    unittest.main()