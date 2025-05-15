from flask import Flask, request, make_response, jsonify
import json

app = Flask(__name__)


@app.route('/event', methods=['POST'])
def handle_event():
    event_data = request.json
    print("Received Event:", json.dumps(event_data, indent=2))
    return "Event processed", 200


@app.route('/', methods=['POST', 'GET'])
def root():
    event_data = request.get_json()
    print("Received Event:", str(event_data))
    return_data = {}
    for data in event_data:
        if data.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            return_data["ValidationResponse"] = data.get(
                "data").get("validationCode")
    return make_response(jsonify(return_data), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
