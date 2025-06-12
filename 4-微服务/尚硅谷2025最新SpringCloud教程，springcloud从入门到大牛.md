参考文档，尚硅谷：

https://www.yuque.com/leifengyang/sutong/oz4gbyh5maa0rmxu

## 3. Nacos - 注册/配置中心

### 3.1安装

1.docker方式：

```
docker run -d -p 8848:8848 -p 9848:9848 -e MODE=standalone --name nacos nacos/nacos-server:v2.4.3
```

### 3.2注册中心

 

### 3.3配置中心

![image-20250208165356614](https://raw.githubusercontent.com/qkd90/figureBed/main/202502081653699.png)

#### 3.3.1命名空间：namespace

##### 1、创建命名空间

打开nacos控制台，点击左侧命名空间标题，可以看到命名空间名称列表中有一个默认的public，public命名空间是nacos的保留空间，默认namespace对应ID为空。即不设置命名空间时候，默认的注册都在public空间下。回过头再看 nacos服务注册与发现 这篇博文的工程测试部分，在nacos-provider和nacos-client工程都启动成功后，nacos管理台看到的注册情况如下

默认的服务列表都在public空间下面，分组名称为默认分组DEFAULT_GROUP。

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202502081702772.jpeg)

那如何创建一个新的命名空间呢，在nacos控制台左侧的命名空间标题，点开后，点击新建命名空间，可以看到弹出的新建命名空间窗口。

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202502081702888.jpeg)

一个nacos注册中心的命名空间名具有唯一性，即命名空间名不可以重复。新建命名空间时候，如果不填写命名空间id，则系统会自动生成命名空间id，生成规则为UUID方式。

这里，我们创建一个空间名为dev，空间id为3bab8e9d-972c-4b11-a44f-74714ac7f471的开发环境命名空间。

##### 2、命名空间工程中使用

增加命名空间后，代码中须要配置命名空间id，代码中不配置命名空间名称。故在之前的配置文件中，增加如下命名空间配置项

```
--- # nacos 配置
spring:
  cloud:
    nacos:
      # nacos 服务地址
      server-addr: @nacos.server@
      username: @nacos.username@
      password: @nacos.password@
      discovery:
        # 注册组
        group: @nacos.discovery.group@
        namespace: ${spring.profiles.active}
      config:
        # 配置组
        group: @nacos.config.group@
        # 命名空间
        namespace: ${spring.profiles.active}
  config:
    import:
      - optional:nacos:application-common.yml
      - optional:nacos:${spring.application.name}.yml
```

${spring.profiles.active} =3bab8e9d-972c-4b11-a44f-74714ac7f471

启动nacos-client和nacos-provider工程

启动nacos-client工程的时候，启动日志里面有关nacos注册中心内容有如下日志信息

[REGISTER-SERVICE] 3bab8e9d-972c-4b11-a44f-74714ac7f471 registering service DEFAULT_GROUP@@nacos-client with instance: {"clusterName":"DEFAULT","enabled":true,"ephemeral":true,"healthy":true,"instanceHeartBeatInterval":5000,"instanceHeartBeatTimeOut":15000,"ip":"192.168.187.1","ipDeleteTimeout":30000,"metadata":{"preserved.register.source":"SPRING_CLOUD"},"port":8081,"weight":1.0}
可以清晰看到，注册信息中包含了命名空间id信息 3bab8e9d-972c-4b11-a44f-74714ac7f471。