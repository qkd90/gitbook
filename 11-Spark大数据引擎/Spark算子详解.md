# Spark 算子详解

## Transformation 算子

### 1. map

对每个元素应用函数：

```scala
val rdd = sc.parallelize(List(1, 2, 3, 4))
val mapped = rdd.map(x => x * 2)
// 结果: [2, 4, 6, 8]
```

### 2. filter

过滤满足条件的元素：

```scala
val rdd = sc.parallelize(List(1, 2, 3, 4, 5))
val filtered = rdd.filter(x => x > 3)
// 结果: [4, 5]
```

### 3. flatMap

将每个元素映射为多个元素并展平：

```scala
val rdd = sc.parallelize(List("hello world", "spark sql"))
val words = rdd.flatMap(line => line.split(" "))
// 结果: ["hello", "world", "spark", "sql"]
```

### 4. reduceByKey

按 Key 聚合：

```scala
val pairs = sc.parallelize(List(("a", 1), ("b", 2), ("a", 3), ("b", 4)))
val reduced = pairs.reduceByKey(_ + _)
// 结果: [("a", 4), ("b", 6)]
```

### 5. groupByKey

按 Key 分组：

```scala
val pairs = sc.parallelize(List(("a", 1), ("b", 2), ("a", 3)))
val grouped = pairs.groupByKey()
// 结果: [("a", [1, 3]), ("b", [2])]
```

### 6. join

连接两个 RDD：

```scala
val rdd1 = sc.parallelize(List(("a", 1), ("b", 2)))
val rdd2 = sc.parallelize(List(("a", 3), ("c", 4)))
val joined = rdd1.join(rdd2)
// 结果: [("a", (1, 3))]
```

### 7. union

合并两个 RDD：

```scala
val rdd1 = sc.parallelize(List(1, 2))
val rdd2 = sc.parallelize(List(3, 4))
val unioned = rdd1.union(rdd2)
// 结果: [1, 2, 3, 4]
```

### 8. distinct

去重：

```scala
val rdd = sc.parallelize(List(1, 2, 2, 3, 3, 3))
val distinct = rdd.distinct()
// 结果: [1, 2, 3]
```

## Action 算子

### 1. collect

返回所有元素（注意内存溢出）：

```scala
rdd.collect()
```

### 2. count

返回元素数量：

```scala
rdd.count()
```

### 3. take

返回前 N 个元素：

```scala
rdd.take(3)
```

### 4. top

返回最大的 N 个元素：

```scala
rdd.top(3)
```

### 5. saveAsTextFile

保存到文件系统：

```scala
rdd.saveAsTextFile("hdfs://output")
```

## 算子优化

### combineByKey

比 groupByKey 和 reduceByKey 更高效：

```scala
val initial = (value: Int) => (value, 1)
val mergeVal = (acc: (Int, Int), value: Int) => (acc._1 + value, acc._2 + 1)
val mergeComb = (acc1: (Int, Int), acc2: (Int, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2)

val result = pairs.combineByKey(initial, mergeVal, mergeComb)
```

## 总结

Spark 提供了丰富的算子，选择合适的算子可以显著提升代码性能和可读性。
