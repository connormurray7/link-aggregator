from abc import ABC, abstractmethod

class WebInterface(ABC):

    def __init__(self):
        self.base_url = "WebInterface"

    def get_json(self, request):
        #Make request
        #Parse response to common format
        #Send
        pass

class StackOverFlow(WebInterface):

    def get_json(self, request):
        print("Inheriting from " + self.base_url)
        return "StackOverFlow"

class HackerNews(WebInterface):

    def get_json(self, request):
        print("Inheriting from " + self.base_url)
        return "HackerNews"
