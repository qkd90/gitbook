# MapReduce 编程模型

## MapReduce 简介

MapReduce 是 Hadoop 的分布式计算框架，它将计算过程抽象为两个阶段：

- **Map（映射）**：将大任务拆分为小任务并行处理
- **Reduce（归约）**：汇总 Map 的结果

MapReduce 的核心思想是**移动计算而非移动数据**，将计算任务分发到数据所在的节点上执行。

## MapReduce 的核心概念

### 1. Split（切片）

- InputSplit 是 MapReduce 对输入文件的逻辑划分
- 每个 Split 对应一个 Map 任务
- Split 大小通常等于 HDFS Block 大小（128MB）

### 2. Map 任务

- 读取 Split 中的数据
- 解析为 Key-Value 对
- 应用用户定义的 map 函数
- 输出中间结果

### 3. Shuffle（洗牌）

- 将 Map 输出按 Key 分区
- 相同 Key 的数据发送到同一个 Reduce 任务
- 包括分区、排序、合并等过程

### 4. Reduce 任务

- 接收 Shuffle 后的数据
- 相同 Key 的 Value 聚合
- 应用用户定义的 reduce 函数
- 输出最终结果

## MapReduce 的工作流程

```
Input → Split → Map → Shuffle → Reduce → Output
```

### 详细流程

1. **InputFormat**：读取输入文件，生成 InputSplit
2. **RecordReader**：将 Split 解析为 `<K1, V1>` 键值对
3. **Mapper**：处理 `<K1, V1>`，输出 `<K2, V2>`
4. **Partitioner**：确定每个 `<K2, V2>` 发送到哪个 Reduce
5. **Spill**：Map 输出写入本地磁盘
6. **Merge**：合并多个 Spill 文件
7. **Fetcher**：Reduce 从 Map 节点拉取数据
8. **Sort**：对拉取的数据按 Key 排序
9. **Reducer**：处理 `<K2, List<V2>>`，输出 `<K3, V3>`
10. **OutputFormat**：写入输出文件

## WordCount 示例

### 完整代码

```java
import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    // Mapper 类
    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    // Reducer 类
    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                          Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

### 执行过程示例

**输入文件**：
```
hello world
hello hadoop
hadoop world
```

**Map 阶段输出**：
```
<hello, 1>
<world, 1>
<hello, 1>
<hadoop, 1>
<hadoop, 1>
<world, 1>
```

**Shuffle 后**：
```
<hadoop, [1, 1]>
<hello, [1, 1]>
<world, [1, 1]>
```

**Reduce 阶段输出**：
```
<hadoop, 2>
<hello, 2>
<world, 2>
```

## Shuffle 详解

Shuffle 是 MapReduce 的核心，连接 Map 和 Reduce 阶段。

### Map 端 Shuffle

1. **环形缓冲区**：Map 输出先写入内存缓冲区（默认 100MB）
2. **溢写（Spill）**：缓冲区达到 80% 时，数据溢写到磁盘
3. **分区与排序**：溢写前按 Key 分区并排序
4. **合并（Merge）**：多个溢写文件合并为一个

### Reduce 端 Shuffle

1. **Copy 阶段**：从各个 Map 节点拉取数据
2. **Merge 阶段**：合并拉取的数据
3. **Sort 阶段**：按 Key 排序
4. **Reduce 执行**：调用 reduce 函数

### Combiner

Combiner 是可选的本地聚合操作，减少网络传输：

- 在 Map 端本地执行
- 输入输出类型必须与 Reducer 相同
- 适用于求和、计数等操作，不适用于求平均

```java
// WordCount 中的 Combiner
job.setCombinerClass(IntSumReducer.class);  // 与 Reducer 相同
```

## MapReduce 的优化

### 1. 数据倾斜

**问题**：某些 Key 的数据远多于其他 Key，导致部分 Reduce 任务执行时间长。

**解决方案**：
- 使用 Combiner 本地聚合
- 自定义 Partitioner 分散热点 Key
- 两阶段聚合（加随机前缀 → 聚合 → 去前缀 → 再聚合）

### 2. 小文件问题

**问题**：大量小文件导致 Map 任务过多，每个 Map 处理数据量小。

**解决方案**：
- 合并小文件
- 使用 CombineFileInputFormat
- 调整 split 大小

### 3. 内存优化

- 调整 Map/Reduce 任务内存
- 调整 Shuffle 缓冲区大小
- 启用压缩（Snappy、LZO）

### 4. 并行度优化

- 调整 Map 任务数（由 split 数量决定）
- 调整 Reduce 任务数（`job.setNumReduceTasks()`）
- 通常 Reduce 数量 = 集群核心数 * 0.95 或 1.75

## MapReduce vs Spark

| 特性 | MapReduce | Spark |
|------|-----------|-------|
| 计算模式 | 磁盘 IO 为主 | 内存计算为主 |
| 迭代计算 | 每次迭代写磁盘 | 数据保留在内存 |
| 延迟 | 分钟级 | 毫秒到秒级 |
| 编程模型 | 仅支持 Map 和 Reduce | 丰富的算子 |
| 容错 | 重新执行任务 | RDD Lineage 重建 |
| 适用场景 | 离线批处理 | 批处理 + 流处理 |

## 总结

MapReduce 是分布式计算的经典模型，虽然在实际应用中逐渐被 Spark 等新一代计算引擎取代，但其分而治之的思想仍然深刻影响着大数据处理。理解 MapReduce 的工作原理有助于更好地理解 Spark、Flink 等框架的设计思想。
