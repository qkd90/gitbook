# Hadoop 环境搭建

## Hadoop 的部署模式

Hadoop 有三种部署模式：

1. **本地模式（Standalone Mode）**：单进程，用于开发和测试
2. **伪分布式模式（Pseudo-Distributed Mode）**：单节点模拟集群
3. **完全分布式模式（Fully-Distributed Mode）**：多节点真实集群

## 环境准备

### 1. 系统要求

- 操作系统：Linux（CentOS 7+、Ubuntu 18.04+）
- Java：JDK 1.8+
- SSH：无密码登录

### 2. 安装 JDK

```bash
# 下载 JDK 并解压
tar -zxvf jdk-8uXXX-linux-x64.tar.gz -C /opt/module/

# 配置环境变量
sudo vi /etc/profile
```

添加以下内容：
```bash
export JAVA_HOME=/opt/module/jdk1.8.0_XXX
export PATH=$PATH:$JAVA_HOME/bin
```

使配置生效：
```bash
source /etc/profile
java -version
```

### 3. 配置 SSH 免密登录

```bash
# 生成密钥
ssh-keygen -t rsa

# 复制公钥到本机（伪分布式）或其他节点（完全分布式）
ssh-copy-id localhost
ssh-copy-id hadoop102
ssh-copy-id hadoop103
ssh-copy-id hadoop104

# 测试
ssh localhost
```

## 本地模式安装

### 1. 下载并解压 Hadoop

```bash
tar -zxvf hadoop-3.X.X.tar.gz -C /opt/module/
```

### 2. 配置环境变量

```bash
sudo vi /etc/profile
```

添加：
```bash
export HADOOP_HOME=/opt/module/hadoop-3.X.X
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

```bash
source /etc/profile
hadoop version
```

### 3. 测试

```bash
# 创建输入目录
mkdir input
cp etc/hadoop/*.xml input/

# 运行示例
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.X.X.jar \
    grep input output 'dfs[a-z.]+'

# 查看结果
cat output/*
```

## 伪分布式模式安装

### 1. 配置 core-site.xml

```xml
<configuration>
    <!-- 指定 HDFS 的地址 -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <!-- 指定 Hadoop 数据存储目录 -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/opt/module/hadoop-3.X.X/data/tmp</value>
    </property>
</configuration>
```

### 2. 配置 hdfs-site.xml

```xml
<configuration>
    <!-- 指定副本数 -->
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

### 3. 配置 yarn-site.xml

```xml
<configuration>
    <!-- 指定 Reducer 获取数据的方式 -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <!-- 指定 YARN 的 ResourceManager 地址 -->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>localhost</value>
    </property>
</configuration>
```

### 4. 配置 mapred-site.xml

```xml
<configuration>
    <!-- 指定 MapReduce 运行在 YARN 上 -->
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

### 5. 格式化 NameNode

```bash
hdfs namenode -format
```

> **注意**：格式化只需执行一次，重复格式化会导致集群 ID 不一致。

### 6. 启动集群

```bash
# 启动 HDFS
start-dfs.sh

# 启动 YARN
start-yarn.sh

# 或者一次性启动所有服务
start-all.sh
```

### 7. 验证

```bash
# 查看进程
jps

# 应该看到以下进程：
# NameNode
# DataNode
# SecondaryNameNode
# ResourceManager
# NodeManager
```

访问 Web UI：
- HDFS：http://localhost:9870
- YARN：http://localhost:8088

## 完全分布式模式安装

### 1. 集群规划

| 节点 | NameNode | DataNode | ResourceManager | NodeManager |
|------|----------|----------|-----------------|-------------|
| hadoop102 | ✓ | ✓ | - | ✓ |
| hadoop103 | - | ✓ | ✓ | ✓ |
| hadoop104 | - | ✓ | - | ✓ |

### 2. 配置 workers（或 slaves）

编辑 `etc/hadoop/workers`：

```
hadoop102
hadoop103
hadoop104
```

### 3. 配置 core-site.xml

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop102:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/opt/module/hadoop-3.X.X/data/tmp</value>
    </property>
</configuration>
```

### 4. 配置 hdfs-site.xml

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>hadoop104:9868</value>
    </property>
</configuration>
```

### 5. 配置 yarn-site.xml

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop103</value>
    </property>
</configuration>
```

### 6. 分发配置

```bash
# 使用 scp 或 rsync 将配置分发到其他节点
scp -r /opt/module/hadoop-3.X.X hadoop103:/opt/module/
scp -r /opt/module/hadoop-3.X.X hadoop104:/opt/module/
```

### 7. 格式化并启动

```bash
# 在 hadoop102 上格式化 NameNode
hdfs namenode -format

# 启动 HDFS
start-dfs.sh

# 在 hadoop103 上启动 YARN
start-yarn.sh
```

### 8. 群起脚本

配置 `start-dfs.sh` 和 `stop-dfs.sh` 中的用户：

```bash
# 在 sbin/start-dfs.sh 和 sbin/stop-dfs.sh 顶部添加
HDFS_DATANODE_USER=root
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
```

```bash
# 在 sbin/start-yarn.sh 和 sbin/stop-yarn.sh 顶部添加
YARN_RESOURCEMANAGER_USER=root
YARN_NODEMANAGER_USER=root
```

## 常见问题

### 1. NameNode 无法启动

- 检查是否已格式化
- 检查防火墙
- 查看日志：`logs/hadoop-*-namenode-*.log`

### 2. DataNode 无法连接 NameNode

- 检查 SSH 免密登录
- 检查 `workers` 文件
- 检查集群 ID 是否一致

### 3. 端口被占用

- 修改配置文件中的端口
- 或者关闭占用端口的进程

## 总结

Hadoop 的环境搭建虽然步骤较多，但遵循配置模板可以顺利完成。理解各个配置文件的作用有助于在实际运维中快速排查问题。
