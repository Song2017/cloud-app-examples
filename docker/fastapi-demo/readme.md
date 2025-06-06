# IND400与企业微信集成API开发项目

## 概述

### 背景

Azure提供MQTT产品Namespace Event Grid，支持事件触发自定义服务。IND400支持订阅Namespace Event
Grid并支持控制命令。为了控制和推送IND400的消息到企业微信，我们开发此API项目来集成企业微信的群机器人和事件触发服务。

### 目标

- 开发一套标准化API，实现Azure MQTT Broker与企业微信之间的双向通信
- 实现IND400的称量数据自动推送至企业微信应用消息中心
- 支持用户通过手机菜单远程控制IND400

### 参与人

| 角色    | 姓名     |
|-------|--------|
| 业务负责人 | 蒋唯     |
| 技术负责人 | 宋广顺，庞伟 |

## 项目范围

### 流程图

- ![img](../files/mt-open-day.png)
- ![swagger](../files/mt-open-day-swagger.png)
- ![wecom messages](../files/mt-open-day-messages.png)

### 功能

- 流程1：IND400推送数据到企业微信

消息状态：设备数据

- 流程2：用户在移动端远程控制IND400

消息状态：发起请求，接收请求，设备数据

- 配置功能：配置群机器人
- 群消息

类型：消息卡片，设备数据详情

### 交付

#### Swagger

- [swagger doc - dev](https://openday-api-xa01mttstmqrgsbx02-dev.switzerlandnorth.azurecontainer.io/docs)

Token is required

- Event MQTT Broker触发器服务
- Weight IND400控制节点

```shell
/POST 
- body: template
mw: 所有设备的称重信息
mwd: 指定设备的称重信息
cz: command Zero
cz: command Tare
```

- Mgmt 管理和配置服务

```shell
/POST 
- body: action
init: 初始化sqlite数据库
config: 设置配置信息
get: 获取历史消息和配置信息

/GET
Message: 获取历史消息
Config: 获取配置信息
```

#### 用例-初始化API服务

- 初始化数据库

```shell
curl -X 'POST' \
  'http://localhost:8080/db' \
  -H 'accept: application/json' \
  -H 'X-API-Key: test' \
  -H 'Content-Type: application/json' \
  -d '{
  "action": "init",
  "clear_table": true
}'
```

- 初始化群机器人

```shell
群机器人支持甚至多个,但是接收消息的只能有一个.wecom_group对应的config_data为群机器人的key值
curl -X 'POST' \
  'http://localhost:8080/db' \
  -H 'accept: application/json' \
  -H 'X-API-Key: test' \
  -H 'Content-Type: application/json' \
  -d '{
  "action": "config",
  "config_id": "wecom_webhooks",
  "config_name": "1",
  "config_data": "{'\''1'\'': '\''https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a6b9d688'\''}",
  "config_status": "ok"
}'

curl -X 'POST' \
  'http://localhost:8080/db' \
  -H 'accept: application/json' \
  -H 'X-API-Key: test' \
  -H 'Content-Type: application/json' \
  -d '{
  "action": "config",
  "config_id": "wecom_group",
  "config_name": "1",
  "config_data": "1",
  "config_status": "ok"
}'
```

## 附录

- https://www.mt.com/cn/zh/home/products/Industrial_Weighing_Solutions/scale-indicator/ind400.html
- https://developer.work.weixin.qq.com/document/path/91770
- https://github.com/Azure-Samples/MqttApplicationSamples