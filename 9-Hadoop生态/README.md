# Hadoop 生态

Hadoop 是大数据处理的基石。本章节涵盖 Hadoop 生态系统的核心组件，包括 HDFS 分布式文件系统、MapReduce 计算框架和 YARN 资源管理器。

## 学习路径

```
Hadoop简介 → HDFS核心概念 → MapReduce编程模型 → Hadoop环境搭建
                                      ↓
                          HDFS常用命令 → HDFS Java API
```

## 章节内容

- [Hadoop简介](Hadoop简介.md) - Hadoop 的历史、生态组件与应用场景
- [HDFS核心概念](HDFS核心概念.md) - 分布式文件系统架构、Block、NameNode、DataNode
- [MapReduce编程模型](MapReduce编程模型.md) - Map-Reduce 计算范式、Shuffle 机制
- [Hadoop环境搭建](Hadoop环境搭建.md) - 单机模式、伪分布式、完全分布式部署
- [HDFS常用命令](HDFS常用命令.md) - HDFS Shell 操作指南
- [HDFS Java API](HDFS%20Java%20API.md) - Java 客户端操作 HDFS

## 适用场景

- 需要以分布式文件系统保存大规模离线数据，并让计算任务靠近数据执行。
- 需要理解 Hive、Spark、Flink 等大数据组件背后的存储、资源管理和批处理基础。
- 需要完成文件上传下载、目录权限、批量计算或 Java 客户端访问 HDFS 等基础工作。

## 知识地图

- **HDFS 存储层**：[HDFS核心概念](HDFS核心概念.md) 解释 Block、NameNode、DataNode 与副本机制；[HDFS常用命令](HDFS常用命令.md) 用于实际文件操作。
- **计算层**：[MapReduce编程模型](MapReduce编程模型.md) 说明 Map、Shuffle、Reduce 的批处理范式，是理解离线计算成本的基础。
- **资源层**：Hadoop 的 YARN 负责集群资源调度，需要和存储、计算的角色一起理解。
- **开发与环境**：[Hadoop环境搭建](Hadoop环境搭建.md) 用于验证单机、伪分布式或集群环境；[HDFS Java API](HDFS%20Java%20API.md) 用于把文件操作接入 Java 程序。

## 学习与实践路径

1. 先阅读 [Hadoop简介](Hadoop简介.md)，明确 HDFS、MapReduce、YARN 各自解决的问题和边界。
2. 按 [Hadoop环境搭建](Hadoop环境搭建.md) 在可控环境完成一次部署，记录 JDK、Hadoop、主机名、网络和配置之间的对应关系。
3. 用 HDFS Shell 完成目录创建、上传、下载、查看、副本或权限等操作，再用 Java API 实现相同的基础读写流程。
4. 编写并运行一个小型 MapReduce 任务，重点观察输入切分、Shuffle、输出目录和失败重试，而不只关注最终结果。
5. 将样例数据、运行命令、日志位置和结果校验方式整理为可重复执行的实验记录，为后续 Hive、Spark 学习提供数据底座。

## 常见产出

- Hadoop 环境与版本清单、节点角色说明、配置变更记录。
- HDFS 目录规划、数据落盘规范、权限约定和常用运维命令。
- Java HDFS 客户端样例、输入输出约定及错误处理说明。
- MapReduce 作业代码、提交命令、结果校验和运行日志定位方式。

## 维护建议

- 环境升级或扩容时同步记录 JDK、Hadoop、配置文件和节点清单，避免只修改单个节点造成版本或配置漂移。
- HDFS 目录、权限、配额和数据保留周期要有明确责任人；生产操作先确认目标路径，避免误删或覆盖数据。
- 持续关注 NameNode、DataNode、磁盘、副本健康度和任务失败情况；元数据与关键配置需要具备可恢复方案。
- 样例和说明应区分开发、测试、生产环境，不在文档中写入真实账号、连接串或业务数据。

## AI 与大数据招聘入口

- [AI 与大数据招聘能力地图](AI与大数据招聘能力地图.md)：以 HDFS、YARN、MapReduce、数据集版本和可重跑任务为主线，面向大数据开发、数据平台和 AI 数据工程岗位梳理作品与面试要点。
