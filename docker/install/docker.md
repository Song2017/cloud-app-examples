## Getting Docker
https://docs.docker.com/compose/install/#scenario-one-install-docker-desktop
- Mac
brew install docker
- Linux
```
# 官网
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

# step 1: 安装必要的一些系统工具
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
# Step 4: 更新并安装 Docker-CE
sudo apt-get -y update
sudo apt-get -y install docker-ce
```

## Getting Docker Compose
https://docs.docker.com/compose/install/
- Mac
brew install docker-compose
- Linux
```
sudo apt-get -y update
sudo apt-get -y install docker-compose-plugin
```


