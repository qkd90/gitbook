# 数据库和中间件

## 章节定位

本章节覆盖后端系统常用的数据存储、缓存、搜索、消息、代理和 SQL 训练内容，是从单体应用走向高并发、高可用系统的关键基础。

## 技术地图

```text
关系型数据库
  ├─ MySQL、Oracle、PostgreSQL
  ├─ 表结构设计、索引、事务、锁
  └─ SQL 训练、慢查询、主从复制

NoSQL 和搜索
  ├─ MongoDB
  └─ Elasticsearch

消息和分析
  ├─ Kafka
  └─ Doris

网关和代理
  └─ Nginx

运维和监控
  ├─ 数据导入导出
  ├─ 监控指标
  └─ 常见报错处理
```

## 学习路径

1. 先掌握 SQL 基础、JOIN、聚合、窗口函数。
2. 学习 MySQL 表设计、索引、事务和锁。
3. 学习 MyBatis、MyBatis-Plus 等 Java 持久层工具。
4. 学习 MongoDB、Elasticsearch、Kafka 的适用场景。
5. 学习 Nginx 反向代理、负载均衡和静态资源配置。
6. 补充监控、备份、恢复、导入导出和故障排查能力。

## 选型建议

- 强事务、复杂查询：优先关系型数据库。
- 文档结构灵活、字段变化频繁：可以考虑 MongoDB。
- 关键词搜索和日志检索：使用 Elasticsearch。
- 异步解耦、削峰、事件流：使用 Kafka。
- 实时报表和多维分析：可以考虑 Doris。
- 统一入口、反向代理、静态资源：使用 Nginx。
