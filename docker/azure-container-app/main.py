import json
import logging
import os
import time
from functools import wraps

import requests
from flask import Flask, request, make_response, jsonify, Response

app = Flask(__name__)

wecom_template = {
    "msgtype": "template_card",
    "template_card": {
        "card_type": "text_notice",
        "source": {
            "icon_url": "https://www.mt.com/etc/designs/mt/widgets/shared/css/images/static/mt-footer-pyramid-logo.png",
            "desc": "METTLER TOLEDO",
            "desc_color": 0
        },
        "main_title": {
            "title": "DBS OpenDay - IoT",
            "desc": "万物互联"
        },
        "emphasis_content": {
            "title": "10.0",
            "desc": "称量数据"
        },
        "quote_area": {
            "type": 1,
            "url": "https://www.mt.com/cn/zh/home.html",
            "appid": "APPID",
            "pagepath": "PAGEPATH",
            "title": "评价",
            "quote_text": "Jack：MT的衡器好~\nBalian：真的好！"
        },
        "sub_title_text": "支付宝口令红包: DBSIot",
        "horizontal_content_list": [
            {
                "keyname": "邀请人",
                "value": "DBS"
            }
        ],
        "jump_list": [
            {
                "type": 1,
                "url": "https://www.mt.com/cn/zh/home.html",
                "title": "MT官网"
            }
        ],
        "card_action": {
            "type": 1,
            "url": "https://www.mt.com/cn/zh/home.html",
            "appid": "APPID",
            "pagepath": "PAGEPATH"
        }
    }
}
# 配置日志格式和输出位置
logging.basicConfig(
    # filename='access.log',
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
    logging.info(f"Request started: {request.method} {request.url} {str(vars(request))}")


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
        response = make_response('empty', 200)
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
            send_message()
    resp = make_response(jsonify(return_data), 200)
    resp.headers["WebHook-Allowed-Origin"] = "*"
    return resp


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.args.get('api-key')

        if not api_key or api_key != os.getenv('api_key'):
            return jsonify(error="Invalid or missing API key"), 401

        return f(*args, **kwargs)

    return decorated


def send_message(json_body: dict = None):
    # "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=**"
    try:
        url = os.getenv('wecom_webhook')
        json_body = json_body or wecom_template
        response = requests.request("POST", url, json=json_body)
        logging.info(f"send_message response: {response.status_code}, {response.text}")
    except Exception as e:
        logging.error(f"send_message error: {str(e)}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
