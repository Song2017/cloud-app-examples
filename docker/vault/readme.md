https://lonegunmanb.github.io/essential-vault/

1. init postgres
```
CREATE TABLE vault_kv_store (
  parent_path TEXT COLLATE "C" NOT NULL,
  path        TEXT COLLATE "C",
  key         TEXT COLLATE "C",
  value       BYTEA,
  CONSTRAINT pkey PRIMARY KEY (path, key)
);

CREATE INDEX parent_path_idx ON vault_kv_store (parent_path);

CREATE TABLE vault_ha_locks (
  ha_key                                      TEXT COLLATE "C" NOT NULL,
  ha_identity                                 TEXT COLLATE "C" NOT NULL,
  ha_value                                    TEXT COLLATE "C",
  valid_until                                 TIMESTAMP WITH TIME ZONE NOT NULL,
  CONSTRAINT ha_key PRIMARY KEY (ha_key)
);
```

2. start
```
docker logs vault

docker-compose down
docker-compose up -d

docker exec -it vault sh
vault operator init

Unseal Key 1: 3OxmLpqjLNvRPpiuOv2Wg2rY5AkhpksC6MhB22oslRwv
Unseal Key 2: k6+xRb2m/hs12XIwbJKVC8uohjQYUUCojIrgNq1wb6oE
Unseal Key 3: D8egDAC1Hgs/ojhhUiONBVlv9YmIIMk87AXLEvRSROQ4
Unseal Key 4: Llq7QtQrtJBkPXQ0sJHX/wuEMQamOJJz6PjWxXec5549
Unseal Key 5: bcp7bED89D8caLRRuYZCSCI1OlTmOZy+v4mjiTyZRPnZ

Initial Root Token: s.67vV7NCGkp8uEj3jPoRG9VFs

vault login
```
admin/admin2024
s.sYVNqsqm0DchHIU28m9DXmNt