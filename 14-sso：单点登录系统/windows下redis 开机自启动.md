1，在redis的目录下执行（执行后就作为windows服务了）
 redis-server.exe --service-install redis.windows.conf

2，安装好后需要手动启动redis
 redis-server.exe --service-start

3，停止服务
 redis-server.exe --service-stop

4，卸载redis服务
 redis-server.exe --service-uninstall

#### 设置Redis的密码

##### 进入Redis的安装目录打开：redis.windows-conf，按下Ctrl+F查找：requirepass，找到编辑保存然后重新启动Redis服务即可。（注意：这里是redis.windows-conf，windows自启动会加载这个配置文件）。

#### 绑定Redis的IP



