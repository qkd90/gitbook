# Flink 实时计算

Apache Flink 是新一代分布式流处理引擎，支持高吞吐、低延迟、有且仅有一次的流处理语义。本章节涵盖 Flink 核心概念、DataStream API、窗口机制、状态管理与集群部署。

## 学习路径

```
Flink核心概念 → Flink环境搭建 → Flink DataStream API → Flink窗口机制
                                              ↓
                              Flink状态管理与检查点 → Flink集群部署
```

## 章节内容

- [Flink核心概念](Flink核心概念.md) - Flink 特点、架构、流批一体理念
- [Flink环境搭建](Flink环境搭建.md) - 本地开发与测试环境配置
- [Flink DataStream API](Flink%20DataStream%20API.md) - 数据源、转换、Sink 操作
- [Flink窗口机制](Flink窗口机制.md) - Tumbling、Sliding、Session 窗口
- [Flink状态管理与检查点](Flink状态管理与检查点.md) - State Backend、Checkpoint、Savepoint
- [Flink集群部署](Flink集群部署.md) - Standalone、YARN、K8s 部署模式
