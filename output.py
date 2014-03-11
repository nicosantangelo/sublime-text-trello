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
    {labels_len} labels {labels}
        """.format(
            name = card.name,
            url = card.url,
            desc = card.desc,
            members = len(card.members),
            comments = badges['comments'],
            votes = badges['votes'],
            attachments = badges['attachments'],
            labels_len = len(card.labels),
            labels = cls.labels(card.labels)
        )

    @classmethod
    def labels(cls, labels):
        return "( " + ", ".join([ cls.label(label) for label in labels]) + " )" if len(labels) > 0 else ""

    @classmethod
    def label(cls, label):
        color = label['color'].capitalize()
        return color + ": " +  label['name'] if label['name'] else color

    @classmethod
    def comments(cls, comments):
        comments_text = ""
        if comments:
            for index, comment_dict in enumerate(comments):
                comments_text += cls.as_list_item(index) + comment_dict['username'] + ": " + comment_dict['text'] + "\n"
        else:
            comments_text = "The card has no comments"

        return comments_text

    @classmethod
    def notifications(cls, notifications):
        output = "Total unread: " + str(len(notifications))
        for index, notification in enumerate(notifications):
            output += "\n\n" + cls.as_list_item(index) + "Nofitication type: " + notification.type + "\n"
            output += cls.notification(notification)

        return output

    @classmethod
    def notification(cls, notification):
        output_array = [key.capitalize() + ": " + notification.data[key]['name'] for key in notification.data.keys() if 'name' in notification.data[key]]
        return "\n".join(output_array)

    @classmethod
    def as_list_item(cls, index):
        return str(index + 1) + ") "