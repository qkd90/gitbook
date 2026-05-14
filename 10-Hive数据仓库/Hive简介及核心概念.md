# Hive 简介及核心概念

## Hive 是什么

Apache Hive 是基于 Hadoop 的数据仓库工具，它将结构化的数据文件映射为数据库表，提供类 SQL 查询语言（HiveQL），使得不熟悉 MapReduce 的用户也能轻松处理海量数据。

**核心特点**：
- 支持 SQL 风格的查询语言（HiveQL）
- 支持数据的抽取、转换和加载（ETL）
- 支持数据存储格式管理
- 提供内置函数和自定义函数
- 适合离线批处理，不适合在线事务

## 为什么需要 Hive

### 传统数据库的局限

1. **数据量**：单机数据库无法处理 PB 级数据
2. **扩展性**：垂直扩展成本高
3. **成本**：商业数据库授权费用高

### Hive 的优势

1. **海量数据处理**：基于 Hadoop，可扩展至数千节点
2. **类 SQL 接口**：学习成本低
3. **生态集成**：与 Hadoop 生态无缝集成
4. **扩展性**：支持自定义函数和存储格式

## Hive 的架构

```
┌─────────────────────────────────────────────┐
│  用户接口 (CLI, JDBC, Web UI, Thrift)        │
├─────────────────────────────────────────────┤
│               HiveQL 解析器                   │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ 解析器   │ │ 编译器    │ │ 优化器        │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
├─────────────────────────────────────────────┤
│             执行引擎                         │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │ MapReduce │ │   Tez    │ │   Spark     │ │
│  └──────────┘ └──────────┘ └─────────────┘ │
├─────────────────────────────────────────────┤
│             元数据存储 (Metastore)            │
├─────────────────────────────────────────────┤
│             数据存储 (HDFS)                   │
└─────────────────────────────────────────────┘
```

### 核心组件

**1. 用户接口**
- **CLI**：命令行界面，最常用
- **JDBC/ODBC**：应用程序接口
- **Web UI**：浏览器界面
- **Thrift Server**：远程服务接口

**2. 驱动器（Driver）**
- **解析器（Parser）**：将 SQL 转换为抽象语法树
- **编译器（Compiler）**：将 AST 编译为执行计划
- **优化器（Optimizer）**：优化执行计划
- **执行器（Executor）**：执行计划

**3. 元数据存储（Metastore）**
- 存储表结构、分区信息、列类型等元数据
- 通常使用 MySQL 等关系型数据库

**4. 数据存储**
- 实际数据存储在 HDFS 上
- 支持多种存储格式（TextFile, ORC, Parquet 等）

## 数据模型

### 1. 数据库（Database）

数据库是表的容器，用于组织和管理表。

```sql
-- 创建数据库
CREATE DATABASE mydb;

-- 使用数据库
USE mydb;

-- 查看数据库
SHOW DATABASES;
```

### 2. 表（Table）

Hive 的表分为两种：

**内部表（Managed Table）**
- Hive 管理数据的生命周期
- 删除表时同时删除数据
- 适合中间数据和临时数据

**外部表（External Table）**
- Hive 只管理元数据，不管理数据
- 删除表时不删除数据
- 适合共享数据和原始数据

```sql
-- 创建内部表
CREATE TABLE internal_table (
    id INT,
    name STRING
) ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';

-- 创建外部表
CREATE EXTERNAL TABLE external_table (
    id INT,
    name STRING
) ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/user/hive/external';
```

### 3. 分区表（Partitioned Table）

分区表将数据按某个列的值进行划分，提高查询效率。

```sql
-- 创建分区表
CREATE TABLE partitioned_table (
    id INT,
    name STRING
) PARTITIONED BY (dt STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';

-- 添加分区
ALTER TABLE partitioned_table ADD PARTITION (dt='2024-01-01');

-- 查询指定分区
SELECT * FROM partitioned_table WHERE dt='2024-01-01';
```

### 4. 分桶表（Bucketed Table）

分桶表将数据按某个列的哈希值分散到多个文件中。

```sql
-- 创建分桶表
CREATE TABLE bucketed_table (
    id INT,
    name STRING
) CLUSTERED BY (id) INTO 4 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';
```

## 数据类型

### 基本数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| TINYINT | 1字节整数 | 10 |
| SMALLINT | 2字节整数 | 100 |
| INT | 4字节整数 | 1000 |
| BIGINT | 8字节整数 | 1000000 |
| FLOAT | 单精度浮点 | 3.14 |
| DOUBLE | 双精度浮点 | 3.14159 |
| STRING | 字符串 | 'hello' |
| BOOLEAN | 布尔值 | true/false |
| TIMESTAMP | 时间戳 | 2024-01-01 12:00:00 |
| DATE | 日期 | 2024-01-01 |

### 复杂数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| ARRAY | 数组 | ARRAY<INT> |
| MAP | 键值对 | MAP<STRING, INT> |
| STRUCT | 结构体 | STRUCT<id:INT, name:STRING> |

```sql
-- 复杂数据类型示例
CREATE TABLE complex_table (
    arr ARRAY<INT>,
    mp MAP<STRING, INT>,
    st STRUCT<id:INT, name:STRING>
);
```

## Hive 与数据库的区别

| 特性 | Hive | 关系型数据库 |
|------|------|-------------|
| 查询语言 | HiveQL | SQL |
| 数据存储 | HDFS | 本地文件系统 |
| 执行引擎 | MapReduce/Tez/Spark | 自定义执行引擎 |
| 延迟 | 高（分钟级） | 低（毫秒级） |
| 数据量 | PB 级 | TB 级 |
| 索引 | 有限 | 完善 |
| 事务 | 有限支持 | 完整支持 |
| 更新/删除 | 有限支持 | 完整支持 |
| 适用场景 | 离线批处理 | 在线事务处理 |

## 总结

Hive 是大数据分析的重要工具，通过类 SQL 接口简化了 MapReduce 编程。理解 Hive 的架构和数据模型是有效使用 Hive 的基础。
