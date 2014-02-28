import unittest

from .util import TrelloElementMock
from trello_collection import TrelloCollection

class TrelloCollectionTests(unittest.TestCase):
    def setUp(self):
        self.collection = TrelloElementMock.collection()
        self.trello_collection = TrelloCollection(self.collection)

    def test_names_returns_every_name_from_the_collection(self):
        self.assertEqual(self.trello_collection.names(), ["first", "second"])

    def test_find_gets_an_element_from_the_collection_by_index(self):
        self.assertEqual(self.trello_collection.find(1), self.collection[1])

    def test_on_init_it_gets_the_property_from_the_trello_element(self):
        trello_element = TrelloElementMock("card")
        collection = TrelloCollection(trello_element, "name") 
        self.assertEqual(collection.elements, trello_element.name)

if __name__ == '__main__':
    unittest.main()