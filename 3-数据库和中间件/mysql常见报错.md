## 1.问题描述

### 1.1

Table 'mysql.db' doesn't exist

Fatal error: Can't open and lock privilege tables: Table 'mysql.host' doesn't exist [closed]

数据库权限部分文件被破坏

## 2.排查问题

### 2.1查看错误日志

目录：/var/log/mysqld.log

配置文件：/etc/my.cnf

```bash
1.从第3000行开始，显示1000行。即显示3000~3999行

cat filename | tail -n +3000 | head -n 1000

2.显示1000行到3000行

cat filename| head -n 3000 | tail -n +1000

tail -n 1000：显示最后1000行

tail -n +1000：从1000行开始显示，显示1000行以后的

head -n 1000：显示前面1000行
```