import unittest

from comment_formatter import CommentFormatter

class CommentFormatterTests(unittest.TestCase):
    def test_format_returns_a_message_when_there_are_no_comments(self):
        self.assertEqual(CommentFormatter.format([]), "The card has no comments")

    def test_(self):
        comments = ["first", "first!!", "c'mon guys"]
        result = "1) first\n2) first!!\n3) c'mon guys\n"
        self.assertEqual(CommentFormatter.format(comments), result)

if __name__ == '__main__':
    unittest.main()