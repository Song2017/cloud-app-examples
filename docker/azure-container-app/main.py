import logging
import time

from flask import Flask, request, make_response, jsonify, Response

app = Flask(__name__)
# 配置日志格式和输出位置
logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 禁用默认的 Werkzeug 日志（可选）
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.DEBUG)  # 只记录错误日志


@app.before_request
def before_request():
    """记录请求开始时间和其他基本信息"""
    request.start_time = time.time()  # 存储请求开始时间到 request 对象
    logging.info(f"Request started: {request.method} {request.url}, {str(vars(request))}")


@app.after_request
def after_request(response: Response):
    """记录响应时间和状态码"""
    duration = round(time.time() - request.start_time, 4)  # 计算请求处理时间
    logging.info(
        f"Request completed in {duration}s with status {response.status_code}"
    )
    return response


@app.route('/event', methods=['POST', "GET"])
def handle_event():
    event_data = request.json
    print("Received Event:", str(event_data), str(request.headers))
    return "Event processed", 200


@app.route('/', methods=['POST', 'GET', "OPTIONS"])
def root():
    # https://learn.microsoft.com/zh-cn/azure/event-grid/end-point-validation-cloud-events-schema
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers["WebHook-Allowed-Origin"] = "*"
        return response

    event_data = request.get_json()
    print("Received Event:", str(event_data), str(request.headers))
    return_data = {"root page": "yes"}
    for data in event_data:
        if isinstance(data, dict) and data.get(
                "eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            return_data["ValidationResponse"] = data.get(
                "data").get("validationCode")
    resp = make_response(jsonify(return_data), 200)
    resp.headers["WebHook-Allowed-Origin"] = "*"
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
