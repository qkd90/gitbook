


## 一、window和linux启动

### 1、[Nacos](https://so.csdn.net/so/search?q=Nacos&spm=1001.2101.3001.7020) 下载

Nacos 下载地址：https://github.com/alibaba/nacos/releases

官方网站： https://nacos.io/zh-cn/docs/quick-start.html

### 2、nacos 配置 MySQL 数据库

- 将 nacos 目录下的 config/nacos-mysql.sql 导入到MySQL，库名随便指定
- 修改 config/application.properties 文件配置 MySQL 数据库

```bash
#*************** Config Module Related Configurations ***************#
### If use MySQL as datasource:
spring.datasource.platform=mysql

### Count of DB:
db.num=1

### Connect URL of DB:
db.url.0=jdbc:mysql://127.0.0.1:3306/nacos_config?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&serverTimezone=UTC
db.user.0=root
db.password.0=123456
1234567891011
```

### 3、启动 nacos

开启 nacos

```bash
Linux/Unix/Mac
启动命令(standalone代表着单机模式运行，非集群模式):

sh startup.sh -m standalone

如果您使用的是ubuntu系统，或者运行脚本报错提示[[符号找不到，可尝试如下运行：

bash startup.sh -m standalone

Windows
启动命令(standalone代表着单机模式运行，非集群模式):

startup.cmd -m standalone
12345678910111213
```

访问地址 http://127.0.0.1:8848/nacos ，默认登陆用户名密码 nacos/nacos，新增命名空间，新建配置文件如下
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734278.png)

## 二、docker启动

### 1、docker 拉取 nacos镜像

DockerHub 下载镜像 https://registry.hub.docker.com/r/nacos/nacos-server

```bash
docker pull nacos/nacos-server
```

### 2、初始化 MySQL 数据库脚本

https://github.com/alibaba/nacos/blob/develop/distribution/conf/nacos-mysql.sql

不知道为啥现在阿里没有脚本了，nacos数据库脚本.sql如下

```sql
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info   */
/******************************************/
CREATE TABLE `config_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) DEFAULT NULL,
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  `c_desc` varchar(256) DEFAULT NULL,
  `c_use` varchar(64) DEFAULT NULL,
  `effect` varchar(64) DEFAULT NULL,
  `type` varchar(64) DEFAULT NULL,
  `c_schema` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfo_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info';

/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_aggr   */
/******************************************/
CREATE TABLE `config_info_aggr` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) NOT NULL COMMENT 'group_id',
  `datum_id` varchar(255) NOT NULL COMMENT 'datum_id',
  `content` longtext NOT NULL COMMENT '内容',
  `gmt_modified` datetime NOT NULL COMMENT '修改时间',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfoaggr_datagrouptenantdatum` (`data_id`,`group_id`,`tenant_id`,`datum_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='增加租户字段';


/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_beta   */
/******************************************/
CREATE TABLE `config_info_beta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL COMMENT 'content',
  `beta_ips` varchar(1024) DEFAULT NULL COMMENT 'betaIps',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfobeta_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info_beta';

/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_tag   */
/******************************************/
CREATE TABLE `config_info_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `tenant_id` varchar(128) DEFAULT '' COMMENT 'tenant_id',
  `tag_id` varchar(128) NOT NULL COMMENT 'tag_id',
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfotag_datagrouptenanttag` (`data_id`,`group_id`,`tenant_id`,`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info_tag';

/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_tags_relation   */
/******************************************/
CREATE TABLE `config_tags_relation` (
  `id` bigint(20) NOT NULL COMMENT 'id',
  `tag_name` varchar(128) NOT NULL COMMENT 'tag_name',
  `tag_type` varchar(64) DEFAULT NULL COMMENT 'tag_type',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `tenant_id` varchar(128) DEFAULT '' COMMENT 'tenant_id',
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`nid`),
  UNIQUE KEY `uk_configtagrelation_configidtag` (`id`,`tag_name`,`tag_type`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_tag_relation';

/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = group_capacity   */
/******************************************/
CREATE TABLE `group_capacity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `group_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'Group ID，空字符表示整个集群',
  `quota` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配额，0表示使用默认值',
  `usage` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用量',
  `max_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个配置大小上限，单位为字节，0表示使用默认值',
  `max_aggr_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '聚合子配置最大个数，，0表示使用默认值',
  `max_aggr_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值',
  `max_history_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大变更历史数量',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='集群、各Group容量信息表';

/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = his_config_info   */
/******************************************/
CREATE TABLE `his_config_info` (
  `id` bigint(64) unsigned NOT NULL,
  `nid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `data_id` varchar(255) NOT NULL,
  `group_id` varchar(128) NOT NULL,
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL,
  `md5` varchar(32) DEFAULT NULL,
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00',
  `src_user` text,
  `src_ip` varchar(20) DEFAULT NULL,
  `op_type` char(10) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`nid`),
  KEY `idx_gmt_create` (`gmt_create`),
  KEY `idx_gmt_modified` (`gmt_modified`),
  KEY `idx_did` (`data_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='多租户改造';


/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = tenant_capacity   */
/******************************************/
CREATE TABLE `tenant_capacity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `tenant_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'Tenant ID',
  `quota` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配额，0表示使用默认值',
  `usage` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用量',
  `max_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个配置大小上限，单位为字节，0表示使用默认值',
  `max_aggr_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '聚合子配置最大个数',
  `max_aggr_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值',
  `max_history_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大变更历史数量',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='租户容量信息表';


CREATE TABLE `tenant_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `kp` varchar(128) NOT NULL COMMENT 'kp',
  `tenant_id` varchar(128) default '' COMMENT 'tenant_id',
  `tenant_name` varchar(128) default '' COMMENT 'tenant_name',
  `tenant_desc` varchar(256) DEFAULT NULL COMMENT 'tenant_desc',
  `create_source` varchar(32) DEFAULT NULL COMMENT 'create_source',
  `gmt_create` bigint(20) NOT NULL COMMENT '创建时间',
  `gmt_modified` bigint(20) NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tenant_info_kptenantid` (`kp`,`tenant_id`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='tenant_info';

CREATE TABLE users (
    username varchar(50) NOT NULL PRIMARY KEY,
    password varchar(500) NOT NULL,
    enabled boolean NOT NULL
);

CREATE TABLE roles (
    username varchar(50) NOT NULL,
    role varchar(50) NOT NULL,
    constraint uk_username_role UNIQUE (username,role)
);

CREATE TABLE permissions (
    role varchar(50) NOT NULL,
    resource varchar(512) NOT NULL,
    action varchar(8) NOT NULL,
    constraint uk_role_permission UNIQUE (role,resource,action)
);

INSERT INTO users (username, password, enabled) VALUES ('nacos', '$2a$10$EuWPZHzz32dJN7jexM34MOeYirDdFAZm2kuWj7VEOJhhZkDrxfvUu', TRUE);

INSERT INTO roles (username, role) VALUES ('nacos', 'ROLE_ADMIN');
```

### 3、docker 启动 nacos（配置 MySQL 连接）

```bash
docker run -d \
-e PREFER_HOST_MODE=ip \
-e MODE=standalone \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=192.168.18.17 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_DB_NAME=nacos \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=Trasen@8812 \
-e NACOS_APPLICATION_PORT=8848 \
-p 8848:8848 -p 9848:9848 -p 9849:9849 \
--name nacos \
--restart=always \
--privileged=true \
nacos/nacos-server:v2.4.3
```

命令解释：

```shell
参数解释：
docker run -d：以分离模式（后台运行）启动容器。

-e PREFER_HOST_MODE=ip：设置Nacos优先使用IP模式。

-e MODE=standalone：指定Nacos以单机模式运行。

-e SPRING_DATASOURCE_PLATFORM=mysql：指定数据源平台为MySQL。

-e MYSQL_SERVICE_HOST=192.168.18.17：MySQL数据库的主机地址。

-e MYSQL_SERVICE_PORT=3306：MySQL数据库的端口号。

-e MYSQL_SERVICE_DB_NAME=nacos：MySQL数据库的名称。

-e MYSQL_SERVICE_USER=root：MySQL数据库的用户名。

-e MYSQL_SERVICE_PASSWORD=Trasen@8812：MySQL数据库的密码。

-e NACOS_APPLICATION_PORT=8848：Nacos应用的端口号。

-p 8848:8848：将容器的8848端口映射到宿主机的8848端口。

-p 9848:9848：将容器的9848端口映射到宿主机的9848端口。

-p 9849:9849：将容器的9849端口映射到宿主机的9849端口。

--name nacos：为容器指定名称为nacos。

--restart=always：设置容器在退出时总是重启。

--privileged=true：赋予容器特权模式，可以访问宿主机的所有设备。

nacos/nacos-server:v2.4.3：指定使用的Nacos镜像及其版本号（v2.4.3）。
```

访问地址： http://192.168.18.17:8848/nacos   默认用户名密码： nacos/nacos，新增命名空间，新建配置文件如下
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734278.png)

### 4、解决问题

#### 1.Nacos Server did not start because dumpservice bean construction failure : No DataSource set

保证数据库连接正确，查看数据库名、刷新数据库连接、检查用户名密码、可加长连接超时时间、设置时区

#### 2.server error: such as timeout. Request nacos server failed

如果是云服务器需要开启 8848、 9848 、9849 端口否则报错 server error: such as timeout. Request nacos server failed:
端口说明：https://nacos.io/zh-cn/docs/2.0.0-compatibility.html

Nacos2.0 （8848、 9848 、9849 ）版本相比 1.X （8848）新增了gRPC的通信方式，因此需要增加2个端口。新增端口是在配置的主端口(server.port)基础上，进行一定偏移量自动生成。

| 端口 | 与主端口的偏移量 | 描述                                                         |
| ---- | ---------------- | ------------------------------------------------------------ |
| 8848 |                  | nacos 主端口号                                               |
| 9848 | 1000             | 客户端 gRPC 请求服务端端口，用于客户端向服务端发起连接和请求 |
| 9849 | 1001             | 服务端 gRPC 请求服务端端口，用于服务间同步等                 |

## 三、docker nacos 集群搭建

拉取镜像和初始化 nacos 数据库和上面的单机模式相同，以下 docker nacos 最新 2.0.4 版本部署成功，云服务器防火墙配置下面用到的端口

### 1、启动集群

注意需要开启 7848 端口，默认端口 8848 减去 1000，否则会报The Raft Group [naming_persistent_service] did not find the Leader node; 

或Nacos cluster is running with 1.X mode, can't accept gRPC request temporarily. Please check the server status or close Double write to force open 2.0 mode. Detail https://nacos.io/en-us/docs/2.0.0-upgrading.html.

或caused: old raft protocol already stop;

172.18.200.132 服务器 nacos1

```bash
docker run -itd \
--privileged=true \
-e PREFER_HOST_MODE=ip \
-e MODE=cluster \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=172.18.200.132 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_DB_NAME=nacos \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=Trasen@8812 \
-e NACOS_APPLICATION_PORT=8848 \
-e NACOS_SERVERS=172.18.200.132:8848,172.18.200.133:8848,172.18.200.134:8848 \
-e NACOS_SERVER_IP=172.18.200.132 \
-p 8848:8848 -p 9848:9848 -p 9849:9849 -p 7848:7848 \
--name nacos1 --restart=always nacos/nacos-server:v2.2.0
```

192.168.1.1 服务器 nacos 2

```bash
docker run -d\
 -e PREFER_HOST_MODE=ip\
 -e MODE=cluster\
 -e SPRING_DATASOURCE_PLATFORM=mysql\
 -e MYSQL_SERVICE_HOST=172.18.200.133\
 -e MYSQL_SERVICE_PORT=3306\
 -e MYSQL_SERVICE_DB_NAME=nacos\
 -e MYSQL_SERVICE_USER=root\
 -e MYSQL_SERVICE_PASSWORD=Trasen@8812\
 -e NACOS_APPLICATION_PORT=8848\
 -e NACOS_SERVERS="172.18.200.132:8848 172.18.200.133:8848 172.18.200.134:8848"\
 -e NACOS_SERVER_IP=172.18.200.133\
 -p 8846:8846 -p 9846:9846 -p 9847:9847 -p 7848:7848\
 --name nacos2 --restart=always nacos/nacos-server:v2.2.0
```

192.168.1.2 服务器 nacos3

```bash
docker run -d\
 -e PREFER_HOST_MODE=ip\
 -e MODE=cluster\
 -e SPRING_DATASOURCE_PLATFORM=mysql\
 -e MYSQL_SERVICE_HOST=172.18.200.134\
 -e MYSQL_SERVICE_PORT=3306\
 -e MYSQL_SERVICE_DB_NAME=nacos\
 -e MYSQL_SERVICE_USER=root\
 -e MYSQL_SERVICE_PASSWORD=Trasen@8812\
 -e NACOS_APPLICATION_PORT=8848\
 -e NACOS_SERVERS="172.18.200.132:8848 172.18.200.133:8848 172.18.200.134:8848"\
 -e NACOS_SERVER_IP=172.18.200.134\
 -p 8848:8848 -p 9848:9848 -p 9849:9849 -p 7848:7848\
 --name nacos3 --restart=always nacos/nacos-server:v2.2.0
```

###### 注意：

v2.2.1+最新版本配置文件中需要增加配置，不然启动报错，具体内容看issues

https://github.com/alibaba/nacos/issues/10130

### 2、查看集群

此时 随便进一个服务地址 即可
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734217.png)
上面的状态全部是 up 不一定集群搭建成功，点击节点元数据查看是否能选取 leader
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734303.png)
或者使用接口获取 leader

http://192.168.1.1:8080/nacos/v1/ns/raft/leader，更多 nacos 相关 API 可参考 https://nacos.io/zh-cn/docs/open-api.html
![在这里插入图片描述](https://img-blog.csdnimg.cn/86c75ad93d9e42168e97ad95096a757a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LiN5oeC5LiA5LyR,size_20,color_FFFFFF,t_70,g_se,x_16)
如果不能选取 leader， 可以查看 nacos/logs 目录下的 nacos.log、 naming-raft.log、protocol-raft.log、nacos-cluster.log 、naming-server.log 日志看是否报错

### 3、nginx 代理 nacos 集群

docker 下载启动 nginx 容器不做阐述

如果你已经挂载了 nginx 的配置文件直接修改即可，没有挂载也可以进入容器修改

default.conf 我配置的比较简单，权重自己配置

```conf
upstream nacosList {
    server 192.168.1.1:8848 weight=1;
	server 192.168.1.2:8848 weight=2;
	server 192.168.1.1:8846 weight=3;
}

server {
    listen       80;
    listen  [::]:80;
    server_name  192.168.1.1;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
    location /nacos {
        proxy_pass  http://nacosList/nacos;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
123456789101112131415161718192021222324
```

我的 nginx 8080 映射 80，如下 nginx f负载均衡成功
![在这里插入图片描述](https://img-blog.csdnimg.cn/c24cf99d8e0a4ac3ae3c557efe022e86.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LiN5oeC5LiA5LyR,size_20,color_FFFFFF,t_70,g_se,x_16)

### 4、关闭双写

nacos 文档说明关闭双写可以节省性能开销
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734322.png)
PUT : http://192.168.1.1:8848/nacos/v1/ns/operator/switches?entry=doubleWriteEnabled&value=false
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734480.png)
logs/naming-server.log 日志中观察到 Disable Double write, stop and clean v1.x cache and features字样，说明关闭双写。
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734880.png)

### 5、服务上下线

nacos 控制台注册的服务可以正常上下线
![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202212091734443.png)