### Prometheus+Alertmanager+Granfan监控告警平台

#### 1.安装组件基本介绍：

**prometheus:**

server端守护进程，负责拉取各个终端exporter收集到metrics（监控指标数据），并记录在本身提供的tsdb时序记录数据库中，默认保留天数15天，可以通过启动参数自行设置数据保留天数。

prometheus官方提供了多种exporter,对外提供web图形查询页面，以及数据库查询访问接口。配置监控规则rules（需自行手动配置），并将触发规则的告警发送至alertmanager ，并由alertmanager中配置的告警媒介向外发送告警。

默认监听9090端口

**grafana：**

由于prometheus本身提供的图形页面过于简陋，所以使用grafana来提供图形页面展示。

grafana 是专门用于图形展示的软件，支持多种数据来源，prometheus只是其中一种。

自带告警功能，且告警规则可在监控图形上直接配置，不过由于此种方式不支持模板变量（dashboard中为了方便展示配置的特殊变量），即每一个指标，每一台设备均需要单独配置，所以实用性较低

默认监听端口：3000

**node_exporter:**

agent端，prometheus官方提供的诸多exporter中的一种，安装与各监控节点主机

负责抓取主机及系统各项信息，如cpu，mem ,disk,networtk.filesystem，...等等各项基本指标，非常全面。并将抓取到的各项指标metrics 通过http协议对方发布，供prometheus server端抓取。

默认监听端口： 9100

**oracle_exporter:**

适用于Oracle的Prometheus导出器，以MySQL导出器为模型。我不是DBA或经验丰富的Go开发人员，因此PR绝对受到欢迎。

##### 1.1通用准备工作

```
#上传到新建的rq文件夹，我有一个压缩包会包括所有的安装包
cd /usr/local/rq

#权限问题，每次添加了文件之后记得赋予权限
cd /usr/local
sudo chmod -R 777 rq

#上传服务文件
cd /usr/lib/systemd/system/

```



#### 2.prometheus-server

##### 2.1基本信息：

- 官方文档地址：[https://prometheus.io/docs/introduction/overview/](https://link.zhihu.com/?target=https%3A//prometheus.io/docs/introduction/overview/)
- github项目下载地址： [https://github.com/prometheus/prometheus](https://link.zhihu.com/?target=https%3A//github.com/prometheus/prometheus)

##### 2.2 安装 prometheus server

- 创建unit file，让systemd 管理prometheus

```shell
 cd /usr/lib/systemd/system
 上传prometheus.service这个文件
 [Unit]
 Description=The Prometheus 2 monitoring system and time series database.
 Documentation=https://prometheus.io
 After=network.target
 [Service]
 EnvironmentFile=-/etc/sysconfig/prometheus   #文件
 User=root
 ExecStart=/usr/local/prometheus/prometheus \
 --storage.tsdb.path=/home/prometheus/prometheus \
 --config.file=/usr/local/prometheus/prometheus.yml \
 --web.listen-address=0.0.0.0:9090 \
 --web.external-url= $PROM_EXTRA_ARGS
 Restart=on-failure
 StartLimitInterval=1
 RestartSec=3
 [Install]
 WantedBy=multi-user.target
```

- 其他运行时参数： ./prometheus --help
- 启动服务

```text
systemctl daemon-reload
systemctl start prometheus.service
systemctl status prometheus.service
```

- 注意开启防火墙端口：

```text
#新增开放一个端口号
firewall-cmd --zone=public --add-port=9100/tcp --permanent
重启防火墙
firewall-cmd --reload
查看所有打开端口
firewall-cmd  --list-ports

firewall-cmd --zone=external --add-forward-port=port=9001:proto=tcp:toport=9100:toaddr=192.168.1.30 --permanent
```

- 浏览器访问：

```text
http://IP:PORT
```

```
防火墙操作参考：
#说明:
#–zone #作用域
#–add-port=80/tcp #添加端口，格式为：端口/通讯协议
#–permanent 永久生效，没有此参数重启后失效
#多个端口:
firewall-cmd --zone=public --add-port=80-90/tcp --permanent
#查看端口是否被占用
lsof -i:9100
```

##### 2.3问题排查



#### 3.node_exporter

##### 3.1基本

node_exporter 在被监控节点安装，抓取主机监控信息，并对外提供http服务，供prometheus抓取监控信息。
项目及文档地址：https://github.com/prometheus/node_exporter
prometheus官方提供了很多不同类型的exporter，列表地址： https://prometheus.io/docs/inst

##### 3.2 安装node_exporter

- 下载并解压

```text
cd /usr/local

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

##### 3.3 配置node_exporter

- 开启关闭collectors:

```text
./node_exporter --help  # 查看支持的所有collectors，可根据实际需求 enable 和 disabled 各项指标收集

如 --collector.cpu=disabled ，不再收集cpu相关信息
```

- Textfile Collector： 文本文件收集器

```text
通过 启动参数 --collector.textfile.directory="DIR" 可开启文本文件收集器
收集器会收集目录下所有*.prom的文件中的指标，指标必须满足 prom格式
```

示例:

```text
echo my_batch_job_completion_time $(date +%s) > /path/to/directory/my_batch_job.prom.$$
mv /path/to/directory/my_batch_job.prom.$$ /path/to/directory/my_batch_job.prom   
echo 'role{role="application_server"} 1' > /path/to/directory/role.prom.$$
mv /path/to/directory/role.prom.$$ /path/to/directory/role.prom 
rpc_duration_seconds{quantile="0.5"} 4773
http_request_duration_seconds_bucket{le="0.5"} 129389
```

即如果node_exporter 不能满足自身指标抓取，可以通过脚本形式将指标抓取之后写入文件，由node_exporter对外提供个prometheus抓取 可以省掉pushgateway

- 有关prom格式和查询语法，将再之后介绍

##### 3.4 配置prometheus抓取node_exporter 指标

- 示例： prometheus.yml

```text
scrape_configs:
# The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
- job_name: 'prometheus'
 # metrics_path defaults to '/metrics'
 # scheme defaults to 'http'.
 static_configs:
 - targets: ['localhost:9090']
- job_name: 'nodes'
 static_configs:
 - targets: ['localhost:9100']
 - targets: ['172.20.94.1:9100']

- job_name: 'node_real_lan'
file_sd_configs:
 - files:
- ./sd_files/real_lan.yml
refresh_interval: 30s
params:   # 可选
collect[]:
 - cpu
 - meminfo
 - diskstats
 - netdev
 - netstat
 - filefd
 - filesystem
 - xfs
```

#### 4.grafana

##### **4.1 官方地址**

- grafana程序下载地址：[https://grafana.com/grafana/download](https://link.zhihu.com/?target=https%3A//grafana.com/grafana/download)
- grafana dashboard 下载地址： [https://grafana.com/grafana/download/](https://link.zhihu.com/?target=https%3A//grafana.com/grafana/download/)

##### **4.2 安装grafana**

###### 4.2.1 linux(centos7)安装

- 下载并安装

```text
cd /usr/local/rq/
yum clean all
yum --installroot=/usr/local/rq localinstall –y --skip-broken ./* grafana-7.4.5-1.x86_64.rpm
```

- 准备service 文件：

```text
[Unit]
Description=Grafana instance
Documentation=http://docs.grafana.org
Wants=network-online.target
After=network-online.target
After=postgresql.service mariadb.service mysqld.service

[Service]
EnvironmentFile=/etc/sysconfig/grafana-server
User=grafana
Group=grafana
Type=notify
Restart=on-failure
WorkingDirectory=/usr/share/grafana
RuntimeDirectory=grafana
RuntimeDirectoryMode=0750
ExecStart=/usr/sbin/grafana-server  \
 --config=${CONF_FILE}  \
 --pidfile=${PID_FILE_DIR}/grafana-server.pid\
 --packaging=rpm  \
 cfg:default.paths.logs=${LOG_DIR}  \
 cfg:default.paths.data=${DATA_DIR} \
 cfg:default.paths.plugins=${PLUGINS_DIR} \
 cfg:default.paths.provisioning=${PROVISIONING_CFG_DIR}

LimitNOFILE=10000
TimeoutStopSec=20

[Install]
WantedBy=multi-user.target
```

- 启动grafana

```text
systemctl enable grafana-server.service
systemctl restart grafana-server.service
```

默认监听3000端口

- 开启防火墙：

```text
firewall-cmd --zone=public --add-port=3000/tcp --permanent
```

##### 4.3 grafana 简单使用流程

- web页面访问：

```text
http://ip:port
```

首次登陆会要求自行设置账号密码 7.2版本会要求输入账号密码之后重置，初始账号密码都是admin

- 使用流程：

- 添加数据源:   http://localhost:9090

- 添加dashboard，配置图形监控面板，也可在官网下载对应服务的dashboard模板，下载地址：[https://grafana.com/grafana/download/](https://link.zhihu.com/?target=https%3A//grafana.com/grafana/download/)

- 导入模板，json 或 链接 或模板编号

- 查看dashboard

- 常用模板编号：

- node-exporter： cn/8919,en/11074

- k8s: 13105

- docker: 12831

- alertmanager: 9578

- blackbox_exportre: 9965

- 重置管理员密码：

  ```
  查看Grafana配置文件，确定grafana.db的路径
   配置文件路径：/etc/grafana/grafana.ini
   [paths]
   ;data = /var/lib/grafana
   [database]
   # For "sqlite3" only, path relative to data_path setting
   ;path = grafana.db
  通过配置文件得知grafana.db的完整路径如下：
   /var/lib/grafana/grafana.db
  
  使用sqlites修改admin密码 
   sqlite3 /var/lib/grafana/grafana.db
   sqlite> update user set password = 
  '59acf18b94d7eb0694c61e60ce44c110c7a683ac6a8f09580d626f90f4a242000746579358d77dd9e570e83fa24faa88a8a6', 
  salt = 'F3FAxVm33R' where login = 'admin';
   .exit
  使用admin admin 登录
  ```

#### **5.alertmanager**

##### 5.1 prometheus + alertmanager 报警过程

- 文档地址：[https://prometheus.io/docs/alerting/latest/configuration/](https://link.zhihu.com/?target=https%3A//prometheus.io/docs/alerting/latest/configuration/)
- 设置警报和通知的主要步骤是：
- 安装和配置 Alertmanager
- 配置Prometheus与Alertmanager对话
- 在Prometheus中创建警报规则

##### 5.2 安装alertmanager

linux（centos7）安装：

- 下载地址： [https://github.com/prometheus/alertmanager](https://link.zhihu.com/?target=https%3A//github.com/prometheus/alertmanager)
- 下载并安装：

```text
wget https://github.com/prometheus/alertmanager/releases/download/v0.20.0/
alertmanager-0.20.0.linux-amd64.tar.gz
tar -xf alertmanager-0.20.0.linux-amd64.tar.gz -C /usr/local
cd /usr/local && ln -sv alertmanager-0.20.0.linux-amd64/ alertmanager && cd alertmanager
```

启动：

```text
nohup ./alertmanager --config.file="alertmanager.yml" --storage.path="data/ --web.listen-address=":9093" &
```

##### 5.3 核心概念

- grouping: 分组
- 分组将类似性质的警报分类为单个通知。当许多系统同时发生故障并且可能同时触发数百到数千个警报时，此功能特别有用。

示例：

```text
发生网络分区时，群集中正在运行数十个或数百个服务实例。您有一半的服务实例不再可以访问数据库。
Prometheus中的警报规则配置为在每个服务实例无法与数据库通信时为其发送警报。结果，数百个警报被发送到Alertmanager。
作为用户，人们只希望获得一个页面，同时仍然能够准确查看受影响的服务实例。因此，可以将Alertmanager配置为按警报的群集和
警报名称分组警报，以便它发送一个紧凑的通知。
```

- 警报的分组，分组通知的时间以及这些通知的接收者由配置文件中的路由树（routing tree）配置。
- Inhibition： 抑制
- 抑制是一种概念，如果某些其他警报已经触发，则抑制某些警报的通知。
- 示例：

```text
正在触发警报，通知您无法访问整个群集。可以将Alertmanager配置为使与该群集有关的所有其他警报静音。这样可以防止与实际问题无关的数百或数千个触发警报的通知。
```

- 通过Alertmanager的配置文件配置禁止。
- Silences： 静默
- 静默是一种简单的方法，可以在给定时间内简单地使警报静音。沉默是根据匹配器配置的，就像路由树一样。检查传入警报是否与活动静默的所有相等或正则表达式匹配项匹配。
- 如果这样做，则不会针对该警报发送任何通知。

##### 5.4 配置prometheus对接alertmanager

- alerting：

```text
alerting:
alertmanagers:
- static_configs:
 - targets: ["127.0.0.1:9093"]
```

- rule_files:

```text
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
- "rules/*.yml"
```

- scrape_configs:

```text
scrape_configs:   
- job_name: 'alertmanager'
 static_configs:
- targets: ['127.0.0.1:9093']
```

##### 5.5 prometheus rules编写

- 示例：

```text
[root@xiang-03 /usr/local/prometheus]#cat rules/node.yml 
groups:
- name: "system info"
 rules:
- alert: "服务器宕机"    # 告警名称 alertname
expr: up == 0    # 告警表达式，当表达式条件满足，即发送告警
for: 1m     # 等待时长，等待自动恢复的时间。
labels:  # 此label不同于 metric中的label，发送给alertmanager之后用于管理告警项，比如匹配到那个label即触发哪种告警
 severity: critical   # key:value 皆可完全自定义
annotations:     # 定义发送告警的内容，注意此地的labels为metric中的label
 summary: "{ {$labels.instance} }:服务器宕机"
 description: "{ {$labels.instance} }:服务器无法连接，持续时间已超过3mins"
- alert: "CPU 使用过高"
expr: 100-(avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))by(instance)*100) > 40
for: 1m
labels:
 servirity: warning
annotations:
 summary: "{ {$labels.instance} }:CPU 使用过高"
 description: "{ {$labels.instance} }:CPU 使用率超过 40%"
 value: "{ {$value} }"
- alert: "CPU 使用率超过90%"
expr: 100-(avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) by(instance)* 100) > 90
for: 1m
labels:
 severity: critical
annotations:
 summary: "{ {$labels.instance} }:CPU 使用率90%"
 description: "{ {$labels.instance} }:CPU 使用率超过90%，持续时间超过5mins"
 value: "{ {$value} }"
```

- 如果需要在配置文件中使用中文，务必注意编码规则为utf8，否则报错

##### 5.6 配置alertmanager

- 详细文档地址： [https://prometheus.io/docs/alerting/latest/configuration/](https://link.zhihu.com/?target=https%3A//prometheus.io/docs/alerting/latest/configuration/)
- 主配置文件： alertmanager.yml
- 模板配置文件： *.tmpl
- 只是介绍少部需要用到的配置，如需查看完整配置，请查看官方文档

###### 5.6.1 alertmanager.yml

- 主配置文件中需要配置：
- global: 发件邮箱配置，
- templates: 指定邮件模板文件（如果不指定，则使用alertmanager默认模板），
- routes： 配置告警规则，比如匹配哪个label的规则发送到哪个后端
- receivers： 配置后端告警媒介： email，wechat，webhook等等
- 先看示例：

```text
vim alertmanager.yml
global:
smtp_smarthost: 'xxx'
smtp_from: 'xxx'
smtp_auth_username: 'xxx'
smtp_auth_password: 'xxx'
smtp_require_tls: false
templates:
- '/alertmanager/template/*.tmpl'
route:
receiver: 'default-receiver'
group_wait: 1s #组报警等待时间
group_interval: 1s  #组报警间隔时间
repeat_interval: 1s  #重复报警间隔时间
group_by: [cluster, alertname]
routes:
- receiver: test
 group_wait: 1s
 match_re:
severity: test
receivers:
- name: 'default-receiver'
email_configs:
- to: 'xx@xx.xx'
 html: '{ { template "xx.html" . } }'
 headers: { Subject: " { { .CommonAnnotations.summary } }" }
- name: 'test'
email_configs:
- to: 'xxx@xx.xx'
 html: '{ { template "xx.html" . } }'
 headers: { Subject: " { { 第二路由匹配测试} }" } 

vim test.tmpl
{ { define "xx.html" } }
<table border="5">
 <tr><td>报警项</td>
<td>磁盘</td>
<td>报警阀值</td>
<td>开始时间</td>
 </tr>
 { { range $i, $alert := .Alerts } }
<tr><td>{ { index $alert.Labels "alertname" } }</td>
<td>{ { index $alert.Labels "instance" } }</td>
<td>{ { index $alert.Annotations "value" } }</td>
<td>{ { $alert.StartsAt } }</td>
</tr>
 { { end } }
</table>
{ { end } }
```

- 详解：

```text
gloable： 

resolve_timeout:    # 在没有报警的情况下声明为已解决的时间
```

- 其他邮件相关配置，如示例

```text
route：  # 所有报警信息进入后的根路由，用来设置报警的分发策略

group_by: ['LABEL_NAME','alertname', 'cluster','job','instance',...]
```

这里的标签列表是接收到报警信息后的重新分组标签，例如，接收到的报警信息里面有许多具有 cluster=A 和alertname=LatncyHigh 这样的标签的报警信息将会批量被聚合到一个分组里面

```text
group_wait: 30s
```

当一个新的报警分组被创建后，需要等待至少group_wait时间来初始化通知，这种方式可以确保您能有足够的时间为同一分组来获取多个警报，然后一起触发这个报警信息。

```text
group_interval: 5m
```

当第一个报警发送后，等待'group_interval'时间来发送新的一组报警信息。

```text
repeat_interval: 5m 
```

如果一个报警信息已经发送成功了，等待'repeat_interval'时间来重新发送他们

```text
match： 
 label_name: NAME
```

匹配报警规则，满足条件的告警将被发给 receiver

```text
match_re:
 label_name: <regex>, ... 
```

正则表达式匹配。满足条件的告警将被发给 receiver

```text
receiver: receiver_name
```

将满足match 和 match_re的告警发给后端 告警媒介（邮件，webhook，pagerduty，wechat，...） 必须有一个default receivererr="root route must specify a default receiver"

```text
routes:
 - <route> ...
```

配置多条规则。

```text
  templates：
   [ - <filepath> ... ]
```

 配置模板，比如邮件告警页面模板

```text
  receivers:
   - <receiver> ...# 列表

- name： receiver_name  # 用于填写在route.receiver中的名字 

 email_configs:   # 配置邮件告警

 - to: <tmpl_string>
send_resolved: <boolean> | default = false   # 故障恢复之后，是否发送恢复通知
```

配置接受邮件告警的邮箱，也可以配置单独配置发件邮箱。 详见官方文档 [https://prometheus.io/docs/alerting/latest/configuration/#email_config](https://link.zhihu.com/?target=https%3A//prometheus.io/docs/alerting/latest/configuration/%23email_config)

```text
- name: ...
  wechat_configs:
  - send_resolved: <boolean> | default = false
 
 api_secret: <secret> | default = global.wechat_api_secret
 api_url: <string> | default = global.wechat_api_url
 corp_id: <string> | default = global.wechat_api_corp_id
 message: <tmpl_string> | default = '{ { template "wechat.default.message" . } }'
 
 agent_id: <string> | default = '{ { template "wechat.default.agent_id" . } }'
 
 to_user: <string> | default = '{ { template "wechat.default.to_user" . } }'
 to_party: <string> | default = '{ { template "wechat.default.to_party" . } }'
 to_tag: <string> | default = '{ { template "wechat.default.to_tag" . } }'    
 # 说明
  to_user: 企业微信用户ID
  to_party: 需要发送的组id
  
  corp_id: 企业微信账号唯一ID 可以在 我的企业 查看       
  agent_id: 应用的 ID，应用管理 --> 打开自定应用查看
  api_secret: 应用的密钥
  
  打开企业微信注册 https://work.weixin.qq.com
  微信API官方文档 https://work.weixin.qq.com/api/doc#90002/90151/90854 
```

###### 5.6.2配置企业微信告警

```text

```

#### 6.oracle-explorer

##### 6.1 运行oracle exporter

解压安装文件到 /usr/local/rq



在启动之前，请确保正确设置了环境变量DATA_SOURCE_NAME。DATA_SOURCE_NAME应该采用Oracle EZCONNECT格式：

https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/configuring-naming-methods.html#GUID-B0437826-43C1-49EC-A94D-B650B6A4A6EE

```
新建一个oracle账户
create user monitor identified by monitor;
赋予账户权限
grant connect, resource to monitor;

直接运行命令：
export DATA_SOURCE_NAME="monitor/monitor@//192.168.0.185:1521/orcl"

同时需要在oracle目录配置 .bash_profile,使用我配置好的文件
然后运行
source .bash_profile

添加
然后使用脚本运行：
sh oracle_exporter.sh

碰到 pinging oracle: empty dsn
export DATA_SOURCE_NAME=C##test/123456@//192.168.18.203:1521/ORCLCDB

碰到 error while loading shared libraries: libclntsh.so.18.1: cannot open shared object file: No such file or directory
配置
export LD_LIBRARY_PATH=/opt/oracle/product/19c/dbhome_1/lib/

```

##### 6.2 orcle相关操作

```
Oracle用户下输入
sqlplus / as sysdba
连接test账户
conn test/123456
```

![下载 (1)](C:\Users\rq\Desktop\下载 (1).jpg)
