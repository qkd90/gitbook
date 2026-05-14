# Flink 窗口机制

## 窗口是什么

窗口是流处理中将无限流分割为有限块进行计算的机制。

## 窗口类型

### 1. 滚动窗口（Tumbling Window）

固定大小、不重叠的窗口。

```java
stream
    .keyBy(0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .sum(1);
```

### 2. 滑动窗口（Sliding Window）

固定大小、可重叠的窗口。

```java
stream
    .keyBy(0)
    .window(SlidingProcessingTimeWindows.of(Time.seconds(10), Time.seconds(5)))
    .sum(1);
```

### 3. 会话窗口（Session Window）

基于会话间隔的窗口。

```java
stream
    .keyBy(0)
    .window(ProcessingTimeSessionWindows.withGap(Time.seconds(30)))
    .sum(1);
```

### 4. 全局窗口（Global Window）

所有数据在一个窗口，需自定义触发器。

```java
stream
    .keyBy(0)
    .window(GlobalWindows.create())
    .trigger(CountTrigger.of(10))
    .sum(1);
```

## 窗口函数

### 1. ReduceFunction

```java
stream
    .keyBy(0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .reduce((a, b) -> Tuple2.of(a.f0, a.f1 + b.f1));
```

### 2. AggregateFunction

```java
stream
    .keyBy(0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .aggregate(new AggregateFunction<Tuple2<String, Integer>, Integer, Integer>() {
        public Integer createAccumulator() { return 0; }
        public Integer add(Tuple2<String, Integer> value, Integer acc) { return acc + value.f1; }
        public Integer getResult(Integer acc) { return acc; }
        public Integer merge(Integer a, Integer b) { return a + b; }
    });
```

### 3. ProcessWindowFunction

```java
stream
    .keyBy(0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .process(new ProcessWindowFunction<Tuple2<String, Integer>, String, Tuple, TimeWindow>() {
        public void process(Tuple key, Context ctx, Iterable<Tuple2<String, Integer>> elements, Collector<String> out) {
            int count = 0;
            for (Tuple2<String, Integer> e : elements) {
                count += e.f1;
            }
            out.collect("Window: " + ctx.window() + ", Count: " + count);
        }
    });
```

## 触发器与驱逐器

### 触发器（Trigger）

决定何时触发窗口计算。

### 驱逐器（Evictor）

在计算前后移除窗口元素。

## 总结

窗口是流处理的核心机制，选择合适的窗口类型对业务逻辑至关重要。
