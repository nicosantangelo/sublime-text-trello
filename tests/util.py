from .mock import Mock, PropertyMock

class TrelloElementMock():
    def __init__(self, name):
        self.name = name

    @classmethod
    def collection(cls):
        return [TrelloElementMock("first"), TrelloElementMock("second")]

    @classmethod
    def mock_property(cls, property_name):
        element = Mock(spec = TrelloElementMock)
        property_mock = PropertyMock()
        setattr(type(element), property_name, property_mock)
        return (element, property_mock)

class TrelloCardMock(object):
    def __init__(self):
        self.name = "card_name"
        self.url  = "card_url"
        self.desc = "card_desc"
        self.members = [TrelloElementMock("user1"), TrelloElementMock("user2")]
        self.labels  = [TrelloElementMock("label1"), TrelloElementMock("label2")]
        self.badges = {
            'votes': 4,
            'comments': 2,
            'attachments': 3
        }

class CommandMock(object):
    def display():
        pass

    def input():
        pass

    @classmethod
    def create(cls):
        return Mock(spec = CommandMock)