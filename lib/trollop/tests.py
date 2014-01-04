import unittest
import json
import urlparse

import trollop
from trollop import TrelloConnection


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

class FakeRequest(object):
    """Mock for requests.session.request.  Init it with the headers and data
    that you want to get back when calling session.request.  Keeps a history of
    requests made, on session.request.history, so you can use a
    record-then-assert pattern."""

    def __init__(self, headers, data):
        self.headers = headers
        self.data = data
        self.history = []

    def __call__(self, method, url, *args, **kwargs):
        path = urlparse.urlparse(url).path
        self.history.append(AttrDict(vars()))
        try:
            return AttrDict(headers=self.headers,
                             text=json.dumps(self.data[path]),
                             status_code=200)
        except KeyError:
            return AttrDict(status_code=404)


class TrollopTestCase(unittest.TestCase):

    headers = {'status': 200}
    data = {}

    def setUp(self):
        self.conn = TrelloConnection('blah', 'blerg')
        # monkeypatch the http client
        self.conn.session.request = FakeRequest(self.headers, self.data)


class TestGetMe(TrollopTestCase):

    data = {'/1/members/me': {
        "id":"4e73a7ef5571166c5f53a93f",
        "fullName":"Brent Tubbs",
        "username":"btubbs",
        "gravatar":"e60b3c53235cd53f5e2b6401678c4f6a",
        "bio":"",
        "url":"https://trello.com/btubbs"
    }}

    def test(self):

        # Ensure that the connection has a 'me' property, with attributes for
        # the json keys returned in the response.  Accessing this attribute
        # will also force an http request
        assert self.conn.me.username == self.data['/1/members/me']['username']

        # Make sure that session.request was called with the right path and
        # method, by inspecting the list of requests made to the mock.
        req1 = self.conn.session.request.history[0]
        assert req1.url.startswith('https://api.trello.com/1/members/me')
        assert req1.method == 'GET'

class SublistTests(TrollopTestCase):
    data = {'/1/members/me/boards/':
                [{'id': 'fakeboard1', 'name': 'Fake Board 1'},
                 {'id': 'fakeboard2', 'name': 'Fake Board 2'}],
            '/1/boards/fakeboard1/lists/':
                [{'id': 'fakeboard1_fakelist', 'idBoard': 'fakeboard1', 'name':
                  'Fake List from Fake Board 1'}],
            '/1/boards/fakeboard2/lists/':
                [{'id': 'fakeboard2_fakelist', 'idBoard': 'fakeboard2', 'name':
                  'Fake List from Fake Board 2'}]}

    def test_cache_bug_fixed(self):
        # assert that fakeboard1 and fakeboard2 have distinct sublists.
        # Fixes https://bitbucket.org/btubbs/trollop/changeset/36e3c41c7016
        assert (self.conn.me.boards[0].lists[0].name ==
                'Fake List from Fake Board 1')
        assert (self.conn.me.boards[1].lists[0].name ==
                'Fake List from Fake Board 2')

class ChecklistItemTests(TrollopTestCase):

    data = { '/1/checklists/fakeCheckListId/checkItems/':
            [
                {   'id':   'fakeCheckItem1',
                    'name': 'fake Check Item 1',
                    'type': 'check',
                    'pos':  123456 },
                {   'id':   'fakeCheckItem2',
                    'name': 'fake Check Item 2',
                    'type': 'check',
                    'pos':  123457 },
            ]}

    def test_checkItem_members(self):
        checklist = self.conn.get_checklist('fakeCheckListId')

        assert(checklist.checkItems[0].name == 'fake Check Item 1')
        assert(checklist.checkItems[0].type == 'check')
        assert(checklist.checkItems[1].pos  == 123457)

class TestLabeled(object):
    def test_Cards_are_labeled(self):
        """
        Cards should have set_label and clear_label methods.
        """
        assert hasattr(trollop.Card, 'set_label')
        assert hasattr(trollop.Card, 'clear_label')
