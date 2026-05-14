# ZooKeeper 简介及核心概念

## ZooKeeper 是什么

Apache ZooKeeper 是一个分布式协调服务，为分布式应用提供配置管理、命名服务、分布式锁等功能。

**核心特点**：
- **层次命名空间**：类似文件系统的树形结构
- **高可用**：集群模式保证服务可用
- **顺序访问**：支持顺序节点
- **Watcher 机制**：数据变化时通知客户端

## 数据模型

ZooKeeper 的数据模型是树形结构，每个节点称为 ZNode。

```
/
├── zookeeper
├── config
│   ├── db_config
│   └── app_config
├── locks
│   └── lock_0001
└── services
    ├── service_a
    └── service_b
```

## ZNode 类型

### 1. 持久节点（PERSISTENT）

创建后一直存在，直到主动删除。

```java
zk.create("/my_node", data, acl, CreateMode.PERSISTENT);
```

### 2. 持久顺序节点（PERSISTENT_SEQUENTIAL）

自动附加递增序号。

```java
zk.create("/my_node_", data, acl, CreateMode.PERSISTENT_SEQUENTIAL);
// 结果: /my_node_0000000001
```

### 3. 临时节点（EPHEMERAL）

客户端断开后自动删除。

```java
zk.create("/my_node", data, acl, CreateMode.EPHEMERAL);
```

### 4. 临时顺序节点（EPHEMERAL_SEQUENTIAL）

临时节点 + 顺序节点。

```java
zk.create("/my_node_", data, acl, CreateMode.EPHEMERAL_SEQUENTIAL);
```

## Watcher 机制

Watcher 是 ZooKeeper 的通知机制，当 ZNode 发生变化时通知客户端。

```java
// 注册 Watcher
byte[] data = zk.getData("/my_node", watchedEvent -> {
    System.out.println("节点变化: " + watchedEvent.getType());
}, null);

// 永久 Watcher（Curator）
client.getData().watched().forPath("/my_node");
```

## ACL 权限控制

ZooKeeper 使用 ACL 控制节点访问权限。

**权限**：
- **CREATE**：创建子节点
- **READ**：读取节点数据和子节点列表
- **WRITE**：设置节点数据
- **DELETE**：删除子节点
- **ADMIN**：设置 ACL

**Scheme**：
- **world**：所有人
- **auth**：认证用户
- **digest**：用户名+密码
- **ip**：IP 地址

```java
// 设置 ACL
List<ACL> acls = new ArrayList<>();
Id id = new Id("digest", DigestAuthenticationProvider.generateDigest("user:password"));
acls.add(new ACL(ZooDefs.Perms.ALL, id));
zk.create("/secure_node", data, acls, CreateMode.PERSISTENT);
```

## 总结

ZooKeeper 是分布式系统的核心协调服务，理解其数据模型和机制是使用 ZooKeeper 的基础。
