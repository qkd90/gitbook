# Kubernetes 云原生实战

## 章节定位

本目录整理 Kubernetes 基础概念、核心对象、网络、KubeSphere 安装和常见问题排查。目标是掌握应用在集群中的声明式部署和运维方式。

## 核心对象

| 对象 | 作用 |
| --- | --- |
| Pod | 最小调度单元 |
| Deployment | 管理无状态应用副本 |
| Service | 提供稳定访问入口 |
| Ingress | 提供 HTTP/HTTPS 入口 |
| ConfigMap | 管理非敏感配置 |
| Secret | 管理敏感配置 |
| PVC | 管理持久化存储 |

## 推荐学习顺序

1. Kubernetes 基础概念。
2. k8s 基础操作。
3. Kubernetes 核心实战。
4. Kubernetes 测试网络。
5. KubeSphere 安装。
6. CrashLoopBackOff 和常见问题排查。

## 排查原则

先看 `kubectl describe` 和 events，再看容器日志。服务访问异常时，要同时检查 Pod、Service、Endpoints、Ingress 和 DNS。
