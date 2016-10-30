"""
Created by Connor Murray (connormurray7@gmail.com)
on 10/14/2016

Contains the interface and implementations of every
external API service that is used on the website.
"""

import requests
from message import LinkAggMessage
from abc import ABC


class WebInterface(ABC):
    """Abstract Base Class for each API class."""

    def __init__(self, url):
        self.base_url = url

    def get_messages(self, request):
        # Make request
        # Parse response to common format
        # Send
        pass


class StackOverFlow(WebInterface):
    """Requests and parses from Stack Overflow API."""

    STACKOVERFLOW_URL = "https://api.stackexchange.com/2.2/search/advanced"

    def __init__(self):
        super().__init__(self.STACKOVERFLOW_URL)

    def get_messages(self, query):
        messages = []
        params = {
            'q': query,
            'order': 'desc',
            'sort': 'relevance',
            'accepted': 'True',
            'site': 'stackoverflow'
        }
        response = requests.get(self.base_url, params).json()
        for item in response['items']:
            messages.append(LinkAggMessage(item['title'], item['link']))
        return {"Stack OverFlow": messages}


class HackerNews(WebInterface):
    """Requests and parses from Hacker News API."""

    HACKER_NEWS_URL = "http://hn.algolia.com/api/v1/search"

    def __init__(self):
        super().__init__(self.HACKER_NEWS_URL)

    def get_messages(self, query):
        messages = []
        params = {'query': query, 'tags': 'story'}
        response = requests.get(self.base_url, params).json()
        for hit in response['hits']:
            messages.append(LinkAggMessage(hit['title'], hit['url']))
        return {"Hacker News": messages}


class Github(WebInterface):
    """Requests and parses from Github API."""

    GITHUB_URL = "https://api.github.com/search/repositories"

    def __init__(self):
        super().__init__(self.GITHUB_URL)

    def get_messages(self, query):
        messages = []
        params = {'q': query, 'sort': 'stars'}
        response = requests.get(self.base_url, params).json()
        for item in response['item']:
            messages.append(LinkAggMessage(item['name'], item['html_url']))
        return {"Github": messages}
