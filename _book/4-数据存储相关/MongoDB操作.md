一、MongoDB：

1.查看数据库相关信息

```shell
mongod.sh mongo
连接数据库

show dbs
展示所有的数据库

show tables 
展示库中所有的表
```

2.查询一条实例

```
db.Vm_vulnerability.find().pretty()
pretty则是格式化显示数据
db.Vm_vulnerability.findOne()
查看对应的表中的一条数据
```

3.

```sh
db.Vm_vulnerability.update({'data_type':'loophole'},{$set:{'last_time':ISODate("2020-09-03T11:27:39Z")}},false,true)
```

6.db.system.users.find()

查看数据库所有用户

7.新建用户

```shell
use admin
switched to db admin
db.createUser({user:"root",pwd:"password",roles:["userAdminAnyDatabase"]})
```

8.导入导出数据：

```
mongoexport -d dbname -c collectionname -o file --type json/csv -f field

参数说明：
-d ：数据库名
-c ：collection名
-o ：输出的文件名
--type ： 输出的格式，默认为json
-f ：输出的字段，如果-type为csv，则需要加上-f "字段名"
```

使用mongodb自带导入工具mongoimport ，在bin目录下面

```
mongoimport -d dbname -c collectionname --file filename --headerline --type json/csv -f field --jsonArray

参数说明：         
-d ：数据库名           
-c ：collection名          
--file ：要导入的文件
--type ： 导入的格式，默认为json          
-f ：输出的字段，如果-type为csv，则需要加上-f "字段名"
--jsonArray:支持数组,如果出现Failed: error unmarshaling bytes on document #0: JSON decoder out of sync - data changing underfoot?使用这个参数试试
```

 

9.查找MongoDB：

ps -ax | grep mongod

10.删除event_manage表所有数据

 db.event_manage.remove({})

二、数据聚合：

1.

db.getCollection("Vm_vulnerability").aggregate([

​	{$match:

​	{"$and":[

​	{"$or":[{"asset_invalid_time":0},{"asset_invalid_time":{$exists:0}}]},

​	{"$or":[{"is_deleted":0},{"is_deleted":{$exists:0}}]},

​	{"group_id":1000032},

​	{"verify":{$ne:2}},

​	{"last_time":{$gte:ISODate("2020-11-01T00:00:00.000Z")}}

​	]}},

​	{$count:"count"}

])

1.$exists语法： { field: { $exists: <boolean> } }

当boolean为true,$exists匹配包含字段的文档，包括字段值为null的文档。

当boolean为false,$exists返回不包含对应字段的文档。

2.

- (>) 大于 - $gt
- (<) 小于 - $lt
- (>=) 大于等于 - $gte
- (<= ) 小于等于 - $lte
- $ne 不等于

2.$unwind

把一个数组对应变为一个一个记录输出