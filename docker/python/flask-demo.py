from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Flask on Port 8080!'


if __name__ == '__main__':
    # 运行服务器，指定端口 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
