storage "postgresql" {
  connection_url = "postgresql://vault01:Vault2024@pgm-uf6mymenlrq9ft47ao.pg.rds.aliyuncs.com:5432/vault"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

ui = true