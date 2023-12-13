1. [running-metabase-on-docker](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)
docker hub: https://hub.docker.com/r/metabase/metabase/tags
docker pull metabase/metabase:v0.47.9
```
docker run -it -p 3000:3000 \
  -e "MB_DB_TYPE=postgres" \
  -e "MB_DB_DBNAME=template1" \
  -e "MB_DB_PORT=30012" \
  -e "MB_DB_USER=user" \
  -e "MB_DB_PASS=admin123" \
  -e "MB_DB_HOST=120.1.1.1" \
   --name metabase metabase/metabase:v0.47.9
```
