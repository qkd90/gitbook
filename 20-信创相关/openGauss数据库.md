## 一、

1. 创建用户组dbgroup。

   ```
   groupadd dbgroup
   ```

2. 创建用户组dbgroup下的普通用户omm，并设置普通用户omm的密码，密码建议设置为omm@123。

   ```
   useradd -g dbgroup omm
   passwd omm
   ```

3. 使用omm用户登录到openGauss包安装的主机，此时注意新建的文件夹要有操作权限

   ```
   sudo chmod -R 777 your_dir
   ```

4. ，解压openGauss压缩包到安装目录（假定安装目录为/opt/software/openGauss，请用实际值替换）。

   ```
   tar -jxf openGauss-x.x.x-操作系统-64bit.tar.bz2 -C /opt/software/openGauss
   ```

5. 假定解压包的路径为/opt/software/openGauss,进入解压后目录下的simpleInstall。

   ```
   cd /opt/software/openGauss/simpleInstall
   ```

6. 执行install.sh脚本安装openGauss。

   ```
   sh install.sh  -w xxxx 
   ```

   上述命令中，-w是指初始化数据库密码（gs_initdb指定），安全需要必须设置。

7. 安装执行完成后，使用ps和gs_ctl查看进程是否正常。

   ```
   ps ux | grep gaussdb
   gs_ctl query -D /opt/software/openGauss/data/single_node
   ```

   执行ps命令，显示类似如下信息：

## 二、数据迁移

https://juejin.cn/post/7223204251005878330

chameleon使用指南：

https://github.com/opengauss-mirror/openGauss-tools-chameleon/blob/master/chameleon%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md

