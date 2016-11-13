import logging
from cache import LinkAggCache
from flask import Flask, request
from logging.handlers import RotatingFileHandler


app = Flask(__name__)


@app.route('/')
def handle_get():
    return app.send_static_file('index.html')

@app.route('/styles.css')
def handle_css():
    return app.send_static_file('styles.css')

@app.route('/search', methods=['POST'])
def handle_request():
    term = request.json['term']  # The search term
    app.logger.info("Received: " + term)
    app.logger.info("Handling request: " + term)
    return app.config['cache'].request(term)

def main():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler("log/link-agg.log", maxBytes=10000, backupCount=1)
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("Appplication started.")
    app.config['cache'] = LinkAggCache(handler)
    app.logger.addHandler(handler)
    app.run()


if __name__ == "__main__":
    main()
