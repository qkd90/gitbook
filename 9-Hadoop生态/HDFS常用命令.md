# HDFS 常用命令

## HDFS 命令基本格式

```bash
hdfs dfs -cmd <args>
# 或
hadoop fs -cmd <args>
```

## 文件操作命令

### 1. 查看目录

```bash
# 查看根目录
hdfs dfs -ls /

# 递归查看
hdfs dfs -ls -R /

# 查看指定目录
hdfs dfs -ls /user/hadoop
```

### 2. 创建目录

```bash
# 创建单级目录
hdfs dfs -mkdir /test

# 创建多级目录
hdfs dfs -mkdir -p /test/sub1/sub2
```

### 3. 上传文件

```bash
# 从本地上传文件
hdfs dfs -put localfile.txt /hdfs/path/

# 从本地移动文件（上传后删除本地文件）
hdfs dfs -moveFromLocal localfile.txt /hdfs/path/

# 追加内容到文件
hdfs dfs -appendToFile local.txt /hdfs/file.txt
```

### 4. 下载文件

```bash
# 下载文件到本地
hdfs dfs -get /hdfs/path/file.txt ./localdir/

# 合并下载多个文件
hdfs dfs -getmerge /hdfs/dir/ local_merged.txt
```

### 5. 查看文件内容

```bash
# 查看文件内容
hdfs dfs -cat /path/to/file

# 查看文件尾部
hdfs dfs -tail /path/to/file
```

### 6. 删除操作

```bash
# 删除文件
hdfs dfs -rm /path/to/file

# 删除目录
hdfs dfs -rm -r /path/to/dir

# 清空回收站
hdfs dfs -expunge
```

### 7. 复制和移动

```bash
# HDFS 内复制
hdfs dfs -cp /src/path /dest/path

# HDFS 内移动
hdfs dfs -mv /src/path /dest/path
```

### 8. 统计信息

```bash
# 统计文件大小
hdfs dfs -du -s /path/to/dir

# 统计文件数量
hdfs dfs -count /path/to/dir
```

### 9. 权限管理

```bash
# 修改文件权限
hdfs dfs -chmod 755 /path/to/file

# 修改文件所有者
hdfs dfs -chown hadoop:hadoop /path/to/file
```

## 管理命令

### 1. NameNode 管理

```bash
# 安全模式
hdfs dfsadmin -safemode get    # 查看状态
hdfs dfsadmin -safemode enter  # 进入
hdfs dfsadmin -safemode leave  # 离开
hdfs dfsadmin -safemode wait   # 等待

# 报表
hdfs dfsadmin -report          # 集群报告
```

### 2. 文件系统检查

```bash
# 检查文件系统
hdfs fsck /

# 检查特定路径
hdfs fsck /user/hadoop -files -blocks
```

### 3. 升级与回滚

```bash
# 升级 NameNode
hdfs namenode -upgrade

# 回滚
hdfs namenode -rollback
```

## 实际应用场景

### 1. 日志收集

```bash
# 创建日志目录
hdfs dfs -mkdir -p /logs/app/$(date +%Y%m%d)

# 上传日志文件
hdfs dfs -put /var/log/app/*.log /logs/app/$(date +%Y%m%d)/
```

### 2. 数据备份

```bash
# 备份重要数据
hdfs dfs -cp /data/important /data/backup/$(date +%Y%m%d)
```

### 3. 数据清理

```bash
# 删除 7 天前的日志
hdfs dfs -find /logs -name "*.log" -mtime +7 -exec hdfs dfs -rm {} \;
```

## 总结

HDFS 命令与 Linux 命令非常相似，掌握这些常用命令可以高效地管理 HDFS 中的数据。
