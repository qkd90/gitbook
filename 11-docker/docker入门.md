# docker操作

## 一、基本操作

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

## 二、清理操作

### 1.清理所有状态为 exited 的容器

```
docker rm $(docker ps -qf status=exited)
```

## 三、容器问题排查

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

