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

## 适用场景

- 团队成员的本地环境不一致，需要把应用与依赖打包为可重复运行的镜像。
- 一个服务需要与数据库、缓存、消息队列等多个依赖一起在本地联调。
- 应用从单机部署迁移到集群，需要统一管理副本、配置、入口、资源与发布。
- 发生 Pod 重启、服务不可达、镜像拉取失败或配置未生效时，需要按对象关系排查。

## 知识地图

- **Docker**：通过 [Docker](1-docker/README.md) 学习镜像、容器、网络、数据卷和 Dockerfile，解决“应用如何稳定打包和运行”。
- **Docker Compose**：把多个本地依赖声明为一个可启动的联调环境，适合开发、测试和小规模部署。
- **Kubernetes**：通过 [Kubernetes 云原生实战](2-k8s云原生实战/README.md) 管理 Pod、Deployment、Service、Ingress、ConfigMap、Secret 和 PVC。
- **交付链路**：源码 → 镜像 → 配置与密钥 → 部署声明 → 健康检查与日志 → 发布、回滚和故障排查。

## 学习与实践路径

1. 先为一个简单 Web 服务编写 Dockerfile，完成构建、运行、查看日志、进入容器和端口访问。
2. 将应用与至少一个依赖服务写入 Compose，明确网络、数据卷、环境变量和启动顺序。
3. 把同一应用拆成镜像、配置和运行参数，避免将环境差异固化进镜像。
4. 在 Kubernetes 中依次落地 Deployment、Service、Ingress、ConfigMap/Secret、PVC 和资源限制。
5. 主动演练镜像版本回退、Pod 重启和服务访问异常，按 describe、events、日志、Service、Endpoints、Ingress、DNS 的顺序定位。

## 常见产出

- 可复现的 Dockerfile、.dockerignore、镜像版本约定和构建命令。
- 用于本地联调的 docker-compose 配置、环境变量模板和数据卷说明。
- Kubernetes 的 Deployment、Service、Ingress、ConfigMap、Secret、PVC 等声明文件。
- 应用健康检查、资源 requests/limits、发布记录、回滚步骤和排障手册。

## 维护建议

- 镜像使用可追踪版本标签，重要发布同时记录对应的代码版本；不要把 latest 当作生产版本。
- 密钥只通过受控的配置渠道注入，不写入镜像、Compose 文件、日志或文档示例。
- 容器要保持无状态，业务数据放在受管存储或明确的数据卷中；容器内的临时修改不能作为正式修复。
- 每次新增服务都确认日志输出、探针、资源限制、依赖连接和升级/回滚策略，避免只验证“能启动”。

## AI 与大数据招聘入口

- [AI 与大数据招聘能力地图](AI与大数据招聘能力地图.md)：以 Docker、Compose、Kubernetes 和故障演练为主线，整理 MLOps、数据平台与云原生岗位的能力证明、项目作品和资料缺口。
