# Linux 搭建 Fabric 区块链测试环境

## 环境说明

Fabric 测试环境通常依赖 Docker、Docker Compose、Go、Git、curl 等工具。建议在干净的 Linux 虚拟机或测试服务器上搭建，避免和生产环境混用。

## 安装基础工具

```bash
yum install -y git curl wget vim
```

Ubuntu 环境：

```bash
apt update
apt install -y git curl wget vim
```

## 安装 Docker

```bash
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
systemctl enable docker
systemctl start docker
docker version
```

如果服务器无法访问外网，需要提前准备离线安装包或配置代理。

## 安装 Docker Compose

```bash
docker compose version
```

如果系统已安装新版 Docker，一般直接支持 `docker compose`。旧版本可能使用 `docker-compose` 命令。

## 安装 Go

下载 Go 安装包后解压：

```bash
tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
```

配置环境变量：

```bash
cat >> /etc/profile <<'EOF'
export GOROOT=/usr/local/go
export GOPATH=/data/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
EOF

source /etc/profile
go version
```

## 下载 Fabric Samples

```bash
mkdir -p /data/fabric
cd /data/fabric
git clone https://github.com/hyperledger/fabric-samples.git
cd fabric-samples
```

如果网络受限，可以从可访问环境下载后上传到服务器。

## 启动测试网络

进入测试网络目录：

```bash
cd /data/fabric/fabric-samples/test-network
```

启动网络：

```bash
./network.sh up
```

创建通道：

```bash
./network.sh createChannel
```

部署链码：

```bash
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go
```

## 验证容器

```bash
docker ps
```

应能看到 peer、orderer、ca 等相关容器。

查看日志：

```bash
docker logs <container-name>
```

## 关闭网络

```bash
./network.sh down
```

## 常见问题

### Docker 权限不足

如果普通用户执行 Docker 报权限错误，可以加入 docker 用户组：

```bash
usermod -aG docker <username>
```

重新登录后生效。

### 镜像拉取失败

检查网络、代理、DNS，必要时配置 Docker 镜像加速或提前离线导入镜像。

### Go 版本不匹配

链码编译失败时，先检查 Go 版本：

```bash
go version
```

Fabric 示例可能对 Go 版本有要求，建议以当前 Fabric Samples 的官方说明为准。

### 测试网络启动失败

排查顺序：

1. `docker ps -a` 查看容器是否异常退出。
2. `docker logs` 查看异常容器日志。
3. 确认端口没有被占用。
4. 执行 `./network.sh down` 清理后重新启动。
