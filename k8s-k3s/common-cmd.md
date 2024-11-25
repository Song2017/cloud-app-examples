1. change default namespace
[kubectl config set-context --current --namespace=atlantis]()
2. show terraform logs
export TF_LOG=DEBUG
3. create a token with admin role
```shell
admin_account="tf-admin"
kubectl create serviceaccount ${admin_account} -n kube-system
kubectl create clusterrolebinding ${admin_account} --clusterrole=cluster-admin --serviceaccount=kube-system:${admin_account} 
kubectl create token admin-sa -n kube-system
kubectl -n kube-system describe secrets $(kubectl -n kube-system get secret | grep ${admin_account} | awk '{print $1}')

kubectl create serviceaccount admin-sa -n default
kubectl create clusterrolebinding admin-sa-binding --clusterrole=cluster-admin --serviceaccount=default:admin-sa
kubectl create token admin-sa -n default
TOKEN=$(kubectl get secret -n default $(kubectl get serviceaccount admin-sa -n default -o jsonpath='{.secrets[0].name}') -o jsonpath='{.data.token}' | base64 --decode)
kubectl create token admin-sa --duration=2160h
```
4. KubeCtl
export KUBECONFIG=~/.kube/config
kubectl scale deployment <deployment-name> --replicas=0
5. delete namespace
kubectl delete namespace argocd
6. logs
crictl pull registry.cn-shanghai.aliyuncs.com/nsmi/rancher-mirrored-coredns-coredns:1.11.3
journalctl -u k3s -f