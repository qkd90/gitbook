# Jar 包部署服务方案

## 适用场景

Jar 包部署适合 Spring Boot、普通 Java 服务、内部工具服务等后端应用。核心目标是让服务具备可启动、可停止、可自恢复、可查看日志、可回滚的能力。

## 目录规范

建议每个服务独立目录：

```text
/data/apps/demo-service
  ├─ app/demo-service.jar
  ├─ config/application-prod.yml
  ├─ logs/
  ├─ backup/
  └─ bin/
```

目录说明：

- `app`：当前运行的 Jar 包。
- `config`：外置配置文件。
- `logs`：运行日志。
- `backup`：历史版本备份，用于快速回滚。
- `bin`：启动、停止、重启脚本。

## 手工启动

```bash
cd /data/apps/demo-service

nohup java \
  -Xms512m \
  -Xmx512m \
  -Dspring.profiles.active=prod \
  -Dspring.config.additional-location=./config/ \
  -jar app/demo-service.jar \
  > logs/start.log 2>&1 &
```

查看进程：

```bash
ps -ef | grep demo-service.jar | grep -v grep
```

查看日志：

```bash
tail -f logs/start.log
```

## systemd 托管

生产环境建议使用 systemd 管理服务。

创建 `/etc/systemd/system/demo-service.service`：

```ini
[Unit]
Description=demo-service
After=network.target

[Service]
Type=simple
WorkingDirectory=/data/apps/demo-service
ExecStart=/usr/bin/java -Xms512m -Xmx512m -Dspring.profiles.active=prod -Dspring.config.additional-location=/data/apps/demo-service/config/ -jar /data/apps/demo-service/app/demo-service.jar
Restart=on-failure
RestartSec=10
SuccessExitStatus=143
StandardOutput=append:/data/apps/demo-service/logs/stdout.log
StandardError=append:/data/apps/demo-service/logs/stderr.log

[Install]
WantedBy=multi-user.target
```

加载配置并启动：

```bash
systemctl daemon-reload
systemctl enable demo-service
systemctl start demo-service
```

常用命令：

```bash
systemctl status demo-service -l
systemctl restart demo-service
systemctl stop demo-service
journalctl -u demo-service -f
```

## 发布流程

```bash
cd /data/apps/demo-service

# 1. 备份当前版本
cp app/demo-service.jar backup/demo-service-$(date +%Y%m%d%H%M%S).jar

# 2. 上传新 Jar 包到临时目录后替换
cp /tmp/demo-service.jar app/demo-service.jar

# 3. 重启服务
systemctl restart demo-service

# 4. 检查状态
systemctl status demo-service -l
tail -n 200 logs/stdout.log
```

## 回滚流程

```bash
cd /data/apps/demo-service

systemctl stop demo-service
cp backup/demo-service-20260101120000.jar app/demo-service.jar
systemctl start demo-service
systemctl status demo-service -l
```

## 健康检查

如果服务提供健康检查接口，可在发布后验证：

```bash
curl -i http://127.0.0.1:8080/actuator/health
```

如果没有健康检查接口，至少检查：

- 进程是否存在。
- 端口是否监听。
- 日志是否出现启动成功关键字。
- 核心接口是否可以正常访问。

```bash
ss -lntp | grep 8080
tail -n 200 logs/stdout.log
```

## 常见问题

### 端口被占用

```bash
ss -lntp | grep 8080
```

确认进程后，优先判断是否为旧服务未退出，不要直接 kill 业务进程。

### 配置文件未生效

重点检查：

- `spring.profiles.active` 是否正确。
- 外置配置路径是否写成绝对路径。
- Jar 包内部配置是否覆盖了外部配置。
- 启动日志中实际加载的 profile 是否符合预期。

### 内存不足

查看系统内存：

```bash
free -h
```

查看 OOM 记录：

```bash
dmesg -T | grep -i "killed process"
```

处理方式：

- 调整 `-Xms`、`-Xmx`。
- 检查批量任务、缓存、线程池配置。
- 结合 GC 日志进一步分析。
