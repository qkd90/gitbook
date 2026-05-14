# ZooKeeper 安装

## 环境准备

- Java 1.8+

## 单机模式安装

### 1. 下载并解压

```bash
tar -zxvf apache-zookeeper-3.8.X-bin.tar.gz -C /opt/module/
```

### 2. 配置

```bash
cd /opt/module/apache-zookeeper-3.8.X-bin/conf
cp zoo_sample.cfg zoo.cfg
```

编辑 `zoo.cfg`：

```properties
# 数据目录
dataDir=/opt/module/apache-zookeeper-3.8.X-bin/data

# 客户端端口
clientPort=2181

# 客户端最大连接数
maxClientCnxns=60

# 心跳间隔（毫秒）
tickTime=2000

# 初始化心跳数
initLimit=10

# 同步心跳数
syncLimit=5
```

### 3. 启动

```bash
bin/zkServer.sh start

# 查看状态
bin/zkServer.sh status

# 连接客户端
bin/zkCli.sh -server localhost:2181
```

## 验证安装

```bash
# 在客户端执行
[zk: localhost:2181] create /test "hello"
[zk: localhost:2181] get /test
[zk: localhost:2181] delete /test
```

## 总结

ZooKeeper 单机模式安装简单，适合开发和测试。
