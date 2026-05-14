# 分布式 ID 生成方案

## 为什么需要分布式 ID

在分布式系统中，我们需要为数据生成全局唯一的 ID。传统的关系型数据库使用自增 ID，但在分布式环境下存在以下问题：

1. **分库分表**：不同表的自增 ID 会重复
2. **数据合并**：不同数据库的 ID 可能冲突
3. **性能瓶颈**：单点自增 ID 生成可能成为瓶颈

## 分布式 ID 的要求

1. **全局唯一**：任何时刻都不能有重复 ID
2. **单调递增**：ID 应该按时间顺序递增
3. **高性能**：生成 ID 的延迟应该尽可能低
4. **高可用**：ID 生成服务不能单点故障
5. **信息安全**：ID 不应该泄露业务信息

## 方案一：UUID

### 实现

```java
String uuid = UUID.randomUUID().toString();
// 输出：550e8400-e29b-41d4-a716-446655440000
```

### 优点

- 实现简单
- 性能极高
- 去中心化

### 缺点

- 长度过长（36 字符）
- 无序，不利于索引
- 不单调，B+ 树索引会频繁分裂
- 可读性差

### 适用场景

日志 ID、临时令牌、不需要排序的场景

## 方案二：数据库自增 ID

### 实现

使用单独的数据库实例专门生成 ID：

```sql
CREATE TABLE id_generator (
    id BIGINT AUTO_INCREMENT PRIMARY KEY
);

-- 每次需要 ID 时插入并获取
INSERT INTO id_generator VALUES (NULL);
SELECT LAST_INSERT_ID();
```

### 多机方案

设置不同的起始值和步长：

- 机器 A：起始值 1，步长 2 → 1, 3, 5, 7...
- 机器 B：起始值 2，步长 2 → 2, 4, 6, 8...

### 优点

- 简单可靠
- 单调递增
- 数字类型，存储高效

### 缺点

- 性能受数据库限制
- 写入压力大
- 可用性依赖数据库

### 适用场景

小规模系统，对性能要求不高

## 方案三：Redis 生成

### 实现

利用 Redis 的原子操作：

```java
// INCR 命令
Long id = redisTemplate.opsForValue().increment("id:generator");

// 批量获取，减少网络调用
List<Long> ids = new ArrayList<>();
for (int i = 0; i < 100; i++) {
    ids.add(redisTemplate.opsForValue().increment("id:generator"));
}
```

### 优点

- 性能高（10w+/s）
- 单调递增
- 实现简单

### 缺点

- 依赖 Redis
- 需要处理 Redis 故障
- ID 可能重复（Redis 重启后）

### 适用场景

已有 Redis 基础设施的系统

## 方案四：号段模式

### 实现原理

从数据库批量获取 ID 段，缓存在应用内存中：

1. 应用请求数据库获取一段 ID（如 1-1000）
2. 应用在内存中依次使用这些 ID
3. 当 ID 用完时，再次请求下一段

```sql
-- ID 段表
CREATE TABLE id_segment (
    tag VARCHAR(64) PRIMARY KEY,  -- 业务标识
    max_id BIGINT,                -- 当前最大 ID
    step INT,                     -- 步长
    update_time TIMESTAMP
);

-- 更新并获取新段
UPDATE id_segment 
SET max_id = max_id + step 
WHERE tag = 'order';
```

### 优点

- 性能极高（内存操作）
- 对数据库压力小
- ID 单调递增

### 缺点

- 应用故障可能浪费 ID
- 需要处理多实例竞争

### 实现：Leaf（美团）

美团开源的 Leaf 支持号段模式和雪花模式。

## 方案五：雪花算法（Snowflake）

### 算法原理

Snowflake 是 Twitter 开源的分布式 ID 生成算法，生成 64 位整数 ID：

```
| 1 bit 符号位 | 41 bit 时间戳 | 10 bit 机器 ID | 12 bit 序列号 |
```

- **符号位（1 bit）**：始终为 0，表示正数
- **时间戳（41 bit）**：毫秒级，可用约 69 年
- **机器 ID（10 bit）**：最多支持 1024 个节点
- **序列号（12 bit）**：同一毫秒内最多生成 4096 个 ID

### Java 实现

```java
public class SnowflakeIdGenerator {
    private final long twepoch = 1288834974657L; // 2010-11-04
    private final long workerIdBits = 5L;
    private final long datacenterIdBits = 5L;
    private final long maxWorkerId = -1L ^ (-1L << workerIdBits);
    private final long maxDatacenterId = -1L ^ (-1L << datacenterIdBits);
    private final long sequenceBits = 12L;
    private final long workerIdShift = sequenceBits;
    private final long datacenterIdShift = sequenceBits + workerIdBits;
    private final long timestampLeftShift = sequenceBits + workerIdBits + datacenterIdBits;
    private final long sequenceMask = -1L ^ (-1L << sequenceBits);

    private long workerId;
    private long datacenterId;
    private long sequence = 0L;
    private long lastTimestamp = -1L;

    public SnowflakeIdGenerator(long workerId, long datacenterId) {
        if (workerId > maxWorkerId || workerId < 0) {
            throw new IllegalArgumentException("Invalid worker ID");
        }
        if (datacenterId > maxDatacenterId || datacenterId < 0) {
            throw new IllegalArgumentException("Invalid datacenter ID");
        }
        this.workerId = workerId;
        this.datacenterId = datacenterId;
    }

    public synchronized long nextId() {
        long timestamp = timeGen();
        if (timestamp < lastTimestamp) {
            throw new RuntimeException("Clock moved backwards");
        }
        if (lastTimestamp == timestamp) {
            sequence = (sequence + 1) & sequenceMask;
            if (sequence == 0) {
                timestamp = tilNextMillis(lastTimestamp);
            }
        } else {
            sequence = 0L;
        }
        lastTimestamp = timestamp;
        return ((timestamp - twepoch) << timestampLeftShift) |
               (datacenterId << datacenterIdShift) |
               (workerId << workerIdShift) |
               sequence;
    }

    private long tilNextMillis(long lastTimestamp) {
        long timestamp = timeGen();
        while (timestamp <= lastTimestamp) {
            timestamp = timeGen();
        }
        return timestamp;
    }

    private long timeGen() {
        return System.currentTimeMillis();
    }
}
```

### 优点

- 性能高（单机 10w+/s）
- ID 单调递增
- 去中心化
- 不依赖外部系统

### 缺点

- 依赖系统时钟（时钟回拨会导致重复 ID）
- 机器 ID 分配需要管理
- 64 位可能在极端场景下不够用

### 时钟回拨问题

**问题**：系统时钟回拨会导致生成重复 ID。

**解决方案**：
1. 容忍小幅度回拨（等待时钟追上）
2. 记录上次时间戳，回拨时拒绝服务
3. 使用扩展的时间戳方案

## 方案对比

| 特性 | UUID | 数据库自增 | Redis | 号段模式 | 雪花算法 |
|------|------|-----------|-------|---------|---------|
| 唯一性 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 单调递增 | ✗ | ✓ | ✓ | ✓ | ✓ |
| 性能 | 高 | 低 | 高 | 极高 | 极高 |
| 可用性 | 极高 | 中 | 中 | 高 | 高 |
| 实现复杂度 | 低 | 低 | 低 | 中 | 中 |
| 依赖外部 | 无 | 数据库 | Redis | 数据库 | 时钟 |

## 实际应用建议

1. **小项目**：数据库自增或 Redis
2. **中型项目**：号段模式（Leaf）
3. **大型项目**：雪花算法或号段模式
4. **需要无序 ID**：UUID
5. **需要可读性**：考虑使用短 ID 或 Base62 编码

## 总结

分布式 ID 生成方案的选择取决于项目的规模、性能要求和基础设施。雪花算法是最常用的方案，但需要注意时钟回拨问题。号段模式在性能和可靠性之间取得了良好的平衡，适合大多数场景。
