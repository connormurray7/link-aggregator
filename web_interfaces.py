#from abc import ABC, abstractmethod
import requests

class WebInterface:

    def __init__(self, url):
        self.base_url = url

    def get_json(self, request):
        #Make request
        #Parse response to common format
        #Send
        pass

class StackOverFlow(WebInterface):

    STACKOVERFLOW_URL = ""

    def __init__(self):
        super().__init__(self.STACKOVERFLOW_URL)

    def get_json(self, request):
        print("Inheriting from " + self.base_url)
        return "StackOverFlow"

class HackerNews(WebInterface):

    HACKER_NEWS_URL = "http://hn.algolia.com/api/v1/search"

    def __init__(self):
        super().__init__(self.HACKER_NEWS_URL)

    def get_json(self, query):
        params = {'query' : query, 'tags' : 'story'}
        response = requests.get(self.base_url, params).json()
        for hit in response['hits']:
            print(hit['url'])
        return "hello"
