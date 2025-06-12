## 配置文件config

### 1.注解：

#### *@EnableTransactionManagement*(proxyTargetClass = true)：

在Mybatis-Plus中,proxyTargetClass = true 的意思是使用CGLIB代理目标类,而不是使用JDK的默认接口代理。

Mybatis-Plus中的Mapper接口使用了两个代理方式:

1.JDK的默认接口代理这种方式下,Mapper接口的实现类是接口的实现类,目标类是接口。

2.CGLIB代理这种方式下,Mapper接口的实现类是目标类的子类,目标类是实体类。

CGLIB代理的好处是:

- 可以代理final方法和类
\- 可以在运行时创建代理类及其实例所以,设置proxyTargetClass = true后,Mybatis-Plus会使用CGLIB代理方式,来代理实体类,产生实体类的子类作为Mapper接口的实现。
这允许Mapper方法调用实体类的final方法,并可以对实体类进行功能扩展。具体的好处可以理解为:**使用接口代理(默认)**

```java
// StudentMapper.java 
public interface StudentMapper {
    void selectById(Student student);
}

// StudentMapperImpl.java
public class StudentMapperImpl implements StudentMapper {
    public void selectById(Student student) {
        // ...
    }
}
```

**使用CGLIB代理(proxyTargetClass = true)**

```java
// StudentMapper.java 
public interface StudentMapper {
    void selectById(Student student);
}

// 无实现类,使用CGLIB代理实体类
public class Student {
    public final void hello() { ... }
}
```

StudentMapper的实现类会成为Student的子类,可以调用hello()方法。所以,总结来说,proxyTargetClass = true允许Mapper方法调用final方法和进行方法增强,这是它的主要作用