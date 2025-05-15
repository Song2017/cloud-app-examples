from flask import Flask, request, make_response, jsonify
import json

app = Flask(__name__)


@app.route('/event', methods=['POST', "GET"])
def handle_event():
    event_data = request.json
    print("Received Event:", str(event_data), str(request.headers))
    return "Event processed", 200


@app.route('/', methods=['POST', 'GET'])
def root():
    event_data = request.get_json()
    print("Received Event:", str(event_data), str(request.headers))
    return_data = {"root page": "yes"}
    for data in event_data:
        if data.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            return_data["ValidationResponse"] = data.get(
                "data").get("validationCode")
    resp = make_response(jsonify(return_data), 200)
    resp.headers["WebHook-Allowed-Origin"] = "*"
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
