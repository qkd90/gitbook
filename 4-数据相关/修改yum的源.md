# 修改yum的源

## 一、配置yum源

鉴于外网的速度问题，修改yum源为阿里云

1，进入yum源配置目录

```
cd /etc/yum.repos.d
```

2，备份系统自带的yum源

```
mv CentOS-Base.repo CentOS-Base.repo.bk
```

3.下载阿里云的yum源：

```
wget -O CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

4.重命名

```
mv Centos-7.repo CentOS-Base.repo
```

5.更新完yum源后，执行下边命令更新yum配置，使操作立即生效

```
yum clean all
yum makecache
```

4，除了阿里云之外，国内还有其他不错的yum源，比如中科大和搜狐的，大家可以根据自己需求下载

中科大的yum源：

```
#wget http://centos.ustc.edu.cn/CentOS-Base.repo
```

sohu的yum源

```
#wget http://mirrors.sohu.com/help/CentOS-Base-sohu.repo
```

理论上讲，这些yum源redhat系统以及fedora也是可以用 的，但是没有经过测试，需要的可以自己测试一下。

## 二、安装yum-downloadonly，下载rpm软件包

方法1、安装yum-downloadonly插件，下载rpm包；

```
yum install yum-downloadonly
yum install --downloadonly --downloaddir=/nginx.rpm pcre
```

如果下载不到yum-downloadonly这个软件包，请查看附件，下载之后解压缩，上传到linux上，进行安装。



方法2、修改配置文件/etc/yum.conf ,将 keepcache=0 修改为 keepcache=1

通过yum安装的软件将会在下面的cachedir中缓存。

cachedir=/var/cache/yum/$basearch/$releasever

例如：

```
# cd /var/cache/yum/x86_64/6/base/packages/
libpcap-1.4.0-4.20130826git2dbcaa1.el6.x86_64.rpm tcpdump-4.0.0-9.20090921gitdf3cb4.2.el6.x86_64.rpm
```