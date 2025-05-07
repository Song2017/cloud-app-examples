## Postgrest
- https://docs.postgrest.org/en/v12/tutorials/tut1.html
- config: https://docs.postgrest.org/en/v12/references/configuration.html
- api: https://postgrest.org/en/stable/references/api/tables_views.html
## DB role
```sql
create role anon noinherit;
create role authenticator noinherit;

GRANT SELECT, INSERT, UPDATE, DELETE ON platform_order TO authenticator;
GRANT SELECT, INSERT, UPDATE, DELETE ON sales_orders_detail TO authenticator;
GRANT SELECT ON sales_orders_detail TO anon;
GRANT SELECT ON platform_order TO anon;

REVOKE SELECT ON TABLE public.sales_orders_detail FROM anon;
```
## command
```shell

docker build -t pgt .
docker run -dt --restart=always  -p 8432:3000  pgt
docker run -it -p 8433:8080 -e API_URL="http://8.1.1.0:8432/" swaggerapi/swagger-ui
```

## API Usage
- generate jwt: https://jwt.io/
```shell
curl --location 'http://8.1.1.0:8432/sales_orders_detail?order=id.asc&offset=1&limit=2&select=id%2Cclient_order_ref' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYXV0aGVudGljYXRvciJ9.X9CdAbo-Lf_nkM2LDNDUMj5L83GyTSOIV8ph6rUOm1k'
```
