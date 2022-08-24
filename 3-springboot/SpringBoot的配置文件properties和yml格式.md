# SpringBoot的配置文件properties和yml格式

## 一.区别

yml文件格式是Spring Boot支持的一种JSON文件格式，相较于传统的Properties配置文件，yml文件以数据为核心，是一种更为直观且容易被电脑识别的数据序列化格式。
application.yml配置文件的工作原理和application.properties是一样的，只不过yml格式配置文件看起来更简洁一些。

- properties

```properties
#application.properties
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://127.0.0.1:3306/ysw_blog
spring.datasource.username=root
spring.datasource.password=你的密码
```

- yml

```yml
#application.yml
spring:
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url: jdbc:mysql://127.0.0.1:3306/ysw_blog
    username: root
    password: 你的密码
1234567
```

注意：application.yml文件使用 “key:（空格）value”格式配置属性，使用缩进控制层级关系。

### 二.yml扩展

yml文件还支持复杂数据类型，例如数组和集合
如下：

### 1.数组或单列集合类型

```xml
person:
	hobby:
		- play
 		- read
 		- sleep
或者
person:
	hobby:
 		play,
 		read,
 		sleep
或者如下方式，推荐使用该方式，[]也可以省略 		
person:
	hobby: [play,read,sleep] 
```

### 2.map集合

```xml
person:
	map:
		k1: v1
		k2: v2
#或者使用行内方式		
person:
	map: {k1: v1,k2: v2}
```