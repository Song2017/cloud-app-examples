1. [running-metabase-on-docker](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)
docker hub: https://hub.docker.com/r/metabase/metabase/tags
docker pull metabase/metabase:v0.47.9
```
docker run -it -p 3000:3000 \
  -e "MB_DB_TYPE=postgres" \
  -e "MB_DB_DBNAME=metabase" \
  -e "MB_DB_PORT=9002" \
  -e "MB_DB_USER=metabase" \
  -e "MB_DB_PASS=metabase123" \
  -e "MB_DB_HOST=139.1.1.1" \
  metabase/metabase:v0.53.11.3
```
