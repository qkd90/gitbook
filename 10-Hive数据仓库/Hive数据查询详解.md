# Hive 数据查询详解

## SELECT 基础

### 基本语法

```sql
SELECT [ALL | DISTINCT] column_name, ...
FROM table_name
[WHERE condition]
[GROUP BY column_name HAVING condition]
[ORDER BY column_name]
[LIMIT n];
```

### 列别名

```sql
SELECT id, name AS employee_name, salary AS monthly_salary
FROM employees;
```

### 算术运算

```sql
SELECT id, name, salary, salary * 12 AS annual_salary
FROM employees;
```

## WHERE 条件

### 比较运算符

```sql
-- 等于
SELECT * FROM employees WHERE salary = 5000;

-- 不等于
SELECT * FROM employees WHERE salary != 5000;

-- 大于/小于
SELECT * FROM employees WHERE salary > 5000 AND salary < 10000;

-- BETWEEN
SELECT * FROM employees WHERE salary BETWEEN 5000 AND 10000;

-- IN
SELECT * FROM employees WHERE department_id IN (1, 2, 3);

-- LIKE
SELECT * FROM employees WHERE name LIKE 'A%';

-- IS NULL
SELECT * FROM employees WHERE department_id IS NULL;
```

### 逻辑运算符

```sql
-- AND
SELECT * FROM employees WHERE salary > 5000 AND department = 'IT';

-- OR
SELECT * FROM employees WHERE department = 'IT' OR department = 'HR';

-- NOT
SELECT * FROM employees WHERE NOT department = 'IT';
```

## 聚合函数

```sql
-- COUNT
SELECT COUNT(*) FROM employees;

-- SUM
SELECT SUM(salary) FROM employees;

-- AVG
SELECT AVG(salary) FROM employees;

-- MAX/MIN
SELECT MAX(salary), MIN(salary) FROM employees;
```

## GROUP BY

```sql
-- 单列分组
SELECT department, COUNT(*) as emp_count
FROM employees
GROUP BY department;

-- 多列分组
SELECT department, location, AVG(salary) as avg_salary
FROM employees
GROUP BY department, location;

-- 分组后过滤
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 6000;
```

## 窗口函数

### ROW_NUMBER

```sql
SELECT id, name, salary, department,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
FROM employees;
```

### RANK 和 DENSE_RANK

```sql
SELECT id, name, salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;
```

### SUM OVER

```sql
SELECT id, name, salary,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    SUM(salary) OVER () as grand_total
FROM employees;
```

### LAG 和 LEAD

```sql
SELECT id, name, salary,
    LAG(salary, 1) OVER (ORDER BY id) as prev_salary,
    LEAD(salary, 1) OVER (ORDER BY id) as next_salary
FROM employees;
```

## JOIN 详解

### INNER JOIN

```sql
SELECT e.id, e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

### LEFT/RIGHT OUTER JOIN

```sql
-- LEFT JOIN：返回左表所有行
SELECT e.id, e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;

-- RIGHT JOIN：返回右表所有行
SELECT e.id, e.name, d.department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
```

### FULL OUTER JOIN

```sql
SELECT e.id, e.name, d.department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
```

### CROSS JOIN

```sql
-- 笛卡尔积
SELECT e.name, d.department_name
FROM employees e
CROSS JOIN departments d;
```

## 内置函数

### 字符串函数

```sql
-- 长度
SELECT LENGTH('Hello');  -- 5

-- 截取
SELECT SUBSTR('Hello World', 1, 5);  -- Hello

-- 连接
SELECT CONCAT('Hello', ' ', 'World');  -- Hello World

-- 替换
SELECT REPLACE('Hello World', 'World', 'Hive');  -- Hello Hive

-- 大小写
SELECT UPPER('hello');  -- HELLO
SELECT LOWER('HELLO');  -- hello
```

### 日期函数

```sql
-- 当前时间
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;

-- 日期格式化
SELECT DATE_FORMAT('2024-01-01', 'yyyy-MM-dd');

-- 日期加减
SELECT DATE_ADD('2024-01-01', 10);  -- 2024-01-11
SELECT DATE_SUB('2024-01-01', 10);  -- 2023-12-22

-- 日期差
SELECT DATEDIFF('2024-01-10', '2024-01-01');  -- 9
```

### 数学函数

```sql
-- 取整
SELECT ROUND(3.14159, 2);  -- 3.14

-- 向下/向上取整
SELECT FLOOR(3.9);  -- 3
SELECT CEIL(3.1);   -- 4

-- 随机数
SELECT RAND();
```

### 条件函数

```sql
-- IF
SELECT IF(salary > 6000, 'High', 'Low') as salary_level
FROM employees;

-- CASE WHEN
SELECT id, name,
    CASE
        WHEN salary > 8000 THEN 'High'
        WHEN salary > 5000 THEN 'Medium'
        ELSE 'Low'
    END as salary_level
FROM employees;

-- COALESCE
SELECT COALESCE(department, 'Unknown') FROM employees;
```

### 集合函数

```sql
-- 数组
SELECT size(arr) FROM array_table;
SELECT arr[0] FROM array_table;

-- MAP
SELECT mp['key'] FROM map_table;

-- STRUCT
SELECT st.id, st.name FROM struct_table;
```

## 查询优化

### 1. 分区裁剪

```sql
-- 使用分区过滤
SELECT * FROM partitioned_table WHERE dt='2024-01-01';

-- 开启严格模式
SET hive.mapred.mode=strict;
```

### 2. 列裁剪

```sql
-- 只查询需要的列
SELECT id, name FROM employees;  -- 优于 SELECT *
```

### 3. JOIN 优化

```sql
-- 小表放前面（Map JOIN）
SELECT /*+ MAPJOIN(d) */ e.*, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.id;
```

### 4. 并行执行

```sql
SET hive.exec.parallel=true;
SET hive.exec.parallel.thread.number=8;
```

## 总结

Hive 提供丰富的查询功能，包括基本 SQL 语法、窗口函数、内置函数等。掌握查询优化技巧可以显著提升大数据查询性能。
