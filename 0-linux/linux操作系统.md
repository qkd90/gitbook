1.sh命令：

```shell
sh [options] [file]
-c string：命令从-c后的字符串读取。
-i：实现脚本交互。
-n：进行脚本的语法检查。
-x：实现脚本逐条语句的跟踪。
```

2.systemctl enable httpd

如果你们的设备  重启不会自动启动apache  执行一下这个命令

这个之前基础组件部署的时候  这个配置没有在脚本里

3.修改后台admin账户密码

```
passwd admin
```

4.切换目录

```shell
#~当前用户目录
cd ~
cd ./文件夹   #切换到当前目录的某个文件夹 ./表示当前目录
cd ..         #切换到上级目录   
cd ../文件夹  #切换到上级目录中的某个文件夹
```

5.防火墙相关：

```shell
查看防火墙某个端口是否开放
firewall-cmd --query-port=3306/tcp

开放防火墙端口3306
firewall-cmd --zone=public --add-port=3306/tcp --permanent

查看防火墙状态
systemctl status firewalld

关闭防火墙
systemctl stop firewalld

打开防火墙
systemctl start firewalld

开放一段端口
firewall-cmd --zone=public --add-port=40000-45000/tcp --permanent

查看开放的端口列表
firewall-cmd --zone=public --list-ports
```

6.修改系统时间

inux系统中有两种时钟：
　　系统时钟：由linux内核通过cpu的工作频率进行计时，系统启动时内核会自动读取硬件时钟，然后由系统时钟独立运行，之后所有的linux的指令与函数都是读取系统的时钟设定
　　硬件时钟：主板时钟设备进行计时，可通过bios进行设置。

```
date -s "2021-01-11 10:25:55"
```

7.

```
tar -zxvf demo.tar.gz -C /home 
解压缩tar.gz文件到home的位置
tar

-c: 建立压缩档案

-x：解压

-t：查看内容

-r：向压缩归档文件末尾追加文件

-u：更新原压缩包中的文件

这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。

-z：有gzip属性的

-j：有bz2属性的

-Z：有compress属性的

-v：显示所有过程

-O：将文件解开到标准输出

下面的参数-f是必须的

-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。

\# tar -cf all.tar *.jpg 

这条命令是将所有.jpg的文件打成一个名为all.tar的包。-c是表示产生新的包，-f指定包的文件名。 

\# tar -rf all.tar *.gif 

这条命令是将所有.gif的文件增加到all.tar的包里面去。-r是表示增加文件的意思。 

\# tar -uf all.tar logo.gif 

这条命令是更新原来tar包all.tar中logo.gif文件，-u是表示更新文件的意思。 

\# tar -tf all.tar 

这条命令是列出all.tar包中所有文件，-t是列出文件的意思 

\# tar -xf all.tar 

这条命令是解出all.tar包中所有文件，-x是解开的意思 
```

3.

```
sudo service sshd status  

查看服务器的ssh服务状态

sudo service sshd start

打开ssh服务
```

\4. scp /Documents/test.txt optadmin@服务器名:/home/optadmin/tmp/ 

将文件test.txt文件放到服务器上的tmp目录下

5.supervisorctl -c /virus/supervisor/supervisord.conf

查看

restart workflow

重启数据流

6.netstat -anlp | grep 50000

查看50000端口是否被占用，如果被占用会显示占用信息

\7. date -s 20140712	或者 	date -s 18:30:50

修改系统时间

8.cat /app/appversion|head -n 1

查看文件的第一行

9.ls | grep -P "test-[1-2]{0,1}[0-9].jpg" | xargs -d"\n" rm

批量删除

10.重启命令：

1、reboot

2、shutdown -r now 立刻重启(root用户使用)

3、shutdown -r 10 过10分钟自动重启(root用户使用)

4、shutdown -r 20:35 在时间为20:35时候重启(root用户使用)

如果是通过shutdown命令设置重启的话，可以用shutdown -c命令取消重启

关机命令：

1、halt   立刻关机

2、poweroff  立刻关机

3、shutdown -h now 立刻关机(root用户使用)

4、shutdown -h 10 10分钟后自动关机

如果是通过shutdown命令设置关机的话，可以用shutdown -c命令取消重启

\11. bash和sh：bash算是更强力的sh

\12. rm -rf MyDocuments

删除MyDocuments且不提示

rmdir MyDocuments

删除空目录

13.ps -ef | grep nginx

查看 Nginx的服务pid等信息

kill -9 pid编号

强制停止对应的进程

14.开启ngsoc.target任务

```
systemctl start ngsoc.target
```

15.ll和ls

ll：罗列出当前文件或目录的详细信息，含有时间、读写权限、大小、时间等信息 ，像Windows显示的详细信息。ll是“ls -l"的别名。相当于Windows里的快捷方式。可以理解为 ll 和 ls -l 的功能是相同的， ll 是 ls -l 的别名。

16.查看历史命令

history 

17.查找文件

```shell
find   path   -option   [   -print ]   [ -exec   -ok   command ]   {} \;

将当前目录及其子目录下所有文件后缀为 .c 的文件列出来:
find . -name "*.c"

查找系统中所有文件长度为 0 的普通文件，并列出它们的完整路径：
find / -type f -size 0 -exec ls -l {} \;


```

