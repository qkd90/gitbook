

# centos7的oracle19c安装折腾指南（包含卸载）

通过yum localinstall 方式安装，而且需要足够的配置，储存空间建议7GB以上

## 第一步：安装软件

yum源 ip、防火墙 就不细描述了。。。

先修改yum的源

centos系统更新：

```
yum clean all 
yum makecache 
yum -y update
```

进入正题：

下载[oracle19c](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.oracle.com%2Ftechnetwork%2Fdatabase%2Fenterprise-edition%2Fdownloads%2Foracle19c-linux-5462157.html)的地址：[https://www.oracle.com/technetwork/database/enterprise-edition/downloads/oracle19c-linux-5462157.html](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.oracle.com%2Ftechnetwork%2Fdatabase%2Fenterprise-edition%2Fdownloads%2Foracle19c-linux-5462157.html)

下载[oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm](https://links.jianshu.com/go?to=http%3A%2F%2Fyum.oracle.com%2Frepo%2FOracleLinux%2FOL7%2Flatest%2Fx86_64%2FgetPackage%2Foracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm)的下载地址：[http://yum.oracle.com/repo/OracleLinux/OL7/latest/x86_64/getPackage/oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm](https://links.jianshu.com/go?to=http%3A%2F%2Fyum.oracle.com%2Frepo%2FOracleLinux%2FOL7%2Flatest%2Fx86_64%2FgetPackage%2Foracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm)

用xftp 或者 WinSCP 上传 rmp包文件。

oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm、oracle-database-ee-19c-1.0-1.el7.x86_64.rpm

![img](https://upload-images.jianshu.io/upload_images/19730272-f1fdc9949d25c7c5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/808/format/png)

1.运行安装命令：
yum localinstall oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm

![img](https://upload-images.jianshu.io/upload_images/19730272-700c82cfeb3e2034.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/796/format/png)

yum localinstall oracle-database-ee-19c-1.0-1.x86_64.rpm

![img](https://upload-images.jianshu.io/upload_images/19730272-3b518904b5dd6a40.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/829/format/png)

## 第二步 配置实例

1、修改字符集以及实例名称

vim /etc/init.d/oracledb_ORCLCDB-19c

```
export ORACLE_SID=ORCLCDB
export TEMPLATE_NAME=General_Purpose.dbc
export CHARSET=ZHS16GBK
export PDB_NAME=ORA19CRPMPDB
export LISTENER_NAME=LISTENER
export NUMBER_OF_PDBS=1
```



![img](https://upload-images.jianshu.io/upload_images/19730272-3737ee90d4a122ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/810/format/png)



2、复制安装配置文件

cd /etc/sysconfig/

cp oracledb_ORCLCDB-19c.conf oracledb_ORCL-19c.conf



![img](https://upload-images.jianshu.io/upload_images/19730272-1b4c98fc52ef3269.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/803/format/png)

## 第三步 安装



/etc/init.d/oracledb_ORCLCDB-19c configure
这一步会很耗时，当然服务器配置好的话不会太慢，20分钟左右



![img](https://upload-images.jianshu.io/upload_images/19730272-27693b5c9e92e170.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/812/format/png)

## 第四步 配置oracle 

设置环境变量，否则sqlplus / as sysdba 无法使用

\#执行

```
vim .bash_profile
```

\#添加一下内容

```
export ORACLE_HOME=/opt/oracle/product/19c/dbhome_1
export PATH=$PATH:/opt/oracle/product/19c/dbhome_1/bin
export ORACLE_SID=ORCLCDB
```

保存退出后

```
source.bash_profile
```



## 第五步 启动服务和监听

```
su oracle #切换到oracle
sqlplus / as sysdba
\#打开sql窗口
startup
\#启动服务
exit 
\#退出命令窗口
cd $ORACLE_HOME/bin
\#定位到bin目录
lsnrctl start
\#启动监听
```

