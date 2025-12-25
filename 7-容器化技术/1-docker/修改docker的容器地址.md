# 修改docker的容器地址

**如果你还想从头学起 Docker，可以看看这个系列的文章哦！**

https://www.cnblogs.com/poloyy/category/1870863.html

 

## 问题背景

```
 docker run -d -p 9999:8080 -i --name tomcat7 -v /usr/local/webapps:/usr/local/tomcat/webapps tomcat:7
```

- 创建容器时，指定了目录映射（-v）
- 如果容器运行之后发现目录映射需要改怎么办？

 

## 删除原有容器，重新创建新的容器

### 删除容器

```
docker rm -f 容器ID/名字
```

 

### 重新创建容器

```
 docker run -d -p 9999:8080 -i --name tomcat7 -v /usr/local/tomcat/webapps:/usr/local/tomcat/webapps tomcat:7
```

重新指定需要映射的目录

 

### 优点

简单粗暴，在测试环境用的更多

 

### 缺点

如果是数据库、服务器相关的容器，创建新的容器，又得重新配置相关东西了

 

## 修改容器配置文件（重点）

### 暂停 Docker 服务

```
systemctl stop docker
```

 

### 进入 Docker 容器配置文件目录下

```
cd /var/lib/docker/containers/ls
```

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201116193321478-1197771523.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201116193321478-1197771523.png)

 

### 进入某个容器的配置文件目录下

容器ID 就是文件夹名称，可通过 docker ps -aq 来查看，不过这是缩写，对照起来看就行

```
cd c614b6db4aed0c8d0c742baa09ff4e2c24761703586460b68633d7b66e62c633ls
```

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201116193439573-1745444526.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201116193439573-1745444526.png)

 

### 修改 config.v2.json

```
vim config.v2.json
```

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117132817621-1524291359.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117132817621-1524291359.png)

- 输入 / ，搜索映射的目录（webapps）
- 也可以找到 MountPoints 
- 若需要重新指定**主机上**的映射目录，则改**绿圈**的两个地方
- 若需要重新指定**容器上**的映射目录，则改**蓝圈**的两个地方

####  

#### MountPoints 节点

其实是一个 json 结构的数据，下图

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117133321919-1553115152.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117133321919-1553115152.png)

 

### 重新启动 Docker 服务

```
systemctl stop dockerdocker start tomcat7cd /usr/local/tomcat/webappsls
```

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117134652784-1402922780.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117134652784-1402922780.png)

重新映射目录成功！！

 

### 注意

- 如果想修改 Docker 容器随着 Docker 服务启动而自启动，可看：https://www.cnblogs.com/poloyy/p/13985567.html
- 如果想修改 Docker 的映射端口，可看：https://www.cnblogs.com/poloyy/p/13940554.html
- 改 hostconfig.json 并不会成功哦

 

### 优点

直接操作配置文件没有副作用，算简单

 

### 缺点

需要暂停 Docker 服务，会影响其他正常运行的 Docker 容器

 

## 使用 docker commit 命令

### 停止 Docker 容器

```
docker stop tomcat7
```

 

### 使用 commit 构建新镜像

```
docker commit tomcat7 new_tomcat7docker images
```

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117104809476-1592000641.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117104809476-1592000641.png)

 

### 使用新镜像重新创建一个 Docker 容器

```
 docker run -d -p 9999:8080 -i --name tomcat77 -v /usr/local/tomcat/webapps:/usr/local/tomcat/webapps tomcat:7
```

 

### 修改新容器的名字

如果新容器想用回旧容器的名字，需要先删了旧容器，再改名

```
docker rm -f tomcat7
docker rename tomcat77 tomcat7
docker ps
```

[![img](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117104824581-229417393.png)](https://img2020.cnblogs.com/blog/1896874/202011/1896874-20201117104824581-229417393.png)

 

### 优点

- 无需停止 Docker 服务，不影响其他正在运行的容器
- 旧容器有的配置和数据，新容器也会有，不会造成数据或配置丢失，对新旧容器都没有任何影响

 

### 缺点

需要生成新的镜像和容器，管理镜像和容器的时间成本会上升