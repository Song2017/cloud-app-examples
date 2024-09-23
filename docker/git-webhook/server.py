import threading

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


def run_script(repo_url, branch):
    subprocess.run(['bash', 'webhook.sh', repo_url, branch])


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        repo_url = data['repository']['clone_url']
        branch = data['ref'].split('/')[-1]
        print(repo_url, branch)
        # subprocess.run(['bash', 'webhook.sh', repo_url, branch])
        # 在单独的线程中运行脚本
        thread = threading.Thread(target=run_script, args=(repo_url, branch))
        thread.start()
        return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
