## k3s
https://docs.k3s.io/zh/cluster-access
需要先安装helm3
```
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get pods --all-namespaces
helm ls --all-namespaces
```
### 使用 kubectl 从外部访问集群
将 /etc/rancher/k3s/k3s.yaml 复制到位于集群外部的主机上的 ~/.kube/config。然后，将 server 字段的值替换为你 K3s Server 的 IP 或名称。现在，你可以使用 kubectl 来管理 K3s 集群。

### 添加helm镜像源
搭建helm镜像源 https://github.com/BurdenBear/kube-charts-mirror
helm repo add stable  https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts/
helm repo add azure http://mirror.azure.cn/kubernetes/charts/
helm repo add bitnami https://charts.bitnami.com/bitnami

### 查找要安装的app
helm repo list
helm search repo redis
helm show readme bitnami/redis

## 安装
https://blog.csdn.net/rockstics/article/details/115768003
helm pull bitnami/redis

helm upgrade -i redis bitnami/redis -n db -f helm_values.yml

helm uninstall redis -n db