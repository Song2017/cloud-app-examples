from pydantic import BaseModel


class LuckyModel(BaseModel):
    lucky_money_msg: str
    we_com_group: str


class WeightModel(BaseModel):
    template: str = "mw"
    wecom_group: str = ""
    topic: str = "sa"
    version: str = "v1.0.0"
    message_type: str = "Request"
    action_code: str = "Read"
    message_id: str = "1234"
    path: str = "Measurement/Weight"
    device_name: str = "Scale1"
    view: str = "All"


class DBModel(BaseModel):
    action: str = "get"
    clear_table: bool = False
    filter: dict = None

    message_id: str = "123"
    message_name: str = "hongbao"
    message_type: str = "lucky"
    message_status: str = ""
    create_time: str = ""

    config_id: str = "wecom_webhooks"
    config_name: str = "1"
    config_data: str = "{}"
    config_status: str = "ok"
