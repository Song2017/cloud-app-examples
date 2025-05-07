FROM crpi-ql917lqri2ngyv0e.cn-shanghai.personal.cr.aliyuncs.com/pub_2024/redis:7.4

VOLUME ["/data"]

COPY redis.conf /etc/redis/redis.conf

CMD [ "redis-server", "/etc/redis/redis.conf" ]