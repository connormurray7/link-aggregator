"""
Created by Connor Murray (connormurray7@gmail.com)
on 10/14/2016

Contains the interface and implementations of every
external API service that is used on the website.
"""

import logging
import requests
from abc import ABC
from linkagg.message import LinkAggMessage


class WebInterface(ABC):
    """Abstract Base Class for each API class."""

    def __init__(self, url):
        self.base_url = url
        self.logger = logging.getLogger(__name__)

    def get_messages(self, request):
        # Make request
        # Parse response to common format
        # Send
        pass

    def default_request(self, params, key, title, url):
        messages = []
        try:
            response = requests.get(self.base_url, params).json()
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return []

        for hit in response[key]:
            messages.append(LinkAggMessage(hit[title], hit[url]))
        return messages


class StackOverFlow(WebInterface):
    """Requests and parses from Stack Overflow API."""

    # STACKOVERFLOW_URL = "https://api.stackexchange.com/2.2/search/advanced"

    def __init__(self, cfg):
        super().__init__(cfg['StackOverflow']['url'])

    def get_messages(self, query):
        params = {
            'q': query,
            'order': 'desc',
            'sort': 'relevance',
            'accepted': 'True',
            'site': 'stackoverflow',
            'pagesize': 15
        }
        messages = self.default_request(params, 'items', 'title', 'link')
        return {"Stack OverFlow": messages}


class HackerNews(WebInterface):
    """Requests and parses from Hacker News API."""

    # HACKER_NEWS_URL = "http://hn.algolia.com/api/v1/search"

    def __init__(self, cfg):
        super().__init__(cfg['HackerNews']['url'])

    def get_messages(self, query):
        params = {
            'query': query,
            'tags': 'story',
            'hitsPerPage': 15
        }
        messages = self.default_request(params, 'hits', 'title', 'url')
        return {"Hacker News": messages}


class Github(WebInterface):
    """Requests and parses from Github API."""

    # GITHUB_URL = "https://api.github.com/search/repositories"

    def __init__(self, cfg):
        super().__init__(cfg['Github']['url'])

    def get_messages(self, query):
        params = {
            'q': query,
            'sort': 'stars',
            'per_page': 15
        }
        messages = self.default_request(params, 'items', 'name', 'html_url')
        return {"Github": messages}
