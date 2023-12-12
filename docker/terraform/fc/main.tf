provider "alicloud" {
  access_key = var.shanghai_access_key
  secret_key = var.shanghai_secret_key
  region     = var.alicloud_region
}

locals {
  service_name         = "nomad-marketing-sms-production"
  function_name        = "cronjob-function"
  image_name_cronjob   = "nomad-marketing-sms-cronjob"
  cronjob_trigger_name = "cronjob-timer"
}

resource "alicloud_fcv2_function" "default" {
  service_name  = local.service_name
  function_name = local.function_name
  description   = "cron-job description"
  runtime       = "custom-container"
  timeout       = 60
  handler       = "index.handler"

  environment_variables = {
    CRYPT_KEY         = var.crypt_key
    CRYPT_IV          = var.crypt_iv
    PG_LOGISTICS_CONN = var.pg_logistics_conn
    PG_MARKET_CONN    = var.pg_market_conn
  }
  custom_container_config {
    image           = "registry-intl-vpc.cn-shanghai.aliyuncs.com/samarkand/${local.image_name_cronjob}:latest"
    command         = null
    args            = null
    web_server_mode = false
  }
}

resource "alicloud_fc_trigger" "default" {
  service    = local.service_name
  function   = local.function_name
  depends_on = [
    alicloud_fcv2_function.default,
  ]
  # 定时触发器的配置  
  name   = local.cronjob_trigger_name
  type   = "timer"
  config = <<EOF
                    {
    "enable": true,
    "payload": "",
    "cronExpression": "CRON_TZ=Asia/Shanghai 0 19 * * * *"
}
EOF  
}
