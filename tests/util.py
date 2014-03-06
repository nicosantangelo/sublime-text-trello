from .mock import Mock, MagicMock, PropertyMock

class TrelloElementMock():
    def __init__(self, name):
        self.name = name
        self.closed = False

    def reload(self):
        pass

    @classmethod
    def collection(cls):
        return [TrelloElementMock("first"), TrelloElementMock("second")]

    @classmethod
    def mock_property(cls, property_name):
        element = Mock(spec = TrelloElementMock)
        property_mock = PropertyMock()
        setattr(type(element), property_name, property_mock)
        return (element, property_mock)

class TrelloCardMock():
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

class TrelloNotificationMock():
    def __init__(self, type, data):
        self.type = type
        self.data = data

class CommandMock():
    def display():
        pass

    def input():
        pass

    def defer(self, fn):
        fn()

    @classmethod
    def create(cls):
        return Mock(spec = CommandMock)

class OperationMock():
    @classmethod
    def create(cls, Operation):
        trello_element = TrelloElementMock("Element name")
        operation = Operation(trello_element)
        operation.command = CommandMock()
        return (operation, trello_element)

    @classmethod
    def instance(cls, operation):
        instance_mock = Mock()
        class_mock = Mock(return_value = instance_mock)
        operation.next_operation_class = MagicMock(return_value = class_mock)
        operation.previous_operation = MagicMock(return_value = class_mock)
        return (class_mock, instance_mock)

