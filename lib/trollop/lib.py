from urllib.parse import urlencode
import json

# import requests
import sublime_requests as requests

def get_class(str_or_class):
    """Accept a name or actual class object for a class in the current module.
    Return a class object."""
    if isinstance(str_or_class, str):
        return globals()[str_or_class]
    else:
        return str_or_class


class TrelloConnection(object):

    def __init__(self, api_key, oauth_token):
        self.session = requests.session()

        self.key = api_key
        self.token = oauth_token

    def request(self, method, path, params=None, body=None):
        if not path.startswith('/'):
            path = '/' + path
        url = 'https://api.trello.com/1' + path

        params = params or {}
        params.update({'key': self.key, 'token': self.token})
        url += '?' + urlencode(params)

        # Trello recently got picky about headers.  Only set content type if
        # we're submitting a payload in the body
        if body:
            headers = {'Content-Type': 'application/json'}
        else:
            headers = None
        response = self.session.request(method, url, data=body, headers=headers)
        response.raise_for_status()
        return response.text

    def get(self, path, params=None):
        return self.request('GET', path, params)

    def post(self, path, params=None, body=None):
        return self.request('POST', path, params, body)

    def put(self, path, params=None, body=None):
        return self.request('PUT', path, params, body)

    def delete(self, path, params=None, body=None):
        return self.request('DELETE', path, params, body)

    def get_board(self, board_id):
        return Board(self, board_id)

    def get_card(self, card_id):
        return Card(self, card_id)

    def get_list(self, list_id):
        return List(self, list_id)

    def get_checklist(self, checklist_id):
        return Checklist(self, checklist_id)

    def get_member(self, member_id):
        return Member(self, member_id)

    def get_notification(self, not_id):
        return Notification(self, not_id)

    def get_organization(self, org_id):
        return Organization(self, org_id)

    @property
    def me(self):
        """
        Return a Membership object for the user whose credentials were used to
        connect.
        """
        return Member(self, 'me')


class Closable(object):
    """
    Mixin for Trello objects for which you're allowed to PUT to <id>/closed.
    """
    def close(self):
        path = self._prefix + self._id + '/closed'
        params = {'value': 'true'}
        result = self._conn.put(path, params=params)


class Deletable(object):
    """
    Mixin for Trello objects which are allowed to be DELETEd.
    """
    def delete(self):
        path = self._prefix + self._id
        self._conn.delete(path)


class Labeled(object):
    """
    Mixin for Trello objects which have labels.
    """

    # TODO: instead of set_label and get_label, just override the 'labels'
    #  property to call set and get as appropriate.

    _valid_label_colors = [
        'green',
        'yellow',
        'orange',
        'red',
        'purple',
        'blue',
    ]

    def set_label(self, color):
        color = color.lower()
        if color not in self._valid_label_colors:
            raise ValueError("invalid color")
        path = self._prefix + self._id + '/labels'
        params = {'value': color}
        self._conn.post(path, params=params)

    def clear_label(self, color):
        color = color.lower()
        if color not in self._valid_label_colors:
            raise ValueError("invalid color")
        path = self._prefix + self._id + '/labels/' + color
        self._conn.delete(path)


class Field(object):
    """
    A simple field on a Trello object.  Maps the attribute to a key in the
    object's _data dict.
    """

    def __init__(self, key=None):
        self.key = key

    def __get__(self, instance, owner):
        # Accessing instance._data will trigger a fetch from Trello if the
        # _data attribute isn't already present.
        return instance._data[self.key]


class DateField(Field):

    def __get__(self, instance, owner):
        raw = super(DateField, self).__get__(instance, owner)
        return raw
        # return isodate.parse_datetime(raw)


class ObjectField(Field):
    """
    Maps an idSomething string attr on an object to another object type.
    """

    def __init__(self, key, cls):

        self.key = key
        self.cls = cls

    def __get__(self, instance, owner):
        return self.related_instance(instance._conn, instance._data[self.key])

    def related_instance(self, conn, obj_id):
        return get_class(self.cls)(conn, obj_id)


class ListField(ObjectField):
    """
    Like an ObjectField, but a list of them.  For fleshing out things like
    idMembers.
    """

    def __get__(self, instance, owner):
        ids = instance._data[self.key]
        conn = instance._conn
        return [self.related_instance(conn, id) for id in ids]


class SubList(object):
    """
    Kinda like a ListField, but for things listed under a URL subpath (like
    /boards/<id>/cards), as opposed to a list of ids in the document body
    itself.
    """

    def __init__(self, cls):
        # cls may be a name of a class, or the class itself
        self.cls = cls

        # A dict of sublists, by instance id
        self._lists = {}

    def __get__(self, instance, owner):
        if not instance._id in self._lists:
            cls = get_class(self.cls)
            path = instance._prefix + instance._id + cls._prefix
            data = json.loads(instance._conn.get(path))
            self._lists[instance._id] = [cls(instance._conn, d['id'], d) for d in data]
        return self._lists[instance._id]


class TrelloMeta(type):
    """
    Metaclass for LazyTrello objects, allowing documents to have Field
    attributes that know their names without them having to be explicitly
    passed to __init__.
    """
    def __new__(cls, name, bases, dct):
        for k, v in dct.items():
            # For every Field on the class that wasn't initted with an explicit
            # 'key', set the field name as the key.
            if isinstance(v, Field) and v.key is None:
                v.key = k
        return super(TrelloMeta, cls).__new__(cls, name, bases, dct)


class LazyTrello(object):
    """
    Parent class for Trello objects (cards, lists, boards, members, etc).  This
    should always be subclassed, never used directly.
    """

    __metaclass__ = TrelloMeta

    # The Trello API path where objects of this type may be found. eg '/cards/'
    @property
    def _prefix(self):
        raise NotImplementedError("LazyTrello subclasses MUST define a _prefix")

    def __init__(self, conn, obj_id, data=None):
        self._id = obj_id
        self._conn = conn
        self._path = self._prefix + obj_id

        # If we've been passed the data, then remember it and don't bother
        # fetching later.
        if data:
            self._data = data

    def __getattr__(self, attr):
        if attr == '_data':
            # Something is trying to access the _data attribute.  If we haven't
            # fetched data from Trello yet, do so now.  Cache the result on the
            # object.
            if not '_data' in self.__dict__:
                self._data = json.loads(self._conn.get(self._path))

            return self._data
        else:
            raise AttributeError("%r object has no attribute %r" %
                                 (type(self).__name__, attr))

    def __unicode__(self):
        tmpl = u'<%(cls)s: %(name_or_id)s>'
        # If I have a name, use that
        if 'name' in self._data:
            return tmpl % {'cls': self.__class__.__name__,
                           'name_or_id': self._data['name']}

        return tmpl % {'cls': self.__class__.__name__,
                       'name_or_id': self._id}

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return str(self.__unicode__())

### BEGIN ACTUAL WRAPPER OBJECTS


class Action(LazyTrello):

    _prefix = '/actions/'
    data = Field()
    type = Field()
    date = DateField()
    creator = ObjectField('idMemberCreator', 'Member')


class Board(LazyTrello, Closable):

    _prefix = '/boards/'

    url = Field()
    name = Field('name')
    pinned = Field()
    prefs = Field()
    desc = Field()
    closed = Field()

    organization = ObjectField('idOrganization', 'Organization')

    actions = SubList('Action')
    cards = SubList('Card')
    checklists = SubList('Checklist')
    lists = SubList('List')
    members = SubList('Member')


class Card(LazyTrello, Closable, Deletable, Labeled):

    _prefix = '/cards/'

    url = Field()
    closed = Field()
    name = Field('name')
    badges = Field()
    checkItemStates = Field()
    desc = Field()
    labels = Field()

    board = ObjectField('idBoard', 'Board')
    list = ObjectField('idList', 'List')

    checklists = ListField('idChecklists','Checklist')
    members = ListField('idMembers', 'Member')

    def add_comment(self, text):
        path = self._path + '/actions/comments'
        return self._conn.post(path, dict(text=text))

    def comments(self):
        path = self._path + '/actions'
        response = self._conn.get(path, dict(filter="commentCard"))
        comments_json = json.loads(response)
        return [comment_json["data"]["text"] for comment_json in comments_json]

class Checklist(LazyTrello):

    _prefix = '/checklists/'

    checkItems = SubList('CheckItem')
    name = Field()
    board = ObjectField('idBoard', 'Board')
    cards = SubList('Card')

    # TODO: provide a nicer API for checkitems.  Figure out where they're
    # marked as checked or not.

    # TODO: Figure out why checklists have a /cards/ subpath in the docs.  How
    # could one checklist belong to multiple cards?

class CheckItem(LazyTrello):

    _prefix = '/checkItems/'

    name = Field()
    pos = Field()
    type = Field()

class List(LazyTrello, Closable):

    _prefix = '/lists/'

    closed = Field()
    name = Field('name')
    url = Field()
    board = ObjectField('idBoard', 'Board')
    cards = SubList('Card')

    # TODO: Generalize this pattern, add it to a base class, and make it work
    # correctly with SubList
    def add_card(self, name, desc=None):
        path = self._prefix + self._id + '/cards'
        body = json.dumps({'name': name, 'idList': self._id, 'desc': desc,
                           'key': self._conn.key, 'token': self._conn.token})
        data = json.loads(self._conn.post(path, body=body))
        card = Card(self._conn, data['id'], data)
        return card


class Member(LazyTrello):

    _prefix = '/members/'

    url = Field()
    fullname = Field('fullName')
    username = Field('username')

    actions = SubList('Action')
    boards = SubList('Board')
    cards = SubList('Card')
    notifications = SubList('Notification')
    organizations = SubList('Organization')


class Notification(LazyTrello):

    _prefix = '/notifications/'

    data = Field()
    date = DateField()
    type = Field()
    unread = Field()

    creator = ObjectField('idMemberCreator', 'Member')


class Organization(LazyTrello):

    _prefix = '/organizations/'

    url = Field()
    desc = Field()
    displayname = Field('displayName')
    name = Field()

    actions = SubList('Action')
    boards = SubList('Board')
    members = SubList('Member')
