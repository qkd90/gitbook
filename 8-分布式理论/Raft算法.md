# Raft 算法

## Raft 简介

Raft 是由 Diego Ongaro 和 John Ousterhout 在 2014 年提出的一种共识算法。与 Paxos 相比，Raft 的设计目标是**易于理解和实现**。

Raft 的核心思想是将共识问题分解为几个相对独立的子问题：
- Leader 选举
- 日志复制
- 安全性保证

## Raft 的角色

Raft 中的节点有三种状态：

### 1. Leader（领导者）
- 处理所有客户端请求
- 向 Follower 复制日志
- 定期发送心跳维持权威

### 2. Follower（跟随者）
- 被动接收来自 Leader 的请求
- 向 Leader 和 Candidate 投票
- 如果超时未收到心跳，转变为 Candidate

### 3. Candidate（候选者）
- 发起 Leader 选举
- 请求其他节点的投票
- 如果获得多数投票，成为 Leader

## 任期（Term）

Raft 将时间划分为连续的任期（Term），每个任期从一个新的 Leader 选举开始。

- Term 是单调递增的逻辑时钟
- 每个节点维护当前的 Term
- 当发现更大的 Term 时，节点更新自己的 Term 并退回 Follower 状态

## Leader 选举

### 选举流程

1. **初始化**：所有节点启动时都是 Follower
2. **超时触发**：如果 Follower 在超时时间内（150-300ms 随机）未收到心跳，转变为 Candidate
3. **发起选举**：
   - 增加当前 Term
   - 投票给自己
   - 向所有其他节点发送 RequestVote RPC
4. **选举结果**：
   - **获得多数投票**：成为 Leader，开始发送心跳
   - **收到更大 Term 的 Leader**：退回 Follower 状态
   - **超时无人胜出**：增加 Term，重新发起选举

### 选举安全性

- 每个节点在每个 Term 最多投一票
- 使用随机超时时间避免选票分裂
- 获得多数票的 Candidate 才能成为 Leader

## 日志复制

### 日志结构

每条日志包含：
- **Term**：创建该日志时的任期
- **Index**：日志在日志数组中的位置
- **Command**：状态机要执行的命令

### 复制流程

1. **客户端发送请求到 Leader**
2. **Leader 将日志追加到本地日志**
3. **Leader 向所有 Follower 发送 AppendEntries RPC**
4. **Follower 将日志追加到本地日志**
5. **当 Leader 收到多数 Follower 的确认后**：
   - 标记该日志为已提交（Committed）
   - 应用到状态机
   - 返回结果给客户端
6. **Leader 在下次心跳时通知 Follower 提交**

### 日志一致性保证

Raft 保证以下日志性质：

1. **日志匹配**：如果两个日志的条目具有相同的 Index 和 Term，那么该条目之前的所有条目都相同
2. **Leader 完整性**：如果某个日志在某个 Term 被提交，那么该日志将出现在所有更高 Term 的 Leader 的日志中

## 安全性

### 选举限制

Raft 增加了一个选举限制：**只有拥有所有已提交日志的 Candidate 才能赢得选举**。

实现方式：
- RequestVote RPC 包含 Candidate 的最后日志 Index 和 Term
- Voter 比较自己的日志与 Candidate 的日志
- 如果 Voter 的日志更新，拒绝投票

### 日志比较规则

日志的新旧比较：
1. 比较最后一条日志的 Term，Term 大的日志更新
2. 如果 Term 相同，Index 大的日志更新

## 成员变更

### 问题

直接从旧配置切换到新配置可能导致两个 Leader 同时存在（脑裂）。

### 解决方案：两阶段成员变更

1. **第一阶段**：切换到过渡配置（旧配置 ∪ 新配置）
2. **第二阶段**：从过渡配置切换到新配置

### 单阶段成员变更（改进版）

现代 Raft 实现通常使用单阶段成员变更：
- 一次只变更一个节点
- 使用特殊的日志条目记录配置变更
- 在配置变更期间禁止 Leader 选举

## Raft 与 Paxos 的对比

| 特性 | Paxos | Raft |
|------|-------|------|
| 理解难度 | 高 | 低 |
| 角色 | Proposer, Acceptor, Learner | Leader, Follower, Candidate |
| 日志复制 | 多阶段 | Leader 主导 |
| 实现复杂度 | 高 | 低 |
| 性能 | 类似 | 类似 |
| 应用场景 | Google Chubby | etcd, Consul |

## Raft 的实际应用

- **etcd**：Kubernetes 的核心配置存储
- **Consul**：服务发现和配置管理
- **TiDB PD**：分布式数据库的元数据管理
- **RocksDB**：分布式存储引擎

## 总结

Raft 通过清晰的角色划分和简化的流程，提供了一种易于理解和实现的共识算法。它在保证强一致性的同时，具有良好的性能和容错能力，是现代分布式系统的核心组件之一。
