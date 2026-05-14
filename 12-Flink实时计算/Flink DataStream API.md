# Flink DataStream API

## DataStream API 概述

DataStream API 是 Flink 处理无界数据流的核心 API。

## 数据源（Source）

### 1. 基于集合

```java
DataStream<Integer> numbers = env.fromElements(1, 2, 3, 4, 5);
```

### 2. 基于文件

```java
DataStream<String> text = env.readTextFile("path/to/file.txt");
```

### 3. 基于 Socket

```java
DataStream<String> text = env.socketTextStream("localhost", 9999);
```

### 4. Kafka Source

```java
Properties props = new Properties();
props.setProperty("bootstrap.servers", "localhost:9092");
props.setProperty("group.id", "flink-group");

FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
    "topic",
    new SimpleStringSchema(),
    props
);
consumer.setStartFromEarliest();

DataStream<String> stream = env.addSource(consumer);
```

## 转换操作（Transformation）

### 1. Map

```java
DataStream<Integer> doubled = numbers.map(x -> x * 2);
```

### 2. FlatMap

```java
DataStream<String> words = text.flatMap((String line, Collector<String> out) -> {
    for (String word : line.split("\\s")) {
        out.collect(word);
    }
});
```

### 3. Filter

```java
DataStream<Integer> even = numbers.filter(x -> x % 2 == 0);
```

### 4. KeyBy

```java
DataStream<Tuple2<String, Integer>> keyed = stream.keyBy(0);
```

### 5. Reduce

```java
DataStream<Tuple2<String, Integer>> reduced = keyed.reduce((a, b) ->
    new Tuple2<>(a.f0, a.f1 + b.f1));
```

### 6. Union

```java
DataStream<Integer> unioned = stream1.union(stream2, stream3);
```

### 7. Connect

```java
ConnectedStreams<Integer, String> connected = stream1.connect(stream2);
```

## 数据接收（Sink）

### 1. 打印

```java
stream.print();
```

### 2. 写入文件

```java
stream.writeAsText("path/to/output.txt");
```

### 3. Kafka Sink

```java
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
    "output-topic",
    new SimpleStringSchema(),
    props
);
stream.addSink(producer);
```

## 示例：WordCount

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<String> text = env.socketTextStream("localhost", 9999);

DataStream<Tuple2<String, Integer>> counts = text
    .flatMap((String line, Collector<Tuple2<String, Integer>> out) -> {
        for (String word : line.split("\\s")) {
            out.collect(Tuple2.of(word, 1));
        }
    })
    .returns(Types.TUPLE(Types.STRING, Types.INT))
    .keyBy(0)
    .sum(1);

counts.print();

env.execute("WordCount");
```

## 总结

DataStream API 提供了丰富的转换操作，支持复杂的流处理逻辑。
