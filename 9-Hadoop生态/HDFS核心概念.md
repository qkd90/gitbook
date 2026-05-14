# HDFS 核心概念

## HDFS 是什么

HDFS（Hadoop Distributed File System）是 Hadoop 的分布式文件系统，设计用于在廉价硬件上运行，提供高吞吐量的数据访问，非常适合大规模数据集。

## HDFS 的设计目标

1. **检测并快速恢复硬件故障**：故障是常态而非例外
2. **流式数据访问**：关注数据访问的吞吐量而非延迟
3. **超大文件**：支持 TB、PB 级别的文件
4. **简单一致性模型**：一次写入，多次读取
5. **移动计算比移动数据更经济**：将计算移动到数据所在位置

## HDFS 的架构

### 主从架构

HDFS 采用主从（Master-Slave）架构：

```
                    ┌─────────────┐
                    │  NameNode   │  (Master)
                    │  元数据管理   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐ ┌───┴─────┐ ┌───┴─────┐
        │ DataNode  │ │ DataNode│ │ DataNode│  (Slaves)
        │  数据块1   │ │  数据块2 │ │  数据块3 │
        └───────────┘ └─────────┘ └─────────┘
```

### NameNode（主节点）

**职责**：
- 管理文件系统的命名空间
- 维护文件与数据块的映射关系
- 处理客户端的读写请求
- 管理数据块的副本策略

**存储内容**：
- **FsImage**：文件系统元数据的持久化快照
- **Edits**：记录所有写操作的日志
- **Block Locations**：数据块与 DataNode 的映射（启动时重建）

**内存限制**：
- NameNode 将所有元数据加载到内存
- 每个文件/目录/数据块约占用 150 字节内存
- 单个 NameNode 大约能管理数千万个文件

### DataNode（从节点）

**职责**：
- 存储实际的数据块
- 执行数据块的读写操作
- 定期向 NameNode 发送心跳和块报告

**工作模式**：
- 每 3 秒发送心跳（可配置）
- 每 6 小时发送完整块报告（可配置）
- 如果 10 分钟未收到心跳，NameNode 认为该 DataNode 故障

## 数据块（Block）

### 基本概念

HDFS 将文件分割成固定大小的块进行存储：

- **Hadoop 1.x**：默认块大小 64MB
- **Hadoop 2.x/3.x**：默认块大小 128MB

### 为什么块要大？

1. **减少寻址时间**：块大可以减少元数据操作
2. **减少网络开销**：减少与 NameNode 的通信
3. **适合流式读取**：大块适合顺序读取

### 数据块副本

HDFS 采用多副本机制保证可靠性：

- **默认副本数**：3（可通过 `dfs.replication` 配置）
- **副本放置策略**：
  - 第 1 个副本：本地节点（如果在集群内）
  - 第 2 个副本：不同机架的随机节点
  - 第 3 个副本：与第 2 个副本同机架的不同节点

```
机架1                    机架2
┌─────┐                 ┌─────┐
│ DN1 │ ← 副本1          │ DN3 │ ← 副本2
└─────┘                 └─────┘
                          ┌─────┐
                          │ DN4 │ ← 副本3
                          └─────┘
```

## HDFS 的读写流程

### 读取文件流程

1. 客户端调用 `FileSystem.open()` 打开文件
2. RPC 调用 NameNode 获取文件的数据块位置
3. NameNode 返回数据块列表及其所在的 DataNode
4. 客户端选择最近的 DataNode 读取数据
5. 读取完成后关闭流

```java
Configuration conf = new Configuration();
FileSystem fs = FileSystem.get(URI.create("hdfs://localhost:9000"), conf);
FSDataInputStream in = fs.open(new Path("/file.txt"));
IOUtils.copyBytes(in, System.out, 4096, false);
IOUtils.closeStream(in);
```

### 写入文件流程

1. 客户端调用 `FileSystem.create()` 创建文件
2. RPC 调用 NameNode 请求创建文件
3. NameNode 检查文件和权限后返回成功
4. 客户端写入数据到第一个 DataNode
5. 第一个 DataNode 将数据复制到第二个 DataNode
6. 第二个 DataNode 复制到第三个 DataNode
7. 所有 DataNode 返回成功
8. 客户端关闭流

```java
Configuration conf = new Configuration();
FileSystem fs = FileSystem.get(URI.create("hdfs://localhost:9000"), conf);
FSDataOutputStream out = fs.create(new Path("/file.txt"));
IOUtils.copyBytes(in, out, 4096, false);
IOUtils.closeStream(out);
```

## HDFS 的容错机制

### 1. NameNode 容错

- **Secondary NameNode**：定期合并 FsImage 和 Edits，不是热备
- **HA（High Availability）**：Active/Standby 双 NameNode
- **Federation**：多个 NameNode 共享 DataNode

### 2. DataNode 容错

- **心跳检测**：NameNode 检测 DataNode 状态
- **副本复制**：发现副本不足时自动复制
- **数据校验**：使用 CRC 校验数据完整性

### 3. 网络拓扑

HDFS 感知网络拓扑，优化副本放置：

```
/                -- 根机架
  /rack1         -- 机架1
    /rack1/node1 -- 节点1
  /rack2         -- 机架2
    /rack2/node2 -- 节点2
```

**距离计算**：
- `/rack1/node1` 到 `/rack1/node1`：距离 0
- `/rack1/node1` 到 `/rack1/node2`：距离 2
- `/rack1/node1` 到 `/rack2/node1`：距离 4

## HDFS 的适用场景

### 适用场景

1. **大文件存储**：GB、TB 级别文件
2. **流式读取**：顺序读取大量数据
3. **一次写入多次读取**：数据写入后不修改
4. **离线批处理**：MapReduce、Spark 批处理
5. **数据仓库**：Hive、Presto 等查询引擎的数据源

### 不适用场景

1. **低延迟访问**：毫秒级响应要求
2. **大量小文件**：NameNode 内存受限
3. **频繁修改**：不支持文件的随机位置修改
4. **多用户写入**：只支持单写入者

## 总结

HDFS 是大数据存储的基石，理解 HDFS 的架构和工作原理是学习大数据技术栈的基础。其主从架构、分块存储、多副本机制等设计理念深刻影响了后续的分布式存储系统。
