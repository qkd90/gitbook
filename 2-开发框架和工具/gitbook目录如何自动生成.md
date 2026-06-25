# GitBook 目录如何自动生成

## 背景

GitBook 使用 `SUMMARY.md` 作为左侧目录。文档较多时，手工维护目录容易遗漏、路径出错或顺序混乱，可以使用目录生成工具自动扫描 Markdown 文件。

本项目使用 `book.json` 配置：

```json
{
    "title": "一条大数据之路",
    "outputfile": "SUMMARY.md",
    "catalog": "all",
    "ignores": [],
    "unchanged": [],
    "sortedBy": "-",
    "disableTitleFormatting": true
}
```

## 安装工具

```bash
npm install -g gitbook-summary
```

如果没有安装 Node.js，需要先安装 Node.js 和 npm。

## 生成目录

在项目根目录执行：

```bash
book sm
```

执行后会重新生成 `SUMMARY.md`。

## 推荐目录规范

```text
一级目录
  ├─ README.md
  ├─ 主题一.md
  ├─ 主题二.md
  └─ 子目录
      ├─ README.md
      └─ 具体文档.md
```

建议每个一级目录和重要二级目录都放一个 `README.md`，作为章节导读。

## 常见问题

### 中文路径显示异常

确认文件保存为 UTF-8 编码，并在支持 UTF-8 的终端中查看。

PowerShell 可以先设置输出编码：

```powershell
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
```

### 新增文件没有出现在目录中

检查：

- 文件扩展名是否为 `.md`。
- 是否在 `book.json` 的 `ignores` 中被忽略。
- 是否已经重新执行 `book sm`。

### 目录顺序不符合预期

当前项目大量目录使用数字前缀，例如 `1-Java开发`、`2-开发框架和工具`。新增章节时建议继续使用数字前缀控制排序。
