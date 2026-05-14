# Hive DML 操作

## DML（数据操作语言）简介

DML 用于对表中的数据进行增删改操作。

## 数据插入

### INSERT INTO

```sql
-- 插入单行数据
INSERT INTO table_name VALUES (1, 'Alice', 5000);

-- 插入多行数据
INSERT INTO table_name VALUES
    (1, 'Alice', 5000),
    (2, 'Bob', 6000),
    (3, 'Charlie', 7000);
```

### INSERT OVERWRITE

```sql
-- 覆盖整个表
INSERT OVERWRITE TABLE table_name
SELECT * FROM source_table;

-- 覆盖指定分区
INSERT OVERWRITE TABLE partitioned_table PARTITION (dt='2024-01-01')
SELECT id, name FROM source_table;
```

### 动态分区插入

```sql
-- 开启动态分区
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

-- 动态分区插入
INSERT INTO partitioned_table PARTITION (country, dt)
SELECT id, name, country, dt FROM source_table;
```

## 数据更新与删除

> **注意**：Hive 的 UPDATE 和 DELETE 需要表支持 ACID（ORC 格式 + 分桶）。

### UPDATE

```sql
UPDATE table_name
SET salary = salary * 1.1
WHERE department = 'IT';
```

### DELETE

```sql
DELETE FROM table_name
WHERE id = 1;
```

### MERGE（Hive 3.0+）

```sql
MERGE INTO target_table AS T
USING source_table AS S
ON T.id = S.id
WHEN MATCHED THEN UPDATE SET T.name = S.name, T.salary = S.salary
WHEN NOT MATCHED THEN INSERT VALUES (S.id, S.name, S.salary);
```

## 数据导出

### 导出到本地

```sql
-- 导出到本地文件系统
INSERT OVERWRITE LOCAL DIRECTORY '/local/output'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT * FROM table_name;
```

### 导出到 HDFS

```sql
-- 导出到 HDFS
INSERT OVERWRITE DIRECTORY '/hdfs/output'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT * FROM table_name;
```

## 查询操作

### 基本查询

```sql
-- 全表扫描
SELECT * FROM employees;

-- 指定列
SELECT id, name, salary FROM employees;

-- 条件过滤
SELECT * FROM employees WHERE salary > 5000;

-- 排序
SELECT * FROM employees ORDER BY salary DESC;

-- 限制结果
SELECT * FROM employees LIMIT 10;
```

### 聚合查询

```sql
-- 聚合函数
SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_salary
FROM employees
GROUP BY department;

-- 条件过滤聚合
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 6000;
```

### JOIN 操作

```sql
-- INNER JOIN
SELECT e.id, e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;

-- LEFT JOIN
SELECT e.id, e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;

-- FULL OUTER JOIN
SELECT e.id, e.name, d.department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
```

### 子查询

```sql
-- WHERE 子句中的子查询
SELECT * FROM employees
WHERE department_id IN (
    SELECT id FROM departments WHERE location = 'Beijing'
);

-- FROM 子句中的子查询
SELECT dept_name, avg_salary
FROM (
    SELECT d.department_name as dept_name, AVG(e.salary) as avg_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    GROUP BY d.department_name
) sub_query
WHERE avg_salary > 6000;
```

## 总结

Hive DML 支持基本的数据操作，但 UPDATE 和 DELETE 需要特殊配置。大多数场景下，Hive 用于批量数据读取和写入。
