# Flink 核心概念

## Flink 是什么

Apache Flink 是一个分布式流处理引擎，支持高吞吐、低延迟、有且仅有一次（exactly-once）的流处理语义。

**核心特点**：
- **流批一体**：批处理是流处理的特例
- **低延迟**：毫秒级延迟
- **高吞吐**：每秒数百万事件
- **容错**：Checkpoint 机制保证状态一致性
- **状态管理**：内置丰富的状态后端

## Flink 的架构

```
┌─────────────────────────────────────────────┐
│              Flink APIs                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │DataStream│ │ DataSet  │ │   Table   │  │
│  │  / SQL   │ │  (Batch) │ │  & SQL   │  │
│  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────┤
│             Flink Core                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Runtime   │ │  State   │ │   Time    │  │
│  │ (Stream)  │ │ Backend  │ │           │  │
│  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────┤
│           Deployment                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Standalone│ │   YARN   │ │  K8s     │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

## 核心组件

### 1. JobManager（Master）

- 协调分布式执行
- 调度 Task
- 协调 Checkpoint
- 协调故障恢复

### 2. TaskManager（Worker）

- 执行具体任务
- 缓冲数据流
- 与其他 TaskManager 交换数据

### 3. 任务执行流程

```
Source → Transformation → Sink
```

## 编程模型

```java
// 创建执行环境
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// 定义数据源
DataStream<String> stream = env.socketTextStream("localhost", 9999);

// 转换操作
DataStream<Tuple2<String, Integer>> counts = stream
    .flatMap((String line, Collector<Tuple2<String, Integer>> out) -> {
        for (String word : line.split(" ")) {
            out.collect(new Tuple2<>(word, 1));
        }
    })
    .returns(Types.TUPLE(Types.STRING, Types.INT))
    .keyBy(0)
    .sum(1);

// 定义数据接收
counts.print();

// 执行
env.execute("WordCount");
```

## 总结

Flink 是新一代流处理引擎，通过流批一体架构和强大的状态管理，提供了低延迟、高吞吐的流处理能力。
