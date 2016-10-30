"""
Created by Connor Murray (connormurray7@gmail.com)
on 10/18/2016

Front door to the data being displayed on the page.
If the request is not cached then it passes along the search
term to every external API interface to make a request.
"""
import json
from collections import OrderedDict
from web_interfaces import *
from message import LinkAggMessage


class LinkAggCache:
    """ Returns JSON for a given request.

    Contains a list of interfaces that it will go to if it has not seen a request.
    Every request is cached with an LRU cache of size LRU_CACHE_SIZE.
    """

    LRU_CACHE_SIZE = 2048

    def __init__(self, handler):
        self.cache = LRUCache(self.LRU_CACHE_SIZE, handler)  # In memory caching layer.
        self.interfaces = []
        self._set_interfaces(handler)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)

    def request(self, req):
        """Accepts request and caches result if not seen before/recently."""
        self.logger.info("Request: " + req)
        if req in self.cache:
            return self.cache[req]
        self.cache[req] = self._request(req)
        return self.cache[req]

    def _request(self, req):
        self.logger.info(req + " was not cached, making API requests")
        responses = []
        for i in self.interfaces:
            responses.append(i.get_messages(req))
        return json.dumps(responses, default=LinkAggMessage.to_dict)

    def _set_interfaces(self, handler):
        self.interfaces.append(StackOverFlow(handler))
        self.interfaces.append(HackerNews(handler))
        # self.interfaces.append(Github(handler))


class LRUCache(OrderedDict):
    """Stores a JSON string of a request.

    Inherits from OrderedDict so the least recently used item
    can be evacuated efficiently.

    Attributes:
        capacity: the maximum size of the cache.
        __setitem__: overrides the OrderedDict __setitem__
    """

    def __init__(self, capacity, handler):
        self.capacity = capacity
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        super().__init__()

    def __setitem__(self, key, value):
        """Will evacuate the LRU item if cache is full."""
        if len(self) == self.capacity:
            self.logger.info("Full, evacuating item")
            self.popitem(False)
        OrderedDict.__setitem__(self, key, value)
