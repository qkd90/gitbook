### es的使用

es使用教程：

https://www.elastic.co/guide/cn/elasticsearch/guide/current/running-elasticsearch.html  

```shell
查索引：curl http://10.60.215.40:9200/_cat/indices?v
查索引里的数据：curl -XGET http://10.60.215.40:9200/label_log-v0-2021_01_13d/_search?pretty
删除索引：curl -X DELETE http://10.60.215.40:9200/label_log-v1-2021_01_01d 
刷新索引：curl -XPOST 10.60.215.40:9200/label_log-v1-2021_01_02d/_cache/clear?pretty
查询某一ip数据：curl -H 'content-Type:application/json' -XGET http://10.60.215.40:9200/label_log-v1-2021_01_19d/_search?pretty -d '{"query":{"match":{"srcIp":"14.204.2.1"}}}'
```

1.新建目录加索引：

```shell
curl -XPUT "http://10.222.10.73:9200/label_log-v0-2020_11_19d" -H 'Content-Type: application/json' -d '
{
   "settings":{
    "number_of_shards":3,
    "number_of_replicas":2
  },
  "mappings":{
    "properties":{
      "id":{"type":"long"},
      "name":{"type":"text"},
      "text":{"type":"text"}
    }
  }
}
```

2.新建和删除某个文档

```shell
curl -XDELETE "http://10.58.11.201:9200/label_log-v0-2020_11_18d"
curl -XPUT "http://10.58.11.201:9200/label_log-v0-2020_11_18d"
```

3.网页查看信