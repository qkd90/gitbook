# 小米手机安装 Magisk 获取 Root 权限指南

现在获取手机 Root 主要通过安装 Magisk 实现，这篇文章将以新手视角介绍如何安装使用 Magisk。

为尽可能介绍明白，文中所提步骤均配上了截图说明（点击文字链接可以查看操作图解）。

## 准备工作

- 安装 Magisk 过程中需要用到 `fastboot` 命令，请确保电脑已[下载相关工具和配置好命令环境变量](https://miuiver.com/add-fastboot-and-adb-environment-variables/)
- 安装 Magisk 过程中需要刷写手机 `boot` 或 `Recovery` 分区，请确保手机已完成 [BL 解锁](https://miuiver.com/how-to-unlock-xiaomi-phone/)，不然无法进行
- 安装 Magisk 正常情况下不会丢数据，但稳妥起见，尤其是新手，建议先外置[备份手机数据](https://miuiver.com/mi-phone-data-backup/)再操作

最后，虽然文中方法已用实机多次验证，但每人环境可能不同，无法承诺获得一致结果，文章仅供参考！

### Windows 配置 fastboot 和 adb 命令环境变量

下面介绍 Windows 如何配置 fastboot 和 adb 环境变量。

1. [点击下载 Android SDK Platform Tools](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)，它包含 fastboot、adb 命令程序文件，下载后完整解压一旁备用（例如解压到 C 盘根目录）。
2. 同时按下键盘上的 `Windows 图标键 + R 字母键`，在弹出“运行”窗口中输入 `sysdm.cpl` 并回车，然后点击“系统属性”窗口“高级”选项，再点击下方的“环境变量”按钮。

[![Windows运行打开系统属性](https://miuiver.com/wp-content/uploads/2022/07/sysdm-cpl.png)](https://miuiver.com/wp-content/uploads/2022/07/sysdm-cpl.png)步骤一：从“运行”打开系统属性

[![Windows环境变量设置选项](https://miuiver.com/wp-content/uploads/2022/07/environment-variables-button.png)](https://miuiver.com/wp-content/uploads/2022/07/environment-variables-button.png)步骤二：点击“环境变量”按钮

3. 选中系统变量下的“Path”，点击“编辑”，然后在新窗口中点击“新建”，输入之前 Android SDK Platform Tools 解压目录路径，添加后关闭窗口。

注：对于 Windows 7 而言，最后一步略有不同，需要将路径追加到已有变量值后面，用 `;` 半角符号间隔（[图解](https://miuiver.com/wp-content/uploads/2022/07/add-environment-variables-win7.png)）。

[![Windows编辑系统变量Path](https://miuiver.com/wp-content/uploads/2022/07/edit-environment-variables.png)](https://miuiver.com/wp-content/uploads/2022/07/edit-environment-variables.png)步骤一：选中系统变量Path编辑

[![Windows添加环境变量路径](https://miuiver.com/wp-content/uploads/2022/07/add-environment-variables.png)](https://miuiver.com/wp-content/uploads/2022/07/add-environment-variables.png)步骤二：添加环境变量路径

4. 到此，添加环境变量就完成了。在“运行”窗口输入 `cmd` 打开命令行，用 `adb version` 或 `fastboot --version` 测试命令是否能正常使用。



## 下载 Magisk

Magisk 下载地址 https://github.com/topjohnwu/Magisk/releases（[选择下载最新版](https://miuiver.com/wp-content/uploads/2022/08/magisk-apk-download.png)，然后安装到手机）。

如果下载遇到打不开情况，请多刷新几次，或者切换不同网络测试。

## 查询手机环境

在继续后面操作前，请先查询以下两点，记下查询结果。

- 手机打开安装的 Magisk，在[主界面查看 Ramdisk 结果](https://miuiver.com/wp-content/uploads/2022/08/check-phone-ramdisk.png)
- 查询手机是否具有单独 `vbmeta` 分区，查询方法请[参考这篇文章](https://miuiver.com/existence-of-vbmeta-partition/)

## 提取相应文件

[查看手机上运行的系统版本是多少](https://miuiver.com/wp-content/uploads/2022/08/view-miui-version.png)，下载[对应系统版本刷机包](https://miuiver.com/)，从里面提取相应文件（请见下面说明）。

- 如果之前 Ramdisk 查询结果为“是”，请提取 `boot.img` 文件
- 如果之前 Ramdisk 查询结果为“否”，请提取 `recovery.img` 文件

> 补充：对于出厂系统就是 Android 13 的新机型，有网友反馈需要提取 `init_boot.img` 文件修补而不是 `boot.img`。

文件提取方法：

- 如果系统版本有线刷包，可以[直接解压提取](https://miuiver.com/wp-content/uploads/2022/08/extract-boot-img-from-fastboot-rom.png)
- 如果系统版本只有卡刷包，需要[从解压的 payload.bin 文件里提取](https://miuiver.com/extracting-boot-img/)（[老机型卡刷包可以直接提取](https://miuiver.com/wp-content/uploads/2022/08/extract-boot-img-from-recovery-rom.png)）

将提取到的文件复制到手机上。

## 生成修补文件

手机打开 Magisk 软件，[点击 Magisk 卡片中的“安装”按钮](https://miuiver.com/wp-content/uploads/2022/08/magisk-installation-button.jpg)。接下来的界面不同机型显示的选项可能不同。

- 如果之前 Ramdisk 查询结果为“否”，请选中“安装到 Recovery”选项
- 如果之前查询手机没有单独 `vbmeta` 分区，请选中“修补 boot 镜像中的 vbmeta”选项

如果显示有其它选项，一般保持默认不要更改。稍微新一些的机型通常不会显示相关选项，所以请忽略。

接下来[点击“选择并修补一个文件”](https://miuiver.com/wp-content/uploads/2022/08/magisk-select-and-patch-a-file.jpg)，选择之前提取到的 `boot.img`，`init_boot.img` 或 `recovery.img` 文件，[点击“开始”](https://miuiver.com/wp-content/uploads/2022/08/magisk-start-installation.jpg)，然后[等待生成修补文件](https://miuiver.com/wp-content/uploads/2022/08/magisk-output-file.jpg)。

补充：据 Magisk 文档指出，小米有个别机型 Ramdisk 结果可能不能准确检测。如果修补 `recovery.img` 文件失败，可以尝试用 `boot.img` 修补，后面安装也遵循 Ramdisk 结果为“是”的做法。

将生成的修补文件复制到电脑上（修补文件默认保存在手机内部存储 Download 目录）。

## 刷写修补文件

将手机关机，长按`音量下键 + 电源键`进入 FASTBOOT 模式，用数据线连接到电脑。

电脑打开存放修补文件的文件夹，按住键盘 `Shift 键`，同时鼠标右键点击文件夹空白处，在右键菜单点击“在此处打开 Powershell 窗口”，然后运行下面刷写命令（命令中的文件名请先自行修改）。

```
# 如果之前修补 boot.img 文件请用这个命令
fastboot flash boot magisk_patched-25200_pU6ZV.img

# 如果之前修补 init_boot.img 文件请用这个命令
fastboot flash init_boot magisk_patched-25200_pU6ZV.img

# 如果之前修补 recovery.img 文件请用这个命令
fastboot flash recovery magisk_patched-25200_pU6ZV.img
```

刷写完成后用下面命令重启手机（补充：如果刷写的是 `recovery.img` 修补文件，也就是 Ramdisk 结果为“否”的机型。在刷写完重启时需要按住 Recovery 组合键，小米的是`音量上键 + 电源键`，待出现启动界面后松开按键，这样进入的系统才能使用 Magisk）。

```
fastboot reboot
```

如无意外，重启手机后就安装好 Magisk 了。打开 Magisk 软件可以看到[已经有 Root 授权管理选项](https://miuiver.com/wp-content/uploads/2022/08/magisk-root-access-management.png)，现在可以开始使用了。

提示：如果刷完后遇到反复重启进不去系统问题，可以尝试先用下面命令禁用启动验证（AVB/DM-Verity），然后重复上一步骤重新刷写修补文件（这个方法仅限具有单独 `vbmeta` 分区的机型使用）。

```
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
```

命令中用到的 `vbmeta.img` 文件从刷机包内提取，方法和之前提取其它文件一样。

或者，如果遇到问题打算放弃 Magisk 安装，只需用之前方法刷回从刷机包提取的原始文件。

## 使用问题补充

### Magisk 如何对软件隐藏 Root

目前比较好的方法是安装 Shamiko 模块实现，具体请查看[这篇文章](https://miuiver.com/magisk-installation-shamiko/)。

### 安装 Magisk 后系统更新注意事项

安装 Magisk 后如果按往常一样更新系统，会出现 [OTA 增量更新失败，需要下载完整包的问题](https://miuiver.com/wp-content/uploads/2022/08/miui-ota-update-failed.png)，并且更新后会丢失 Magisk 安装。

采取下面更新步骤可以避免上述问题（仅适合 [A/B 分区机型](https://miuiver.com/checks-for-ab-partitions-support/)使用。其它机型忽略第 3 步骤，更新后重新安装 Magisk）。

1. 平时[关闭系统自动更新](https://miuiver.com/wp-content/uploads/2021/04/miui-disable-auto-update.png)，以防后台自动下载安装更新
2. 当要更新系统时，先打开 Magisk 软件，[点击“卸载 Magisk”，选择“还原原厂映像”](https://miuiver.com/wp-content/uploads/2022/08/magisk-restore-boot-img.png)
3. 运行系统更新，[安装后先不要点重启，打开 Magisk 软件点击“安装”，选择“安装到未使用的槽位”](https://miuiver.com/wp-content/uploads/2022/08/magisk-system-update-steps.png)，之后再重启

### 更新 Magisk 方法

Magisk 更新分 [Magisk 软件 和 Magisk 安装](https://miuiver.com/wp-content/uploads/2022/08/update-magisk.png)，两者都可以在 Magisk 软件内操作更新（先更新 Magisk 软件，再更新 Magisk 安装）。

由于网络环境和应用权限问题，在 Magisk 里的点击更新软件可能会遇到不能下载或安装的问题。可以直接[访问 GitHub 下载 APK 文件](https://github.com/topjohnwu/Magisk/releases)覆盖安装，然后再[更新 Magisk 安装，选择“直接安装”模式](https://miuiver.com/wp-content/uploads/2022/08/installation-av-magisk-uppdatering.png)即可。

### 卸载 Magisk 方法

打开 Magisk 软件，停用已安装模块（如果有的话），[点击“卸载 Magisk”按钮，选择“完全卸载”](https://miuiver.com/wp-content/uploads/2022/08/uninstall-magisk.png)，卸载后会自动重启生效。

提示：如果之前安装 Magisk 时取消了“保持强制加密”选项（修补文件那步，通常只在旧机型和旧版本上有显示该选项，且默认不会取消），则卸载 Magisk 后系统可能会自动加密用户数据，操作前记得外置备份数据。