docker pull emqx/mqttx-web

docker run -d --name mqttx-web -p 80:80 emqx/mqttx-web

docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx
admin/public
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 80:18083 emqx/emqx