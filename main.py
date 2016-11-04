import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from cache import LinkAggCache

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
    logger = logging.getLogger(__name__)
    handler = RotatingFileHandler("log/link-agg.log", maxBytes=10000, backupCount=1)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("Starting application")
    app.config['cache'] = LinkAggCache()
    app.run()
