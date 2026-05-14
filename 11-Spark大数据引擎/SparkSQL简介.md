# SparkSQL 简介

## 什么是 SparkSQL

SparkSQL 是 Spark 处理结构化数据的模块，提供 DataFrame 和 Dataset API，支持 SQL 查询。

## DataFrame vs Dataset vs RDD

| 特性 | RDD | DataFrame | Dataset |
|------|-----|-----------|---------|
| 类型安全 | 是 | 否 | 是 |
| 优化 | 无 | Catalyst | Catalyst |
| API | Scala/Java/Python | 多语言 | Scala/Java |
| 性能 | 低 | 高 | 高 |

## 创建 DataFrame

```scala
// 从 RDD 创建
val df = rdd.toDF("id", "name", "salary")

// 从 JSON 创建
val df = spark.read.json("path/to/data.json")

// 从 CSV 创建
val df = spark.read
    .option("header", "true")
    .csv("path/to/data.csv")

// 从 Hive 创建
val df = spark.table("hive_table")
```

## DataFrame 操作

```scala
// 选择列
df.select("id", "name")

// 过滤
df.filter(df("salary") > 5000)

// 分组聚合
df.groupBy("department").agg(avg("salary"))

// 排序
df.orderBy(df("salary").desc)

// JOIN
df1.join(df2, df1("dept_id") === df2("id"))
```

## SQL 查询

```scala
// 注册临时表
df.createOrReplaceTempView("employees")

// 执行 SQL
val result = spark.sql("""
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    HAVING AVG(salary) > 5000
""")
```

## 总结

SparkSQL 通过 DataFrame API 提供了更高效、更易用的结构化数据处理方式。
