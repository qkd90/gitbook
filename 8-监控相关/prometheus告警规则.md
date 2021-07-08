# prometheus告警规则

1.prometheus自身监控

```
  - alert: PrometheusJobMissing
    expr: absent(up{job="prometheus"})
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Prometheus自身job不在线 (instance {{ $labels.instance }})      
      description: "Prometheus自身job不在线\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

 - alert: PrometheusAllTargetsMissing
    expr: count by (job="prometheus") (up) == 0
    for: 0m
    labels:
      severity: critical
    annotations:
      summary: Prometheus的job中所有目标掉线 (instance {{ $labels.instance }})
      description: "Prometheus的job中所有目标掉线\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: PrometheusConfigurationReloadFailure
    expr: prometheus_config_last_reload_successful != 1
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Prometheus 配置重载失败 (instance {{ $labels.instance }})
      description: "Prometheus 配置重载失败\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: PrometheusTooManyRestarts
    expr: changes(process_start_time_seconds{job=~"prometheus|pushgateway|alertmanager"}[15m]) > 2
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Prometheus重启太多次 (instance {{ $labels.instance }})
      description: "Prometheus在15分钟内重启超过两次. 可能进入了崩溃循环.\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: PrometheusAlertmanagerConfigurationReloadFailure
    expr: alertmanager_config_last_reload_successful != 1
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Prometheus AlertManager 配置重载失败 (instance {{ $labels.instance }})
      description: "AlertManager 配置重载失败\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: PrometheusAlertmanagerConfigNotSynced
    expr: count(count_values("config_hash", alertmanager_config_hash)) > 1
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Prometheus AlertManager 配置未同步 (instance {{ $labels.instance }})
      description: "AlertManager集群实例配置不同步\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"
```

2.linux主机监控

```
  - alert: HostOutOfMemory
    expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 20
    for: 1m
    labels:
      severity: warning
    annotations:
      summary:主机内存使用率大于80% (instance {{ $labels.instance }})
      description: "主机内存使用率大于80%\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostMemoryUnderMemoryPressure
    expr: rate(node_vmstat_pgmajfault[1m]) > 1000
    for: 2m
    labels:
      severity: warning
    annotations:
      summary:主机内存压力大(instance {{ $labels.instance }})
      description: "节点内存压力很大,主要页面错误率高\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostUnusualNetworkThroughputIn
    expr: sum by (instance) (rate(node_network_receive_bytes_total[2m])) / 1024 / 1024 > 100
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: 主机异常接受数据 (instance {{ $labels.instance }})
      description: "主机网络接口可能接收了太多数据 (> 100 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostUnusualNetworkThroughputOut
    expr: sum by (instance) (rate(node_network_transmit_bytes_total[2m])) / 1024 / 1024 > 100
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: 主机异常上传数据 (instance {{ $labels.instance }})
      description: "主机网络接口可能发送了太多数据 (> 100 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostUnusualDiskReadRate
    expr: sum by (instance) (rate(node_disk_read_bytes_total[2m])) / 1024 / 1024 > 50
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: 主机异常磁盘读取率 (instance {{ $labels.instance }})
      description: "磁盘可能读取太多数据 (> 50 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostUnusualDiskWriteRate
    expr: sum by (instance) (rate(node_disk_written_bytes_total[2m])) / 1024 / 1024 > 50
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: 主机异常磁盘写入率 (instance {{ $labels.instance }})
      description: "磁盘可能写入了太多数据 (> 50 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  # Please add ignored mountpoints in node_exporter parameters like
  # "--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|run)($|/)".
  # Same rule using "node_filesystem_free_bytes" will fire when disk fills for non-root users.
  - alert: HostOutOfDiskSpace
    expr: (node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes < 20 and ON (instance, device, mountpoint) node_filesystem_readonly == 0
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: 主机磁盘空间不足 (instance {{ $labels.instance }})
      description: "磁盘使用率大于80%\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostUnusualDiskReadLatency
    expr: rate(node_disk_read_time_seconds_total[1m]) / rate(node_disk_reads_completed_total[1m]) > 0.1 and rate(node_disk_reads_completed_total[1m]) > 0
    for: 2m
    labels:
      severity: warning
    annotations:
      summary:主机异常磁盘读取延迟 (instance {{ $labels.instance }})
      description: "磁盘读取延迟一直增加 (read operations > 100ms)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostUnusualDiskWriteLatency
    expr: rate(node_disk_write_time_seconds_total[1m]) / rate(node_disk_writes_completed_total[1m]) > 0.1 and rate(node_disk_writes_completed_total[1m]) > 0
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: 主机异常磁盘写入延迟 (instance {{ $labels.instance }})
      description: "磁盘写入延迟一直增加 (write operations > 100ms)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostHighCpuLoad
    expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100) > 80
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: 主机 CPU 负载高于80%(instance {{ $labels.instance }})
      description: "CPU 负载高于80%\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostSystemdServiceCrashed
    expr: node_systemd_unit_state{state="failed"} == 1
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: 主机 systemd 服务崩溃 (instance {{ $labels.instance }})
      description: "主机 systemd 服务崩溃 \n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"



  - alert: HostNetworkReceiveErrors
    expr: rate(node_network_receive_errs_total[2m]) / rate(node_network_receive_packets_total[2m]) > 0.01
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: Host Network Receive Errors (instance {{ $labels.instance }})
      description: "Host {{ $labels.instance }} interface {{ $labels.device }} has encountered {{ printf \"%.0f\" $value }} receive errors in the last five minutes.\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostNetworkTransmitErrors
    expr: rate(node_network_transmit_errs_total[2m]) / rate(node_network_transmit_packets_total[2m]) > 0.01
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: 主机网络传输错误(instance {{ $labels.instance }})
      description: "主机 {{ $labels.instance }} interface {{ $labels.device }} 在过去五分钟内已经遭遇 {{ printf \"%.0f\" $value }}传输错误\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostNetworkInterfaceSaturated
    expr: (rate(node_network_receive_bytes_total{device!~"^tap.*"}[1m]) + rate(node_network_transmit_bytes_total{device!~"^tap.*"}[1m])) / node_network_speed_bytes{device!~"^tap.*"} > 0.8
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: 主机网络接口饱和(instance {{ $labels.instance }})
      description: "网络接口 \"{{ $labels.interface }}\" 在 \"{{ $labels.instance }}\" 已经过载.\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostConntrackLimit
    expr: node_nf_conntrack_entries / node_nf_conntrack_entries_limit > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: 主机连接限制(instance {{ $labels.instance }})
      description: "主机状态监测数量接近极限\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: HostClockSkew
    expr: (node_timex_offset_seconds > 0.05 and deriv(node_timex_offset_seconds[5m]) >= 0) or (node_timex_offset_seconds < -0.05 and deriv(node_timex_offset_seconds[5m]) <= 0)
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: 主机时钟偏差 (instance {{ $labels.instance }})
      description: "检测到时钟偏差,时钟不同步.\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

```

