## install
https://github.com/bitnami/charts/tree/main/bitnami/redis
https://blog.csdn.net/rockstics/article/details/115768003
```
- default
helm upgrade -i redis bitnami/redis -n db
- install redis, standalone
helm install redis bitnami/redis -n db -f helm_values.yml
- expose redis nodeport
kc apply -f svc_ie.yml
helm uninstall redis -n db
```
### issue
1. permission denied on append file
sudo chown -R 1001:1001 redis-data/