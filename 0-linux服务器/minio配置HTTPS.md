

## 1. **下载并安装 Minio**

下载 Minio 二进制文件：

```
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O /home/ubuntu/minio
```

（根据你的系统架构选择合适的版本，上面是 64 位 Linux 示例）

进入minio目录，Ubuntu复制到环境变量

```
sudo cp minio /usr/local/bin/
```

赋予执行权限：

```
chmod +x /usr/local/bin/minio
```

查看版本

```
minio --version
```

## 2. **创建数据存储目录**

Minio 需要一个目录来存储数据，例如：



```
mkdir -p /home/ubuntu/minio/data
```

## 3. **配置 HTTPS 证书**

Minio 默认从 ~/.minio/certs/ 读取证书文件（~ 是运行 Minio 的用户主目录）。你需要将证书放入正确位置。

创建证书目录：

```
mkdir -p ~/.minio/certs
```

复制证书文件：

将 private.key和 public.crt放入 ~/.minio/certs/：

```
cp /path/to/your/private.key ~/.minio/certs/private.key 
cp /path/to/your/public.crt ~/.minio/certs/public.crt
```



确保文件权限正确：

```
chmod 600 ~/.minio/certs/private.key 
chmod 644 ~/.minio/certs/public.crt
```



## 4. **运行 Minio 并启用 HTTPS**

直接运行 Minio，指定数据目录和域名：

```
MINIO_DOMAIN=minio.example.com MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 minio server /home/ubuntu/minio/data --address "172.0.0.1:9000" --console-address ":9002"
```

- MINIO_DOMAIN：设置 Minio 的域名，客户端将通过此域名访问。
- /home/ubuntu/minio/data：数据存储路径。
- --address "172.0.0.1:9000"：监听本地服务器网卡地址的 9000 端口（默认端口，可改为其他端口，例如 :443）。
-  --console-address ":9002"：web管理页面9002端口

运行后，Minio 会自动检测 ~/.minio/certs/ 中的证书并启用 HTTPS。

## 5. **后台运行（可选）**

为了让 Minio 在后台持续运行，可以使用 nohup 或将其配置为系统服务。

### 使用 nohup：



```
nohup MINIO_DOMAIN=minio.example.com minio server /minio/data --address :9000 &
```

### 配置为系统服务（推荐）

创建服务文件：

```
sudo nano /etc/systemd/system/minio.service
```



输入以下内容（根据实际情况调整路径和用户）：

```
[Unit]
Description=Minio Service
After=network.target

[Service]
Type=simple
User=minio-user
Group=minio-group
Environment="MINIO_DOMAIN=minio.example.com"
ExecStart=/usr/local/bin/minio server /minio/data --address :9000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```



创建 Minio 用户和组：

```
sudo groupadd -r minio-group
sudo useradd -r -g minio-group minio-user
sudo chown minio-user:minio-group /minio/data
```

启用并启动服务：

```shell
sudo systemctl daemon-reload
sudo systemctl enable minio.service
sudo systemctl start minio.service
#检查服务状态
sudo systemctl status minio.service+
#检查最新日志
journalctl -u minio.service -r
```



TTPS 访问**

在浏览器或通过 curl 测试：

text

收起自动换行复制

```
https://minio.example.com:9000
```

或者：

bash

收起自动换行复制

```
curl https://minio.example.com:9000
```

- 如果配置正确，你将看到 Minio 的登录界面或 API 响应。

- 你的 

  imageUrl

   将变为：

  text

  收起自动换行复制

  `"https://minio.example.com/system-tongue/2025/04/03/deb422a0baa64eaa853e2b4884db2249.png"`

## 7. **（可选）配置防火墙**

如果服务器有防火墙，确保开放 9000 端口（或你自定义的端口）：

```
ubuntu
`sudo ufw allow 9000`
centos
`sudo firewall-cmd --add-port=9000/tcp --permanent sudo firewall-cmd --reload`
```

## 8. **（可选）使用默认 HTTPS 端口 443**

如果想用标准的 HTTPS 端口（443），修改启动命令或服务配置中的 --address：

bash

收起自动换行复制

```
MINIO_DOMAIN=minio.example.com minio server /minio/data --address :443
```

然后确保 443 端口未被其他服务占用，并更新防火墙规则。

### 1. **准备证书文件**

确保你已经拥有 HTTPS 证书，通常包括：

- 私钥文件（例如 private.key）
- 证书文件（例如 public.crt）

这些文件可以通过自签名证书生成（用于测试），或者从证书颁发机构（如 Let's Encrypt）获取。

#### 自签名证书（可选，测试用）：

如果你还没有证书，可以用以下命令生成自签名证书：

bash

收起自动换行复制

```
openssl req -x509 -newkey rsa:4096 -keyout private.key -out public.crt -days 365 -nodes
```

生成后，将 private.key 和 public.crt 保存到某个目录，例如 /minio/certs/。



# docker启动



```
docker run -d \
  --name minio2 \
  -p 9000:9000 \
  -p 9002:9002 \
  -v /home/ubuntu/minio/data:/data \
  -v /home/ubuntu/.minio/certs:/root/.minio/certs \
  -e "MINIO_DOMAIN=mentalcare.trasen.cn" \
  -e "MINIO_ROOT_USER=minio" \
  -e "MINIO_ROOT_PASSWORD=minio@123" \
  minio/minio server /data  --console-address ":9002"
```

