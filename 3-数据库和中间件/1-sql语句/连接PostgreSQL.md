# 连接PostgreSQL

连接数据库也可以分为两种：

1. 命令行连接，即PostgreSQL自带的psql命令行工具
2. 图形工具连接，即各种软件开发商提供的客户端工具，常用的有PgAdmin，navicate for postgresql，前者是一款免费工具，后者是一款收费工具。大家根据自己的需要使用。

下面我们分别介绍这两种连接方式。

## 1. 命令行连接

通过Linux系统平台的命令行界面或Windows系统平台的cmdline界面进行连接。在上一章的内容中，我们安装了两个软件包，分别是 postgresql96 和 postgresql96-server 。postgresql96为我们提供了连接数据库工具的客户端软件psql，postgresql96-server 是服务端软件。psql命令有两种格式，分别是：

```
psql postgres://username:password@host:port/dbname  
psql -U username -h hostname -p port -d dbname 
```

先解释第一个命令格式里各个参数：

- username：连接数据的用户名，默认值是postgres
- password：密码，默认值是postgres
- host：主机名，默认值是localhost
- port：端口，默认值是5432
- dbname：要连接的数据库名，默认值是postgres

第二个命令的各个参数：

- -U username 用户名，默认值postgres
- -h hostname 主机名，默认值localhost
- -p port 端口号，默认值5432
- -d dbname 要连接的数据库名，默认值postgres

但是在知道了这个命令的基本用法以后，却并不能直接连接到刚启动的数据库上，我们先尝试一下：



![img](https://upload-images.jianshu.io/upload_images/3545483-e4812c1a6ae7a604.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/447/format/webp)

image.png



可以看到连接直接失败了，这是为什么呢？从出错信息里我们看到，原因是认证失败。

查看了PostgreSQL的官网文档以后才知道，PostgreSQL安装及初始化完成以后，在它的配置文件里，默认只允许本机连接，而且连接到服务器的认证方式是peer和ident。如下图所示：



![img](https://upload-images.jianshu.io/upload_images/3545483-5e4c339f90528d12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/522/format/webp)

image.png



这个配置是在data目录下的pg_hba.conf文件里设置的，这个文件里的命令格式解释如下：

- TYPE：指的是连接类型，一般有local和host两种，local指的是本地连接，host指的是从远程主机连接或本地主机的localhost地址连接
- DATABASE：指的是要连接的数据库，all表示所有，还可以使用具体的数据库名，比如postgres
- USER：指的是用来连接的用户名，all表示所有用户，还可以使用具体的用户名，比如postgres
- ADDRESS：指的是连接数据库的客户端IP地址来源，127.0.0.1/32表示只允许来自己本机的连接，0.0.0.0/0表示允许来自所有ip的连接，192.168.1.0/24表示允许192.168.1.1-192.168.1.255这个地址段的ip地址连接
- METHOD：表示连接的时候使用的认证方式，常用的有trust，表示信任所有连接。md5，表示需要连接的客户端提供一个加密密码来登录。

在linux系统上，data目录默认在`/var/lib/psql/9.6/`下。

本地连接非常好理解，就是从安装PostgreSQL的主机上连接，那 peer 和 ident 认证又是怎么回事呢？PostgreSQL的官方文档的官方文档上是这么说的：

peer认证是安装了PostgreSQL服务端的系统，通过getpeereid()函数获取连接客户端的用户名，然后通过map映射来进行客户认证的一种认证方式，要求只能用在客户端和服务端都安装在同一台电脑上时，客户端连接服务端的认证。

ident认证是客户端从一个ident服务器上获取一个用户名，作为连接服务器端数据库的用户的认证方式，也可能用到map映射。这种认证方式只支持TCP/IP连接的方式。

上面的两个认证里都提到了map映射，map映射又指的什么呢？

map映射是用来将系统用户映射到对应的postgres数据库用户，用来限制指定的用户使用指定的账号来登陆。

介绍了这么多概念，可能不是很好理解，我们举个例子说明并实际操作一下就明白了。map映射是在data目录下的`pg_ident.conf`目录里配置的，其基本定义格式如下：

```
# MAPNAME       SYSTEM-USERNAME         PG-USERNAME
mm              root                    postgres
```

- MAPNAME指的是映射的名称
- SYSTEM-USERNAME就是系统用户的名称，比如root
- PG-USERNAME就是数据库里存在的用户名称，比如postgres

上面定义的map意思就是，我定义了一个叫做mm的映射，当客户端用户是root的时候，允许它用postgres用户来登陆。

那么我们来尝试连接一下。先将pg_hba.conf里的连接认证方式修改为下面的格式：



![img](https://upload-images.jianshu.io/upload_images/3545483-75b592645d39b741.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/554/format/webp)

image.png



然后重启PostgreSQL服务，再进行连接。命令如下：

```
systemctl restart postgresql-9.6
psql -U postgres
```

![img](https://upload-images.jianshu.io/upload_images/3545483-c48a06cf99f04444.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/423/format/webp)

image.png



可以看到，此时就能够正常连接了。
我们尝试一下切换到另外一个用户test，然后再使用这个命令连接，命令如下：

```
su - test
psql -U postgres
```



![img](https://upload-images.jianshu.io/upload_images/3545483-fc8bd69b06435efb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/441/format/webp)

image.png


可以看到，此时的用户名不是root，就不能使用postgres用户来连接，提示认证失败。那么再回到root用户，然后尝试一下PostgreSQL另外一种连接方式，命令如下：
`psql postgres://postgres@`

![img](https://upload-images.jianshu.io/upload_images/3545483-59d38549fa1dde7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/366/format/webp)

image.png


从上图中可以看到，可以正常连接。



最后我们总结一下：
（1）.PostgreSQL的连接命令psql有两种连接方式。不带-h参数或host参数时，是local连接，用的是peer认证方式，通过unix或者linux系统的socket进行连接。但是如果使用-h localhost、-h 127.0.0.1、postgres@localhost 或 postgres@127.0.0.1 这样的格式，则会使用host类型，使用TCP/IP的方式连接，使用的是ident的认证方式。我们刚才只修改了peer认证使用map映射，因此ident认证会提示出错，如下所示：



![img](https://upload-images.jianshu.io/upload_images/3545483-231528e09b79eefa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/460/format/webp)

image.png

（2）需要修改配置文件设置好连接方式和认证方式，保证能够正常连接。

上面所有的内容就是命令行连接方式的内容

## 2. 图形界面连接

使用datagrip连接：



下载完成后直接安装，安装的过程就不过多说了，相信安装软件对于大家还是不难的。安装好以后，打开pgAdmin 3的界面，如下所示：

![img](https://upload-images.jianshu.io/upload_images/3545483-5026090ba59e80e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/985/format/webp)

image.png



- 左边的对象浏览器是你的服务器页面，pgAdmin 将服务器分为一个个服务器组，一个组里可以包含多台服务器，便于管理。
- 右边上面位置则是用来显示服务器或服务器中的数据库、表的各种详细信息页面
- 右边下面位置则是用来执行SQL语句的位置，这也是为什么pgAdmin被成为管理和开发平台的原因之一。

点击文件，选择添加服务器：



image.png



在服务器信息页面填写服务器详细信息：

- 名称：你给这个服务器取的名字，比如244服务器

- 主机：服务器的ip地址

- 端口号：默认值5432，如果你的服务器修改了监听的端口好，则可以在这里修改

- 服务：可不填

- 维护数据库：即你要连接的数据库

- 用户名：用来连接的用户名

- 密码：连接的用户的密码

- 颜色：你可以选择一种颜色来标记你的服务器

- 组：为你服务器选择的管理组
  填写完成后如下所示：

  image.png

  点击确定以后就会自动连接数据库，这个过程是默认保存密码的。因此会弹出一个提示，忽略提示即可。但是连接出错了，如下所示：

  image.png

前面我们讲到，刚安装好并初始化完毕后，PostgreSQL服务器默认监听的地址是本地地址，即localhost。而pgAdmin我们一般都是在自己的电脑上安装，然后远程连接到机房的物理服务器上。那怎么允许我们的机器可以连接到PostgreSQL服务器端呢？这里涉及到data目录下两个配置文件：

- postgresql.conf

- pg_hba.conf

  在postgresql.conf中有一个listen_address的配置，它的默认值如下：

  ![img](https://upload-images.jianshu.io/upload_images/3545483-0a8b380878921556.png?imageMogr2/auto-orient/strip|imageView2/2/w/537/format/webp)

  默认监听localhost，这就是为什么刚安装好的PostgreSQL只能在本机上连接的原因。我们将这个地址修改为0.0.0.0或服务器的ip地址，如下所示：

  ```
  listen_addresses = '192.168.1.244'
  ```

  然后重启服务器，查看一下PostgreSQL服务端监听的地址：

  image.png

  可以看到，确实监听在192.168.1.244这个地址上了。这个时候还有一个问题，那就是认证的问题。刚才我们讲过peer和ident两种认证方式，前者只适用于本地连接，而后者则需要从ident服务器上获取用户名。都不适合我们当前的连接方式，那么还需要再修改认证方式，这里要介绍的认证方式是md5和trusted。

md5 认证方式是通过账号密码的方式认证，但是密码的传输过程是使用md5加密的
trust 认证方式则是不进行任何认证，默认信任所有的连接，属于最不安全的一种认证方式。

但是从第一章到现在，我们都没讲过PostgreSQL的密码设置问题，也没有为数据库设置一个密码，那么我们只能先使用trusted的认证方式先连接到数据库上，再考虑修改数据库密码的问题。修改pg_hba.conf中的连接方式如下：
`host all all trust`
重启服务器，再从pgAdmin上连接：

image.png



此时可以连接成功，连接成功后，服务器的信息会出现在左边窗口的服务器组里。双击服务器名称，就能看到服务器的详细信息，如下所示：



image.png

以上就是所有图形工具连接PostgreSQL的内容。

最后来总结一下：
要想成功连接到安装好的数据库上，需要考虑到下面三个配置文件

- pg_hba.conf：用来配置连接位置、认证方式
- postgresql.conf：用来配置服务器端监听的地址和端口，配置选项是listen_addresses和listen_port。
- pg_ident.conf：用来设置ident和peer认证方式的用户名映射

## 3. 需要注意的问题

- 一定要理解本地连接、远程连接的概念以及和pg_hba.conf中的TYPE类型进行对应
- 从自己本机连接服务器上的PostgreSQL的时候，要考虑服务器上面有没有防火墙，如果有的话，要在防火墙上将PostgreSQL监听的端口放开。RHEL7 放开5432端口的命令如下：

```
firewall-cmd --zone=public --add-port=5432/tcp --permanent
firewall-cmd --reload
```