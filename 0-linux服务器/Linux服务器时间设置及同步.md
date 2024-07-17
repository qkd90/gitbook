## **[1 手动设置](http://blog.csdn.net/jesseyoung/article/details/43488351)**

  date命令：
  date :查看当前时间，结果如下：Wed Feb  4 16:29:51 CST 2015
  date -s 16:30:00 :设置当前时间，结果如下：Wed Feb  4 16:30:00 CST 2015
  date -s "YYYY-MM-DD hh:mm[:ss]" 如date -s "2015-02-04 16:30:00"
  hwclock -w（将时间写入bios避免重启失效）

## 2.

  ntpdate命令：
  ntpdate -u 210.72.145.44

 注意：若不加上-u参数， 会出现以下提示：no server suitable for synchronization found
  -u：从man ntpdate中可以看出-u参数可以越过防火墙与主机同步；
  210.72.145.44：中国国家授时中心的官方服务器。

  ntp常用服务器：
  中国国家授时中心：210.72.145.44
  NTP服务器(上海) ：ntp.api.bz
  美国：time.nist.gov 
  复旦：ntp.fudan.edu.cn 
  微软公司授时主机(美国) ：time.windows.com 
  台警大授时中心(台湾)：asia.pool.ntp.org

  经测试中国国家授时中心与NTP上海服务器可以正常同步时间，注意需要加上-u参数！
***\*[3 时区修改](http://blog.csdn.net/jesseyoung/article/details/43488351)\**
  3.1 即时生效**

```crystal
    [root@localhost /]# cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    [root@localhost /]# hwclock
```

  **3.2 重启生效**
  修改/etc/sysconfig/clock文件，把ZONE的值改为Asia/Shanghai，UTC值改为false，改完后的文件如下：

```ruby
# The time zone of the system is defined by the contents of /etc/localtime.
# This file is only for evaluation by system-config-date, do not rely on its
# contents elsewhere.
ZONE="Asia/Shanghai"
UTC=false
ARC=false
```