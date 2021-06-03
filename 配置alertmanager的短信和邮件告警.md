### 配置alertmanager的短信,邮件,微信告警

#### 1.修改配置文件 alertmanager.yml

```
global:
  #全局配置，设置邮件的相关信息
  smtp_from: 'xxx@qq.com'
  smtp_smarthost: 'smtp.qq.com:465'
  smtp_auth_username: 'xxxx@qq.com'
  smtp_auth_password: 'xxxx'	#授权码
  smtp_require_tls: false
  smtp_hello: 'qq.com'  

route:   # route用来设置报警的分发策略
  group_by: ['alertname']  # 采用哪个标签来作为分组依据
  group_wait: 10s   # 组告警等待时间。也就是告警产生后等待10s，如果有同组告警一起发出
  group_interval: 10s  # 两组告警的间隔时间
  repeat_interval: 20m  # 重复告警的间隔时间，减少相同邮件的发送频率
  receiver: 'default-receiver'  # 设置默认接收人
  routes:   # 可以指定哪些组接手哪些消息
  - receiver: 'default-receiver'  
    continue: true
    group_wait: 10s
  - receiver: 'fping-receiver'  
    group_wait: 10s
    match_re:  #根据标签分组，匹配标签dest=szjf的为fping-receiver组
      dest: szjf

receivers:
- name: 'default-receiver'
  email_configs:
  - to: 'xxxxxxxx@qq.com'
- name: "fping-receiver"
  webhook_configs:
  - url: 'http://127.0.0.1:9095/dingtalk'
    send_resolved: true
```

即为全局设置，在 **Alertmanager** 配置文件中，只要全局设置配置了的选项，全部为公共设置，可以让其他设置继承，作为默认值，可以子参数中覆盖其设置。其中 `resolve_timeout` 用于设置处理超时时间，也是生命警报状态为解决的时间， 这个时间会直接影响到警报恢复的通知时间，需要自行结合实际生产场景来设置主机的恢复时间，默认是5分钟。在全局设置中可以设置smtp服务，同时也支持slack、victorops、pagerduty等，在这里只讲我们常用的Email，钉钉，企业微信， 同时也可以自己使用go语言开发的gubot进行二次开发，对接自定义webhook通知源。

#### 2.修改prometheus的配置文件

中间部分修改如下，其他不动

```
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - localhost:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  #自己编写的告警发送规则文件
  - "/usr/local/rq/prometheus/node-up.rules"
  
```

![image-20210512135548320](C:\Users\rq\AppData\Roaming\Typora\typora-user-images\image-20210512135548320.png)

#### 3.建立node-up.rules文件

该文件控制告警的内容，内存大于80，cpu大于70，磁盘大于70的时候报警

```
groups:
- name: test
  rules:
  - alert: 内存使用率过高
    expr: 100-(node_memory_Buffers_bytes+node_memory_Cached_bytes+node_memory_MemFree_bytes)/node_memory_MemTotal_bytes*100 > 80 
    for: 1m  # 告警持续时间，超过这个时间才会发送给alertmanager
    labels:
      severity: warning
    annotations:
      summary: "Instance {{ $labels.instance }} 内存使用率过高"
      description: "{{ $labels.instance }} of job {{$labels.job}}内存使用率超过阈值,当前使用率{{ $value }}%."

  - alert: cpu使用率过高
    expr: 100-avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance)*100 > 70
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "Instance {{ $labels.instance }} cpu使用率过高"
      description: "{{ $labels.instance }} of job {{$labels.job}}cpu使用率超过阈值,当前使用率{{ $value }}%."
      # 尽可能把详细告警信息写入summary标签值，因为告警短信/邮件/钉钉发送的内容使用了summary标签中的值。

  - alert: 磁盘使用率过高
    expr: (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 > 70
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "Instance {{ $labels.instance }} 磁盘使用率过高"
      description: "{{ $labels.instance }} of job {{$labels.job}}磁盘使用率过高超过阈值,当前使用率{{ $value }}%."
      # 尽可能把详细告警信息写入summary标签值，因为告警短信/邮件/钉钉发送的内容使用了summary标签中的值。    

```

#### 3.springboot进行请求的代码

在web_demo_jar里面，直接运行sendsms脚本

#### 4.告警邮件和短信的模板

![image-20210512112107316](C:\Users\rq\AppData\Roaming\Typora\typora-user-images\image-20210512112107316.png)

![image-20210512154229564](C:\Users\rq\AppData\Roaming\Typora\typora-user-images\image-20210512154229564.png)

