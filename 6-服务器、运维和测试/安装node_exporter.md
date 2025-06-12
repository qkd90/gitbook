##### 安装node_exporter

- 安装

```shell
#新建一个rq文件夹在下面的路径
cd /usr/local/rq
#上传压缩文件里面的node-export
#进入system里面把node exporter的service文件上传
cd /usr/lib/systemed/system
#执行压缩文件里面的脚本chmod.sh
cd /usr/local/rq/node_exporter
sh chmod.sh
```

- 启动服务：

```text
systemctl daemon-reload
systemctl start node_exporter.service
systemctl status node_exporter.service
```

- 可以手动测试是否可以获取metrics信息：

```text
curl http://localhost:9100/metrics
```

- 开启防火墙：

  ```
  firewall-cmd --zone=public --add-port=9100/tcp --permanent
  ```

##### 