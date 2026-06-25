# Doris

## 简介

Apache Doris 是一款面向实时分析的 MPP 数据库，适合报表分析、用户画像、日志分析、数据服务接口、BI 查询等场景。它支持高并发查询、列式存储、向量化执行和多种数据导入方式。

## 核心角色

| 角色 | 说明 |
| --- | --- |
| FE | Frontend，负责元数据、SQL 解析、查询规划、调度 |
| BE | Backend，负责数据存储、执行计划、数据导入 |
| Broker | 访问外部存储的辅助组件，部分场景使用 |

生产集群通常至少部署 3 个 FE 和多个 BE，单机环境只适合学习和验证。

## Docker 单机体验

拉取镜像：

```bash
docker pull apache/doris:all-in-one-2.1.7
```

启动：

```bash
docker run -d \
  --name doris \
  -p 8030:8030 \
  -p 8040:8040 \
  -p 9030:9030 \
  apache/doris:all-in-one-2.1.7
```

端口说明：

| 端口 | 说明 |
| --- | --- |
| 8030 | FE Web UI |
| 8040 | BE Web UI |
| 9030 | MySQL 协议连接端口 |

连接 Doris：

```bash
mysql -h 127.0.0.1 -P 9030 -uroot
```

## 基础 SQL

创建数据库：

```sql
CREATE DATABASE demo;
USE demo;
```

创建明细模型表：

```sql
CREATE TABLE user_event (
    user_id BIGINT,
    event_time DATETIME,
    event_type VARCHAR(64),
    device VARCHAR(64),
    amount DECIMAL(18, 2)
)
DUPLICATE KEY(user_id, event_time)
DISTRIBUTED BY HASH(user_id) BUCKETS 10
PROPERTIES (
    "replication_num" = "1"
);
```

写入数据：

```sql
INSERT INTO user_event VALUES
(1, '2026-01-01 10:00:00', 'login', 'android', 0),
(1, '2026-01-01 10:05:00', 'pay', 'android', 99.00);
```

查询：

```sql
SELECT event_type, COUNT(*) AS cnt, SUM(amount) AS total_amount
FROM user_event
GROUP BY event_type;
```

## 表模型选择

| 模型 | 适用场景 |
| --- | --- |
| Duplicate Key | 明细数据、日志、行为事件 |
| Aggregate Key | 固定维度聚合指标 |
| Unique Key | 需要按主键更新的宽表 |

选择建议：

- 日志和流水类数据优先 Duplicate Key。
- 指标聚合类数据使用 Aggregate Key。
- 用户画像、订单宽表等需要更新的数据使用 Unique Key。

## 数据导入方式

常见方式：

- `INSERT INTO`：小批量写入或调试。
- Stream Load：通过 HTTP 导入本地或实时数据。
- Broker Load：从 HDFS、对象存储导入。
- Routine Load：持续消费 Kafka。
- Flink Connector：实时写入 Doris。

Stream Load 示例：

```bash
curl --location-trusted -u root: \
  -H "format: json" \
  -H "strip_outer_array: true" \
  -T data.json \
  http://127.0.0.1:8030/api/demo/user_event/_stream_load
```

## 常见问题

### 查询连接不上

检查：

- `9030` 端口是否映射。
- 容器是否正常启动。
- FE 是否启动完成。

```bash
docker logs -f doris
```

### 副本数不满足

单机测试时表属性设置：

```sql
PROPERTIES ("replication_num" = "1");
```

生产环境不要随意降低副本数，需要结合节点数量和可用性要求。

### 导入失败

排查：

- 字段顺序和类型是否匹配。
- JSON 是否为合法格式。
- 分区、分桶、唯一键是否符合表定义。
- 查看导入任务错误信息。
