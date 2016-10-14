from web_interfaces import *
import json


class APIParser:

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
