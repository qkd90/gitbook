### 进行挂载磁盘准备：

```
# 查看磁盘
fdisk -l
# 格式化磁盘 
mkfs.ext4 /dev/vdb
```

### 创建挂载点：

在Docker的数据目录下创建挂载点,用于挂载硬盘分区。

```
sudo mkdir -p /trasen
```

### 挂载硬盘分区：

使用mount命令将格式化的硬盘分区挂载到创建的挂载点。

```
sudo mount /dev/vdb /trasen
```

### 设置挂载自动化

可以在/etc/fstab文件中设置启动时自动挂载,避免每次重启后手动挂载。

```
blkid /dev/vdb
# 输出结果
/dev/sdb: UUID="3af607ac-5ebe-4cd5-bb5f-760434575364" TYPE="ext4"
# 编辑文件
vim /etc/fstab
#添加如下内容
UUID=c02575ac-9a28-4446-967a-244a2ab4b910 /trasen    ext4    defaults    1 2
```

