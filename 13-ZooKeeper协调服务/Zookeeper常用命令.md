# ZooKeeper 常用命令

## 服务端命令

```bash
# 启动
bin/zkServer.sh start

# 停止
bin/zkServer.sh stop

# 重启
bin/zkServer.sh restart

# 查看状态
bin/zkServer.sh status

# 查看模式
bin/zkServer.sh print-cmd
```

## 客户端命令

### 连接

```bash
# 连接本地
bin/zkCli.sh

# 连接远程
bin/zkCli.sh -server hadoop102:2181
```

### 节点操作

```bash
# 创建节点
create /path [data] [acl] [mode]
create /test "hello"
create -s /seq "data"  # 顺序节点
create -e /ephemeral "data"  # 临时节点

# 查看节点
ls /
ls -R /  # 递归查看

# 获取节点数据
get /test

# 设置节点数据
set /test "new data"

# 删除节点
delete /test
deleteall /path  # 递归删除

# 查看状态
stat /test
```

### Watcher 命令

```bash
# 监听数据变化
get /test watch

# 监听子节点变化
ls /test watch
```

### 配额命令

```bash
# 设置配额
setquota -n 10 /path  # 子节点数限制
setquota -b 1024 /path  # 数据长度限制

# 查看配额
listquota /path

# 删除配额
delquota -n /path
delquota -b /path
```

## 四字命令

```bash
# 查看状态
echo stat | nc localhost 2181

# 查看配置
echo conf | nc localhost 2181

# 查看连接
echo cons | nc localhost 2181

# 查看监控
echo mntr | nc localhost 2181

# 退出
echo ruok | nc localhost 2181
```

## 总结

掌握 ZooKeeper 的常用命令是日常运维的基础。
