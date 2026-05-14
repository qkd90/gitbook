# Spark Streaming

## 什么是 Spark Streaming

Spark Streaming 是 Spark 的可扩展、高吞吐、容错的流处理引擎。

**核心概念**：
- **DStream**：离散化流，代表连续的数据流
- **微批处理**：将流数据分为小批次进行处理

## 创建 StreamingContext

```scala
import org.apache.spark.streaming.{Seconds, StreamingContext}

val ssc = new StreamingContext(sc, Seconds(1))  // 1 秒批次
```

## 数据源

### 1. 文件流

```scala
val lines = ssc.textFileStream("hdfs://path/to/dir")
```

### 2. Kafka 流

```scala
import org.apache.spark.streaming.kafka010._

val kafkaParams = Map[String, Object](
    "bootstrap.servers" -> "localhost:9092",
    "key.deserializer" -> classOf[StringDeserializer],
    "value.deserializer" -> classOf[StringDeserializer],
    "group.id" -> "spark-streaming"
)

val stream = KafkaUtils.createDirectStream[String, String](
    ssc,
    PreferConsistent,
    Subscribe[String, String](topics, kafkaParams)
)
```

### 3. Socket 流

```scala
val lines = ssc.socketTextStream("localhost", 9999)
```

## 转换操作

```scala
// Word Count 示例
val lines = ssc.socketTextStream("localhost", 9999)
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.reduceByKey(_ + _)
wordCounts.print()
```

## 窗口操作

```scala
// 窗口长度 3 秒，滑动间隔 2 秒
val windowedCounts = pairs.reduceByKeyAndWindow(
    (a: Int, b: Int) => a + b,
    Seconds(3),
    Seconds(2)
)
```

## 状态管理

```scala
// updateStateByKey
val updateFunc = (values: Seq[Int], state: Option[Int]) => {
    val currentCount = values.sum
    val previousCount = state.getOrElse(0)
    Some(currentCount + previousCount)
}

val stateDStream = pairs.updateStateByKey[Int](updateFunc)
```

## 启动与停止

```scala
// 启动
ssc.start()
ssc.awaitTermination()

// 停止
ssc.stop(stopSparkContext = true, stopGracefully = true)
```

## 总结

Spark Streaming 适合微批处理场景，与 Spark Core 和 SparkSQL 无缝集成。
