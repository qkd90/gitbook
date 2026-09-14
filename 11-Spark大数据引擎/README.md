# Spark 大数据引擎

Apache Spark 是统一的快速大数据分析引擎，支持批处理、流处理、机器学习和图计算。本章节涵盖 Spark 核心概念、RDD 编程、SparkSQL 和 Spark Streaming。

## 学习路径

```
Spark简介 → Spark RDD → Spark算子详解 → SparkSQL简介 → Spark Streaming
```

## 章节内容

- [Spark简介](Spark简介.md) - Spark 特点、架构、与 Hadoop 对比
- [Spark RDD](Spark%20RDD.md) - 弹性分布式数据集核心概念
- [Spark算子详解](Spark算子详解.md) - Transformation 和 Action 算子详解
- [SparkSQL简介](SparkSQL简介.md) - DataFrame、Dataset、SQL 查询
- [Spark Streaming](Spark%20Streaming.md) - 微批处理流计算

## 适用场景

- 需要在统一计算引擎上完成离线 ETL、SQL 分析、批量聚合或流式处理。
- 需要理解从 RDD 编程模型到 DataFrame、Dataset、SQL 的抽象演进，并选择合适的开发入口。
- 需要把 Hadoop/Hive 中的数据转换为可供指标、报表或下游服务消费的结果数据。

## 知识地图

- **基础与运行模型**：[Spark简介](Spark简介.md) 建立对 Spark 架构、应用提交与 Hadoop 关系的整体认识。
- **核心计算抽象**：[Spark RDD](Spark%20RDD.md) 解释不可变数据集、分区和计算血缘；[Spark算子详解](Spark算子详解.md) 区分 Transformation 与 Action。
- **SQL 分析入口**：[SparkSQL简介](SparkSQL简介.md) 面向 DataFrame、Dataset 和 SQL，适合结构化数据处理。
- **流式扩展**：[Spark Streaming](Spark%20Streaming.md) 介绍微批处理模型，应结合输入、输出和故障恢复语义理解。

## 学习与实践路径

1. 从 Spark 的 Driver、Executor、任务和分区关系入手，先理解一段程序在集群中如何被拆分和执行。
2. 用 RDD 完成一次读取、转换、聚合和输出，观察惰性执行、宽窄依赖和触发 Action 的时机。
3. 将同一份数据改用 DataFrame 或 SQL 完成，比较代码表达、字段约束和执行计划信息。
4. 选择一个批处理或微批流处理案例，明确输入数据格式、分区键、输出位置、重复执行和结果校验方式。
5. 在数据量逐步增加时观察 Shuffle、数据倾斜、缓存、并行度和输出文件数量，再进行有证据的调优。

## 常见产出

- Spark 作业入口、依赖说明、提交命令与运行参数清单。
- RDD 或 DataFrame/SQL 的数据转换逻辑、输入输出 schema 和结果校验 SQL。
- 分区、缓存、Shuffle、并行度等调优记录，以及对应的运行证据。
- 批处理或 Streaming 作业的失败重跑、输出幂等和数据核对方案。

## 维护建议

- 先稳定输入数据 schema、时间口径和输出契约，再优化算子与资源参数；数据契约变化往往比代码改动风险更大。
- 作业上线后关注执行时长、失败率、Shuffle、倾斜、资源使用和输出数据量，避免仅凭一次成功运行判断稳定。
- 输出目录、临时目录和检查点等运行产物应与代码、环境分开管理，并明确保留和清理规则。
- 任何性能优化都应留下基线、改动、结果和回退方案，防止下一次升级无法判断收益或风险。

## AI 与大数据招聘入口

- [AI 与大数据招聘能力地图](AI与大数据招聘能力地图.md)：以执行模型、分区与 Shuffle、可靠重跑、数据质量和 AI 数据集构建为核心，组织大数据开发与数据工程岗位的项目作品和面试准备。
