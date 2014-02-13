import unittest

from .util import TrelloElementMock
from output import Output

class OutputTests(unittest.TestCase):
    def test_comments_returns_a_message_when_there_are_no_comments(self):
        self.assertEqual(Output.comments([]), "The card has no comments")

    def test_comments_a_ordered_list(self):
        comments = ["first", "first!!", "c'mon guys"]
        result = "1) first\n2) first!!\n3) c'mon guys\n"
        self.assertEqual(Output.comments(comments), result)

    def test_card_returns_the_information_of_the_card(self):
        card = TrelloElementMock("card name")
        output = "URL: " + card.url + "\n" + card.desc 
        self.assertEqual(Output.card(card), output)

if __name__ == '__main__':
    unittest.main()