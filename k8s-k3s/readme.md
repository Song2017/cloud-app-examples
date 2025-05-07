## Install
国内 https://docs.k3s.io/zh/quick-start
```shell
curl -sfL https://get.k3s.io | sh -
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--tls-san x.x.x.x" sh -s -
curl -sfL https://get.k3s.io | sh -s - --tls-san 47.96.1.60 --pause-image=registry.cn-shanghai.aliyuncs.com/nsmi/rancher-mirrored-pause:3.6
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh - 
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn INSTALL_K3S_SKIP_SELINUX_RPM=true sh  -
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh - --tls-san 47.96.1.60 --pause-image=registry.cn-shanghai.aliyuncs.com/nsmi/rancher-mirrored-pause:3.6 

echo $K3S_CONFIG_FILE
ls /etc/rancher/k3s
cat /etc/rancher/k3s/k3s.yaml
```

```
OS Ubuntu 22.0
防火墙
ufw disable
```
```
镜像加速 /etc/rancher/k3s/registries.yaml
mirrors:
  docker.io:
    endpoint:
      - "https://d2tuf8g*.mirror.aliyuncs.com"
```
```
安装k3s
https://docs.rancher.cn/docs/k3s/quick-start/_index     

离线安装, 要提前下载install.sh 和 k3s执行文件后运行
单节点:  INSTALL_K3S_SKIP_DOWNLOAD=true ./install.sh
k3s执行文件: curl -Lo /usr/local/bin/k3s https://github.com/k3s-io/k3s/releases/download/v1.27.3+k3s1/k3s; chmod a+x /usr/local/bin/k3s
install sh: https://get.k3s.io/

server 配置项: https://docs.k3s.io/zh/cli/server
k3s server --write-kubeconfig-mode=644
k3s server \
  --write-kubeconfig-mode "0644"    \
  --tls-san "foo.local"             \
  --node-label "foo=bar"
  # --docker \
  # --debug 

```
remove k3s
```
server: /usr/local/bin/k3s-uninstall.sh
agent: /usr/local/bin/k3s-agent-uninstall.sh

```
## Run in Docker
```
https://docs.k3s.io/zh/advanced#%E5%9C%A8-docker-%E4%B8%AD%E8%BF%90%E8%A1%8C-k3s

sudo docker run \
  --privileged \
  --name k3s-server-1 \
  --hostname k3s-server-1 \
  -p 6443:6443 \
  -d rancher/k3s:v1.27.3-k3s1 \
  server

sudo docker cp k3s-server-1:/etc/rancher/k3s/k3s.yaml ~/.kube/config
```
## rancher
rancher是管理多个集群的dashboard
https://www.rancher.cn/quick-start/
```
sudo docker run --privileged -d --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher:stable
```

## common issues
### dashboard
k3s kubectl -n kubernetes-dashboard create token admin-user
### file permission
sudo chown -R 1001:1001 redis-data/
### failed to pull and unpack image "docker.io/rancher/mirrored-pause:3.6"
sudo nano /etc/systemd/system/k3s.service
ExecStart=/usr/local/bin/k3s server --pause-image=registry.cn-shanghai.aliyuncs.com/nsmi/rancher-mirrored-pause:3.6 --disable-https
sudo systemctl daemon-reload
sudo systemctl restart k3s
### nothing provides container-selinux >= 3:2.191.0-1 needed by k3s-selinux-1.6-1.el9.noarch from rancher-k3s-common-stable
INSTALL_K3S_SELINUX_WARN=true

## DB App install step
1. create PV and PVC: pre.yml
2. helm install app
3. expose app service 