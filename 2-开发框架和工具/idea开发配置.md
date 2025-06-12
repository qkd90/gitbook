## 1.idea 快速删除所有空行

用ctrl+r进行内容替换，使用正则表达式，用^\s*\n 替换 空即可

## 2.project目录忽略文件配置

### 开启忽略设置

- 打开 Settings（Windows/Linux 系统通过 File -> Settings 进入；macOS 系统通过 IntelliJ IDEA -> Preferences 进入）。
- 导航到 Editor -> File Types。

### 添加忽略模式

- 在 Ignored files and folders 字段中添加 *.flattened-pom.xml。
- 点击 Apply 或 OK 保存设置。