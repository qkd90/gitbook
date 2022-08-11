# k8s创建容器报错CrashLoopBackOff



```
 kubectl delete -f sc.yaml
```

  1、查看指定pod的日志

```
kubectl logs <pod_name>

kubectl logs -f <pod_name> #类似tail -f的方式查看(tail -f 实时查看日志文件 tail -f 日志文件log)
```

2、查看指定pod中指定容器的日志

```
kubectl logs <pod_name> -c <container_name>
```

PS：查看Docker容器日志

```
docker logs <container_id>
```

