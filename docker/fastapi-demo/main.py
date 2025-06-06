import base64
import copy
import datetime
import json
import os
import time
from pathlib import Path

import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from db_sqlite import Message, Config
from utils import Util, LoggingMiddleware, SwaggerAuthMiddleware, _logger
from model import WeightModel, DBModel

# Open Day
# Ben Song GuangShun MT-CHN <GuangShun.Song@mt.com>

_db_file = "db/open-day.db"
_util = Util(db_path=_db_file)
_db = _util.db_sqlite
server = FastAPI(title="Open Day", version="1.0.0", docs_url=None)
server.add_middleware(LoggingMiddleware)
server.add_middleware(SwaggerAuthMiddleware, api_key=Util.API_KEY)


@server.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=getattr(server, "openapi_url"),
        title=getattr(server, "title"),
        swagger_js_url="https://mt-cloud-tool.oss-cn-hangzhou.aliyuncs.com/swagger/swagger-ui-bundle.js",
        swagger_css_url="https://mt-cloud-tool.oss-cn-hangzhou.aliyuncs.com/swagger/swagger-ui.css",
        # swagger_favicon_url="/static/swagger-ui/favicon.png"
    )


@server.get("/", tags=["Event"], summary="Root page")
async def root():
    return {"message": "Welcome to Open Day!"}


@server.options("/event", tags=["Event"], summary="Endpoint for MQTT broker")
async def event_endpoint_options(response: Response):
    response.headers["WebHook-Allowed-Origin"] = "*"
    response.status_code = 200
    return {"message": "success"}


@server.get("/event", tags=["Event"], summary="Endpoint for MQTT broker")
async def event_endpoint_get(api_key: str = Depends(Util.get_api_key)):
    return {"message": "/event GET"}


@server.post("/event", tags=["Event"], summary="Endpoint for MQTT broker")
async def event_endpoint_post(
        event_data: dict, response: Response,
        api_key: str = Depends(Util.get_api_key)):
    # send message to wechat
    msg_resp = "no message sent"
    msg_id = f"mqtt-{Util.utc_now()}"
    _logger.info(f"event_endpoint_post start: {event_data}")
    is_send = isinstance(event_data, dict) and any([
        event_data.get("data_base64"),
        event_data.get("subject")])
    mqtt_payload = base64.b64decode(
        event_data.get("data_base64") or "Cg==").decode()
    json_body: dict = copy.deepcopy(Util.WECOM_TEMPLATE)
    template_card = json_body["template_card"]
    template_card["quote_area"]["title"] = "设备信息"
    try:
        mqtt_payload_dict = json.loads(mqtt_payload)

        # extract weight info
        message = mqtt_payload_dict.get("Message", {})
        header = message.get("Header", {})
        measure = message.get("Measurement", [{}])[0]
        time_stamp = float(measure.get('Timestamp') or header.get(
            'Timestamp') or time.time() * 1000) // 1000
        w_date = datetime.datetime.fromtimestamp(time_stamp)
        quote_text = f"时间：{str(w_date)}\n"
        quote_text += f"重量：{measure.get('gross')} {measure.get('uomCode')}"
        template_card["quote_area"]["quote_text"] = quote_text
    except Exception as e:
        # retail type message
        _logger.error(f"event_endpoint_post: {str(e)}")
        lines: list = mqtt_payload.strip().split('\r\n')
        quote_text = f"时间：{lines[1].split(':')[1].strip()} {':'.join(lines[2].split(':')[1:]).strip()}\n"
        quote_text += f"重量：{lines[3].split(':')[1].strip()}"
        template_card["quote_area"]["quote_text"] = quote_text
        _logger.info("event_endpoint_post: " + str(e))
        mqtt_payload_dict = dict()

    if is_send:
        emphasis_content = {
            "title": "设备数据",
            "desc": event_data.get("subject"),
        }
        # 发送请求 s1_send_request
        # 收到请求 s2_confirm_request
        # 设备数据 desc + 口令红包 s3_receive_device_data
        data = _db.filter_by_dict(Message, {"message_type": "mobile"})
        if len(data) > 0:
            db_msg = Message().model_from_dict(data[0])
            if db_msg.tag == "s1_send_request" or mqtt_payload_dict.get("wecom_group"):
                emphasis_content = {
                    "title": "收到请求",
                    "desc": event_data.get("subject"),
                }
                json_body["template_card"][
                    "sub_title_text"] = "设备处理中"
                db_msg.tag = "s2_confirm_request"
                _db.save_messages(db_msg)
            elif db_msg.tag == "s2_confirm_request":
                json_body["template_card"][
                    "sub_title_text"] = _util.lucky_msg.get(_util.wecom_group)
                db_msg.tag = "s3_receive_device_data"
                _db.save_messages(db_msg)

        # extract messages
        json_body["template_card"]["emphasis_content"] = emphasis_content
        msg_resp = await _util.wecom_send_card(json_body, msg_id=msg_id)
        msg_resp += await _util.wecom_send_txt(content=mqtt_payload, msg_id=msg_id)
        _db.save_messages(Message(
            message_id=msg_id, event_data=mqtt_payload,
            message_data=json.dumps(json_body), message_type="mqtt"
        ))
    response.headers["WebHook-Allowed-Origin"] = "*"
    return {"message": msg_resp}


@server.get("/weight", tags=["Weight"], summary="User manage devices")
async def weight_endpoint_get():
    return {"message": '/weight'}


@server.post("/weight", tags=["Weight"], summary="User manage devices")
async def weight_endpoint_post(
        event_data: WeightModel, response: Response,
        api_key: str = Depends(Util.get_api_key)):
    pay_load: dict = _util.mqtt_payload_template.get(event_data.template)
    message_id = f"mobile-{Util.utc_now()}"
    if not pay_load:
        req_header_data = {
            "Version": event_data.version,
            "MessageType": event_data.message_type,
            "ActionCode": event_data.action_code,
            "MessageID": event_data.message_id,
            "DeviceName": event_data.device_name,
            "Path": event_data.path,
            "View": event_data.view,
        }
        header_data = {k: v for k, v in req_header_data.items() if v}
        pay_load = pay_load or {"Message": {"Header": header_data}}
    pay_load["message_id"] = message_id
    pay_load["wecom_group"] = event_data.wecom_group
    try:
        json_body: dict = copy.deepcopy(Util.WECOM_TEMPLATE)
        emphasis_content = {
            "title": "发送请求",
            "desc": "IND400",
        }
        # extract messages
        json_body["template_card"]["emphasis_content"] = emphasis_content
        json_body["template_card"]["sub_title_text"] = "移动端发送请求获取设备数据"
        msg_resp = await _util.wecom_send_card(json_body, msg_id=message_id)
        _db.save_messages(Message(
            message_id=message_id, event_data=json.dumps(pay_load),
            message_data=json.dumps(json_body), message_type="mobile",
            tag="s1_send_request"
        ))
        _logger.info("weight_endpoint_post: send wecom message: " + msg_resp)
        _util.send_event(topic=event_data.topic, payload=json.dumps(pay_load))
    except Exception as e:
        err = "weight_endpoint_post error: " + str(e)
        _logger.error(err)
        return {"message": err}
    return {"message": 'ok'}


@server.post("/mgmt", tags=["Mgmt"], summary="App management: config, history data")
async def topic_db_post(
        model: DBModel, response: Response,
        api_key: str = Depends(Util.get_api_key)):
    if model.action == "init":
        sqlite_file = os.path.join(Util.CWD, _db_file)
        file_path = Path(sqlite_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        _db.init_db(model.clear_table)
    if model.action == "get":
        data = _db.filter_by_dict(Message, filter_dict=model.filter)
        return JSONResponse(content=data, status_code=200)
    if model.action == "config":
        db_config = Config().model_from_dict(model.model_dump())
        _db.upsert_config(data=db_config)
    return {"message": 'ok'}


@server.put("/mgmt", tags=["Mgmt"], summary="App management: config, history data")
async def topic_db_put(
        model: DBModel, response: Response,
        api_key: str = Depends(Util.get_api_key)):
    db_msg = Message().model_from_dict(model.model_dump())
    _db.save_messages(db_msg)
    return {"message": 'ok'}


@server.get("/mgmt", tags=["Mgmt"], summary="App management: config, history data")
async def topic_db_get(
        item_id: str = "",
        db_model: str = "Message",
        api_key: str = Depends(Util.get_api_key)):
    if db_model == "Message":
        filter_dict = dict()
        if item_id:
            filter_dict["message_id"] = item_id
        data = _db.filter_by_dict(Message, filter_dict=filter_dict)
    else:
        filter_dict = dict()
        if item_id:
            filter_dict["config_id"] = item_id
        data = _db.filter_by_dict(Config, filter_dict=filter_dict)
    if len(data) == 1:
        data = data[0]
    return JSONResponse(content=data, status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        server,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(asctime)s - %(levelprefix)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": "%(asctime)s - %(levelprefix)s %(client_addr)s '%(request_line)s' %(status_code)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                }
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr"
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default"],
                    "level": "INFO"
                },
                "uvicorn.error": {
                    "level": "ERROR",
                },
                "uvicorn.access": {
                    "handlers": ["access"],
                    "level": "INFO",
                    "propagate": False
                }
            }
        })
