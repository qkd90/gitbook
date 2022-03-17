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

1.清理所有状态为 exited 的容器

```
docker rm $(docker ps -qf status=exited)
```

