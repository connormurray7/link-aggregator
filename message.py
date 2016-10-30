"""
Created by Connor Murray (connormurray7@gmail.com)
on 10/22/2016

Wrapper class for an entry in every request.
"""


class LinkAggMessage:

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def to_dict(obj):
        return obj.__dict__
