# 前言：

partition by关键字是分析性函数的一部分，它和聚合函数（如group by）不同的地方在于它能返回一个分组中的多条记录，而聚合函数一般只有一条反映统计值的记录。
partition by用于给结果集分组，如果没有指定那么它把整个结果集作为一个分组。
partition by与group by不同之处在于前者返回的是分组里的每一条数据，并且可以对分组数据进行排序操作。后者只能返回聚合之后的组的数据统计值的记录。

常用的函数：

```
row_number() over(partition by ... order by ...)
rank() over(partition by ... order by ...)
dense_rank() over(partition by ... order by ...)
count() over(partition by ... order by ...) 求分组后的总数
max() over(partition by ... order by ...) 求分组后的最大值
min() over(partition by ... order by ...) 求分组后的最小值
sum() over(partition by ... order by ...) 求分组后的总和
avg() over(partition by ... order by ...) 求分组后的平均值
first_value() over(partition by ... order by ...) 求分组后的第一个值
last_value() over(partition by ... order by ...) 求分组后的最后一个值
lag() over(partition by ... order by ...) 取出分组后前n行数据
lead() over(partition by ... order by ...) 取出分组后后n行数据
```

# 一、rank()

rank() over(partition by A order by B)
是按照A进行分组，分组里面的数据按照B进行排序，over即在什么之上，rank()即跳跃排序(比如存在两个第一名，接下来就是第三名) 举例：

```
1
select 课程, 学生ID, 分数, rank() over (partition by 课程 order by 分数 desc) as 排名 from 成绩表
```

查询结果：

| 课程 | 学生ID | 分数 | 排名 |
| :--: | :----: | :--: | :--: |
| 语文 |   1    |  99  |  1   |
| 语文 |   5    |  99  |  1   |
| 语文 |   7    |  89  |  3   |
| 语文 |   9    |  79  |  4   |

# 二、row_number()

row_number() over(partition by A order by B)
row_number(): 如果有两个第一名时，只返回一个结果。 举例：

```
1
select 课程, 学生ID, 分数, row_number() over (partition by 课程 order by 分数 desc) as 排名 from 成绩表
```

查询结果：

| 课程 | 学生ID | 分数 | 排名 |
| :--: | :----: | :--: | :--: |
| 语文 |   1    |  99  |  1   |
| 语文 |   5    |  99  |  2   |
| 语文 |   7    |  89  |  3   |
| 语文 |   9    |  79  |  4   |

# 三、dense_rank()

dense_rank() over(partition by A order by B)
dense_rank(): 连续排序(如果有两个第一名时，接下来仍然是第二名) 举例：

```
1
select 课程, 学生ID, 分数, rank() over (partition by 课程 order by 分数 desc) as 排名 from 成绩表
```

查询结果：

| 课程 | 学生ID | 分数 | 排名 |
| :--: | :----: | :--: | :--: |
| 语文 |   1    |  99  |  1   |
| 语文 |   5    |  99  |  1   |
| 语文 |   7    |  89  |  2   |
| 语文 |   9    |  79  |  3   |

------

其他用法，就不一一列举了，和上面用法类似，请看开头的简介～
以上～～