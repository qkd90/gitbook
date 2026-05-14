# ZooKeeper Java 客户端

## 原生 API

### 连接

```java
ZooKeeper zk = new ZooKeeper("localhost:2181", 3000, watchedEvent -> {
    System.out.println("事件: " + watchedEvent.getType());
});
```

### 节点操作

```java
// 创建
String path = zk.create("/test", "data".getBytes(),
    ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);

// 读取
byte[] data = zk.getData("/test", false, null);
Stat stat = new Stat();
data = zk.getData("/test", false, stat);

// 更新
Stat newStat = zk.setData("/test", "new data".getBytes(), stat.getVersion());

// 删除
zk.delete("/test", stat.getVersion());

// 子节点
List<String> children = zk.getChildren("/test", false);

// 检查存在
boolean exists = zk.exists("/test", false);
```

### Watcher

```java
zk.getData("/test", event -> {
    System.out.println("节点变化: " + event.getType());
}, null);
```

## Curator 框架

Curator 是 Apache 提供的 ZooKeeper 客户端，封装了常见操作。

### Maven 依赖

```xml
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-framework</artifactId>
    <version>5.X.X</version>
</dependency>
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-recipes</artifactId>
    <version>5.X.X</version>
</dependency>
```

### 连接

```java
CuratorFramework client = CuratorFrameworkFactory.newClient(
    "localhost:2181",
    new ExponentialBackoffRetry(1000, 3));
client.start();
```

### 节点操作

```java
// 创建
client.create().forPath("/test", "data".getBytes());
client.create().creatingParentsIfNeeded().forPath("/a/b/c");

// 读取
byte[] data = client.getData().forPath("/test");

// 更新
client.setData().forPath("/test", "new data".getBytes());

// 删除
client.delete().deletingChildrenIfNeeded().forPath("/test");

// 子节点
List<String> children = client.getChildren().forPath("/test");
```

### Watcher

```java
// NodeCache
NodeCache cache = new NodeCache(client, "/test");
cache.getListenable().addListener(() -> {
    ChildData data = cache.getCurrentData();
    if (data != null) {
        System.out.println("数据: " + new String(data.getData()));
    }
});
cache.start();

// PathChildrenCache
PathChildrenCache pathCache = new PathChildrenCache(client, "/test", true);
pathCache.getListenable().addListener((client, event) -> {
    System.out.println("事件: " + event.getType());
});
pathCache.start();
```

### 分布式锁

```java
InterProcessMutex lock = new InterProcessMutex(client, "/locks/my_lock");

lock.acquire();
try {
    // 临界区
} finally {
    lock.release();
}
```

### Leader 选举

```java
LeaderSelector selector = new LeaderSelector(client, "/leader", new LeaderSelectorListenerAdapter() {
    public void takeLeadership(CuratorFramework client) throws Exception {
        System.out.println("我是 Leader");
        // Leader 逻辑
    }
});
selector.autoRequeue();
selector.start();
```

## 总结

推荐使用 Curator 框架，它提供了更高级的抽象和自动重试机制。
