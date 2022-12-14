## 概述

不知不觉，MySQL8.0已经发布好多个GA小版本了，MySQL8.0版本基本已到稳定期。今天主要介绍从5.7升级到8.0版本的过程及注意事项，有想做版本升级的小伙伴可以参考下。

## 注意事项

mysql从5.7升级到8.0是支持的，但是只支持GA版本的升级，并且要求版本为5.7.9或者更高
在升级到8.0之前，建议升级到5.7的最新版本。仅仅支持从5.7版本升级到8.0，不支持5.6版本升级到8.0

升级之前我们需要了解下MySQL5.7和8.0有哪些不同，简单总结出MySQL8.0以下几点新特性：

- 默认字符集由latin1变为utf8mb4。
- MyISAM系统表全部换成InnoDB表。
- JSON特性增强。
- 支持不可见索引，支持直方图。
- sql_mode参数默认值变化。
- 默认密码策略变更。
- 新增角色管理。
- 支持窗口函数，支持Hash join。

根据版本变化及官方升级教程，列举出以下几点注意事项：

- 注意字符集设置。为了避免新旧对象字符集不一致的情况，可以在配置文件将字符集和校验规则设置为旧版本的字符集和比较规则。
- 密码认证插件变更。为了避免连接问题，可以仍采用5.7的mysql_native_password认证插件。
- sql_mode支持问题。8.0版本sql_mode不支持NO_AUTO_CREATE_USER，要避免配置的sql_mode中带有NO_AUTO_CREATE_USER。
- 是否需要手动升级系统表。在MySQL 8.0.16版本之前，需要手动的执行mysql_upgrade来完成该步骤的升级，在MySQL 8.0.16版本及之后是由mysqld来完成该步骤的升级。

## 准备工作

1、备份数据（包括当前的数据库和日志文件）

```
--备份数据
mysqldump -uroot -p ycapp_dflg_prod --single_transaction  --flush-logs --master-data=2 >/backup/ycapp.sql
--备份视图、函数、存储过程、事件、触发器的定义============================================================================#!/bin/bash# ./output_db_object_definition.sh > dev/null 2>&1
db_user="root"
db_pwd="xxxx"
db_host="localhost"
db_port=3306
db_name="xxxx" 
save_file="/home/scripts/${db_name}_object_definition.sql"
# view,function,procedure,event,triggeroutput_type='view,function,procedure,event,trigger' 
(cat <<out
/*
ouput object‘s definition for database "$db_name"
ouput time: $(date "+%Y-%m-%d %H:%M:%S")
ouput object type: $output_type
*/
out
)>$save_fileecho "">> $save_file
echo "">> $save_file
 # 视图if [[ $output_type == *"view"* ]]
then	echo "-- ------------------------------------------------------------" >> $save_file
	echo "-- views" >> $save_file
	echo "-- ------------------------------------------------------------" >> $save_file
	mysql -h$db_host -P$db_port -u$db_user -p$db_pwd --skip-column-names \	-e "select concat('SHOW CREATE VIEW ',table_schema,'.',table_name,';') from information_schema.views where table_schema='$db_name'" |\
	sed 's/;/\\G/g' | mysql -h$db_host -P$db_port -u$db_user -p$db_pwd $db_name |\
	sed 's/Create View: kk_begin\n/g' | sed 's/[ ]*character_set_client:/;\nkk_end/g' |\
	sed -n '/kk_begin/{:a;N;/kk_end/!ba;s/.*kk_begin\|kk_end.*//g;p}'  >> $save_file
fi # 函数if [[ $output_type == *"function"* ]]
then	echo "-- ------------------------------------------------------------" >> $save_file
	echo "-- function" >> $save_file
	echo "-- ------------------------------------------------------------" >> $save_file
	mysql -h$db_host -P$db_port -u$db_user -p$db_pwd --skip-column-names \	-e "select concat('SHOW CREATE FUNCTION ',routine_schema,'.',routine_name,';') from information_schema.routines where routine_schema='$db_name' and ROUTINE_TYPE='FUNCTION'" |\
	sed 's/;/\\G/g' | mysql -h$db_host -P$db_port -u$db_user -p$db_pwd $db_name |\
	sed 's/Create Function: kk_begin\ndelimiter $$\n/g' | sed 's/[ ]*character_set_client:/$$ \ndelimiter ;\nkk_end/g' |\
	sed -n '/kk_begin/{:a;N;/kk_end/!ba;s/.*kk_begin\|kk_end.*//g;p}' >> $save_file
 fi # 存储过程if [[ $output_type == *"procedure"* ]]
then	echo "-- ------------------------------------------------------------" >> $save_file
	echo "-- procedure" >> $save_file
	echo "-- ------------------------------------------------------------" >> $save_file
	mysql -h$db_host -P$db_port -u$db_user -p$db_pwd --skip-column-names \	-e "select concat('SHOW CREATE PROCEDURE ',routine_schema,'.',routine_name,';') from information_schema.routines where routine_schema='$db_name' and ROUTINE_TYPE='PROCEDURE'" |\
	sed 's/;/\\G/g' | mysql -h$db_host -P$db_port -u$db_user -p$db_pwd $db_name |\
	sed 's/Create Procedure: kk_begin\ndelimiter $$\n/g' | sed 's/[ ]*character_set_client:/$$ \ndelimiter ;\nkk_end/g' |\
	sed -n '/kk_begin/{:a;N;/kk_end/!ba;s/.*kk_begin\|kk_end.*//g;p}' >> $save_file
fi # 事件if [[ $output_type == *"event"* ]]
then	echo "-- ------------------------------------------------------------" >> $save_file
	echo "-- event" >> $save_file
	echo "-- ------------------------------------------------------------" >> $save_file
	mysql -h$db_host -P$db_port -u$db_user -p$db_pwd --skip-column-names \	-e "select concat('SHOW CREATE EVENT ',EVENT_SCHEMA,'.',EVENT_NAME,';') from information_schema.events where EVENT_SCHEMA='$db_name'" |\
	sed 's/;/\\G/g' | mysql -h$db_host -P$db_port -u$db_user -p$db_pwd |\
	sed 's/Create Event: kk_begin\ndelimiter $$\n/g' | sed 's/[ ]*character_set_client:/$$ \ndelimiter ;\nkk_end/g' |\
	sed -n '/kk_begin/{:a;N;/kk_end/!ba;s/.*kk_begin\|kk_end.*//g;p}' >> $save_file
fi # 触发器if [[ $output_type == *"trigger"* ]]
then	echo "-- ------------------------------------------------------------" >> $save_file
	echo "-- trigger" >> $save_file
	echo "-- ------------------------------------------------------------" >> $save_file
	mysql -h$db_host -P$db_port -u$db_user -p$db_pwd --skip-column-names \	-e "select concat('SHOW CREATE TRIGGER ',TRIGGER_SCHEMA,'.',TRIGGER_NAME,';') from information_schema.triggers where TRIGGER_SCHEMA='$db_name';" |\
	sed 's/;/\\G/g' | mysql -h$db_host -P$db_port -u$db_user -p$db_pwd $db_name|\
	sed 's/SQL Original Statement: kk_begin\ndelimiter $$\n/g' | sed 's/[ ]*character_set_client:/$$ \ndelimiter ;\nkk_end/g' |\
	sed -n '/kk_begin/{:a;N;/kk_end/!ba;s/.*kk_begin\|kk_end.*//g;p}' >> $save_file
fi # ^M, you need to type CTRL-V and then CTRL-Msed -i "s/\^M//g" $save_file

登录后复制
```

## 安装mysql

### 1.下面mysql官网提供的mysql repo源

centos的yum 源中默认是没有mysql的，所以我们需要先去官网下载mysql的repo源并安装；

mysql官网下载链接：mysql repo下载地址 如下：

> https://dev.mysql.com/downloads/

### 2.下载软件包rpm文件

文件下载到 /usr/local/mysql 文件夹下；

```bash
cd /usr/local
mkdir mysql
cd mysql
wget  https://repo.mysql.com//mysql80-community-release-el7-1.noarch.rpm
```

### 3.安装 yum repo文件并更新 yum 缓存

```bash
rpm -ivh mysql57-community-release-el7-11.noarch.rpm
```

执行结果：

会在/etc/yum.repos.d/目录下生成两个repo文件mysql-community.repo mysql-community-source.repo

更新 yum 命令

```bash
yum clean all
yum makecache
```

### 4.使用 yum安装mysql

当我们在使用yum安装mysql时，yum默认会从yum仓库中安装mysql最新的GA版本；如何选择自己的版本；

第一步： 查看mysql yum仓库中mysql版本，使用如下命令

```bash
yum repolist all | grep mysql
```

可以看到 MySQL 5.5 5.6 5.7为禁用状态 而MySQL 8.0为启用状态；

第二步 使用 yum-config-manager 命令修改相应的版本为启用状态最新版本为禁用状态，根据需要安装的版本修改

```bash
yum-config-manager --disable mysql80-community #关闭8.0版本
yum-config-manager --enable mysql57-community #开启5.7版本
```

或者可以编辑 mysql repo文件，

```bash
cat /etc/yum.repos.d/mysql-community.repo 
```

将相应版本下的enabled改成 1 即可；

### 5.安装mysql 命令如下：

```bash
yum install mysql-community-server
```

### 6.开启mysql 服务

> 在开启前最最重要的一步，防止数据库运行后，产生数据库大小写敏感无法更改的问题！

```bash
#(使用repo安装的mysql，生成的文件为my.cnfreoNew,修改为my.cnf即可)
vi /etc/my.cnf
```

在[mysqlId]下增加配置

```bash
lower_case_table_names=1
```

然后ESC退出，:wq退出并保存，然后在启动服务

```bash
systemctl start mysqld.service
```

### 7.获取初始密码登录mysql

mysql在安装后会创建一个root@locahost账户，并且把初始的密码放到了/var/log/mysqld.log文件中；

```bash
cat /var/log/mysqld.log | grep password
```

### 8.使用初始密码登录mysql

```bash
mysql -u root -p  #会提示输入密码
```

修改初始密码：

```bash
#注意位数和种类至少大+写+小写+符号+数字
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Trasen@8812';
```

### 9.允许用户远程登录

2，输入以下语句，进入mysql库：

```sql
use mysql
```

3，更新域属性，'%'表示允许外部访问：

```sql
update user set host='%' where user ='root';
```

4，执行以上语句之后再执行：

```sql
FLUSH PRIVILEGES;
```

5，再执行授权语句：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'WITH GRANT OPTION;
```

然后外部就可以通过账户密码访问了。

6，其它说明：

FLUSH PRIVILEGES; 命令本质上的作用是：

将当前user和privilige表中的用户信息/权限设置从mysql库(MySQL数据库的内置库)中提取到内存里。

MySQL用户数据和权限有修改后，希望在"不重启MySQL服务"的情况下直接生效，那么就需要执行这个命令。

通常是在修改ROOT帐号的设置后，怕重启后无法再登录进来，那么直接flush之后就可以看权限设置是否生效

### 10.忘记密码-重置密码

输入初始密码后，如果遇到下面的错误

> ERROR 1045 (28000): Access denied for user ‘root’@‘localhost’ (using password: YES)]

重置密码解决MySQL for Linux错误

在[mysqld]后面任意一行添加skip-grant-tables用来跳过密码验证的过程;设置完密码记得删除

```bash
vim /etc/my.cnf #注：windows下修改的是my.ini
skip-grant-tables# 在[mysqld]后面任意一行添加skip-grant-tables用来跳过密码验证的过程;设置完密码记得删除
12
```

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202211241528190.png)
重启mysql ，就可以免密码登陆了，然后进行修改密码

```bash
systemctl restart mysqld.service 
```

或

```bash
service mysqld restart
```

进入mysql：

```sql
mysql -u root
use mysql;

#清空密码：
update user set authentication_string='' where user='root';
```

退出mysql,屏蔽skip-grant-tables,在skip-grant-tables前面添加#，如上张图所示：

```
vim /etc/my.cnf
```

重启mysql服务生效，进入mysql

```
mysql -u root
```

![image-20221124153945178](https://raw.githubusercontent.com/qkd90/figureBed/main/202211241539233.png)

1、需要执行如下语句修改密码：

```bash
set password='your password';
```

2、如果密码符合Mysql要求，会修改成功。如果出现以下错误信息：

> ERROR 1819 (HY000): Your password does not satisfy the current policy
> requirements

执行如下两条语句：

```bash
set global validate_password.policy=0;
set global validate_password.length=1;
```

然后再次执行步骤1中的语句即可，这样密码就算是设置好了。

## 修改密码

```
Alter user '用户名'@'主机名' identified by '新密码';
alter user 'wyy'@'192.168.0.105' identified by '123';
```

## 授权

### 给用户授权所有权限

```
grant all privileges on *.* to '用户名'@'主机名' with grant option;

grant all privileges on *.* to 'wyy'@'192.168.0.105' with grant option;
```

grant：授权、授予
privileges:权限，特权
第一个星号：表示所有数据库
第二个星号：表示所有表
with grant option：表示该用户可以给其他用户赋予权限，但不能超过该用户的权限。这个不加也行。

例如：如果wyy只有select、update权限，没有insert、delete权限，给另一个用户授权时，只能授予它select、update权限，不能授予insert、delete权限。

### 给用户授权个别权限

all privileges 可换成 select,update,insert,delete,drop,create 等操作

```
grant select,insert,update,delete on *.* to '用户名'@'主机名';
```

#### 给用户授权指定权限

###### 给用户授予指定的数据库权限

```
grant all privileges on 数据库 . * to 'wyy'@'192.168.0.105';

grant all privileges on xrs . * to 'wyy'@'192.168.0.105';
将数据库名为xrs的所有权限赋予wyy
1234
```

###### 给用户授予指定的表权限

```
grant all privileges on 数据库 . 指定表名 to 'wyy'@'192.168.0.105';
将某个数据库下的某个表的权限赋予wyy
12
```

### 注意：

网上有的直接创建并赋权：

grant all privileges * . * to ‘要创建的用户’@‘localhost’ identified by ‘自定义密码’;

我在mysql8试了不行（8版本以下还没试过），要先创建用户再进行赋权，不能同时进行

## 7、刷新权限

```
flush privileges;
```

还有一种方法，就是重新启动mysql服务器，来使新设置生效。­

## 8、查看用户授权

```
show grants for 'wyy'@'192.168.0.105';

12
```

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202211251758011.png)

## 9、撤销用户授权（销权）

```
revoke all privileges on *.* from 'wyy'@'192.168.0.105';
1
```

用户有什么权限就撤什么权限

### 9.在防火墙中开启3306端口

第一步：开启firewall3306端口防火墙

```bash
firewall-cmd --zone=public --list-ports 查看所有打开的端口
firewall-cmd --zone=public --add-port=80/tcp --permanent    开启一个端口，添加--permanent永久生效，没有此参数重启后失效
firewall-cmd --permanent --add-port=80/tcp  开放端口80
firewall-cmd --permanent --remove-port=80/tcp   移除端口80
firewall-cmd --reload   重启防火墙，修改后重启防火墙生效
12345
```

第二步： 重启防火墙

```bash
systemctl enable iptables.service
systemctl start iptables.service
12
```

第三步： 将mysql 服务加入开机启动项，并启动mysql进程

```bash
systemctl enable mysqld.service
systemctl start mysqld.service
12
```

第四步：开启mysql远程服务：

外网 Navicat 连接 Mysql
修改mysql数据库下的user表中host的值

可能是你的帐号不允许从远程登陆，只能在localhost。这个时候只要在localhost的那台电脑，登入mysql后，更改 “mysql” 数据库里的 “user” 表里的 “host” 项，从"localhost"改称"%"登录mysql数据库 执行如下命令：

```bash
mysql -u root -p
use mysql;
update user set host='%' where user='root';
123
```

### 10.使用navicat进行连接测试

> 使用navicat远程连接mysql时报2059错误解决方法

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202211241528615.png)
1、管理员权限打开cmd
输入`mysql -u root -p`进入输入密码后进入mysql数据库；

2、修改加密规则及密码

```bash
ALTER USER 'root'@'localhost' IDENTIFIED BY '你的mysql密码' PASSWORD EXPIRE NEVER; #修改加密规则
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的mysql密码'; #修改密码

FLUSH PRIVILEGES; #刷新数据
```

此处报错：

```bash
//执行
ALTER USER 'root'@'%' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER;

//报错
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
12345
```

错误1819 (HY000):您的密码不满足当前策略要求

改为较复杂的密码即可

```bash
ALTER USER 'root'@'%' IDENTIFIED BY 'rt123RT!@#' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'rt123RT!@#';
FLUSH PRIVILEGES; #刷新数据
```

3、退出，重启mysql

```bash
service mysqld restart
```

在使用navicat即可登录成功

### 11.MySQL V8.0设置大小写不敏感后不能正常启动

> 之前安装MySQL时大小写是敏感的，结果公司RDS上的生产库中配置是不敏感的，导致不同步，今天需要把开发数据库也修改为大小写不敏感，经过网上搜索，需要修改my.cnf配置文件。

> 第一步：查找my.cnf文件位置
> 1、使用 find / -name “my.cnf”

> /etc/my.cnf 找到my.cnf 文件位于 /etc 目录下。

> 2、vi /etc/my.cnf
> 尾部增加配置
> lower_case_table_names=1

> ESC :wq 退出并保存。

> 3、重启MySQL
> 停掉MySQL服务：service mysqld stop
> 启动MySQL服务：service mysqld start

> 结果却出错了，显示：Job for mysqld.service failed because the control process exited with error code. See “systemctl status mysqld.service” and"journalctl -xe" for details.
>
> 找了半天也没找到错误原因，把新加的 lower_case_table_names=1 注释掉以后，可以正常启动了。

**Mysql8.0开启忽略表大小写,无法启动，解决方案**

> mysql8.0默认是区分大小写。
> 因此如果要设置忽略大小写，需要在安装完成之后，初始化数据库的时候进行设置。
> /usr/sbin/mysqld --initialize --user=mysql --lower-case-table-names=1

初始化完成之后在启动数据库,否则的话就会是无效的。

如果要是已经启动了数据库，在配置文件中再去修改，就会造成数据库无法启动的情况。

如果出现这个情况

> 首先需要删除掉 /var/lib/mysql 文件夹下面的所有的文件。
> 再去修改配置文件my.cnf
> 添加lower_case_table_names=1 在启动mysql。
> 这样可以完美解决

三、多个root用户密码修改



## 疑难解答

### 1.有多个root用户如何解决

公司服务器出现多个root用户，密码还不一致

先查询都有哪些用户

```
select host,user from mysql.user;
```

删除多余用户

```
drop user '用户名'@'主机名';
drop user 'wyy'@'192.168.0.105';
```

创建需要用户

```
create user '用户名'@'允许那个主机链接' identified by '密码';

create user 'wyy'@'192.168.0.105' identified by 'wyy18222';
只允许192.168.0.105的主机链接
```
