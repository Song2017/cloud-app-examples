from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        repo_url = data['repository']['clone_url']
        branch = data['ref'].split('/')[-1]
        print(repo_url, branch)
        subprocess.run(['bash', 'handle_webhook.sh', repo_url, branch])
        return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)