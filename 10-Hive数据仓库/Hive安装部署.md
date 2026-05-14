# Hive 安装部署

## 环境准备

### 前置条件

1. **Java**：JDK 1.8+
2. **Hadoop**：Hadoop 2.x 或 3.x
3. **数据库**：MySQL 5.7+（用于 Metastore）

## 安装步骤

### 1. 下载并解压

```bash
tar -zxvf apache-hive-3.1.X-bin.tar.gz -C /opt/module/
```

### 2. 配置环境变量

```bash
sudo vi /etc/profile
```

添加：
```bash
export HIVE_HOME=/opt/module/apache-hive-3.1.X-bin
export PATH=$PATH:$HIVE_HOME/bin
```

```bash
source /etc/profile
hive --version
```

### 3. 配置 MySQL Metastore

**安装 MySQL**：
```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

**创建 Hive 数据库和用户**：
```sql
CREATE DATABASE metastore;
CREATE USER 'hive'@'%' IDENTIFIED BY 'hive_password';
GRANT ALL PRIVILEGES ON metastore.* TO 'hive'@'%';
FLUSH PRIVILEGES;
```

**下载 MySQL JDBC 驱动**：
```bash
cp mysql-connector-java-8.0.XX.jar $HIVE_HOME/lib/
```

### 4. 配置 Hive

**创建配置文件**：
```bash
cd $HIVE_HOME/conf
cp hive-env.sh.template hive-env.sh
cp hive-default.xml.template hive-site.xml
cp hive-log4j2.properties.template hive-log4j2.properties
```

**配置 hive-env.sh**：
```bash
export HADOOP_HOME=/opt/module/hadoop-3.X.X
export HIVE_CONF_DIR=/opt/module/apache-hive-3.1.X-bin/conf
export HIVE_AUX_JARS_PATH=/opt/module/apache-hive-3.1.X-bin/lib
```

**配置 hive-site.xml**：
```xml
<configuration>
    <!-- JDBC 连接 URL -->
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://localhost:3306/metastore?useSSL=false&amp;serverTimezone=UTC</value>
    </property>

    <!-- JDBC 驱动 -->
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.cj.jdbc.Driver</value>
    </property>

    <!-- 数据库用户名 -->
    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>hive</value>
    </property>

    <!-- 数据库密码 -->
    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>hive_password</value>
    </property>

    <!-- Hive 数据临时目录 -->
    <property>
        <name>hive.exec.scratchdir</name>
        <value>/tmp/hive</value>
    </property>

    <!-- Metastore 仓库目录 -->
    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>/user/hive/warehouse</value>
    </property>

    <!-- Metastore 自动创建表 -->
    <property>
        <name>hive.metastore.schema.verification</name>
        <value>false</value>
    </property>
</configuration>
```

### 5. 初始化 Metastore

```bash
# 初始化数据库
schematool -dbType mysql -initSchema

# 验证
schematool -dbType mysql -info
```

### 6. 创建 HDFS 目录

```bash
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -mkdir -p /tmp/hive
hdfs dfs -chmod g+w /user/hive/warehouse
hdfs dfs -chmod g+w /tmp/hive
```

### 7. 解决依赖冲突

```bash
# 删除冲突的日志包
rm $HIVE_HOME/lib/log4j-slf4j-impl-*.jar

# 复制 Hadoop 的包
cp $HADOOP_HOME/share/hadoop/common/lib/guava-XX.X.jar $HIVE_HOME/lib/
```

## 启动 Hive

### 1. 启动 Metastore 服务

```bash
nohup hive --service metastore &
```

### 2. 启动 HiveServer2

```bash
nohup hiveserver2 &
```

### 3. 使用 CLI 连接

```bash
# 本地模式
hive

# 远程模式（通过 JDBC）
beeline -u jdbc:hive2://localhost:10000 -n hadoop
```

### 4. 测试

```sql
-- 创建数据库
CREATE DATABASE test_db;

-- 使用数据库
USE test_db;

-- 创建表
CREATE TABLE test_table (
    id INT,
    name STRING
) ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';

-- 插入数据
INSERT INTO test_table VALUES (1, 'Alice'), (2, 'Bob');

-- 查询
SELECT * FROM test_table;
```

## 常见问题

### 1. 元数据初始化失败

- 检查 MySQL 是否启动
- 检查 JDBC 驱动是否在 classpath 中
- 检查数据库权限

### 2. HiveServer2 无法启动

- 检查端口 10000 是否被占用
- 查看日志：`/tmp/$USER/hive.log`

### 3. 权限问题

- 确保 HDFS 目录有正确的权限
- 设置 `hive.exec.scratchdir` 权限

## 总结

Hive 的安装主要包括环境准备、Metastore 配置和服务启动。正确配置 MySQL Metastore 是确保 Hive 正常运行的关键。
