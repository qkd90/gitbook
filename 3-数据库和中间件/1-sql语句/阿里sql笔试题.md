## 1.获取指定客户每月的消费额

### 题目：

某金融公司某项目下有如下 2 张表：

交易表 trade（t_id：交易流水号，t_time：交易时间，t_cus：交易客户，t_type：交易类型【1表示消费，0表示转账】，t_amount：交易金额）:

![img](https://uploadfiles.nowcoder.com/images/20230309/0_1678331443413/9BB1ED91E7F2227E9D94B94E8A469F89)

客户表 customer（c_id：客户号，c_name：客户名称）:

![img](https://uploadfiles.nowcoder.com/images/20230302/0_1677762791193/B449589A603EBD7A70389B265020A5CD)

现需要查询 Tom 这个客户在 2023 年每月的消费金额（按月份正序显示），示例如下：

![img](https://uploadfiles.nowcoder.com/images/20230302/0_1677762852190/B0084452BFF4D1E99C21A054C1F2BF6A)

请编写 SQL 语句实现上述需求。

```

```



### 答案：

```sql
select date_format(t_time, "%Y-%m") as time, sum(t_amount) as total
from trade
where year(t_time) = 2023
  and t_type = 1
  and t_cus in (select c_id from customer where c_name = "Tom")
group by date_format(t_time, "%Y-%m")
order by date_format(t_time, "%Y-%m");
```

### 解析：

本题难点集中在：

1.如何筛选出2023年的数据: year(t_time) = 2023

2.如何根据年月分组:group by date_format(t_time, "%Y-%m")

## 2.查询连续入住多晚的客户信息？

某酒店客房信息数据及某晚入住信息数据如下：

客房信息表guestroom_tb(room_id-房间号,room_type-房间类型,room_price-房间价格)，如下所示：



![img](https://uploadfiles.nowcoder.com/images/20220616/0_1655389021797/D848B5088FABD9151CEF8AABE1406FFD)

入住信息表checkin_tb(info_id-信息id.room_id-房间号,user_id-客户id,checkin_time-入住时间,checkout_time-退房时间)，

该表存储该晚客户入住信息及后续退房信息；如下所示：

![img](https://uploadfiles.nowcoder.com/images/20220616/0_1655389166285/4F91A4E3D52CD176BD2B80B407836CCF)

问题：请查询该酒店从6月12日开始连续入住多晚的客户信息？

要求输出：客户id、房间号、房间类型、连续入住天数（按照入住天数升序排序）

示例数据结果如下：



![img](https://uploadfiles.nowcoder.com/images/20220617/0_1655473049464/6B8E9BC85483BC9FA78B624DE227A0C3)

解释：以客户203为例，在2022-06-12入住酒店，在2022-06-14退房，

连续在12日晚、13日晚入住在该酒店，故结果如上；

其他结果同理。

```sql
select ct.user_id,
       ct.room_id,
       gt.room_type,
       datediff(ct.checkout_time, checkin_time) days
from checkin_tb ct
         left join guestroom_tb gt
                   on ct.room_id = gt.room_id
where datediff(ct.checkout_time, checkin_time) > 1
```

## 3.统计所有课程参加培训人次

某公司员工培训信息数据如下：

员工培训信息表cultivate_tb(info_id-信息id,staff_id-员工id,course-培训课程)，如下所示：

注：该公司共开设了三门课程，员工可自愿原则性培训0-3项，每项课程每人可培训1次。

![img](https://uploadfiles.nowcoder.com/images/20220325/397036_1648216131633/42053E9A3A0CAAC141054FCECBD9B1B8)

问题：请统计该公司所有课程参加培训人次？

示例数据结果如下：



![img](https://uploadfiles.nowcoder.com/images/20220328/397036_1648478239477/9EECADEDCE1700CCCE82328E947621B0)

解释：course1课程共有员工1、3、4、7共4名员工培训；

course2课程共有员工1、2、4、7共4名员工培训；

course3课程共有员工3、4、5共3名员工培训；

```

```

## 4.查询培训指定课程的员工信息

某公司员工信息数据及员工培训信息数据如下：

员工信息表staff_tb(staff_id-员工id,staff_name-员工姓名,staff_gender-员工性别,post-员工岗位类别,department-员工所在部门)，如下所示：



![img](https://uploadfiles.nowcoder.com/images/20220324/397036_1648127201644/2174413654E19E49F428BA34F3322473)

员工培训信息表cultivate_tb(info_id-信息id,staff_id-员工id,course-培训课程)，如下所示：

注：该公司共开设了三门课程，员工可自愿原则性培训0-3项；

![img](https://uploadfiles.nowcoder.com/images/20220325/397036_1648216131633/42053E9A3A0CAAC141054FCECBD9B1B8)

问题：请查询培训课程course3的员工信息？

注：只要培训的课程中包含course3课程就计入结果

要求输出：员工id、姓名，按照员工id升序排序；
示例数据结果如下：



![img](https://uploadfiles.nowcoder.com/images/20220325/397036_1648216347914/CB408FB737BD41276AE9D171FAB2CF72)

解释：有员工3、4、5培训了course3课程，故结果如上

```

```

## 5.推荐内容准确的用户平均评分

某产品2022年2月8日系统推荐内容给部分用户的数据，以及用户信息和对推荐内容的评分交叉表部分数据如下：

推荐内容表recommend_tb（rec_id-推荐信息id，rec_info_l-推荐信息标签，rec_use-推荐目标用户id，rec_time-推荐时间），如下所示：

![img](https://uploadfiles.nowcoder.com/images/20220219/397036_1645261871034/82324E5E097EDF3F8906360797985587)

用户信息及评分交叉表user_action_tb（user_id-用户id，hobby_l-用户喜好标签，score-综合评分），如下所示：

注：该表score为对所有推荐给该用户的内容的综合评分，在计算用户平均评分切勿将推荐次数作为分母



![img](https://uploadfiles.nowcoder.com/images/20220219/397036_1645261891282/27E09175A9B66D11886CA23D11CE2332)

问题：请统计推荐内容准确的用户平均评分？(结果保留3位小数)
注：（1）准确定义：推荐的内容标签与用户喜好标签一致；如推荐多次给同一用户，有一次及以上准确就归为准确。
示例数据结果如下：



![img](https://uploadfiles.nowcoder.com/images/20220219/397036_1645261908637/95B767CBCC6137446D1DCA61DB5FB4BA)

解释：一共推荐8条内容，其中推荐给101、103、105、106四位用户的内容准确,

四位用户的评分分别是88、78、90、82，故平均评分=（88+78+90+82）/4=84.500

```

```

