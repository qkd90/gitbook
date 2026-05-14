# Hive DDL 操作

## DDL（数据定义语言）简介

DDL 用于定义和管理数据库、表、视图等对象的结构。

## 数据库操作

### 创建数据库

```sql
-- 基本创建
CREATE DATABASE mydb;

-- 如果不存在则创建
CREATE DATABASE IF NOT EXISTS mydb;

-- 创建数据库并指定位置
CREATE DATABASE mydb
LOCATION '/user/hive/mydb';

-- 创建数据库并添加注释
CREATE DATABASE mydb
COMMENT 'My test database';

-- 创建数据库并添加属性
CREATE DATABASE mydb
WITH DBPROPERTIES ('creator'='hadoop', 'date'='2024-01-01');
```

### 查看数据库

```sql
-- 查看所有数据库
SHOW DATABASES;

-- 使用通配符查看
SHOW DATABASES LIKE 'my*';

-- 查看数据库详情
DESC DATABASE mydb;

-- 查看数据库扩展信息
DESC DATABASE EXTENDED mydb;
```

### 删除数据库

```sql
-- 删除空数据库
DROP DATABASE mydb;

-- 删除数据库及其中的表
DROP DATABASE mydb CASCADE;

-- 如果存在则删除
DROP DATABASE IF EXISTS mydb;
```

### 修改数据库

```sql
-- 修改数据库属性
ALTER DATABASE mydb SET DBPROPERTIES ('edited-by'='hadoop');
```

> **注意**：Hive 不支持修改数据库名称和位置。

## 表操作

### 创建表

```sql
CREATE [EXTERNAL] TABLE [IF NOT EXISTS] table_name
[(col_name data_type [COMMENT col_comment], ...)]
[COMMENT table_comment]
[PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
[CLUSTERED BY (col_name, col_name, ...)
 [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS]
[ROW FORMAT row_format]
[STORED AS file_format]
[LOCATION hdfs_path]
[TBLPROPERTIES (property_name=property_value, ...)]
[AS select_statement]
```

### 内部表与外部表

**内部表（Managed Table）**：
```sql
CREATE TABLE employees (
    id INT,
    name STRING,
    salary DOUBLE,
    department STRING
) ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;
```

**外部表（External Table）**：
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS external_logs (
    timestamp STRING,
    level STRING,
    message STRING
) ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
LOCATION '/user/hadoop/logs';
```

### 加载数据

```sql
-- 从本地加载
LOAD DATA LOCAL INPATH '/local/path/data.txt'
INTO TABLE employees;

-- 从 HDFS 加载
LOAD DATA INPATH '/hdfs/path/data.txt'
INTO TABLE employees;

-- 覆盖数据
LOAD DATA LOCAL INPATH '/local/path/data.txt'
OVERWRITE INTO TABLE employees;
```

### 查看表

```sql
-- 查看所有表
SHOW TABLES;

-- 查看表结构
DESC table_name;

-- 查看表详细信息
DESC FORMATTED table_name;

-- 查看建表语句
SHOW CREATE TABLE table_name;
```

### 修改表

```sql
-- 重命名表
ALTER TABLE old_name RENAME TO new_name;

-- 添加列
ALTER TABLE table_name ADD COLUMNS (new_col STRING COMMENT 'new column');

-- 修改列
ALTER TABLE table_name CHANGE old_col new_col NEW_TYPE;

-- 替换列
ALTER TABLE table_name REPLACE COLUMNS (
    col1 INT,
    col2 STRING
);
```

### 删除表

```sql
-- 删除表
DROP TABLE table_name;

-- 清空表数据
TRUNCATE TABLE table_name;
```

## 分区表操作

### 创建分区表

```sql
CREATE TABLE partitioned_users (
    id INT,
    name STRING
) PARTITIONED BY (country STRING, dt STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';
```

### 添加分区

```sql
-- 添加单个分区
ALTER TABLE partitioned_users ADD PARTITION (country='US', dt='2024-01-01');

-- 添加多个分区
ALTER TABLE partitioned_users ADD
    PARTITION (country='US', dt='2024-01-02')
    PARTITION (country='CN', dt='2024-01-01');
```

### 删除分区

```sql
ALTER TABLE partitioned_users DROP PARTITION (country='US', dt='2024-01-01');
```

### 查看分区

```sql
-- 查看所有分区
SHOW PARTITIONS partitioned_users;

-- 查看特定分区
SHOW PARTITIONS partitioned_users PARTITION(country='US');
```

## 分桶表操作

### 创建分桶表

```sql
CREATE TABLE bucketed_users (
    id INT,
    name STRING
) CLUSTERED BY (id)
SORTED BY (id ASC)
INTO 4 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';
```

### 插入数据

```sql
-- 开启分桶插入
SET hive.enforce.bucketing=true;

INSERT INTO bucketed_users
SELECT id, name FROM source_users;
```

## 视图操作

### 创建视图

```sql
CREATE VIEW IF NOT EXISTS view_employees AS
SELECT id, name, salary
FROM employees
WHERE salary > 5000;
```

### 查看视图

```sql
SHOW TABLES LIKE 'view_*';
DESC view_employees;
```

### 删除视图

```sql
DROP VIEW view_employees;
```

## 索引操作（Hive 0.7+）

> **注意**：Hive 3.0 已废弃索引，推荐使用物化视图或分区。

```sql
-- 创建索引
CREATE INDEX idx_name
ON TABLE employees (name)
AS 'COMPACT'
WITH DEFERRED REBUILD;

-- 重建索引
ALTER INDEX idx_name ON employees REBUILD;

-- 删除索引
DROP INDEX idx_name ON employees;
```

## 总结

Hive DDL 操作与 SQL 类似，但增加了一些大数据特有的功能（分区、分桶、外部表等）。掌握这些操作是高效使用 Hive 的基础。
