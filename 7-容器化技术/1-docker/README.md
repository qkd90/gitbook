# Docker

## 章节定位

Docker 用于把应用、依赖和运行环境打包成镜像，再以容器方式运行。它是本地环境统一、应用交付和 Kubernetes 部署的基础。

## 学习路径

```text
镜像
  ↓
容器
  ↓
端口映射
  ↓
数据卷
  ↓
网络
  ↓
Dockerfile
  ↓
Docker Compose
```

## 常用命令

```bash
docker images
docker ps -a
docker logs -f <container>
docker exec -it <container> sh
docker stop <container>
docker rm <container>
docker rmi <image>
```

## 实战建议

- 容器内应用日志优先输出到标准输出。
- 数据库、中间件等有状态服务要挂载数据卷。
- 镜像标签不要只用 `latest`，生产环境要固定版本。
- Dockerfile 尽量减少层数和无用文件。
- Compose 适合本地或小规模环境，生产编排优先 Kubernetes。
