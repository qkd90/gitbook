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

## 适用场景

- 需要持续消费事件流，在秒级或更低延迟下完成清洗、聚合、告警或实时指标计算。
- 需要处理乱序事件、按业务时间开窗、维护用户或设备等维度状态，并在故障后恢复处理进度。
- 需要构建实时数仓、实时看板或在线数据服务，并与 Kafka、数据库、缓存、分析存储等系统对接。

## 知识地图

- **运行与时间语义**：[Flink核心概念](Flink核心概念.md) 说明流批一体、处理时间与事件时间等基础语义。
- **数据处理主链路**：[Flink DataStream API](Flink%20DataStream%20API.md) 覆盖 Source、转换算子和 Sink，是作业从输入到输出的骨架。
- **窗口与乱序数据**：[Flink窗口机制](Flink窗口机制.md) 用于选择滚动、滑动或会话窗口，并明确窗口结束与迟到数据的处理方式。
- **可靠性**：[Flink状态管理与检查点](Flink状态管理与检查点.md) 连接状态、Checkpoint 和 Savepoint，决定故障恢复与发布升级的安全边界。
- **运行环境**：[Flink环境搭建](Flink环境搭建.md) 与 [Flink集群部署](Flink集群部署.md) 负责从本地验证走向 Standalone、YARN 或 Kubernetes 运行。

## 学习与实践路径

1. 在本地用一个可控数据源跑通 Source、转换和 Sink，先确认输入 schema、输出格式与异常日志位置。
2. 为包含时间字段的事件定义事件时间、乱序容忍和窗口类型，使用少量样例验证跨窗口、迟到和空窗口行为。
3. 引入 Keyed State 或 Operator State，明确状态键、过期策略和状态增长风险。
4. 开启并验证 Checkpoint；发布前生成 Savepoint，模拟停止、恢复和版本升级，检查结果是否重复或遗漏。
5. 部署到目标集群后，持续观察吞吐、延迟、反压、Checkpoint 成功率、状态大小和源端积压，再调整并行度与资源。

## 常见产出

- DataStream 作业代码、事件 schema、时间字段说明和输入输出契约。
- 窗口、Watermark、状态键、TTL、Checkpoint 与 Savepoint 的配置说明。
- 作业部署文件、资源规划、版本升级/回滚和故障恢复步骤。
- 实时指标口径、源端积压与数据质量监控项，以及与离线结果的核对记录。

## 维护建议

- 先固定事件字段、时间语义和主键/分区键，再调整窗口和并行度；这些基础契约变化会影响状态与历史结果。
- 状态结构、状态名称、Checkpoint 和 Savepoint 要纳入发布评审，避免升级后无法恢复或产生重复数据。
- 实时作业不能只监控“是否运行”，还要监控反压、延迟、Checkpoint 失败、状态膨胀、消费积压和 Sink 写入错误。
- 重跑、补数与离线校正要明确边界和幂等策略，不能直接用线上实时作业覆盖历史数据。

## 招聘准备入口

- [AI 与大数据招聘能力地图](AI与大数据招聘能力地图.md)：将 DataStream、窗口、状态、Checkpoint/Savepoint 和集群部署资料组织成实时计算、数据平台与 AI 实时特征流水线岗位的实战和面试准备路径。
