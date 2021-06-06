### prometheus配套的各个数据库监控部署

#### 1.mongodb

#### 2.kafka

##### 1.1在linux搭建一套kafka+zookeeper环境：

###### 1.1.1 zookeeper

- 拉取镜像

```
docker pull zookeeper
```

默认是摘取最新版本 **zookeeper:latest**。

- 查看当前镜像

```
docker images
```

-  准备工作

将它部署在 /usr/local/zookeeper 目录下：

```
cd /usr/local && mkdir zookeeper && cd zookeeper
```

创建data目录，用于挂载容器中的数据目录：

```
mkdir data
```

![img](https://img2018.cnblogs.com/i-beta/1577453/202002/1577453-20200218110633631-1450938810.png)

- 正式部署

- 部署命令：

```
docker run -d -e TZ="Asia/Shanghai" -p 2181:2181 -v $PWD/data:/data --name zookeeper --restart always zookeeper
```

- 命令详细说明：

```
-e TZ="Asia/Shanghai" # 指定上海时区 
-d # 表示在一直在后台运行容器
-p 2181:2181 # 对端口进行映射，将本地2181端口映射到容器内部的2181端口
--name # 设置创建的容器名称
-v # 将本地目录(文件)挂载到容器指定目录；--restart always #始终重新启动zookeeper
```

- **查看容器启动情况：**

```
docker ps -a
```

![img](https://img2018.cnblogs.com/i-beta/1577453/202002/1577453-20200218111223382-266770946.png)

注：状态（STATUS）为Up，说明容器已经启动成功。

- 测试

- 使用zk命令行客户端连接zk

```
docker run -it --rm --link zookeeper:zookeeper zookeeper zkCli.sh -server zookeeper
```

说明：`-server zookeeper`是启动`zkCli.sh`的参数

![img](https://img2018.cnblogs.com/i-beta/1577453/202002/1577453-20200218111608512-516451599.png)

![img](https://img2018.cnblogs.com/i-beta/1577453/202002/1577453-20200218111735060-225718424.png)

- 其它命令

```
# 查看zookeeper容器实例进程信息
docker top zookeeper

# 停止zookeeper实例进程
docker stop zookeeper

# 启动zookeeper实例进程
docker start zookeeper

# 重启zookeeper实例进程
docker restart zookeeper

# 查看zookeeper进程日志
docker logs -f zookeeper

# 杀死zookeeper实例进程
docker kill -s KILL zookeeper

# 移除zookeeper实例
docker rm -f -v zookeeper
```

