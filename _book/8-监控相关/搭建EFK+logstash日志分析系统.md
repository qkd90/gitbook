### 搭建EFK+logstash日志分析系统

EFK不是一个软件，而是一套解决方案，并且都是开源软件，之间互相配合使用，完美衔接，高效的满足了很多场合的应用，是目前主流的一种日志系统。EFK是三个开源软件的缩写，分别表示：Elasticsearch , FileBeat, Kibana , 其中ELasticsearch负责日志保存和搜索，FileBeat负责收集日志，Kibana 负责界面,当然EFK和大名鼎鼎的ELK只有一个区别，那就是EFK把ELK的Logstash替换成了FileBeat，因为Filebeat相对于Logstash来说有2个好处：
 1、侵入低，无需修改程序目前任何代码和配置
 2、相对于Logstash来说性能高，Logstash对于IO占用很大

当然FileBeat也并不是完全好过Logstash，毕竟Logstash对于日志的格式化这些相对FileBeat好很多，FileBeat只是将日志从日志文件中读取出来，当然如果你日志本身是有一定格式的，FileBeat也可以格式化，但是相对于Logstash来说，还是差一点

**Elasticsearch**

Elasticsearch是个开源分布式搜索引擎，提供搜集、分析、存储数据三大功能。它的特点有：分布式，零配置，自动发现，索引自动分片，索引副本机制，restful风格接口，多数据源，自动搜索负载等。

**FileBeat**

Filebeat隶属于Beats。目前Beats包含六种工具：
 Packetbeat（搜集网络流量数据）
 Metricbeat（搜集系统、进程和文件系统级别的 CPU 和内存使用情况等数据）
 Filebeat（搜集文件数据）
 Winlogbeat（搜集 Windows 事件日志数据）
 Auditbeat（ 轻量型审计日志采集器）
 Heartbeat（轻量级服务器健康采集器）

**Kibana**

Kibana可以为 Logstash 、Beats和 ElasticSearch 提供的日志分析友好的 Web 界面，可以帮助汇总、分析和搜索重要数据日志。

![EFK架构图](https://upload-images.jianshu.io/upload_images/1783810-fb619da96567824d.png?imageMogr2/auto-orient/strip|imageView2/2/w/704/format/png)

#### 安装Elasticsearch

注意安装Elasticsearch之前需要有java8的环境，查看java版本

```
java -version
```

下载Elasticsearch，本文以Elasticsearch6.2.4为例，当前Elasticsearch最新版本为Elasticsearch6.4.0，注意Elasticsearch、Kibana、FileBeat一定要使用相同的版本

```ruby
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.tar.gz
```

解压

```css
tar -zxvf elasticsearch-6.2.4.tar.gz
```

进入Elasticsearch主目录，修改配置

```undefined
vi config/elasticsearch.yml
```

添加以下配置，或者将对应的配置注释取消修改，如果不修改配置会报错：

```
You must address the points described in the following lines before starting Elasticsearch.\nbootstrap check failure [1] of [1]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
```



```css
#对外开放地址
network.host: 0.0.0.0 
# 对外开放访问端口
http.port: 9200
# 集群名称
cluster.name: cluster-name
# 跨域支持
http.cors.enabled: true
# 初始化时master节点的选举列表
cluster.initial_master_nodes: [ "node-name" ]
```

由于Elasticsearch不能使用root用户打开，所以需要专门创建一个用户来启动Elasticsearch

```css
$ adduser elastic
#设置密码
$ passwd elastic
#需要输入2次密码
#授权
$ chmod -R 777 /usr/local/elasticsearch-6.2.4
#切换用户
$ su elastic
```

创建的用户名为elastic，其中/usr/local/elasticsearch-6.2.4为解压出来的Elasticsearch主目录

启动Elasticsearch

```undefined
./bin/elasticsearch
```

