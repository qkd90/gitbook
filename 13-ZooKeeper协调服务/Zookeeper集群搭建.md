# ZooKeeper 集群搭建

## 集群规划

| 节点 | 主机 | clientPort |
|------|------|------------|
| zk1 | hadoop102 | 2181 |
| zk2 | hadoop103 | 2181 |
| zk3 | hadoop104 | 2181 |

## 配置集群

### 1. 配置 zoo.cfg

在每台节点上编辑 `conf/zoo.cfg`：

```properties
dataDir=/opt/module/zookeeper-3.8.X/data
clientPort=2181
tickTime=2000
initLimit=10
syncLimit=5

# 集群配置
server.1=hadoop102:2888:3888
server.2=hadoop103:2888:3888
server.3=hadoop104:2888:3888
```

**端口说明**：
- **2888**：Follower 与 Leader 通信端口
- **3888**：选举 Leader 的端口

### 2. 创建 myid 文件

在每个节点的 `dataDir` 目录下创建 `myid` 文件：

```bash
# 在 hadoop102
echo 1 > /opt/module/zookeeper-3.8.X/data/myid

# 在 hadoop103
echo 2 > /opt/module/zookeeper-3.8.X/data/myid

# 在 hadoop104
echo 3 > /opt/module/zookeeper-3.8.X/data/myid
```

### 3. 启动集群

```bash
# 在每个节点上执行
bin/zkServer.sh start

# 查看状态
bin/zkServer.sh status
```

**预期结果**：
- 一个 Leader
- 两个 Follower

### 4. 验证集群

```bash
# 连接到任一节点
bin/zkCli.sh -server hadoop102:2181

# 创建节点
[zk: hadoop102:2181] create /test "cluster data"

# 在另一节点验证
bin/zkCli.sh -server hadoop103:2181
[zk: hadoop103:2181] get /test
```

## 集群角色

### Leader

- 处理写请求
- 发起投票

### Follower

- 处理读请求
- 参与 Leader 选举投票

### Observer

- 处理读请求
- 不参与投票（仅扩展读性能）

## 选举机制

1. 每个节点启动时都是 LOOKING 状态
2. 发起选举投票
3. 超过半数节点投票给同一节点时，该节点成为 Leader
4. 其他节点成为 Follower

## 总结

ZooKeeper 集群需要至少 3 个节点，推荐奇数节点。集群可以容忍 (N-1)/2 个节点故障。
