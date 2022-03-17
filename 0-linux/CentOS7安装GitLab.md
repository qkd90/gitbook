# CentOS7安装GitLab

## **文章目录**

- 卸载gitlab

- 安装依赖库

- 安装gitlab-ce

- 登录gitlab

- gitlab日常使用

- - 文件路径
  - gitlab服务构成
  - gitlab常用命令

**01 卸载gitlab**
注意：如果之前没有安装gitlab可以跳过`卸载gitlab`步骤，直接进入安装依赖库

### **1、停止gitlab**

```
# 停止gitlab
gitlab-ctl stop

# 查看gitlab状态
gitlab-ctl status
```

输出结果如果都是down说明停止成功

![img](https://pic1.zhimg.com/v2-a795a5955966dfa7a780957528830820_r.jpg)

### **2、卸载gitlab（注意这里写的是gitlab-ce）**

```
rpm -e gitlab-ce
```

### **3、查看gitlab进程**

```
ps -ef | grep gitlab
```

### **4、杀掉带有好多…的进程**

```
kill -9 202859
```

杀掉后，执行ps -ef | grep gitlab确认一遍，还有没有gitlab的进程

![img](https://pic2.zhimg.com/v2-94786a169cb5c8ad63b8020da592f8f5_r.jpg)

### **5、删除所有包含gitlab文件**

```
find / -name gitlab | xargs rm -rf
```

## **02 安装依赖库**

```
# 安装依赖
yum install -y curl policycoreutils openssh-server

# 打开http, https和ssh访问
systemctl enable sshd
systemctl start sshd
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
systemctl reload firewalld

# 安装postfix，用来发送通知邮件
yum install -y postfix
systemctl enable postfix
systemctl start postfix
```

## **03 安装gitlab-ce**

下载GitLab社区版安装包，下载地址：

```
gitlab官网:
https://packages.gitlab.com/gitlab/gitlab-ce?utm_source=ld246.com
```

国内建议使用的清华大学的镜像源下载GitLab，下载地址：

```
清华大学镜像源下载:
https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el8
```

在下载好安装包后，放到自己习惯放的路径下即可，笔者这里放到`/usr/local`目录



```
# 进入安装包所在目录
cd /usr/local
# rpm方式安装gitlab，一般出现gitlab的logo图案表示安装完毕了
rpm -ivh gitlab-ce-13.7.2-ce.0.el8.x86_64.rpm
```

![img](https://pic1.zhimg.com/v2-08d6ec0d11c7a1c0cfa4b9f029706154_r.jpg)

如果访问不了，记得关闭防火墙:

```
systemctl stop firewalld
systemctl disable firewalld
```

内存要大于4G，内存不足报错:

```
free -m
```

需要用到的端口:

```
# puma['port'] = 8080
# postgresql['port'] = 5432
# redis['port'] = 6379
# sentinel['port'] = 26379
# nginx['listen_port'] = nil
# nginx['listen_https'] = nil
```

注意新配置的端口号不要被其他进程占用，且要在防火墙设置放开

查看 puma，nginx，redis端口是否被占用，可以使用 命令 gitlab-ctl tail puma 追踪查看启动信息

编辑gitlab配置文件:`vim /etc/gitlab/gitlab.rb`

注释如下配置

```
# external_url 'http://gitlab.example.com'
```

添加如下配置:

```
# 配置http协议所使用的访问地址,不加端口号默认为80
external_url 'http://192.168.138.8:9080'
#修改默认端口
nginx['listen_port'] = 9080
# 修改puma服务器端口
puma['port']=9081
# 配置时区为 亚洲/上海 东八区时间
gitlab_rails['time_zone'] = 'Asia/Shanghai'
# 后台认证地址
gitlab_workhorse['auth_backend'] = "http://localhost:9081"
```

注意：因为从GitLab 13.0开始，Puma是默认的Web服务器，并且Unicorn默认情况下处于禁用状态。

执行如下命令查看版本:

```
cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
```

如果小于13.0版本默认使用的是unicorn，默认为`unicorn['port'] = 8080`

如果大于13.0版本默认使用的是puma，在`/etc/gitlab/gitlab.rb`配置中，查看puma的端口是否被占用，默认为`puma['port']=8080`，修改为服务器没有被占用的端口

```
puma['port']=9080
```

如果8080端口被占用，/var/log/gitlab/puma/current会报如下错误:

```
2021-01-11_12:46:07.24719 Errno::EADDRINUSE: Address already in use - bind(2) for "127.0.0.1" port 8080
```

`/var/log/gitlab/nginx/current`会报如下错误:

```
2021-01-11_12:44:01.18684 2021/01/11 20:43:58 [emerg] 21319#0: still could not bind()
2021-01-11_12:44:01.24463 2021/01/11 20:44:01 [emerg] 21324#0: bind() to 0.0.0.0:8080 failed (98: Address already in use)
2021-01-11_12:44:01.74656 2021/01/11 20:44:01 [emerg] 21324#0: bind() to 0.0.0.0:8080 failed (98: Address already in use)
2021-01-11_12:44:02.24768 2021/01/11 20:44:01 [emerg] 21324#0: bind() to 0.0.0.0:8080 failed (98: Address already in use)
```

刷新配置，让配置生效:

```
gitlab-ctl reconfigure
```

重启服务:

```
gitlab-ctl restart
```

## **04 登录gitlab**

进入gitlab网址：`http://192.168.138.8:9080`， 设置root用户密码，至少8个字符，为了方便记忆，这里设置为root1234

设置好root用户密码，重新登录

![img](https://pic2.zhimg.com/v2-63fe59ec6cd865ec63fe31617aa587fd_r.jpg)

登录成功页面如下:

![img](https://pic1.zhimg.com/v2-14a3ead767384b1c89eae081c7b7ffac_r.jpg)

## **05 gitlab日常使用**

### **文件路径**

安装成功后，可以利用`rpm -ql gitlab-ce`查询其文件安装路径及相关文件路径

```
# 主要配置文件目录
主配置文件: /etc/gitlab/gitlab.rb
默认安装路径：/opt/gitlab
代码仓库保存位置：/var/opt/gitlab/git-data/repositories
代码仓库备份位置：/var/opt/gitlab/backups
nginx配置文件: /var/opt/gitlab/nginx/conf/gitlab-http.conf
postgresql数据及配置目录：/var/opt/gitlab/postgresql/data
redis默认配置目录：/var/opt/gitlab/redis
各服务数据及配置文件保存路径：/var/opt/gitlab
日志地址：/var/log/gitlab
```

### **gitlab服务构成**

```
# Gitlab服务构成
nginx: 静态web服务器
gitlab-shell: 用于处理Git命令和修改authorized keys列表
gitlab-workhorse: 轻量级的反向代理服务器
logrotate：日志文件管理工具
postgresql：数据库
redis：缓存数据库
sidekiq：用于在后台执行队列任务（异步执行）
unicorn：HTTP服务，13.0版本之前GitLab Rails应用是托管在这个服务器上
puma：HTTP服务，13.0版本后GitLab Rails应用是托管在这个服务器上
```

### **gitlab常用命令**

```
# 重新编译gitlab的配置
gitlab-ctl reconfigure
# 启动
gitlab-ctl start
# 停止
gitlab-ctl stop
# 重启
gitlab-ctl restart

# 实时查看日志
gitlab-ctl tail
# 实时各个模块日志
gitlab-ctl tail redis/postgresql/gitlab-workhorse/logrotate/nginx/sidekiq/unicorn/puma
# 帮助命令
gitlab-ctl --help
# 检查gitlab
gitlab-rake gitlab:check SANITIZE=true --trace
```