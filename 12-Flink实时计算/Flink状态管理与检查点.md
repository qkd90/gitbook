# Flink 状态管理与检查点

## 状态管理

Flink 是有状态的流处理引擎，状态是跨多个事件的数据。

## 状态类型

### 1. ValueState

存储单个值。

```java
ValueStateDescriptor<Integer> descriptor = new ValueStateDescriptor<>(
    "myState", Types.INT, 0);
ValueState<Integer> state = getRuntimeContext().getState(descriptor);

state.update(42);
int value = state.value();
```

### 2. ListState

存储列表。

```java
ListStateDescriptor<String> descriptor = new ListStateDescriptor<>(
    "listState", Types.STRING);
ListState<String> state = getRuntimeContext().getListState(descriptor);

state.add("item1");
for (String item : state.get()) {
    // 处理
}
```

### 3. MapState

存储键值对。

```java
MapStateDescriptor<String, Integer> descriptor = new MapStateDescriptor<>(
    "mapState", Types.STRING, Types.INT);
MapState<String, Integer> state = getRuntimeContext().getMapState(descriptor);

state.put("key", 42);
int value = state.get("key");
```

### 4. ReducingState

聚合状态。

```java
ReducingStateDescriptor<Integer> descriptor = new ReducingStateDescriptor<>(
    "reducingState", (a, b) -> a + b, Types.INT);
ReducingState<Integer> state = getRuntimeContext().getReducingState(descriptor);

state.add(10);
state.add(20);
// state.get() = 30
```

## 状态后端

### 1. MemoryStateBackend

状态存储在 JVM 内存中。

```java
env.setStateBackend(new MemoryStateBackend());
```

### 2. FsStateBackend

状态存储在文件系统中。

```java
env.setStateBackend(new FsStateBackend("hdfs://path/to/checkpoints"));
```

### 3. RocksDBStateBackend

状态存储在 RocksDB 中，适合大状态。

```java
env.setStateBackend(new RocksDBStateBackend("hdfs://path/to/checkpoints"));
```

## Checkpoint

Checkpoint 是定期的状态快照，用于故障恢复。

### 启用 Checkpoint

```java
env.enableCheckpointing(60000);  // 每 60 秒
```

### 配置

```java
CheckpointConfig config = env.getCheckpointConfig();

// 精确一次语义
config.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

// 最小间隔
config.setMinPauseBetweenCheckpoints(30000);

// 超时时间
config.setCheckpointTimeout(60000);

// 最大并发
config.setMaxConcurrentCheckpoints(1);

// 外部化检查点
config.enableExternalizedCheckpoints(
    ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);
```

## Savepoint

Savepoint 是手动创建的 Checkpoint，用于升级和维护。

### 创建 Savepoint

```bash
flink savepoint <jobId> [targetDirectory]
```

### 从 Savepoint 恢复

```bash
flink run -s <savepointPath> <jarFile>
```

## 总结

状态管理和 Checkpoint 是 Flink 容错的核心机制，正确配置可以保证数据的一致性和系统的可靠性。
