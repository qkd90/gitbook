# 排查 K8s 问题

## 排查顺序

Kubernetes 问题不要只看 Pod 日志，建议按资源链路逐层检查：

```text
Node
  ↓
Namespace
  ↓
Pod
  ↓
Container
  ↓
Service
  ↓
Ingress
  ↓
ConfigMap / Secret / PVC
```

## 查看集群状态

```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get ns
kubectl get events -A --sort-by=.lastTimestamp
```

查看节点详情：

```bash
kubectl describe node <node-name>
```

重点关注：

- `Ready` 状态。
- CPU、内存、磁盘压力。
- kubelet 是否正常。
- 节点 taint 是否影响调度。

## 查看 Pod

```bash
kubectl get pod -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

多容器 Pod 查看指定容器日志：

```bash
kubectl logs <pod-name> -c <container-name> -n <namespace>
```

查看上一次崩溃日志：

```bash
kubectl logs <pod-name> -n <namespace> --previous
```

## 常见状态

| 状态 | 常见原因 |
| --- | --- |
| `Pending` | 资源不足、节点选择器不匹配、PVC 未绑定 |
| `ImagePullBackOff` | 镜像地址错误、仓库无权限、网络不通 |
| `CrashLoopBackOff` | 容器启动后反复退出、配置错误、依赖不可用 |
| `CreateContainerConfigError` | ConfigMap、Secret、环境变量配置错误 |
| `Evicted` | 节点资源不足，Pod 被驱逐 |
| `Running` 但不可访问 | Service、端口、探针、网络策略或 Ingress 配置错误 |

## kubelet 排查

查看 kubelet 状态：

```bash
systemctl status kubelet.service -l
```

查看详细日志：

```bash
journalctl -xefu kubelet
```

常见问题：

- 证书过期。
- CNI 网络插件异常。
- 容器运行时异常。
- 节点磁盘或内存压力。

## Service 排查

```bash
kubectl get svc -n <namespace>
kubectl describe svc <service-name> -n <namespace>
kubectl get endpoints <service-name> -n <namespace>
```

如果 Service 没有 endpoints，通常说明 selector 没有匹配到 Pod。

检查 selector：

```bash
kubectl get pod -n <namespace> --show-labels
kubectl get svc <service-name> -n <namespace> -o yaml
```

## Ingress 排查

```bash
kubectl get ingress -n <namespace>
kubectl describe ingress <ingress-name> -n <namespace>
kubectl logs -n ingress-nginx deploy/ingress-nginx-controller
```

重点检查：

- 域名是否解析到 Ingress 地址。
- path 是否匹配。
- backend service 和 port 是否正确。
- TLS secret 是否存在。

## 进入容器排查

```bash
kubectl exec -it <pod-name> -n <namespace> -- sh
```

容器内常用命令：

```bash
env
cat /etc/resolv.conf
nslookup kubernetes.default
curl -v http://service-name:port
```

如果镜像很精简，没有工具，可以启动临时调试容器：

```bash
kubectl run debug --rm -it --image=busybox:1.36 -- sh
```

## 卸载管理组件

仅在重装或清理实验环境时使用：

```bash
yum erase -y kubelet kubectl kubeadm kubernetes-cni
```

生产环境不要直接卸载，应先确认节点是否可以下线，并完成 Pod 驱逐和业务迁移。
