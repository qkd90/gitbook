

参照嵩山版

## 命名

### 1.Service/DAO 层方法命名规约

1） 获取单个对象的方法用 get 做前缀。
2） 获取多个对象的方法用 list 做前缀。
3） 获取统计值的方法用 count 做前缀。
4） 插入的方法用 save/insert 做前缀。
5） 删除的方法用 remove/delete 做前缀。
6） 修改的方法用 update 做前缀。

### 2.领域模型命名规约

1） 数据对象：xxxDO，xxx 即为数据表名。
2） 数据传输对象：xxxDTO，xxx 为业务领域相关的名称。
3） 展示对象：xxxVO，xxx 一般为网页名称。
4） POJO 是 DO/DTO/BO/VO 的统称，禁止命名成 xxxPOJO。

### 3.类的命名

C == create == 增

R == read == 查：获取/读取/查找/查询 get、fetch、acquire、read、search、find、query

U == update == 改

D == delete == 删