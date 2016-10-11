import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from api_parser import APIParser

app = Flask(__name__)

@app.route('/')
def handle_get():
    return "Hello there"

@app.route('/search', methods=['POST'])
def handle_request():
    data = request.json['term'] # The search term
    app.logger.info("Received: " + data)
    return "Received the request"

if __name__ == "__main__":
    handler = RotatingFileHandler('log/link-agg.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    #app.run()
    a = APIParser()
    a.check_interfaces()
