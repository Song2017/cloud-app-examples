import json

from fastapi import Security, HTTPException, Request
from datetime import datetime, timezone

import functools
import logging
import os
import time
import sys

import paho.mqtt.client as mqtt
import ssl
import threading

import requests

from fastapi.security.api_key import APIKeyHeader, APIKeyQuery
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import PlainTextResponse

from starlette.types import ASGIApp, Receive, Scope, Send

from db_sqlite import DBSqlite3, Config

# create logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
_logger = logging.getLogger(__name__)
_logger.addHandler(handler)
_logger.setLevel(logging.INFO)

api_key_in_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_in_query = APIKeyQuery(name="X-API-Key", auto_error=False)
connected_cond = threading.Condition()
connected_prop = False
connection_error = None
subscribed_cond = threading.Condition()
subscribed_prop = False
published_cond = threading.Condition()
published_prop = False
received_cond = threading.Condition()
received_prop = False


class Util:
    API_KEY = os.getenv("api_key") or "test"  # In production, use environment variables
    CERT_KEY = json.loads(os.getenv(
        "cert_key", '[]').replace("'", '"'))
    CERT_PEM = json.loads(os.getenv(
        "cert_pem", '[]').replace("'", '"'))
    WECOM_TEMPLATE: dict = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {
                "icon_url": "https://www.mt.com/etc/designs/mt/"
                            "widgets/shared/css/images/static/mt-footer-pyramid-logo.png",
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
                "title": "附言",
                "quote_text": "Wayne：欢迎参加DBS Open day！\nBen：惊喜多多~"
            },
            "sub_title_text": "欢迎参加DBS Open Day！",
            "horizontal_content_list": [
                {
                    "keyname": "邀请人",
                    "value": "Jocelyn"
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

    CWD = os.getcwd()

    def __init__(self, db_path: str = "db/open-day.db"):
        self.db_sqlite = DBSqlite3(db_path)
        self.lucky_msg = {"1": "今天开放日很高兴", "2": "今天很高兴开放日 ",
                          "3": "很高兴开放日今天", "4": "很高兴今天开放日"}

    @property
    def api_host(self) -> str:
        data = self.db_sqlite.filter_by_dict(Config, {"config_id": "api_host"})
        if len(data) > 0:
            return data[0].get('config_data')
        return "http://localhost:8080"

    @property
    def wecom_url_dict(self) -> dict:
        wecom_webhooks = os.getenv('wecom_webhooks', '{}').replace("'", '"')
        data = self.db_sqlite.filter_by_dict(Config, {"config_id": "wecom_webhooks"})
        if len(data) > 0:
            wecom_webhooks = data[0].get('config_data').replace("'", '"')
        return json.loads(wecom_webhooks)

    @property
    def wecom_group(self) -> str:
        data = self.db_sqlite.filter_by_dict(Config, {"config_id": "wecom_group"})
        if len(data) > 0:
            return data[0].get('config_data')
        return ""

    @staticmethod
    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    async def get_api_key(api_key_header: str = Security(api_key_in_header)):
        if api_key_header == Util.API_KEY:
            return api_key_header
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Please check API key"
        )

    @staticmethod
    async def get_api_key_query(api_key: str = Security(api_key_in_query)):
        if api_key == Util.API_KEY:
            return api_key
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Please check API key"
        )

    @functools.cached_property
    def mqtt_connection_settings(self) -> dict:
        cert_pem_file = os.path.join(Util.CWD, "cert.pem")
        cert_key_file = os.path.join(Util.CWD, "cert.key")
        if not os.path.exists(cert_pem_file) or not os.path.exists(cert_key_file):
            with open(cert_pem_file, "w") as f:
                f.write("\n".join(Util.CERT_PEM) + "\n")
            with open(cert_key_file, "w") as f:
                f.write("\n".join(Util.CERT_KEY) + "\n")
        return {
            "MQTT_CLEAN_SESSION": True,
            "MQTT_CLIENT_ID": "odcli",
            "MQTT_HOST_NAME": "xa01mttstmqegnsbx01.switzerlandnorth-1.ts.eventgrid.azure.net",
            "MQTT_TCP_PORT": 8883,
            "MQTT_KEEP_ALIVE_IN_SECONDS": 60,
            "MQTT_USERNAME": "odcli",
            "MQTT_PASSWORD": "",
            "MQTT_USE_TLS": True,
            "MQTT_CERT_FILE": cert_pem_file,
            "MQTT_KEY_FILE": cert_key_file,
            "MQTT_KEY_FILE_PASSWORD": ""
        }

    @functools.cached_property
    def mqtt_payload_template(self) -> dict:
        # todo set template name
        # time 设置
        return {
            "m": {
                "Message": {
                    "Header": {
                        "Version": "v1.0.0",
                        "MessageType": "Request",
                        "ActionCode": "Read",
                        "MessageID": "1234",
                        "Path": "Measurement"
                    }
                }
            },
            "mw": {
                "Message": {
                    "Header": {
                        "Version": "v1.0.0",
                        "MessageType": "Request",
                        "ActionCode": "Read",
                        "MessageID": "1234",
                        "Path": "Measurement/Weight"
                    }
                }
            },
            "mwd": {
                "Message": {
                    "Header": {
                        "Version": "v1.0.0",
                        "MessageType": "Request",
                        "ActionCode": "Read",
                        "MessageID": "1234",
                        "Path": "Measurement/Weight",
                        "DeviceName": "Scale1"
                    }
                }
            },
            "cz": {
                "Message": {
                    "Header": {
                        "Version": "v1.0.0",
                        "MessageType": "Request",
                        "ActionCode": "Update",
                        "MessageID": "1234",
                        "Path": "Command"
                    },
                    "Command": {
                        "DeviceName": "Scale1",
                        "CommandCode": "Zero"
                    }
                }
            },
            "ct": {
                "Message": {
                    "Header": {
                        "Version": "v1.0.0",
                        "MessageType": "Request",
                        "ActionCode": "Update",
                        "MessageID": "1234",
                        "Path": "Command"
                    },
                    "Command": {
                        "DeviceName": "Scale1",
                        "CommandCode": "Tare"
                    }
                }
            }
        }

    def send_event(self, client_id: str = "", topic: str = "Transfer", payload: str = "{}") -> bool:
        def on_connect(client, _userdata, _flags, rc):
            global connected_prop
            _logger.info("Connected to MQTT broker")
            # # In Paho CB thread.
            with connected_cond:
                if rc == mqtt.MQTT_ERR_SUCCESS:
                    connected_prop = True
                else:
                    raise Exception(mqtt.connack_string(rc))
                connected_cond.notify_all()

        def on_subscribe(client, _userdata, mid, _granted_qos):
            global subscribed_prop
            _logger.info(f"Subscribe for message id {mid} acknowledged by MQTT broker")
            # # In Paho CB thread.
            with subscribed_cond:
                subscribed_prop = True
                subscribed_cond.notify_all()

        def on_publish(_client, _userdata, mid):
            _logger.info(f"Sent publish with message id {mid}")
            global published_prop
            # # In Paho CB thread.
            with published_cond:
                published_prop = True
                published_cond.notify_all()

        def on_message(_client, _userdata, message):
            _logger.info(f"Received message on topic {message.topic} with payload {message.payload}")
            global received_prop
            # # In Paho CB thread.
            with received_cond:
                received_prop = True
                received_cond.notify_all()

        def on_disconnect(_client, _userdata, rc):
            _logger.info("Received disconnect with error='{}'".format(mqtt.error_string(rc)))
            global connected_prop
            # # In Paho CB thread.
            with connected_cond:
                connected_prop = False
                connected_cond.notify_all()

        def wait_for_connected(timeout: float = None) -> bool:
            with connected_cond:
                connected_cond.wait_for(lambda: connected_prop or connection_error, timeout=timeout, )
                if connection_error:
                    raise connection_error
                return connected_prop

        def wait_for_subscribed(timeout: float = None) -> bool:
            with subscribed_cond:
                subscribed_cond.wait_for(
                    lambda: subscribed_prop, timeout=timeout,
                )
                return subscribed_prop

        def wait_for_published(timeout: float = None) -> bool:
            with published_cond:
                published_cond.wait_for(
                    lambda: published_prop, timeout=timeout,
                )
                return published_prop

        def wait_for_receive(timeout: float = None) -> bool:
            with received_cond:
                received_cond.wait_for(
                    lambda: received_prop, timeout=timeout,
                )
                return received_prop

        def wait_for_disconnected(timeout: float = None):
            with connected_cond:
                connected_cond.wait_for(lambda: not connected_prop, timeout=timeout, )

        def create_mqtt_client(p_client_id, connection_settings):
            def_mqtt_client = mqtt.Client(
                client_id=p_client_id,
                clean_session=connection_settings['MQTT_CLEAN_SESSION'],
                protocol=mqtt.MQTTv311,
                transport="tcp",
            )
            if 'MQTT_USERNAME' in connection_settings:
                def_mqtt_client.username_pw_set(
                    username=connection_settings['MQTT_USERNAME'],
                    password=connection_settings['MQTT_PASSWORD'] if 'MQTT_PASSWORD' in connection_settings else None
                )
            if connection_settings['MQTT_USE_TLS']:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.minimum_version = ssl.TLSVersion.TLSv1_2
                context.maximum_version = ssl.TLSVersion.TLSv1_3

                if connection_settings['MQTT_CERT_FILE']:
                    context.load_cert_chain(
                        certfile=connection_settings['MQTT_CERT_FILE'],
                        keyfile=connection_settings['MQTT_KEY_FILE'],
                        password=connection_settings['MQTT_KEY_FILE_PASSWORD']
                    )
                if "MQTT_CA_FILE" in connection_settings:
                    context.load_verify_locations(
                        cafile=connection_settings['MQTT_CA_FILE'],
                    )
                else:
                    context.load_default_certs()

                def_mqtt_client.tls_set_context(context)
            return def_mqtt_client

        # INITIALIZE
        _logger.info("Initializing Paho MQTT client")
        client_id = client_id or self.mqtt_connection_settings["MQTT_CLIENT_ID"]
        mqtt_client = create_mqtt_client(client_id, self.mqtt_connection_settings)

        # ATTACH HANDLERS
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.on_publish = on_publish
        mqtt_client.on_subscribe = on_subscribe
        mqtt_client.on_message = on_message
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.enable_logger()

        # CONNECT
        _logger.info("{}: Starting connection".format(client_id))
        hostname = self.mqtt_connection_settings['MQTT_HOST_NAME']
        port = self.mqtt_connection_settings['MQTT_TCP_PORT']
        keepalive = self.mqtt_connection_settings["MQTT_KEEP_ALIVE_IN_SECONDS"]
        mqtt_client.connect(hostname, port, keepalive)
        _logger.info("Starting network loop")
        mqtt_client.loop_start()

        # WAIT FOR CONNECT
        if not wait_for_connected(timeout=10):
            _logger.info("{}: failed to connect.  exiting sample".format(client_id))
            sys.exit(1)

        # SUBSCRIBE
        (_subscribe_result, subscribe_mid) = mqtt_client.subscribe(topic)
        _logger.info(f"Sending subscribe requestor topic \"{topic}\" with message id {subscribe_mid}")

        # WAIT FOR SUBSCRIBE
        if not wait_for_subscribed(timeout=10):
            _logger.info("{}: failed to subscribe.  exiting sample without publishing".format(client_id))
            sys.exit(1)

        # PUBLISH
        publish_result = mqtt_client.publish(topic, payload)
        _logger.info(
            f"Sending publish with payload \"{payload}\" on topic \"{topic}\" with message id {publish_result.mid}")

        # WAIT FOR PUBLISH
        if not wait_for_published(timeout=10):
            _logger.info("{}: failed to publish.  exiting sample".format(client_id))
            sys.exit(1)

        # WAIT FOR MESSAGE RECEIVED
        if not wait_for_receive(timeout=10):
            _logger.info("{}: failed to receive meessage.  exiting sample".format(client_id))
            sys.exit(1)

        # DISCONNECT
        _logger.info("{}: Disconnecting".format(client_id))
        mqtt_client.disconnect()
        wait_for_disconnected(5)
        return True

    def msg_url(self, msg_id: str) -> str:
        return f"{self.api_host}/db?msg_id={msg_id}&X-API-Key={self.API_KEY}"

    async def wecom_send_card(self, json_body: dict = None, url: str = None,
                              msg_id: str = None):
        # "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=**"
        try:
            _logger.info(f"send_message start: {url}, {json_body}")
            url = url or self.wecom_url_dict.get(self.wecom_group)
            json_body = json_body or Util.WECOM_TEMPLATE
            # 企业微信提示“已停止访问该网页”
            # json_body["template_card"]["quote_area"]["url"] = self.msg_url(msg_id=msg_id)
            # json_body["template_card"]["card_action"]["url"] = self.msg_url(msg_id=msg_id)
            response = requests.request("POST", url, json=json_body)
            _logger.info(f"send_message response: {response.status_code}, {response.text}")
            return "ok"
        except Exception as e:
            err_msg = f"send_message error: {str(e)}"
            _logger.error(err_msg)
            return err_msg

    async def wecom_send_txt(self, content: str = "", url: str = None,
                             msg_id: str = None):
        # "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=**"
        try:
            _logger.info(f"send_message start: {url}, {content}")
            url = url or self.wecom_url_dict.get(self.wecom_group)
            json_body = {
                "msgtype": "text",
                "text": {
                    "content": content,
                    "mentioned_list": ["@all"],
                    # "mentioned_mobile_list": ["@all"]
                }
            }
            response = requests.request("POST", url, json=json_body)
            _logger.info(f"send_message response: {response.status_code}, {response.text}")
            return "ok"
        except Exception as e:
            err_msg = f"send_message error: {str(e)}"
            _logger.error(err_msg)
            return err_msg


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 记录请求信息
        _logger.info(f"request '{request.method} {request.url.path} {request.client.host}'")
        if request.query_params:
            _logger.info(f"query params '{request.query_params}'")
        if "application/json" in request.headers.get("Content-Type", ""):
            try:
                body = await request.json()
                _logger.info(f"body: '{body}'")
            except Exception as e:
                _logger.warning(f"'Failed to parse JSON body: {e}'")

        # 执行路由处理
        response = await call_next(request)

        # 计算处理时间
        process_time = (time.time() - start_time) * 1000
        _logger.info(f"response '{response.status_code} in {process_time:.2f}ms'")

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
