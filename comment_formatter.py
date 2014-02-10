class CommentFormatter():
    @classmethod
    def format(cls, comments):
        comments_text = ""
        if comments:
            for index, comment_str in enumerate(comments):
                comments_text += str(index + 1) + ") " + comment_str + "\n"
        else:
            comments_text = "The card has no comments"      

        return comments_text