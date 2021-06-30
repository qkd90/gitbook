# kafka命令行操作

1.kafka

```shell
/usr/share/kafka_2.11-2.3.0/bin/
```

2.查看kafka的topic

```shell
./kafka-topics.sh --zookeeper localhost:2181 --list
```

3.查询某一个topic的信息

```shell
./kafka-topics.sh --zookeeper localhost:2181 --topic SANGFOR_EVENT_EVENT --describe
```

4.查询消费者组

```shell
/usr/share/kafka_2.11-2.3.0/bin/kafka-consumer-groups.sh  --bootstrap-server localhost:9092 --list
```

5.查询特定组的

```shell
/usr/share/kafka_2.11-2.3.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group sip --describe
```

6.新建topic

```shell
/usr/share/kafka_2.11-2.3.0/bin/kafka-topics.sh --create --topic siplogger --zookeeper localhost:2181 --replication-factor 1 --partitions 1 
```

7.生产者，消费者

```shell
kafka生产者客户端命令
./kafka-console-producer.sh --broker-list 10.60.215.10:9092 --topic siplogger

kafka消费者客户端命令
./kafka-console-consumer.sh --bootstrap-server 10.60.215.10:9092 --from-beginning --topic siplogger

查看consumer组内消费的offset
./kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --zookeeper localhost:2181 --group test --topic testKJ1
./kafka-consumer-offset-checker.sh --zookeeper 10.60.215.10:12181 --group group1 --topic group1

```

8.