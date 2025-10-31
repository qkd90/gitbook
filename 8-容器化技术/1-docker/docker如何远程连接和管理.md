## 远程docker地址 端口默认是2375

如果远程docker没有开启2375端口是链接不上的下面是配置docker端口方法

```shell
1. 编辑docker.service
vim /usr/lib/systemd/system/docker.service
找到 ExecStart字段修改如下
#ExecStart=/usr/bin/dockerd-current -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock 
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock

2. 重启docker重新读取配置文件，重新启动docker服务
systemctl daemon-reload
systemctl restart docker

3. 开放防火墙端口
firewall-cmd --zone=public --add-port=6379/tcp --permanent

4.刷新防火墙
firewall-cmd --reload

5.再次配置远程docker就可以了
6.如果重启不起来 估计是这个 unix://var/run/docker.sock 文件位置不对 
find / -name docker.sock 查找一下正确位置就好了
```
