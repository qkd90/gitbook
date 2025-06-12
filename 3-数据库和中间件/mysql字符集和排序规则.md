# 默认设置

**mysql8.0新建对的，然后字符集和排序规则都不设置，新建后，你会发现mysql默认设置为如下值：**

1. 字符集 ：utf8mb4
2. 排序规则：utf8mb4_0900_ai_ci

```cpp
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

# 字符集

## utf8mb4和utf8

以utf8为例，它最多支持 3 个字节，当你存4字节的 utf8 编码字符时，会入库失败（常见的如：emoji ），在2010年重新发布了 utf8mb4 支持utf8。

## 其他字符集

**使用如下指令可以查看mysql支持的其他字符集及每个字符集对应的默认的排序集合。**

```cpp
show character set;
```

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202302020845479.png)

# 排序规则

**关于排序规则命名，通常都是在相应的字符集后面加上下划线`_排序方式`，常见的有如下三种方式：**

## ci结尾

ci结尾表示大小写不敏感（case insensitive）,这点也是程序往往容易忽略的一个bug，大部分场景下，特别是模糊搜索时，我们可能更希望搜索a时，a和A都会出现，但有些特殊情况，我们只希望出现a，而这时如果程序中没有做特殊处理，你查出来相当于有多条数据，却只映射到一个对象时，此时程序会抛出异常又或者查出了多条数据，当你程序没有特殊处理，只默认处理第一条此时会出现不该出现的数据展现了出来。

## ca结尾

cs表示大小写敏感（case sensitive）

## bin结尾

bin表示字符串每个字符串用二进制数据编译存储，区分大小写，而且可以存二进制的内容。

# 乱序问题

**关于mysql乱序问题，在初学时真的有点头疼，有时你会发现，照着别人的文章，一毛一样的设置，结果文章可以成功，而你的却不行。还有一种情况，你尝试某个方法成功后，下次遇到时，再进行一毛一样的操作，你会发现这次不灵了。**

**乱序问题除了我们程序的编码问题外，mysql里头也有好几个地方涉及到字符集的操作：**

1. character_set_server：mysql server（服务端）默认字符集，可以用如下命令查看：

```cpp
show variables like 'character_set_server'
```

1. character_set_database：数据库默认字符集。

```cpp
show variables like 'character_set_database'
```

1. character_set_client：客户端发送的查询使用的字符集。

```cpp
show variables like 'character_set_client'
```

1. character_set_connection：MySQL Server接收客户端发布的查询请求后，将其转换为character_set_connection变量指定的字符集。

```cpp
show variables like 'character_set_connection'
```

1. character_set_results：mysql server把结果集和错误信息转换为character_set_results指定的字符集，并发送给客户端。

```cpp
 show variables like 'character_set_results'
```

1. character_set_system：系统元数据(字段名等)字符集

```cpp
  show variables like 'character_set_system'
```

**上述的某个阶段和其他阶段设置的字符集和不一致的时候，都可能出现乱序现象。**