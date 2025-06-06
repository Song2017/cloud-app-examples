# IND400 and WeChat Work Integration API Development Project

## Overview

### Background

Azure provides the MQTT product Namespace Event Grid, which supports event-triggered custom services. IND400 supports
subscribing to the Namespace Event Grid and issuing control commands. To control and push IND400 messages to WeChat
Work, we have developed this API project to integrate WeChat Work's group bot with the event-triggered service.

### Objectives

- Develop a standardized API to enable bidirectional communication between Azure's MQTT Broker and WeChat Work.
- Automatically push IND400 weighing data to WeChat Work's application message center.
- Support remote control of IND400 via mobile phone menus.

### Participants

| Role            | Name                     |
|-----------------|--------------------------|
| Business Owner  | Jiang Wei                |
| Technical Leads | Song Guangshun, Pang Wei |

## Project Scope

### Flowchart

- ![img](../files/mt-open-day.png)
- ![swagger](../files/mt-open-day-swagger.png)
- ![wecom messages](../files/mt-open-day-messages.png)

### Features

- **Flow 1**: IND400 pushes data to WeChat Work  
  **Message Status**: Device Data

- **Flow 2**: Users remotely control IND400 via mobile devices  
  **Message Status**: Request Initiated, Request Received, Device Data

- **Configuration**: Group Bot Setup
- **Group Messages**:  
  **Type**: Message Card, Device Data Details

### Deliverables

#### Swagger Documentation

- [Swagger Doc - Dev](https://openday-api-xa01mttstmqrgsbx02-dev.switzerlandnorth.azurecontainer.io/docs)  
  *A token is required for access.*

- Event: MQTT Broker Trigger Service
- Weight: IND400 Control Node

```shell
/POST 
- body: template
mw: Weighing information from all devices
mwd: Weighing information from a specific device
cz: Command Zero
cz: Command Tare
```

- Mgmt (Management and Configuration Service)

```shell
/POST 
- body: action
init: Initialize SQLite database
config: Set configuration information
get: Retrieve historical messages and configuration data

/GET
Message: Retrieve historical messages
Config: Retrieve configuration information
```

#### Use Case - Initialize API Service

- **Initialize Database**

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

- **Initialize Group Bot**

```shell
Group bots can be configured multiple times, but only one can receive messages. The `wecom_group` configuration corresponds to the group bot's key value.
curl -X 'POST' \
  'http://localhost:8080/db' \
  -H 'accept: application/json' \
  -H 'X-API-Key: test' \
  -H 'Content-Type: application/json' \
  -d '{
  "action": "config",
  "config_id": "wecom_webhooks",
  "config_name": "1",
  "config_data": "{'1': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a6b9d688'}",
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

## Appendices

- [IND400 Product Page](https://www.mt.com/cn/zh/home/products/Industrial_Weighing_Solutions/scale-indicator/ind400.html)
- [WeChat Work Developer Documentation](https://developer.work.weixin.qq.com/document/path/91770)
- [Azure MQTT Application Samples](https://github.com/Azure-Samples/MqttApplicationSamples)