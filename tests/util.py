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

class CommandMock(object):
    def execute():
        pass

    @classmethod
    def create(cls):
        return Mock(spec = CommandMock)