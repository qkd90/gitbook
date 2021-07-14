# mysql exporter各个参数说明

## 1.连接数和线程数

mysql_global_status_max_used_connections	连接数

mysql_global_status_threads_connected	线程数

## 2.每秒io处理次数（iops）

node_disk_read_bytes_total    主机接受字节数	+	node_disk_written_bytes_total	主机发送字节数

## 3.每秒事务数（tps）

mysql_global_status_handlers_total{handler="commit"}	+	mysql_global_status_handlers_total{handler="rollback"}

## 4.每秒查询数（qps）

mysql_global_status_queries

## 5.网络带宽

mysql_global_status_bytes_received	接受字节数	+	mysql_global_status_bytes_sent	发送字节数

