## Redis Dockerfile
This repository contains **Dockerfile** of [Redis](http://redis.io/) for [Docker](https://www.docker.com/)'s [automated build](https://registry.hub.docker.com/u/songgs/redis/) published to the public [Docker Hub Registry](https://registry.hub.docker.com/).

### Conf
enable default settings
```
# 守护进程（daemon），守护进程是linux中后台运行的进程，执行过程中打印的信息不显示在终端，完全不受任何终端影响
# docker container需要一个主进程, 如果只有redis, 并且设置为daemonize, 则docker进程不能独立运行
daemonize no
requirepass Pass123456

# 宿主机路径要挂载为绝对路径
dir /data

# mkdir -p ./data/logs
logfile "/data/logs/redis.log"
syslog-enabled yes
syslog-ident redis
```

### Usage

#### Run `redis-server`

    docker run -d --name redis -p 6379:6379 songgs/redis

#### Run `redis-server` with persistent data directory. (creates `dump.rdb`)

    docker run -d -p 6379:6379 -v <data-dir>:/data --name redis songgs/redis

#### Run `redis-server` with persistent data directory and password.
docker run --restart=always -dt -p 6379:6379 -v /root/redis:/home --name redis  crpi-ql917lqri2ngyv0e.cn-shanghai.personal.cr.aliyuncs.com/pub_2024/redis:7.4 redis-server /home/redis.conf --requirepass pass1234

#### Run `redis-cli`

    docker run -it --rm --link redis:redis songgs/redis bash -c 'redis-cli -h redis'

    ACL setUSER admin01 on >Admin0727

### Refer
- https://github.com/dockerfile/redis/blob/master/README.md