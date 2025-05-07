# 设置代理和验证服务
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GOSUMDB="sum.golang.google.cn"

# 重新执行依赖安装
go mod tidy