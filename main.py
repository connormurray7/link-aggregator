import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from cache import *

app = Flask(__name__)


@app.route('/')
def handle_get():
    return app.send_static_file('index.html')


@app.route('/search', methods=['POST'])
def handle_request():
    term = request.json['term']  # The search term
    logging.getLogger("link-agg").info("Received: " + term)
    return app.config['cache'].request(term)


if __name__ == "__main__":
    log = logging.getLogger("link-agg")
    handler = RotatingFileHandler('log/link-agg.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    app.config['cache'] = LinkAggCache()
    app.run()
