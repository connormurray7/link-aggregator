"""
Created by Connor Murray (connormurray7@gmail.com)
on 10/18/2016

Front door to the data being displayed on the page.
If the request is not cached then it passes along the search
term to every external API interface to make a request.
"""
from collections import OrderedDict
from web_interfaces import *
from message import LinkAggMessage
import json


class LinkAggCache:
    """ Returns JSON for a given request.

    Contains a list of interfaces that it will go to if it has not seen a request.
    Every request is cached with an LRU cache of size LRU_CACHE_SIZE.
    """

    LRU_CACHE_SIZE = 2048

    def __init__(self):
        self.cache = LRUCache(self.LRU_CACHE_SIZE) # In memory caching layer.
        self.interfaces = []
        self._set_interfaces()

    def request(self, req):
        """Accepts request and caches result if not seen before/recently."""
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
        # self.interfaces.append(Github())


class LRUCache(OrderedDict):
    """Stores a JSON string of a request.

    Inherits from OrderedDict so the least recently used item
    can be evacuated efficiently.

    Attributes:
        capacity: the maximum size of the cache.
        __setitem__: overrides the OrderedDict __setitem__
    """

    def __init__(self, capacity):
        self.capacity = capacity
        super()

    def __setitem__(self, key, value):
        """Will evacute the LRU item if cache is full."""
        if len(self) == self.capacity:
            self.popitem(False)
        OrderedDict.__setitem__(self, key, value)
