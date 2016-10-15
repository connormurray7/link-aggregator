import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from link_aggregator import *

app = Flask(__name__)


@app.route('/')
def handle_get():
    return "Hello there"


@app.route('/search', methods=['POST'])
def handle_request():
    term = request.json['term']  # The search term
    app.logger.info("Received: " + term)
    return app['cache'].request(term)


if __name__ == "__main__":
    handler = RotatingFileHandler('log/link-agg.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.config['cache'] = LinkAggCache()
    app.run()