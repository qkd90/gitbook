# 容器化技术

## 章节定位

容器化技术章节覆盖 Docker、Docker Compose、Kubernetes 和 KubeSphere，目标是掌握应用镜像构建、容器运行、服务编排、集群部署和云原生故障排查。

## 学习路径

```text
Docker 基础
  ↓
镜像、容器、网络、数据卷
  ↓
Docker Compose 本地编排
  ↓
Kubernetes 基础对象
  ↓
Deployment、Service、Ingress、ConfigMap、Secret、PVC
  ↓
KubeSphere 和集群运维
```

## 章节内容

- Docker 入门、常用命令、远程连接、部署 Nginx、部署 Python 项目。
- Docker Compose 编排和 docker-maven-plugin。
- Kubernetes 基础概念、核心实战、网络测试、KubeSphere 安装。
- CrashLoopBackOff、Pod 异常、Service 和 Ingress 排查。

## 实战建议

- 本地先用 Docker 和 Compose 跑通服务。
- 再把应用拆成镜像、配置、环境变量、数据卷。
- 上 Kubernetes 前先明确端口、健康检查、资源限制和日志输出。
- 生产集群中不要直接修改容器内部文件，应通过镜像和配置声明式管理。
