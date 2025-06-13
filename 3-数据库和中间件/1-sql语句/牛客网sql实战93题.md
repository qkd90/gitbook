#### **SQL15** 查找employees表emp_no与last_name的员工信息

![image-20211105151700503](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20211105151700503.png)

```
SELECT * FROM employees
WHERE emp_no % 2 = 1
AND last_name <> 'Mary'
ORDER BY hire_date DESC;
```

