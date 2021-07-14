# oracledb exporter各个参数说明

## 1.当前会话连接数和连接数

oracledb_sessions_value	会话数

oracledb_process_count	连接数

```
oracledb_sessions_value{status="ACTIVE",type="BACKGROUND"} 47
oracledb_sessions_value{status="ACTIVE",type="USER"} 3
oracledb_sessions_value{status="INACTIVE",type="USER"} 30
```

```
oracledb_process_count 189
```

## 2.Oracle初始化文件中相关参数值

oracledb_max_utilization	oracledb_limit_value	

若LIMIT_VALU-MAX_UTILIZATION<=5，则表明与RESOURCE_NAME相关的Oracle初始化参数需要调整。可以通过修改Oracle初始化参数文件$ORACLE_BASE/admin/CKDB/pfile/initORCL.ora来修改。

## 3.表空间top100

oracledb_size_dba_segments_top100_table_bytes

占用空间大小，单位为bytes

```
oracledb_size_dba_segments_top100_table_bytes{segment_name="ARGUMENT$"} 1.1534336e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="BAS_DIAGNOSIS"} 1.572864e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="BAS_DICT_DETAIL"} 1.1534336e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="BAS_HLHT_MATCH_ITEMS"} 7.340032e+06
oracledb_size_dba_segments_top100_table_bytes{segment_name="BAS_PRICE_ITEMS"} 8.388608e+06
oracledb_size_dba_segments_top100_table_bytes{segment_name="BAS_PRICE_STAT"} 3.145728e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="BIL_OUTPATIENT_DETAIL"} 1.572864e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="BIL_OUTPATIENT_LIST"} 1.2582912e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="BIL_OUTPATIENT_PRINT"} 9.437184e+06
oracledb_size_dba_segments_top100_table_bytes{segment_name="BIN$xoVl60gVRV7gUz0SqMAm9g==$0"} 1.3631488e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CAD_PATIENT_CARD"} 1.79306496e+08
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_DIS_DITAIL"} 4.6137344e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_FEE_DRUG"} 7.6546048e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_FEE_SPECI"} 1.44703488e+08
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_ORDEREXEC"} 4.4040192e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_ORDEREXEC_LOCK"} 1.3631488e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_ORDER_FEE_SPECI"} 4.4040192e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_ORDER_FEE_SPE_TYPE"} 3.7224448e+08
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_INPATIENT_ORDEXEC_FRQ_RECORD"} 1.81403648e+08
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_MEDTECH_APPLY"} 9.437184e+06
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_OUPATIENT_RESULT"} 1.572864e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_OUTPATIENT_BUDGET"} 4.6137344e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_OUTPATIENT_COST"} 4.2991616e+07
oracledb_size_dba_segments_top100_table_bytes{segment_name="CHG_OUTPATIENT_SETTLEMENT"} 7.340032e+06
```

## 4.慢查询和大查询

oracledb_slow_queries_p95_time_usecs	oracledb_big_queries_p95_rows

排序之后，超过95%的执行时间的慢查询和超过95%的记录个数的查询

p99同理为超过99%

```
oracledb_slow_queries_p95_time_usecs 3.7217005e+07
# HELP oracledb_slow_queries_p99_time_usecs Gauge metric with percentile 99 of elapsed time.
# TYPE oracledb_slow_queries_p99_time_usecs gauge
oracledb_slow_queries_p99_time_usecs 1.31968605e+08
```



```
oracledb_big_queries_p95_rows 166
# HELP oracledb_big_queries_p99_rows Gauge metric with percentile 99 of returned rows.
# TYPE oracledb_big_queries_p99_rows gauge
oracledb_big_queries_p99_rows 173
```

## 5.等待时间

oracledb_wait_time_concurrency	并发等待时间

oracledb_wait_time_commit	提交等待时间

oracledb_wait_time_system_io	系统io等待时间

oracledb_wait_time_user_io   用户io等待时间

oracledb_wait_time_application	应用等待时间

oracledb_wait_time_network	网络等待时间

## 

