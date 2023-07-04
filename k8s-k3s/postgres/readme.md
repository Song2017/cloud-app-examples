## helm
```
# prepare config, service, pv
kubectl apply -f pre.yml

helm search repo postgresql
helm pull bitnami/postgresql
helm upgrade -i pg bitnami/postgresql -n db -f helm_values.yml
helm uninstall pg -n db
```
### issues
1. access credentials
https://github.com/bitnami/charts/issues/2061#issuecomment-607326308
Postgres将密码写入文件.
如果挂载了独立的PVC, 那么在uninstall chart后, 需要将PVC和PV也删掉.
否则, 登录密码还是第一次安装时的配置


## guide
https://blog.sjgo.online/post/27/

## Todo
1. connect pool: pgbouncer
2. pgadmin: UI
3. backup
4. master-slave