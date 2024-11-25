# install k3s on RHEL aliyun_3_x64_20G_alibase_20240819.vhd
# rancher-mirror.rancher.cn/k3s/v1.30.6-k3s1/k3s
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | \
  INSTALL_K3S_MIRROR=cn INSTALL_K3S_SKIP_SELINUX_RPM=true sh -s - \
  --system-default-registry "registry.cn-hangzhou.aliyuncs.com"
# create token for terraform
kubectl apply -f k3s-token.yaml
# fix the GFW (The Great Firewall of China) issues
#sed -i '$d' /etc/systemd/system/k3s.service
#echo '    --pause-image=registry.cn-shanghai.aliyuncs.com/nsmi/rancher-mirrored-pause:3.6 \' >> /etc/systemd/system/k3s.service
# "^rancher/(.*)": "mirrorproject/rancher-images/$1"
# tail -n 20 /var/lib/rancher/k3s/agent/containerd/containerd.log
#cat >> /etc/rancher/k3s/registries.yaml <<EOF
#mirrors:
#  "docker.io":
#    endpoint:
#      - "https://docker.mirrors.ustc.edu.cn" # 可根据需求替换 mirror 站点
#      - "https://registry-1.docker.io"
#EOF
#systemctl restart k3s
#sudo systemctl daemon-reload && sudo systemctl restart k3s
#systemctl restart k3s-agent.service
#terraform import kubernetes_deployment.coredns kube-system/coredns
#terraform import kubernetes_deployment.metrics_server kube-system/metrics-server
#terraform import kubernetes_deployment.local_path_provisioner kube-system/local-path-provisioner
# setup OS env variables
export TF_VAR_cluster_token=".."
export TF_VAR_atlantis_env_secure='{}'
# rm k3s
```
server: /usr/local/bin/k3s-uninstall.sh
agent: /usr/local/bin/k3s-agent-uninstall.sh
```