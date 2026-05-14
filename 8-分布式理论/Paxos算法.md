# Paxos 算法

## Paxos 简介

Paxos 是由 Leslie Lamport 在 1990 年提出的一种基于消息传递的分布式一致性算法。它是分布式系统中最著名的共识算法之一，被广泛应用于各种分布式系统中。

Paxos 解决的问题是：在可能发生消息丢失、重复、延迟的不可靠网络环境中，如何让多个节点就某个值达成一致。

## Paxos 的角色

Paxos 算法中有三种角色：

1. **Proposer（提议者）**：提出提案（Proposal），包括提案编号（Proposal ID）和提案值（Value）
2. **Acceptor（接受者）**：对提案进行投票，决定是否接受该提案
3. **Learner（学习者）**：学习被选中的提案值

> 注：在实际系统中，一个节点可以同时担任多个角色。

## Paxos 的两阶段协议

### 第一阶段：Prepare（准备阶段）

1. **Proposer 选择提案编号 n，向超过半数的 Acceptor 发送 Prepare(n) 请求**
2. **Acceptor 收到 Prepare(n) 后的响应规则**：
   - 如果 n > 任何已响应的 Prepare 请求编号，Acceptor 响应：
     - 承诺不再接受编号小于 n 的提案
     - 返回已经接受过的编号最大的提案（如果有）
   - 否则，拒绝该请求

### 第二阶段：Accept（接受阶段）

1. **Proposer 收到超过半数的 Acceptor 响应后**：
   - 如果任何 Acceptor 返回了已接受的提案，使用其中编号最大的提案值
   - 否则，Proposer 使用自己的提案值
   - 向这些 Acceptor 发送 Accept(n, value) 请求

2. **Acceptor 收到 Accept(n, value) 后的响应规则**：
   - 如果 n >= 任何已响应的 Prepare 请求编号，接受该提案
   - 否则，拒绝该提案

3. **Learner 学习被批准的提案**：
   - 当提案被超过半数的 Acceptor 接受后，该提案被批准
   - Learner 需要获取被批准的提案值

## Paxos 示例

假设有 5 个 Acceptor（A1-A5），两个 Proposer（P1, P2）：

### 场景 1：无冲突
```
P1: Prepare(1) → A1, A2, A3
    ← Promise(1, null)  (A1, A2, A3 都未接受过提案)
P1: Accept(1, "X") → A1, A2, A3
    ← Accepted(1, "X")  (超过半数接受，提案通过)
```

### 场景 2：冲突解决
```
P1: Prepare(1) → A1, A2
P2: Prepare(2) → A3, A4, A5
    ← Promise(2, null)  (P2 获得多数)
P2: Accept(2, "Y") → A3, A4, A5
    ← Accepted(2, "Y")  (P2 的提案先通过)

P1: Prepare(1) → A1, A2
    ← Promise(1, null)  (P1 也获得多数，但编号小)
P1: Accept(1, "X") → A1, A2
    ← Rejected  (A1, A2 已经承诺不响应编号<2的提案)
```

## Paxos 的核心思想

### 1. 提案编号的唯一性
每个提案必须有唯一的编号，通常使用 `(节点ID, 计数器)` 组合保证。

### 2. 多数派原则
只要超过半数的 Acceptor 接受了某个提案，该提案就被批准。这保证了：
- 任何两个多数派集合必有交集
- 如果某个提案被批准，后续的提案必须使用该值

### 3. 值的选择约束
如果编号小于 n 的某个提案已经被批准，那么编号为 n 的提案必须使用该值。这通过 Prepare 阶段返回已接受的提案来实现。

## Multi-Paxos

Basic Paxos 只能就单个值达成一致。在实际应用中，通常需要就一系列值达成一致（如日志条目）。

**Multi-Paxos 的优化**：
1. **跳过 Prepare 阶段**：如果只有一个 Proposer，后续提案可以跳过 Prepare 阶段
2. **Leader 选举**：选举一个 Leader 作为唯一的 Proposer，避免冲突

## Paxos 的优缺点

### 优点
- 理论严谨，正确性可证明
- 能够容忍节点故障（最多容忍 (N-1)/2 个故障）
- 保证强一致性

### 缺点
- 理解复杂，难以实现
- 两阶段提交，延迟较高
- 活锁问题：多个 Proposer 可能反复冲突

## 实际应用场景

- Google Chubby 分布式锁服务
- 分布式数据库的元数据管理
- 配置中心的数据同步

## 总结

Paxos 是分布式一致性算法的里程碑，虽然理解难度大，但其思想深刻影响了后续的共识算法（如 Raft）。在实际工程中，通常使用基于 Paxos 的优化版本或其衍生算法（如 Multi-Paxos、Fast Paxos）。
