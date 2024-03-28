## linux下nginx基本命令

### nginx指定配置文件启动

```
/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
```

```javascript
cd /usr/local/nginx/sbin/
./nginx 
./nginx -s stop
./nginx -s quit
./nginx -s reload
```

复制

./nginx -s quit:此方式停止步骤是待nginx进程处理任务完毕进行停止。 ./nginx -s stop:此方式相当于先查出nginx进程id再使用kill命令强制杀掉进程。

查询nginx进程

```javascript
ps aux|grep nginx
```

复制

重启 nginx 1.先停止再启动（推荐）： 对 nginx 进行重启相当于先停止再启动，即先执行停止命令再执行启动命令。如下：

```javascript
./nginx -s quit
./nginx
```

复制

### 2.重新加载配置文件：

当 ngin x的配置文件 nginx.conf 修改后，要想让配置生效需要重启 nginx，使用-s reload不用先停止 ngin x再启动 nginx 即可将配置信息在 nginx 中生效，如下：

./nginx -s reload

启动成功后，在浏览器可以看到这样的页面：

## **Windows下Nginx的启动、停止等命令**

在Windows下使用Nginx，我们需要掌握一些基本的操作命令，比如：启动、停止Nginx服务，重新载入Nginx等，下面我就进行一些简单的介绍。

假设你安装在 C:\server\nginx-1.0.2目录下，

cmd命令进入安装文件；

**1、启动：**

C:\server\nginx-1.0.2>start nginx

或

C:\server\nginx-1.0.2>nginx.exe

注：建议使用第一种，第二种会使你的cmd窗口一直处于执行中，不能进行其他命令操作。

**2、停止：**

C:\server\nginx-1.0.2>nginx.exe -s stop

或

C:\server\nginx-1.0.2>nginx.exe -s quit

注：stop是快速停止nginx，可能并不保存相关信息；quit是完整有序的停止nginx，并保存相关信息。

**3、重新载入Nginx：**

C:\server\nginx-1.0.2>nginx.exe -s reload

当配置信息修改，需要重新载入这些配置时使用此命令。

**4、重新打开日志文件：**

C:\server\nginx-1.0.2>nginx.exe -s reopen

**5、查看Nginx版本：**

C:\server\nginx-1.0.2>nginx -v