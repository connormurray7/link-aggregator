class LinkAggMessage:

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def to_dict(obj):
        return obj.__dict__