#from abc import ABC, abstractmethod
import requests
import json

class LinkAggMessage():

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def to_dict(o):
        return o.__dict__


class WebInterface:

    def __init__(self, url):
        self.base_url = url

    def get_messages(self, request):
        #Make request
        #Parse response to common format
        #Send
        pass

class StackOverFlow(WebInterface):

    STACKOVERFLOW_URL = "https://api.stackexchange.com/2.2/search/advanced"

    def __init__(self):
        super().__init__(self.STACKOVERFLOW_URL)

    def get_messages(self, query):
        messages = []
        params = {
            'q' : query,
            'order' : 'desc',
            'sort' : 'relevance',
            'accepted' : 'True',
            'site' : 'stackoverflow'
        }
        response = requests.get(self.base_url, params).json()
        for item in response['items']:
            messages.append(LinkAggMessage(item['title'], item['link']))
        return {"Stack OverFlow" : messages}

class HackerNews(WebInterface):

    HACKER_NEWS_URL = "http://hn.algolia.com/api/v1/search"

    def __init__(self):
        super().__init__(self.HACKER_NEWS_URL)

    def get_messages(self, query):
        messages = []
        params = {'query' : query, 'tags' : 'story'}
        response = requests.get(self.base_url, params).json()
        for hit in response['hits']:
            messages.append(LinkAggMessage(hit['title'], hit['url']))
        return {"Hacker News" : messages}
