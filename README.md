# 一条大数据之路

## 项目定位

这是一个面向后端开发、大数据工程、运维部署和工程实践的 GitBook 知识库。目标不是简单堆放零散笔记，而是把日常开发、问题排查、架构设计、数据处理和技术选型整理成一套可以持续补充的技术体系。

整体内容以 Java 后端和大数据方向为主线，覆盖从编程基础、开发框架、数据库中间件、微服务、服务器运维、容器化、分布式理论，到 Hadoop、Hive、Spark、Flink、ZooKeeper 等大数据核心组件。同时保留 Python 和 AI、区块链、信创数据库、安卓设备等个人实践专题。

## 技术体系总览

```text
编程基础
  ├─ Java 基础、集合、并发、IO、JVM
  ├─ 算法题解、剑指 Offer、LeetCode 热题
  └─ 代码规范、接口设计、异常处理

工程开发
  ├─ Spring Boot、Spring Cloud、Sa-Token、MyBatis-Plus
  ├─ Maven、Git、IDEA、GitBook、日志框架
  └─ 项目结构、统一返回、统一异常、权限和租户

数据与中间件
  ├─ MySQL、Oracle、PostgreSQL、MongoDB
  ├─ Kafka、Elasticsearch、Nginx、Doris
  └─ SQL 训练、数据库设计、监控指标、数据导入导出

微服务与分布式
  ├─ Nacos、Spring Cloud、配置中心、服务治理
  ├─ CAP、Paxos、Raft、分布式锁、分布式事务
  └─ 分布式 ID、幂等、限流、熔断和降级

大数据平台
  ├─ Hadoop、HDFS、MapReduce
  ├─ Hive、数仓建模、离线 SQL
  ├─ Spark、RDD、SparkSQL、Spark Streaming
  └─ Flink、窗口、状态、Checkpoint、实时计算

运维和交付
  ├─ Linux、systemd、Shell、网络、防火墙
  ├─ Prometheus、Alertmanager、Grafana、EFK
  ├─ Docker、Docker Compose、Kubernetes、KubeSphere
  └─ Jar 包部署、服务巡检、故障排查、测试工具

扩展专题
  ├─ Python、FastAPI、AI 模型部署
  ├─ Hyperledger Fabric、FISCO BCOS
  ├─ 达梦、OceanBase、openGauss
  └─ 安卓设备、ADB、手机 root
```

## 推荐学习路径

### 1. 后端开发路线

1. Java 基础、集合、异常、泛型、Stream、并发基础。
2. Maven、Git、IDEA、编码规范和常用调试方式。
3. Spring Boot、统一异常、统一返回、参数校验、拦截器。
4. MyBatis-Plus、MongoTemplate、Redis、Kafka、Nginx。
5. 项目结构设计、权限认证、数据权限、租户系统。
6. 微服务治理、配置中心、注册中心、接口调用和链路排查。

### 2. 大数据工程路线

1. 分布式系统基本概念、CAP、Raft、分布式锁和事务。
2. Hadoop、HDFS、MapReduce，理解离线计算基础。
3. Hive DDL、DML、分区表、分桶表、查询优化。
4. Spark RDD、SparkSQL、Spark Streaming，掌握批流一体思路。
5. Flink DataStream、窗口、状态、Checkpoint，掌握实时计算。
6. ZooKeeper、Kafka、调度、监控和数据质量。

### 3. 运维交付路线

1. Linux 基础命令、文件权限、磁盘、网络、防火墙、时间同步。
2. Jar 包部署、systemd 托管、日志目录、启动参数和健康检查。
3. Docker 镜像、容器、网络、数据卷、Compose 编排。
4. Kubernetes Pod、Deployment、Service、Ingress、ConfigMap、Secret。
5. Prometheus、Alertmanager、Grafana、EFK 日志平台。
6. 常见故障定位：启动失败、端口占用、资源不足、网络不通、证书异常。

## 文档组织规范

每个主题文档建议保持以下结构，便于后续持续补充：

```text
# 标题

## 背景和适用场景
说明这个技术解决什么问题，什么时候需要用。

## 核心概念
整理关键术语、架构角色、运行机制。

## 快速开始
给出最小可运行步骤或最常用命令。

## 常见配置
列出生产或开发环境中经常调整的配置。

## 实战案例
结合后端、大数据、运维场景给出示例。

## 常见问题
记录错误现象、排查命令、原因和解决方案。

## 延伸阅读
放官方文档、关联章节或后续学习方向。
```

## 本地预览和目录生成

### 安装目录生成工具

```bash
npm install -g gitbook-summary
```

### 生成 SUMMARY.md

```bash
book sm
```

### GitBook 在线地址

https://qiangrens-organization.gitbook.io/qkd90/

## 持续维护建议

- 新增技术点时，优先放到已有大类下；只有主题明显独立时再新增一级目录。
- 操作类文档要包含环境、命令、验证方式和回滚方案。
- 原理类文档要包含概念边界、架构图或流程图、典型场景和常见误区。
- 问题排查类文档要记录现象、日志关键字、定位步骤、根因和最终修复方式。
- 命令和配置尽量使用代码块，避免只写截图或口语描述。
