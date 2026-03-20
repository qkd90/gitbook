## docker单机启动

```
docker pull apache/doris:be-4.0.2

docker run -d \
  --name doris-be \
  -p 8030:8030 \
  -p 8040:8040 \
  -p 9050:9050 \
  apache/doris:be-4.0.2
```

