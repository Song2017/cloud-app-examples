1. 使用阿里云的源（mirror）来加速软件包的下载和更新
```
cp /etc/apt/sources.list /etc/apt/sources.list.bak
sed -i "s@http://deb.debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list
sed -i "s@http://security.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list

apt update
```