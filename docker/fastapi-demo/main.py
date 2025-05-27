import base64
import copy
import json
import logging
import os
import time

import requests
from fastapi import FastAPI, Security, HTTPException, Depends, Response, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN
import uvicorn
from starlette.responses import PlainTextResponse

from starlette.types import ASGIApp, Receive, Scope, Send

# Open Day
# Author: Ben Song
server = FastAPI(title="Open Day", version="1.0.0", docs_url=None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key_in_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class Util:
    API_KEY = os.getenv("api_key") or "test"  # In production, use environment variables
    WECOM_URL = os.getenv('wecom_webhook')
    WECOM_URL_DICT = json.loads(os.getenv('wecom_webhooks') or '{}')
    WECOM_TEMPLATE: dict = {
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

    @staticmethod
    async def get_api_key(api_key_header: str = Security(api_key_in_header)):
        if api_key_header == Util.API_KEY:
            return api_key_header
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Please check API key"
        )

    @staticmethod
    async def send_message(json_body: dict = None, url: str = None):
        # "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=**"
        try:
            logging.info(f"send_message start: {url}, {json_body}")
            url = url or Util.WECOM_URL or Util.WECOM_URL_DICT.get("")
            json_body = json_body or Util.WECOM_TEMPLATE
            response = requests.request("POST", url, json=json_body)
            logging.info(f"send_message response: {response.status_code}, {response.text}")
            return "ok"
        except Exception as e:
            err_msg = f"send_message error: {str(e)}"
            logging.error(err_msg)
            return err_msg


class LuckyModel(BaseModel):
    lucky_money_msg: str
    we_com_group: str


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 记录请求信息
        logger.info(f"--> {request.method} {request.url.path} from {request.client.host}")
        if request.query_params:
            logger.info(f"Query Params: {request.query_params}")
        if "application/json" in request.headers.get("Content-Type", ""):
            try:
                body = await request.json()
                logger.info(f"Body: {body}")
            except Exception as e:
                logger.warning(f"Failed to parse JSON body: {e}")

        # 执行路由处理
        response = await call_next(request)

        # 计算处理时间
        process_time = (time.time() - start_time) * 1000  # 毫秒
        logger.info(f"<-- {response.status_code} in {process_time:.2f}ms")

        return response


class SwaggerAuthMiddleware:
    def __init__(self, app: ASGIApp, api_key: str = None) -> None:
        self.server = app
        self.api_key = api_key

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["path"] == "/docs" and self.api_key not in str(
                scope.get('query_string')) and self.api_key not in str(scope.get('headers')):
            response = PlainTextResponse("Error: Unauthorized", status_code=401)
            await response(scope, receive, send)
        else:
            await self.server(scope, receive, send)


server.add_middleware(LoggingMiddleware)
server.add_middleware(SwaggerAuthMiddleware, api_key=Util.API_KEY)


@server.get("/", tags=["Test"])
async def root():
    return {"message": "Welcome to Open Day"}


@server.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=server.openapi_url,
        title=server.title,
        swagger_js_url="https://mt-cloud-tool.oss-cn-hangzhou.aliyuncs.com/swagger/swagger-ui-bundle.js",
        swagger_css_url="https://mt-cloud-tool.oss-cn-hangzhou.aliyuncs.com/swagger/swagger-ui.css",
        # swagger_favicon_url="/static/swagger-ui/favicon.png"
    )


@server.get("/secured", tags=["Test"])
async def secured_endpoint(api_key: str = Depends(Util.get_api_key)):
    return {"message": f"success - {api_key}"}


@server.options("/event", tags=["Event"])
async def event_endpoint_options(response: Response):
    response.headers["WebHook-Allowed-Origin"] = "*"
    response.status_code = 200
    return {"message": "success"}


@server.get("/event", tags=["Event"])
async def event_endpoint_get(api_key: str = Depends(Util.get_api_key)):
    return {"message": "/event GET"}


@server.post("/event", tags=["Event"])
async def event_endpoint_post(
        event_data: dict, response: Response,
        api_key: str = Depends(Util.get_api_key)):
    # send message to wechat
    msg_resp = "no message sent"
    logging.info(f"event_endpoint_post start: {event_data}")
    is_send = isinstance(event_data, dict) and any([
        event_data.get("send_message"),
        event_data.get("subject", "").startswith(
            os.getenv("msg_subject") or "device")])

    if is_send:
        json_body: dict = copy.deepcopy(Util.WECOM_TEMPLATE)
        json_body["template_card"]["emphasis_content"] = {
            "title": event_data.get("subject"),
            "desc": base64.b64decode(event_data.get(
                "data_base64") or "Cg==").decode()
        }
        msg_resp = await Util.send_message(json_body)
    response.headers["WebHook-Allowed-Origin"] = "*"
    return {"message": msg_resp}


@server.post("/lucky", tags=["Lucky"])
async def lucky_endpoint_post(
        event_data: LuckyModel, response: Response,
        api_key: str = Depends(Util.get_api_key)):
    # send message to wechat
    msg_resp = "no message sent"
    if event_data.lucky_money_msg and event_data.we_com_group:
        json_body: dict = copy.deepcopy(Util.WECOM_TEMPLATE)
        template_card = json_body["template_card"]
        template_card["emphasis_content"] = {
            "title": event_data.lucky_money_msg,
            "desc": "支付宝口令红包"
        }
        template_card["sub_title_text"] = "欢迎参加DBS Open Day！！"
        template_card["quote_area"]["quote_text"] = "Wayne：抢红包啦~\nBen：Welcome to Open day！！"

        msg_resp = await Util.send_message(json_body, Util.WECOM_URL_DICT.get(
            event_data.we_com_group))
    response.headers["WebHook-Allowed-Origin"] = "*"
    return {"message": msg_resp}


if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8080, log_level="info")
