class Output():
    @classmethod
    def card(cls, card):
        badges = card.badges
        return """
{name} ({url})
    {desc}

The card has:
    {members} members
    {comments} comments
    {votes} votes
    {attachments} attachments
    {labels} labels
        """.format(
            name = card.name,
            url = card.url,
            desc = card.desc,
            members = len(card.members),
            comments = badges['comments'],
            votes = badges['votes'],
            attachments = badges['attachments'],
            labels = len(card.labels)
        )

    @classmethod
    def comments(cls, comments):
        comments_text = ""
        if comments:
            for index, comment_dict in enumerate(comments):
                comments_text += str(index + 1) + ") " + comment_dict['username'] + ": " + comment_dict['text'] + "\n"
        else:
            comments_text = "The card has no comments"

        return comments_text