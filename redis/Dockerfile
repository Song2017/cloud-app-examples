FROM redis:7.2-rc1-alpine

VOLUME ["/data"]

COPY redis.conf /etc/redis/redis.conf

CMD [ "redis-server", "/etc/redis/redis.conf" ]