## 0.写在前面

- 在下载新版本或者更新`python`版本时，一定不要删除系统自带的python版本！不然会带来很多麻烦，包括yum、pip等命令不能用的情况，这时需要修改相应py文件头的环境变量，会变得相当麻烦
- 如果你只是更改了系统默认的python软连接，而没有删除自带的python，可参考这篇文章进行处理；如果已经使用`rm`命令删除了原本的python及其配置文件，可使用下述恢复方法，恢复之后需要重新下载和安装你之前已经配置好的更高级别的python环境

## 1. 删除干净python环境

```shell
rpm -qa|grep python|xargs rpm -ev --allmatches --nodeps
whereis python|xargs rm -frv
```

## 2.查看系统版本

```shell
cat /etc/redhat-release
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/035763f0bb2940478d4fb19d745acd74.png)

## 3.使用wget分别下载python以及yum的rpm包

一定要下载和你系统版本对应的文件，[资源网址](http://vault.centos.org/)

> 其实基本都是把`7.2.1511`换成你对应版本号即可

```shell
mkdir /usr/local/src/python
cd /usr/local/src/python
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-backports-1.0-8.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/libxml2-python-2.9.1-6.el7_2.3.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-backports-ssl_match_hostname-3.5.0.1-1.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-chardet-2.2.1-1.el7_1.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-devel-2.7.5-76.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-iniparse-0.4-9.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-ipaddress-1.0.16-2.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-kitchen-1.1.1-5.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-libs-2.7.5-76.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-pycurl-7.19.0-19.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-setuptools-0.9.8-7.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-urlgrabber-3.10-9.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/python-virtualenv-15.1.0-2.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-4.11.3-35.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-build-4.11.3-35.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-build-libs-4.11.3-35.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-libs-4.11.3-35.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-python-4.11.3-35.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/rpm-sign-4.11.3-35.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-3.4.3-161.el7.centos.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-metadata-parser-1.1.4-10.el7.x86_64.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-plugin-aliases-1.1.31-50.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.31-50.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-plugin-protectbase-1.1.31-50.el7.noarch.rpm
wget http://vault.centos.org/7.2.1511/os/x86_64/Packages/yum-utils-1.1.31-50.el7.noarch.rpm
```

## 4.安装

```shell
rpm -Uvh --replacepkgs lvm2-python-libs*.rpm --nodeps --force
rpm -Uvh --replacepkgs libxml2-python*.rpm --nodeps --force 
rpm -Uvh --replacepkgs python*.rpm --nodeps --force
rpm -Uvh --replacepkgs rpm-python*.rpm yum*.rpm --nodeps --force
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/99e00fd19c5b4627b31c89b0eee8493b.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE5NzE2MTQz,size_16,color_FFFFFF,t_70)

## 5. 测试是否可用

```shell
python -V
//或`python` 但记得按`ctrl`+`D`退出python shell
```