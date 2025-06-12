### centos7 设置MongoDB开机自启动

1在/usr/lib/systemd/system/目录下新建mongodb.service文件，内容如下：

```
[Unit] 
   
Description=mongodb  
After=network.target remote-fs.target nss-lookup.target 
   
[Service] 
Type=forking 
ExecStart=/root/mongodb/bin/mongod --config  /root/mongodb/bin/mongodb.conf
ExecReload=/bin/kill -s HUP $MAINPID 
ExecStop=/root/mongodb/bin/mongod --shutdown --config  /root/mongodb/bin/mongodb.conf
PrivateTmp=true 
     
[Install] 
WantedBy=multi-user.target
```

2.启动服务

```
systemctl daemon-reload
systemctl start mongodb
systemctl status mongodb
#开机启动    
systemctl enable mongodb.service
```

3.