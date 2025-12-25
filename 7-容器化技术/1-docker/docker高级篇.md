# docker高级篇

## Docker轻量级可视化工具Portainer

创建portainer_data数据卷

```shell
docker volume create portainer_data
```

## 迁移docker的默认安装(存储)目录

如果是通过 Ubuntu 的 apt-get 安装的 Docker，默认的安装目录应该是： /var/lib/docker 。 为了完全确定，可以使用以下的命令查询真正的安装路径： 

```
sudo docker info | grep "Docker Root Dir"
```

下文以/store/software/docker 这个路径作为要迁移的新 Docker 安装(存储)目录

 在开始迁移之前，首先复制原 Docker 安装(存储)目录到新的路径下： 

```
cp -a /var/lib/docker /store/software/ 
```

然后备份原目录数据：

```
 mv -u /var/lib/docker /var/lib/docker.bak
```

配置Docker数据目录修改Docker的启动参数,设置--graph参数使用挂载的硬盘作为数据目录。

```shell
vim  /etc/docker/daemon.json
```

增加数据目录：data-root

```json
{
 "data-root": "/disksda/docker",
 "registry-mirrors": [
        "https://8z24i0b8.mirror.aliyuncs.com",
        "https://hub-mirror.c.163.com",
        "https://mirror.baidubce.com"
        ],
 "bip":"192.161.20.1/24",
 "exec-opts": ["native.cgroupdriver=systemd"],
 "log-driver": "json-file",
 "log-opts": {"max-size": "100m"},
 "storage-driver": "overlay2"
}
```

重启docker

```shell
# 移动docker目录
mv /var/lib/docker /disksda/docker

sudo systemctl daemon-reload 
sudo systemctl restart docker
```

验证结果

使用docker info命令,查看Storage Driver和Docker Root Dir参数,确认Docker已使用挂载的硬盘作为数据目录。熟练掌握Docker和Linux存储管理,可以让我们更轻松解决在使用过程中遇到的存储问题。

## docker
