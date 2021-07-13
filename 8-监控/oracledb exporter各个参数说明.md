# oracledb exporter各个参数说明

1.oracledb_sessions_value	当前会话连接数

```
oracledb_sessions_value{status="ACTIVE",type="BACKGROUND"} 47
oracledb_sessions_value{status="ACTIVE",type="USER"} 3
oracledb_sessions_value{status="INACTIVE",type="USER"} 30
```

2.oracledb_max_utilization	oracledb_limit_value	

若LIMIT_VALU-MAX_UTILIZATION<=5，则表明与RESOURCE_NAME相关的Oracle初始化参数需要调整。可以通过修改Oracle初始化参数文件$ORACLE_BASE/admin/CKDB/pfile/initORCL.ora来修改。

3.