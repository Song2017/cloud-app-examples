## Aliyun镜像加速器
https://cr.console.aliyun.com/cn-beijing/instances/mirrors
- Linux
```
通过修改daemon配置文件/etc/docker/daemon.json来使用加速器

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://asd.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Aliyun Ubunutu 加速器
sed -i "s@http://deb.debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list
sed -i "s@http://security.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list