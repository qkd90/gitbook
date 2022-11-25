

# MySQL 5.7以上 root用户默认密码问题

CentOS系统用yum安装MySQL的朋友，请使用 ***grep "temporary password" /var/log/mysqld.log*** 命令，返回结果最后冒号后面的字符串就是root的默认密码。

（如果不存在/var/log/mysqld.log文件，请确保您已经启动过一次MySQL服务。CentOS 7启动MySQL服务的命令是：***systemctl start mysqld.service***）

```
mysql -uroot -p
```

在MySQL的这篇名为《[Changes in MySQL 5.7.4 (2014-03-31, Milestone 14)](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-4.html)》的文档里，有这么一段：

Incompatible Change: MySQL deployments installed using mysql_install_db now are secure by default. The following changes have been implemented as the default deployment characteristics:

 

The installation process creates only a single root account, 'root'@'localhost', automatically generates a random password for this account, and marks the password expired. The MySQL administrator must connect as root using the random password and use SET PASSWORD to select a new password. (The random password is found in the .mysql_secret file in the home directory of the effective user running the script.)

 

Installation creates no anonymous-user accounts.

 

Installation creates no test database.

 

个人渣翻如下：

不兼容的更改：MySQL的部署安装使用mysql_install_db，现在默认是安全的。下面的更改已被实现并成为默认部署特性：

 

在安装的过程里，将仅创建一个root账户——'root'@'localhost'，**同时将自动生成一个随机密码给它**，并标记此密码已过期。**MySQL****管理员必须使用随机密码登陆root****账户，并使用SET PASSWORD****去设置一个新的密码**。（**随机密码可以在运行安装脚本的有效用户其主目录中的****.mysql_secret****文件中找到。**）

 

安装时不创建匿名用户账户。

 

安装时不创建测试数据库。

 

有关重点我已经有红色加粗字体标出。不过这个是脚本部署的，我当时是直接将MySQL源添加进了系统源里，然后用***yum install mysql-community-server***命令安装的，所以自然是没有办法在主目录里找到“.mysql_secret”文件。那密码会在哪儿呢？

其实MySQL在运行的时候会有一个日志文件，它存在于/var/log/mysqld.log，我们在安装完成后第一次启动MySQL服务时，MySQL生成的随机密码就在这个文件里，我们可以直接用下面这条命令显示出这个文件里的所有内容：

***cat /var/log/mysqld.log***

![img](https://sources.yanning.wang/images/Archives/379/03.png)

 

这满屏幕密密麻麻的字，看着就晕，如果我说密码已经在上面的截图里了，你能马上找到吗？肯定得花好久，所以我们这里可以用个更方便的命令：

***grep "temporary password" /var/log/mysqld.log***

![img](https://sources.yanning.wang/images/Archives/379/04.png)

 使用该临时密码登录

![img](https://sources.yanning.wang/images/Archives/379/05.png)

 

现在好不容易进入了控制台，接下来要做的就是修改密码了，毕竟这么一串密码谁都记不住吧？设置新密码的命令是：

***SET PASSWORD = PASSWORD('你的新密码');***

不过需要注意的是现在MySQL已经强制要求强密码，已经不能再用弱密码比如“123456”了。如果你设置的密码过于简单，会提示错误：

ERROR 1819 (HY000): Your password does not satisfy the current policy requirements

（2017.5.31补充：这是因为MySQL在5.6.6加入了“validate_password”插件，它默认设置下要求用户使用强密码。如果需要使用弱密码请您查阅笔者另外一篇博客：《[MySQL 5.6.6+ 使用弱密码](https://www.yanning.wang/archives/520.html)》）

![img](https://sources.yanning.wang/images/Archives/379/06.png)

 