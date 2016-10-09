from flask import Flask, request
app = Flask(__name__)

@app.route('/search', methods=['POST'])
def handle_request():
    data = request.json['term'] # The search term
    print(data)
    return "got the data"

