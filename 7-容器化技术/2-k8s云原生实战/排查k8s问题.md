# 排查k8s问题

1.看日志

```
systemctl status kubelet.service -l
```

查看详细内容

```
 journalctl -xefu kubelet
```

2.卸载k8s管理组件

```
yum erase -y kubelet kubectl kubeadm kubernetes-cni
```

