# Flink 环境搭建

## 环境准备

### 要求

- Java 8 或 Java 11
- 操作系统：Linux、macOS、Windows

## 本地安装

### 1. 下载

```bash
wget https://archive.apache.org/dist/flink/flink-1.XX.X/flink-1.XX.X-bin-scala_2.12.tgz
```

### 2. 解压

```bash
tar -xzf flink-1.XX.X-bin-scala_2.12.tgz
cd flink-1.XX.X
```

### 3. 启动

```bash
./bin/start-cluster.sh
```

### 4. 验证

访问 Web UI：http://localhost:8081

提交示例任务：
```bash
./bin/flink run examples/streaming/WordCount.jar
```

## IDEA 开发环境

### Maven 依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-java</artifactId>
        <version>1.XX.X</version>
    </dependency>
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-streaming-java</artifactId>
        <version>1.XX.X</version>
    </dependency>
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-clients</artifactId>
        <version>1.XX.X</version>
    </dependency>
</dependencies>
```

## 总结

Flink 的本地安装非常简单，适合快速开发和测试。
