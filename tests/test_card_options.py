import unittest
from .mock import MagicMock

from .util import TrelloElementMock
from card_options import CardOptions

class CardOptionsTests(unittest.TestCase):
    def setUp(self):
        card = TrelloElementMock("card_name")
        self.card_options = CardOptions(card)

    def test_names_returns_the_card_operations(self):
        self.assertEqual(["..", "Show", "Comments", "Comment", "Archive", "Exit"], self.card_options.names())

    def test_callback_calls_the_method_at_the_given_index(self):
        action = self.mock_action_at(1)
        self.card_options.callback(1)
        action.assert_called_with()

    def mock_action_at(self, index):
        option = self.card_options.options[index]
        option["action"] = MagicMock()
        return option["action"]

if __name__ == '__main__':
    unittest.main()