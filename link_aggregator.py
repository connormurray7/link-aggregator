from web_interfaces import *
import json
from collections import OrderedDict


class LinkAggMessage:

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def to_dict(obj):
        return obj.__dict__


class LinkAggCache:

    def __init__(self):
        self.cache = {}
        self.interfaces = []
        self._set_interfaces()

    def request(self, req):
        if req in self.cache:
            return self.cache[req]
        self.cache[req] = self._request(req)
        return self.cache[req]

    def _request(self, req):
        responses = []
        for i in self.interfaces:
            responses.append(i.get_messages(req))
        return json.dumps(responses, default=LinkAggMessage.to_dict)

    def _set_interfaces(self):
        self.interfaces.append(StackOverFlow())
        self.interfaces.append(HackerNews())


class LRUCache(OrderedDict):

    def __init__(self, capacity):
        self.capacity = capacity
        super()

    def __setitem__(self, key, value):
        if len(self) == self.capacity:
            self.popitem(False)
        OrderedDict.__setitem__(self, key, value)

