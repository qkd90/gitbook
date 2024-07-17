## 1.原有的python和yum删干净

```
1、删除现有Python
[root@Xxxx ~]# rpm -qa|grep python|xargs rpm -ev --allmatches --nodeps ##强制删除已安装程序及其关联
[root@Xxxx~]# whereis python |xargs rm -frv ##删除所有残余文件 ##xargs，允许你对输出执行其他某些命令
[root@Xxxx~]# whereis python ##验证删除，返回无结果
2、删除现有的yum
[root@Xxxx ~]# rpm -qa|grep yum|xargs rpm -ev --allmatches --nodeps
[root@Xxxx~]# whereis yum |xargs rm -frv
```

## 2.下载对应的Python2和Yum的rpm包

使用的是中科大的源

```shell
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-chardet-2.2.1-3.el7.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-devel-2.7.5-89.el7.x86_64.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-iniparse-0.4-9.el7.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-libs-2.7.5-89.el7.x86_64.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-pycurl-7.19.0-19.el7.x86_64.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-setuptools-0.9.8-7.el7.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-urlgrabber-3.10-10.el7.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/rpm-python-4.11.3-45.el7.x86_64.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/libxml2-python-2.9.1-6.el7.5.x86_64.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/python-2.7.5-89.el7.x86_64.rpm

wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-3.4.3-168.el7.centos.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-metadata-parser-1.1.4-10.el7.x86_64.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-plugin-aliases-1.1.31-54.el7_8.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.31-54.el7_8.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-plugin-protectbase-1.1.31-54.el7_8.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-updateonboot-1.1.31-54.el7_8.noarch.rpm
wget https://mirrors.ustc.edu.cn/centos/7/os/x86_64/Packages/yum-utils-1.1.31-54.el7_8.noarch.rpm
```

## 3.安装rpm

```
rpm -ivh --force *.rpm --nodeps
```

 它会自动安装该目录下的rpm包！然后坐等success~

![image-20240708111904395](https://raw.githubusercontent.com/qkd90/figureBed/main/202407081119971.png)

## 4.检查安装

```
yum -v
```

