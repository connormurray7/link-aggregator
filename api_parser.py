from web_interfaces import *

class APIParser:

    def __init__(self):
        self.cache = {}
        self.interfaces = []
        self._set_interfaces()

    def _set_interfaces(self):
        self.interfaces.append(StackOverFlow())
        self.interfaces.append(HackerNews())

    def check_interfaces(self):
        for i in self.interfaces:
            print(i.get_json("Hello!"))
