import logging
from cache import LinkAggCache
from flask import Flask, request
from logging.handlers import RotatingFileHandler


application = Flask(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler("log/link-agg.log", maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info("applicationplication started.")
application.config['cache'] = LinkAggCache(handler)
application.logger.addHandler(handler)

@application.route('/')
def handle_get():
    return application.send_static_file('index.html')

@application.route('/styles.css')
def handle_css():
    return application.send_static_file('styles.css')

@application.route('/search', methods=['POST'])
def handle_request():
    term = request.json['term']  # The search term
    application.logger.info("Received: " + term)
    application.logger.info("Handling request: " + term)
    return application.config['cache'].request(term)

def main():
    application.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
