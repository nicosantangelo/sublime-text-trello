class TrelloCache():
    _last_list = None

    @classmethod
    def set(cls, list):
       cls._last_list = list

    @classmethod
    def get(cls):
        return cls._last_list

    @classmethod
    def is_empty(cls):
        return cls.get() == None
        