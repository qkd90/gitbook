#  Hyperledger Cello的rq使用手册

## 1.简介

![Typical Scenario](https://cello.readthedocs.io/en/latest/images/scenario.png)

Hyperledger Cello (HLC) 是一个区块链供应和运营系统，它帮助人们以更有效的方式使用和管理区块链。

Cello 基于先进的区块链技术和现代 PaaS 工具，提供以下主要功能：

- 管理区块链网络的生命周期，例如，创建/开始/停止/删除/保持健康自动地。
- 支持自定义区块链网络配置，例如网络规模、共识类型。
- 支持多种底层基础架构，包括裸机、虚拟机、vSphere、本地[Docker](https://www.docker.com/)主机、swarm 和[Kubernetes](https://kubernetes.io/)。更多支持正在路上。
- 通过与[ElasticStack](https://www.elastic.co/)等现有工具集成，扩展了监控、日志记录、健康和分析能力等高级功能。

使用 Cello，区块链开发人员可以：

- 从头开始快速构建区块链即服务 (BaaS) 平台。
- 立即提供可定制的区块链，例如 Hyperledger Fabric v1.x 网络。
- 检查系统状态和管理链，上传智能合约和测试......通过仪表板。
- 在裸机、虚拟云（例如，虚拟机、vsphere 云）、容器集群（例如，Docker、Swarm、Kubernetes）之上维护一个正在运行的区块链网络池。

## 2.cello架构介绍

**Hyperledger Cello主要分为两大模块，master和worker，遵循典型的Master-Workers架构。**

**Master**：持有Cello服务，通过相应的管理API管理Workers内的区块链网络。通常，主节点提供Web仪表板（端口8080）和RESTful API（端口80）。建议使用Linux（例如，Ubuntu 18.04）作为Master。
**Worker**：用于保存区块链网络的节点。Cello支持worker node从单个服务器到群集的多种类型。

### 2.2 Master安装

该master包括几种服务：
1、operator dashboard：为运营商提供Web UI。
2、user dashboard：为用户提供Web UI。
3、engine：为连锁消费者提供RESTful API。
4、watchdog：注意健康检查。

**系统要求**（无论是master节点还是worker节点系统要求都是一样的）
1、硬件：8c16g100g（8c16g100g是官方给的标准。当前使用的硬件为4核8G，暂时没有出现问题）
2、Linux内核> = 3.0.0
3、Docker引擎：1.10.0+（Docker 18.0+支持是实验性的）
4、docker-compose：1.10.0+

## 3.创建一套区块链系统的完整流程

### 3.1 准备工作

安装docker

安装docker-compose

### 3.2部署流程

1.获取项目代码

```
git clone https://github.com/hyperledger/cello -b release-0.9.0-h3c
```

2.编译版本镜像，直接进入代码目录，执行make docker

![img](https://img-blog.csdnimg.cn/20200929134833339.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

3.版本编译完成后的查看结果，如下：

![img](https://img-blog.csdnimg.cn/20200929134922249.png)

4.执行make start，即可启动cello，效果如下图：

![img](https://img-blog.csdnimg.cn/20200929135452669.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

5.这时候可以通过docker ps命令查看启动的docker

![img](https://img-blog.csdnimg.cn/20200929142632460.png)

6.可以通过浏览器访问cello的operator-dashboard管理界面了。

在此之前，需要打开本机的2375端口，供创建主机使用，脚本如下：

```
docker run -d -v /var/run/docker.sock:/var/run/docker.sock -p 0.0.0.0:2375:2375 bobrik/socat TCP-LISTEN:2375,fork UNIX-CONNECT:/var/run/docker.sock
```

执行成功后，效果如下：

![img](https://img-blog.csdnimg.cn/2020092914382481.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

7.在主机中安装执行apt-get install nfs-common，进入到script/worker_node目录执行./setup.sh

![img](https://img-blog.csdnimg.cn/20200929144446826.png)

8.cello已经安装完毕，在浏览器中输入:http://服务器ip/8071，界面如下：

![img](https://img-blog.csdnimg.cn/20200929142726865.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

默认用户名和密码是admin/pass

登陆后的界面如下：

![img](https://img-blog.csdnimg.cn/20200929142844845.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

这个时候，可以通过界面搭建区块链网络了。

点击主机管理--〉添加，出现如下界面

![img](https://img-blog.csdnimg.cn/20200929143108348.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

在“名称”中输入需要创建的主机名，在“服务地址”中输入本机的ip:2375,其他选项默认，然后点击“提交”,成功后，效果如下

![img](https://img-blog.csdnimg.cn/20200929144748990.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击“组织管理”-〉“添加”，分别创建一个peer组织和一个orderer组织，如下

![img](https://img-blog.csdnimg.cn/20200929145037595.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/20200929145135126.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

创建成功后的效果如下：

![img](https://img-blog.csdnimg.cn/20200929150435507.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击网络管理->新建网络，创建一个区块链网络

![img](https://img-blog.csdnimg.cn/20200929151441798.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击提交后效果如下：![img](https://img-blog.csdnimg.cn/20200929151528139.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

等片刻后，在主机上通过docker ps命令可以看到peer orderer ca节点都已经启动

![img](https://img-blog.csdnimg.cn/20200929151713555.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

此时可以登陆user-dashboard，在浏览器导航栏输入http://主机ip:8081,如下

![img](https://img-blog.csdnimg.cn/202009291522217.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

回到operator-dashboard，在用户管理中找到创建组织的时候自动生成的组织用户，默认密码是666666，登陆user-dashboard后的效果如下

![img](https://img-blog.csdnimg.cn/20200929160112200.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击通道管理->创建通道，创建一个通道如下：

![img](https://img-blog.csdnimg.cn/2020092916025772.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击“提交”后，生成通道，效果如下：

![img](https://img-blog.csdnimg.cn/20200929160351752.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击“添加节点”，在组织中选择想要的节点添加到通道中，如下

![img](https://img-blog.csdnimg.cn/20200929160544112.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击“提交”，节点添加成功后的效果如下

![img](https://img-blog.csdnimg.cn/20200929160655888.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击“链码管理”->"上传链码"，选择一个链码压缩包上传，需要注意，链码压缩包需要连同所在目录一块压缩成zip格式上传，同时需要计算压缩包的md5值

![img](https://img-blog.csdnimg.cn/20200929160959832.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

上传成功后，点击“安装”，把链码安装到通道的节点中，如下

![img](https://img-blog.csdnimg.cn/20200929161301519.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

回到主机串口下，执行docker pull hyperledger/fabric-ccenv:1.4.2，然后把镜像的tag修改成latest，docker tag fc0f502399a6 hyperledger/fabric-ccenv:latest

![img](https://img-blog.csdnimg.cn/2020092916233347.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

点击“实例化链码”，配置通道，实例化参数，以及背书策略

![img](https://img-blog.csdnimg.cn/20200929161416660.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

链码实例化成功后，整个区块链系统的搭建已经完成，此时可以验证链码的执行效果

点击"通道管理"->“通道详情”->"实例化链码列表"，选择对应的链码，然后输入invoke或者query参数，即可验证效果

![img](https://img-blog.csdnimg.cn/20200929162900550.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/20200929163007392.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3J0eGll,size_16,color_FFFFFF,t_70)

在图上的示例中使用了fabric官方的example 02的例子，通过a给b转帐的动作来演示链码的执行效果。
