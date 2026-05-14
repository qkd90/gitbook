# Flink 集群部署

## Standalone 模式

### 1. 配置 flink-conf.yaml

```yaml
jobmanager.rpc.address: hadoop102
jobmanager.rpc.port: 6123
jobmanager.memory.process.size: 1600m
taskmanager.memory.process.size: 1728m
taskmanager.numberOfTaskSlots: 2
```

### 2. 配置 workers

```
hadoop102
hadoop103
hadoop104
```

### 3. 启动

```bash
./bin/start-cluster.sh
```

## YARN 模式

### 1. Session 模式

```bash
# 启动 Session
yarn-session.sh -jm 1024m -tm 2048m

# 提交任务
flink run -m yarn-session -c com.example.WordCount ./wordcount.jar
```

### 2. Per-Job 模式

```bash
flink run -m yarn-cluster -c com.example.WordCount ./wordcount.jar
```

### 3. Application 模式

```bash
flink run-application -t yarn-application ./wordcount.jar
```

## Kubernetes 模式

### 1. Session 模式

```bash
kubectl create -f jobmanager-service.yaml
kubectl create -f jobmanager-deployment.yaml
kubectl create -f taskmanager-deployment.yaml
```

### 2. Application 模式

```bash
flink run-application -t kubernetes-application \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    ./wordcount.jar
```

## 总结

Flink 支持多种部署模式，可根据基础设施选择合适的方案。
