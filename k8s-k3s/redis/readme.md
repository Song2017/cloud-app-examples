## 安装
https://blog.csdn.net/rockstics/article/details/115768003
```
helm upgrade -i redis bitnami/redis -n db
- install redis, standalone
helm install redis bitnami/redis -n db -f helm_values.yml
- expose redis
kc apply -f svc_ie.yml

```
### issue
1. permission denied on append file
sudo chown -R 1001:1001 redis-data/

### installed readme
```
Redis&reg; can be accessed on the following DNS names from within your cluster:

    redis-master.db.svc.cluster.local for read/write operations (port 6379)
    redis-replicas.db.svc.cluster.local for read-only operations (port 6379)


To get your password run:
    export REDIS_PASSWORD=$(kubectl get secret --namespace db redis -o jsonpath="{.data.redis-password}" | base64 -d)

To connect to your Redis&reg; server:
1. Run a Redis&reg; pod that you can use as a client:

   kubectl run --namespace db redis-client --restart='Never'  --env REDIS_PASSWORD=$REDIS_PASSWORD  --image docker.io/bitnami/redis:7.0.11-debian-11-r20 --command -- sleep infinity

   Use the following command to attach to the pod:

   kubectl exec --tty -i redis-client \
   --namespace db -- bash

2. Connect using the Redis&reg; CLI:
   REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis-master
   REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis-replicas

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace db svc/redis-master 6379:6379 &
    REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h 127.0.0.1 -p 6379
```