# Spark RDD

## RDD 是什么

RDD（Resilient Distributed Dataset）是 Spark 的核心数据结构，代表一个不可变、可分区、可并行计算的元素集合。

**核心特性**：
- **不可变**：创建后不能修改
- **分布式**：数据分布在集群的多个节点上
- **弹性**：故障时可通过 Lineage 重建
- **分区**：数据按分区组织

## RDD 的创建

### 1. 从集合创建

```scala
val data = Array(1, 2, 3, 4, 5)
val rdd = sc.parallelize(data, 3)  // 3 个分区
```

### 2. 从外部存储创建

```scala
// 从本地文件
val rdd = sc.textFile("file:///path/to/file.txt")

// 从 HDFS
val rdd = sc.textFile("hdfs://localhost:9000/input.txt")

// 从多个文件
val rdd = sc.textFile("hdfs://localhost:9000/*.txt")
```

## RDD 的操作

### Transformation（转换）

返回新的 RDD，延迟执行：

```scala
// map
val rdd2 = rdd.map(x => x * 2)

// filter
val rdd3 = rdd.filter(x => x > 2)

// flatMap
val rdd4 = rdd.flatMap(x => Array(x, x*2))

// union
val rdd5 = rdd1.union(rdd2)

// distinct
val rdd6 = rdd.distinct()

// groupByKey
val pairs = sc.parallelize(List(("a", 1), ("b", 2), ("a", 3)))
val grouped = pairs.groupByKey()

// reduceByKey
val reduced = pairs.reduceByKey((a, b) => a + b)
```

### Action（动作）

触发计算并返回结果：

```scala
// collect
rdd.collect()  // 返回所有元素

// count
rdd.count()  // 返回元素数量

// first
rdd.first()  // 返回第一个元素

// take
rdd.take(5)  // 返回前 5 个元素

// reduce
rdd.reduce((a, b) => a + b)  // 聚合

// saveAsTextFile
rdd.saveAsTextFile("hdfs://output")
```

## RDD 的依赖

### 窄依赖（Narrow Dependency）

父 RDD 的每个分区只被子 RDD 的一个分区使用：
- map
- filter
- union

### 宽依赖（Wide Dependency）

父 RDD 的分区被子 RDD 的多个分区使用：
- groupByKey
- reduceByKey
- sortByKey

## 容错机制

RDD 通过 Lineage（血统）实现容错：

```
rdd1 → map → rdd2 → filter → rdd3 → reduceByKey → rdd4
```

如果 rdd3 的某个分区丢失，可以通过 rdd2 重新计算该分区。

## 总结

RDD 是 Spark 的基石，理解其概念和操作是掌握 Spark 编程的基础。
