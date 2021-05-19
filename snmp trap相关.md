#### snmp trap相关



##### SNMP的基本知识介绍

简单网络管理协议（SNMP－Simple Network Management Protocol) 是一个与网络设备交互的简单方法。SNMP代理提供大量的对象标识符（OID－ObjectIdentifiers）一个OID是一个唯一的键值对。该代理存放这些值并让它们可用。一个SNMP管理器（客户）可以向代理查询键值对中的特定信息。从程序员的角度看，这和导入大量的全局变量没有多少区别。SNMP的OID是可读或可写的。尽管向一个SNMP设备写入信息的情况非常少，但它是各种管理应用程序用来控制设备的方法（例如针对交换机的可管理GUI）。SNMP中有一个基本的认证框架，能够让管理员发送公共名来对OID读取或写入的认证。绝大多数的设备使用不安全的公共名 "public" 。 SNMP协议通过UDP端口161和162进行通信的。

##### MIB和OID

OID(对象标识符），是SNMP代理提供的具有唯一标识的键值。MIB（管理信息基）提供数字化OID到可读文本的映射。

##### snmptrap命令生成

```shell
/home/fantom/party/snmp/bin/snmptrap -v1 -c public 10.222.10.112 1.3.6.1.4.1.1 10.222.10.112 1 1 0 .1.3.6.1.2.1.1.1.0 s 'test device SysDesc'

/home/fantom/party/snmp/bin/snmptrap -v 2c -c public 10.222.10.112 1.3.6.1.4.1.2345 SNMPv2-MIB\:\:sysLocation.0 s 'just here'
```

| snmptrap                    | 命令               |
| --------------------------- | ------------------ |
| -v 2c<br />-v1              | Snmp协议版本       |
| -c public                   | 共同体             |
| 10.222.10.112               | snmp代理的IP       |
| "aaa"                       | 主机名称, 可以为空 |
| 1.3.6.1.4.1.2345            | Enterprise-OID     |
| SNMPv2-MIB\:\:sysLocation.0 | 数据OID            |
| s                           | 数据类型           |
| "This is a test"            | 数据值             |

![image-20210112130654131](C:\Users\User\AppData\Roaming\Typora\typora-user-images\image-20210112130654131.png)



##### snmp trap安装配置