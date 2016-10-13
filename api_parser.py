from web_interfaces import *

class APIParser:

    def __init__(self):
        self.cache = {}
        self.interfaces = []
        self._set_interfaces()

    def request(self, req):
        if(req in self.cache):
            return self.cache[req]
        self.cache[req] = self._request(req)

    def _request(self, req):
        r = "["
        for i in self.interfaces:
            r += i.get_json(req) + ","
        return r[:-1]

    def _set_interfaces(self):
        self.interfaces.append(StackOverFlow())
        self.interfaces.append(HackerNews())

    def check_interfaces(self):
        for i in self.interfaces:
            print(i.get_json("microservices"))
