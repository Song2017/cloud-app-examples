## install dashboard
```
https://blog.csdn.net/weixin_52270081/article/details/121426166 

https://www.cnblogs.com/databank/p/15664859.html
https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/web-ui-dashboard/
https://stackoverflow.com/questions/39864385/how-to-access-expose-kubernetes-dashboard-service-outside-of-a-cluster
https://blog.csdn.net/vampiresuper/article/details/122041917

https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml
安装dashboard及service
k3s kubectl create  -f recommended.yml -f dashboard.admin-rbac.yml
更新service type
kubectl -n kubernetes-dashboard edit service kubernetes-dashboard
  change the .spec.type to NodePort

查找对外端口: kubectl -n kubernetes-dashboard get service kubernetes-dashboard
https://120.46.78.11:30013/
创建登录token: 
k3s kubectl -n kubernetes-dashboard create token admin-user
```