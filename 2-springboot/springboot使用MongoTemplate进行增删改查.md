### springboot使用MongoTemplate进行增删改查

1.首先添加依赖

```
<!-- springboot 整合 mongodb   -->
   <dependency> 
	    <groupId>org.springframework.boot</groupId>
	    <artifactId>spring-boot-starter-data-mongodb</artifactId>
   </dependency>
```

2.使用的时候引入

```
@Autowired
private MongoTemplate mongoTemplate;
```

