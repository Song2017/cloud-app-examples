variable "alicloud_region" {
  type        = string
  description = "Alicloud region"
  default = "cn-shanghai"
}

variable "shanghai_access_key" {
  type     = string
  description = "Alicloud access key"  
  nullable = false
  sensitive = true
}

variable "shanghai_secret_key" {
  type     = string
  description = "Alicloud secret key"  
  nullable = false
  sensitive = true
}

variable "pg_logistics_conn" {
  type        = string
  description = "PG_LOGISTICS_CONN"
  sensitive = true
}

variable "pg_market_conn" {
  type        = string
  description = "PG_MARKET_CONN"
 sensitive = true
}

variable "crypt_iv" {
  type        = string
  description = "CRYPT_IV"
  sensitive = true
}

variable "crypt_key" {
  type        = string
  description = "CRYPT_KEY"
  sensitive = true
}