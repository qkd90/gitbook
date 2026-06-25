# Linux 服务器

## 章节定位

本目录整理 Linux 服务器日常操作、服务部署、系统查看、磁盘、网络、防火墙、时间同步和常见故障处理。

## 基础能力

```text
文件和目录
  ├─ ls、cd、cp、mv、rm、find、du

进程和服务
  ├─ ps、top、systemctl、journalctl

网络和端口
  ├─ ip、ss、curl、ping、firewall-cmd

磁盘和权限
  ├─ df、lsblk、mount、chmod、chown

日志和排查
  ├─ tail、grep、less、dmesg
```

## 推荐排查顺序

1. 看服务状态。
2. 看进程和端口。
3. 看应用日志和系统日志。
4. 看磁盘、内存、CPU。
5. 看网络连通性。
6. 看配置变更和最近发布。

## 生产建议

- 服务统一由 systemd、Docker 或 Kubernetes 托管。
- 日志、数据、安装包分目录管理。
- 重要服务配置开机自启。
- 定期检查磁盘空间、时间同步和安全更新。
