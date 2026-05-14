# Hadoop 简介

## Hadoop 的历史

Hadoop 起源于 Google 的三篇论文：

1. **2003 年**：Google 发表 GFS 论文，描述了分布式文件系统
2. **2004 年**：Google 发表 MapReduce 论文，描述了分布式计算框架
3. **2006 年**：Doug Cutting 基于 Google 论文实现了 Hadoop

Hadoop 的名字来源于 Doug Cutting 儿子的玩具大象。

## Hadoop 是什么

Hadoop 是一个开源的分布式系统基础架构，由 Apache 基金会开发。它允许使用简单的编程模型在大规模计算机集群上分布式处理海量数据集。

**核心特性**：
- **高可靠性**：自动维护数据的多份副本
- **高效性**：能够在节点间动态移动数据
- **高可扩展性**：可以扩展成千上万个节点
- **高容错性**：能够自动处理节点故障
- **低成本**：运行在廉价商用机器上

## Hadoop 的核心组件

### 1. HDFS（Hadoop Distributed File System）

Hadoop 分布式文件系统，负责数据存储。

**特点**：
- 主从架构（NameNode + DataNode）
- 分块存储（默认 128MB/块）
- 多副本机制（默认 3 副本）
- 一次写入，多次读取

### 2. MapReduce

分布式计算框架，负责数据处理。

**核心思想**：
- **Map 阶段**：将大任务分解为小任务并行执行
- **Reduce 阶段**：汇总 Map 的结果

```java
// WordCount 示例
public class WordCount {
    public static class TokenizerMapper 
         extends Mapper<Object, Text, Text, IntWritable>{
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        
        public void map(Object key, Text value, Context context) {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }
    
    public static class IntSumReducer 
         extends Reducer<Text,IntWritable,Text,IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values,
                          Context context) {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            context.write(key, new IntWritable(sum));
        }
    }
}
```

### 3. YARN（Yet Another Resource Negotiator）

资源管理器，负责集群资源调度。

**组件**：
- **ResourceManager**：全局资源管理器
- **NodeManager**：单个节点的资源管理器
- **ApplicationMaster**：每个应用的任务管理器
- **Container**：资源抽象

## Hadoop 生态系统

```
┌──────────────────────────────────────────────┐
│                  应用层                        │
├──────────┬──────────┬───────────┬────────────┤
│   Hive   │   HBase  │   Spark   │    Flink   │
├──────────┴──────────┴───────────┴────────────┤
│              计算引擎层                        │
├──────────┬──────────┬───────────┬────────────┤
│ MapReduce│    Tez   │  Spark    │   Storm    │
├──────────┴──────────┴───────────┴────────────┤
│             资源管理层 (YARN)                   │
├──────────────────────────────────────────────┤
│           存储层 (HDFS + 其他)                 │
├──────────┬──────────┬───────────┬────────────┤
│   HDFS   |   HBase  |    S3     |    OSS     │
└──────────┴──────────┴───────────┴────────────┘
```

**核心生态组件**：

| 组件 | 功能 |
|------|------|
| **HDFS** | 分布式文件系统 |
| **YARN** | 资源调度器 |
| **MapReduce** | 分布式计算框架 |
| **Hive** | 数据仓库工具（SQL on Hadoop） |
| **HBase** | 分布式列式数据库 |
| **ZooKeeper** | 分布式协调服务 |
| **Flume** | 日志收集系统 |
| **Sqoop** | 数据导入导出工具 |
| **Kafka** | 分布式消息队列 |
| **Spark** | 快速通用计算引擎 |
| **Flink** | 流处理引擎 |

## Hadoop 的应用场景

### 1. 离线批处理
- 海量日志分析
- 数据仓库 ETL
- 用户行为分析

### 2. 数据挖掘
- 用户画像
- 推荐系统
- 风控模型

### 3. 机器学习
- 分类算法
- 聚类算法
- 协同过滤

### 4. 搜索引擎
- 索引构建
- 网页抓取

## Hadoop 的优势与局限

### 优势

1. **处理海量数据**：PB 级数据处理能力
2. **线性扩展**：增加机器即可提升性能
3. **成本低**：运行在廉价机器上
4. **生态完善**：丰富的周边工具
5. **容错性好**：自动处理故障

### 局限

1. **延迟高**：不适合低延迟场景
2. **小文件问题**：NameNode 内存受限
3. **编程复杂**：MapReduce 编程模型复杂
4. **不适合迭代计算**：中间结果需写磁盘

## 总结

Hadoop 是大数据处理的基石，虽然近年来被 Spark、Flink 等新一代引擎取代，但其核心思想（分布式存储、分布式计算）仍然深刻影响着大数据技术栈。学习 Hadoop 是理解整个大数据生态的重要一步。
