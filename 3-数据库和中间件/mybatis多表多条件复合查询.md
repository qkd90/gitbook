编写UserMapper接口,继承tk.mybatis.mapper.common.Mapper接口

```java
public interface UserMapper extends Mapper<User> {
}  
```

在UserMapper接口方法中使用Example和PageHelper进行条件分页查询

```
java
PageHelper.startPage(page, size);
Example example = new Example(User.class);
Example.Criteria criteria = example.createCriteria();
if (StringUtils.isNotBlank(name)) {
    criteria.andLike("name", "%" + name + "%");
}
if (age != null) {
    criteria.andEqualTo("age", age);
}
List<User> list = mapper.selectByExampleAndResultMap(example, "UserResultMap");
PageInfo<User> pageInfo = new PageInfo<>(list);
```