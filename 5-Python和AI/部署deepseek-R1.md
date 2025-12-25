## 1.简介

GitHub地址：

```
https://github.com/deepseek-ai/DeepSeek-R1
```

## 2.ollama部署

官网一键部署：

```
https://ollama.com/
```

但是由于我们服务器访问GitHub有问题 所有手动部署步骤如下：

### 2.1 下载二进制文件 ollama

将 Ollama 的二进制文件下载到 PATH 中的目录：

```
sudo curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama
sudo chmod +x /usr/bin/ollama
```

### 2.2 将 Ollama 添加为自启动服务（推荐）

首先，为 Ollama 创建用户：

```
sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama
```

然后在该位置：/etc/systemd/system/ollama.service 创建服务文件

```shell
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

最后启动服务：

```
sudo systemctl daemon-reload
sudo systemctl enable ollama
```

### 2.3 启动 Ollama

使用以下命令启动 Ollama：systemd

```
sudo systemctl start ollama
```

### 三、更新

再次运行之前的安装语句来更新 Ollama：

```
curl -fsSL https://ollama.com/install.sh | sh
```



或者下载 Ollama 二进制文件：

```
sudo curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama
sudo chmod +x /usr/bin/ollama
```

### 四、安装特定版本

设置 `OLLAMA_VERSION`字段，，可以安装对应的版本

```
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.1.32 sh
```



### 五、查看日志



查看作为启动服务运行的 Ollama 的日志：

```
journalctl -e -u ollama
```



### 六、卸载



- 删除 Ollama 服务：

```
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
```



- 从 bin 目录中删除 Ollama 二进制文件： `/usr/local/bin `,`/usr/bin` ,`/bin`

```
sudo rm $(which ollama)
```



- 删除下载的模型和 Ollama 服务用户和组：

```
sudo rm -r /usr/share/ollama
sudo userdel ollama
sudo groupdel ollama
```