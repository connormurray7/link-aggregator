"""
Created by Connor Murray (connormurray7@gmail.com)
on 10/18/2016

Front door to the data being displayed on the page.
If the request is not cached then it passes along the search
term to every external API interface to make a request.
"""
import logging
import json
import time
import configparser
from collections import OrderedDict, deque
from linkagg.message import LinkAggMessage
from linkagg.web_interfaces import StackOverFlow, HackerNews, Github


class LinkAggCache(object):
    """ Returns JSON for a given request.

    Contains a list of interfaces that it will go to if it has not seen a request.
    Every request is cached with an LRU cache of size LRU_CACHE_SIZE.
    """

    def __init__(self, handler):
        self.requests = deque()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        cfg = configparser.ConfigParser()
        cfg.read('settings.ini')
        self.interfaces = []
        self._set_interfaces(cfg)
        self.rate_limit = int(cfg['Cache']['rate.limit'])
        self.cache = LRUCache(int(cfg['Cache']['size']))  # In memory caching layer.

    def request(self, req):
        """Accepts request and caches result if not seen before/recently."""
        if req in self.cache:
            return self.cache[req]
        if self._need_rate_limit():
            self.logger.info("Rate limiting request: " + req)
            return "Request error"
        self.cache[req] = self._request(req)
        return self.cache[req]

    def _request(self, req):
        self.logger.info(req + " was not cached, making API requests")
        responses = []
        for i in self.interfaces:
            responses.append(i.get_messages(req))
        return json.dumps(responses, default=LinkAggMessage.to_dict)

    def _set_interfaces(self, cfg):
        self.interfaces.append(StackOverFlow(cfg))
        self.interfaces.append(HackerNews(cfg))
        self.interfaces.append(Github(cfg))

    def _need_rate_limit(self):
        if len(self.requests) < self.rate_limit:
            return False
        if self.requests[-1] - self.requests[0] < 1:  # Requests within 1 sec.
            return False
        self.requests.popleft()
        self.requests.append(time.time())
        return True


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
        self.logger = logging.getLogger(__name__)
        super().__init__()

    def __setitem__(self, key, value):
        """Will evacuate the LRU item if cache is full."""
        if len(self) == self.capacity:
            self.logger.info("Cache reached capacity " + self.capacity + " evacuating item")
            self.popitem(False)
        OrderedDict.__setitem__(self, key, value)
