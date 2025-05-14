from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/event', methods=['POST'])
def handle_event():
    event_data = request.json
    print("Received Event:", json.dumps(event_data, indent=2))
    return "Event processed", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)