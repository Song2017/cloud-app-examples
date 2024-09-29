import os
import threading
import time

import requests
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


def run_script(repo_url, branch):
    subprocess.run(['bash', 'webhook.sh', repo_url, branch])


def run_webhook(data: dict):
    repo_url = data['repository']['clone_url']
    branch = data['ref'].split('/')[-1]
    print("run_webhook", branch, repo_url)
    subprocess.run(['bash', 'webhook.sh', branch])
    # 在单独的线程中运行脚本
    # thread = threading.Thread(target=run_script, args=(repo_url, branch))
    # thread.start()


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # run_webhook(request.json)
        url = os.getenv('WEBHOOK_ASYNC')
        print("webhook", str(request.json)[:100])
        # Define the headers
        headers = {
            # "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Example of an Authorization header
            "Content-Type": "application/json",  # Specify content type if needed
            "X-Fc-Invocation-Type": "Async"
        }

        # Make the POST request
        response = requests.post(url, headers=headers, json=request.json)
        print("response", vars(response))
        return jsonify({'status': 'success'}), 200


@app.route('/webhook-sleep', methods=['POST'])
def webhook_async():
    if request.method == 'POST':
        print("webhook_async", str(request.json)[:100])
        run_webhook(request.json)
        # time.sleep(int(os.getenv('SLEEP_TIME') or 10))
        return jsonify({'status': 'success'}), 200


@app.route('/webhook', methods=['GET'])
def get_webhook():
    return "webhook"


@app.route('/pre-freeze', methods=['GET', 'POST', 'PUT', 'DELETE'])
def fc_webhook_pre_freeze():
    print('pre-freeze')
    time.sleep(30)
    return "webhook"


@app.route('/pre-stop', methods=['GET', 'POST', 'PUT', 'DELETE'])
def fc_webhook_pre_stop():
    print('pre-stop')
    time.sleep(30)
    return "webhook"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
