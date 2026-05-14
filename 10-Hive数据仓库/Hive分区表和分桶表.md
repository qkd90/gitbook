# Hive 分区表和分桶表

## 分区表（Partitioned Table）

### 什么是分区

分区是将表数据按某个列的值划分为不同的目录，查询时只扫描相关分区，提高效率。

### 分区表的创建

```sql
CREATE TABLE partitioned_users (
    id INT,
    name STRING,
    age INT
) PARTITIONED BY (country STRING, dt STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';
```

### 分区存储结构

```
/user/hive/warehouse/partitioned_users/
├── country=CN/
│   ├── dt=2024-01-01/
│   │   └── data.txt
│   └── dt=2024-01-02/
│       └── data.txt
└── country=US/
    └── dt=2024-01-01/
        └── data.txt
```

### 分区操作

```sql
-- 添加分区
ALTER TABLE partitioned_users ADD PARTITION (country='CN', dt='2024-01-03');

-- 删除分区
ALTER TABLE partitioned_users DROP PARTITION (country='CN', dt='2024-01-01');

-- 查看分区
SHOW PARTITIONS partitioned_users;

-- 修复分区（手动添加分区后）
MSCK REPAIR TABLE partitioned_users;
```

### 分区查询

```sql
-- 分区裁剪（只扫描指定分区）
SELECT * FROM partitioned_users
WHERE country='CN' AND dt='2024-01-01';

-- 分区字段不可以在 SELECT 中使用（除非是分区列）
```

### 静态分区 vs 动态分区

**静态分区**：手动指定分区

```sql
INSERT INTO partitioned_users PARTITION (country='CN', dt='2024-01-01')
SELECT id, name, age FROM source_users;
```

**动态分区**：自动识别分区

```sql
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT INTO partitioned_users PARTITION (country, dt)
SELECT id, name, age, country, dt FROM source_users;
```

## 分桶表（Bucketed Table）

### 什么是分桶

分桶是将数据按某个列的哈希值分散到固定数量的文件中，适合抽样和 JOIN 优化。

### 分桶表的创建

```sql
CREATE TABLE bucketed_users (
    id INT,
    name STRING,
    age INT
) CLUSTERED BY (id)
SORTED BY (id ASC)
INTO 4 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';
```

### 分桶存储结构

```
/user/hive/warehouse/bucketed_users/
├── 000000_0  -- 桶 1
├── 000001_0  -- 桶 2
├── 000002_0  -- 桶 3
└── 000003_0  -- 桶 4
```

### 分桶规则

桶编号 = hash(分桶列) % 桶数量

### 分桶插入

```sql
-- 开启分桶强制
SET hive.enforce.bucketing=true;
SET hive.enforce.sorting=true;

INSERT INTO bucketed_users
SELECT id, name, age FROM source_users;
```

## 分区与分桶的比较

| 特性 | 分区表 | 分桶表 |
|------|--------|--------|
| 划分依据 | 列的值 | 列的哈希值 |
| 目录结构 | 每个分区一个目录 | 每个桶一个文件 |
| 适用场景 | 按时间/地区过滤 | 抽样、JOIN 优化 |
| 数量 | 动态增加 | 固定数量 |
| 数据倾斜 | 可能 | 较均匀 |
| 查询效率 | 高（分区裁剪） | 中（桶裁剪） |

## 组合使用

```sql
CREATE TABLE complex_table (
    id INT,
    name STRING
) PARTITIONED BY (dt STRING)
CLUSTERED BY (id) INTO 4 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';
```

```
/user/hive/warehouse/complex_table/
├── dt=2024-01-01/
│   ├── 000000_0
│   ├── 000001_0
│   └── ...
└── dt=2024-01-02/
    ├── 000000_0
    └── ...
```

## 总结

分区和分桶是 Hive 优化的重要手段。分区适合按范围过滤，分桶适合抽样和 JOIN 优化。合理组合使用可以显著提升查询性能。
