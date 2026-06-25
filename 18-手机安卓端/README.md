# 手机安卓端

## 章节定位

本章节记录安卓设备调试、ADB 命令和机器人设备控制相关内容，适合移动端联调、自动化测试、设备管理和现场排查。

## 核心内容

- ADB 安装和设备连接。
- 查看设备、安装应用、卸载应用。
- 读取日志、截屏、录屏。
- 输入文本、点击、滑动、按键。
- 设备网络、权限和进程排查。

## 常用命令

```bash
adb devices
adb install app.apk
adb uninstall com.example.app
adb shell
adb logcat
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png .
```

## 排查建议

- 设备连不上时，先检查 USB 调试、驱动、数据线和授权弹窗。
- 多设备连接时，命令要加 `-s 设备号`。
- 自动化控制失败时，先用截图确认当前页面是否符合预期。
