## 卸载nginx

### 1.使用whereis命令

whereis命令可以定位二进制文件、源码文件和手册页的位置。对于Nginx,可以运行:

```bash
whereis nginx
```

结果：

```
nginx: /usr/sbin/nginx /usr/lib64/nginx /etc/nginx /usr/share/nginx /usr/share/man/man8/nginx.8.gz /usr/share/man/man3/nginx.3pm.gz
```

可以看到Nginx的安装目录在/usr/local/nginx。

### 2. 查看Nginx进程

使用ps aux命令查看Nginx进程,在命令行参数中可以看到安装目录，同时可以看到是否在运行

```
ps aux | grep nginx
```

### 3.停止Nginx

```
systemctl stop nginx
```

### 4.删除nginx文件

```
rm -rf  /usr/sbin/nginx /usr/lib64/nginx /etc/nginx /usr/share/nginx /usr/share/man/man8/nginx.8.gz /usr/share/man/man3/nginx.3pm.gz
```

### 5.删除Nginx用户和组

如果在编译安装时创建过nginx用户和组,需要删除:

```
bash
userdel nginx 
groupdel nginx
```

### 6.删除配置文件(可选)

如果要彻底移除Nginx,可以删除其配置文件:

```
bash
rm -f /etc/nginx/nginx.conf 
rm -rf /etc/nginx/conf.d/
```

## 安装nginx

在CentOS 7系统中部署Nginx 1.20.1版本,步骤如下:

### 1. 安装前置环境

```shell
yum -y install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel
```

### 2.下载和安装Nginx 1.20.1

```
mkdir /usr/local/nginx
wget https://nginx.org/download/nginx-1.20.1.tar.gz 
tar -zxvf  nginx-1.20.1.tar.gz
cd nginx-1.20.1
## with-http-ssl-module
./configure --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module

make
make install 
```

### 3.创建软链接（也就是配置全局命令）

```
ln -s /rgzn/nginx/sbin/nginx /usr/bin/nginx
```

### 4.启动Nginx查看版本

```
nginx  
nginx -v
```

### 5.设置开机启动

```
echo "nginx" >> /etc/rc.local
```
