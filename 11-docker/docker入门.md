# docker与微服务

## 基本操作

1.docker查看镜像

已经在运行的镜像

```
docker ps
```

全部镜像

```
docker ps -a
```

2.docker查看已经拉下来的镜像

```
docker images
```

3.更换docker配置，使用中国加速器

```
vim  /etc/docker/daemon.json
```

```
{
  "registry-mirrors" : [
    "https://14phm32t.mirror.aliyuncs.com",
    "http://registry.docker-cn.com",
    "http://docker.mirrors.ustc.edu.cn",
    "http://hub-mirror.c.163.com"
  ],
  "insecure-registries" : [
    "registry.docker-cn.com",
    "docker.mirrors.ustc.edu.cn",
    "192.168.18.105:5000"
  ],
  "debug" : true,
  "experimental" : true
}
```

4.进入docker容器

```
docker attach a2737a8fc891
```

5.重启docer容器

```
docker restart a2737a8fc891
```

6.删除docker容器

```
docker rm a2737a8fc891
```

## 清理操作

### 1.清理所有状态为 exited 的容器

```
docker rm $(docker ps -qf status=exited)
```

### 2.清理所有悬挂（<none>）镜像

```sh
docker image prune
# or
docker rmi $(docker images -qf "dangling=true")
```

### 3.清理所有无用数据卷：

```sh
docker volume prune
```

由于prune操作是批量删除类的危险操作，所以会有一次确认。 如果不想输入y来确认，可以添加-f操作。慎用！

### 4.清理停止的容器 

```sh
docker rm -lv CONTAINER
```

-l是清理link，v是清理volume。 这里的CONTAINER是容器的name或ID，可以是一个或多个。

参数列表：

| Name, shorthand | Default | Description                                             |
| --------------- | ------- | ------------------------------------------------------- |
| –force, -f      | false   | Force the removal of a running container (uses SIGKILL) |
| –link, -l       | false   | Remove the specified link                               |
| –volumes, -v    | false   | Remove the volumes associated with the container        |

### 清理所有停止的容器 ¶

通过docker ps可以查询当前运行的容器信息。 而通过docker ps -a，可以查询所有的容器信息，包括已停止的。

在需要清理所有已停止的容器时，通常利用shell的特性，组合一下就好。

```sh
docker rm $(docker ps -aq)
```

其中，ps的-q，是只输出容器ID，方便作为参数让rm使用。 假如给rm指定-f，则可以清理所有容器，包括正在运行的。

这条组合命令，等价于另一条命令：

```sh
docker container prune
```

container子命令，下面包含了所有和容器相关的子命令。 包括docker ps，等价于docker container ps或docker container ls。 其余还有start、stop、kill、cp等，一级子命令相当于二级子命令在外面的alias。 而prune则是特别提供的清理命令，这在其它的管理命令里还可以看到，比如image、volume。

### 按需批量清理容器 

清除所有已停止的容器，是比较常用的清理。 但有时会需要做一些特殊过滤。

这时就需要使用docker ps --filter。

比如，显示所有返回值为0，即正常退出的容器：

```sh
docker ps -a --filter 'exited=0'
```

同理，可以得到其它非正常退出的容器。

目前支持的过滤器有：

> - id (container’s id)
> - label (label=<key> or label=<key>=<value>)
> - name (container’s name)
> - exited (int - the code of exited containers. Only useful with –all)
> - status (created|restarting|running|removing|paused|exited|dead)
> - ancestor (<image-name>[:<tag>], <image id> or <image@digest>) - filters containers that were created from the given image or a descendant.
> - before (container’s id or name) - filters containers created before given id or name
> - since (container’s id or name) - filters containers created since given id or name
> - isolation (default|process|hyperv) (Windows daemon only)
> - volume (volume name or mount point) - filters containers that mount volumes.
> - network (network id or name) - filters containers connected to the provided network
> - health (starting|healthy|unhealthy|none) - filters containers based on healthcheck status

### 清理失败 [¶](https://note.qidong.name/2017/06/26/docker-clean/#清理失败)

如果在清理容器时发生失败，通过重启Docker的Daemon，应该都能解决问题。

```sh
# systemd
sudo systemctl restart docker.service

# initd
sudo service docker restart
```

### 清理镜像 

与清理容器的ps、rm类似，清理镜像也有images、rmi两个子命令。 images用来查看，rmi用来删除。

清理镜像前，应该确保该镜像的容器，已经被清除。

```sh
docker rmi IMAGE
```

其中，IMAGE可以是name或ID。 如果是name，不加TAG可以删除所有TAG。

另外，这两个命令也都属于alias。 docker images等价于docker image ls，而docker rmi等价于docker image rm。

### 按需批量清理镜像 

与ps类似，images也支持--filter参数。

与清理相关，最常用的，当属<none>了。

```sh
docker images --filter "dangling=true"
```

这条命令，可以列出所有悬挂（dangling）的镜像，也就是显示为<none>的那些。

```sh
docker rmi $(docker images -qf "dangling=true")
```

这条组合命令，如果不写入Bash的alias，几乎无法使用。 不过还有一条等价命令，非常容易使用。

```sh
docker image prune
```

prune和images类似，也同样支持--filter参数。 其它的filter有：

> - dangling (boolean - true or false)
> - label (label=<key> or label=<key>=<value>)
> - before (<image-name>[:<tag>], <image id> or <image@digest>) - filter images created before given id or references
> - since (<image-name>[:<tag>], <image id> or <image@digest>) - filter images created since given id or references
> - reference (pattern of an image reference) - filter images whose reference matches the specified pattern

### 清理所有无用镜像 ¶

这招要慎用，否则需要重新下载。

```sh
docker image prune -a
```

### 清理数据卷 ¶

数据卷不如容器或镜像那样显眼，但占的硬盘却可大可小。

数据卷的相关命令，都在docker volume中了。

一般用docker volume ls来查看，用docker volume rm VOLUME来删除一个或多个。

不过，绝大多数情况下，不需要执行这两个命令的组合。 直接执行docker volume prune就好，即可删除所有无用卷。

注意：这是一个危险操作！甚至可以说，这是本文中最危险的操作！ 一般真正有价值的运行数据，都在数据卷中。 （当然也可能挂载到了容器外的文件系统里，那就没关系。） 如果在关键服务停止期间，执行这个操作，很可能会丢失所有数据！

## 容器问题排查

### 1.查看docker日志

```shell
$ docker logs [OPTIONS] CONTAINER_ID
  Options:
        --details        显示更多的信息
    -f, --follow         跟踪实时日志
        --since string   显示自某个timestamp之后的日志，或相对时间，如42m（即42分钟）
        --tail string    从日志末尾显示多少行日志， 默认是all
    -t, --timestamps     显示时间戳
        --until string   显示自某个timestamp之前的日志，或相对时间，如42m（即42分钟）
```

直接查看日志

```
docker logs -f -t --tail=100 CONTAINER_ID
```

查看指定时间后的日志，只显示最后100行：

```shell
docker logs -f -t --since="2018-02-08" --tail=100 CONTAINER_ID
```

查看最近30分钟的日志:

```shell
$ docker logs --since 30m CONTAINER_ID
```

查看某时间之后的日志：

```shell
$ docker logs -t --since="2018-02-08T13:23:37" CONTAINER_ID
```

查看某时间段日志：

```shell
$ docker logs -t --since="2018-02-08T13:23:37" --until "2018-02-09T12:23:37" CONTAINER_ID
```

## docker volume

### Volume概念

众所周知，Docker Image可以理解成多个只读文件叠加而成，因此Docker Image是只读的。

当我们将其运行起来，就相当于在只读的Image外包裹了一层读写层变成了容器。

当你删除容器之后，使用这个镜像重新创建一个容器，此时的镜像的只读层还和原来的一样，但是你在读写层的修改全部都会丢失。

那么问题就来了，如果想要持久化在读写层的数据，该怎么利用docker做到呢？

docker使用volume实现数据的持久化，不仅如此volume还能帮助容器和容器之间，容器和host之间共享数据。

```
docker volume create [OPTIONS] [VOLUME]
```

Docker volumes 保存在服务器的 Docker 存储目录下。Linux 系统中，Docker 存储目录为 /var/lib/docker/volumes，通常用户并不需要去关心 Docker 存储目录的位置，因为可以通过 CLI 与 volumes 沟通。

### 常用操作

通过 docker run 命令的 -v（--volume）选项将 volume 挂载到一个 container 上。

```bash
$ docker run -d --name my-app -v my-volume:/usr/src/app my-app:1.0
```

上面的命令将一个名为 my-volume 的卷映射到 Docker container 中的 /usr/src/app 目录下的代码。

使用 docker volume ls 打印所有 Docker volumes：

```bash
$ docker volume ls
DRIVER    VOLUME NAME
local     my-volume  
```

也可以使用 docker volume create 命令，创建 volumes。

```bash
$ docker volume create my-volume
```

一般很少使用 docker volume create 命令，因为大多数都是通过 docker run -v 命令或者 Docker Compose 创建。

如果创建 volume 时没有传递名称，Docker 会自动生成一个随机的名称。

```bash
$ docker run -d --name my-app -v /usr/src/app my-app:1.0
```

可以通过 docker inspect 命令获得 container 的详细信息，来查看 volume 的名称。

```bash
$ docker inspect my-app
```

docker inspect 命令的输出结果会包含 "Mounts" 字段信息，里面包含了 volume 的相关信息。

```bash
...
        "Mounts": [
            {
                "Type": "volume",
                "Name": "my-volume",
                "Source": "/var/lib/docker/volumes/my-volume/_data",
                "Destination": "/usr/src/app",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
...
```

Docker 还提供了 bind mounts 选项，bind mounts 与 Docker volumes 十分类似，bind mount 是一个将会挂载到 Docker container 上的主机上的目录。bind mount 与 Docker volume 的主要区别是，Docker engine 可以通过 docker volume 命令管理 docker volume，并且 docker volume 都被保存到 Docker 的存储目录中。

例如，用户桌面上的一个目录可以被当作 container 的 bind mount。

```bash
$ docker run -d --name my-app -v ~/Desktop/my-app:/usr/src/app my-app:1.0
```

当输入 docker volume ls 命令时，bind mounts 也不会显示在打印结果里，因为 bind mounts 并不归 Docker 管理。

> Manage data in Docker
>
> Use bind mounts
>
> YouTube: "Docker Volumes explained in 6 minutes"
>
> YouTube: "What is Docker Volume | How to create Volumes | What is Bind Mount | Docker Storage"

清理所有无用数据卷：

```sh
docker volume prune
```
