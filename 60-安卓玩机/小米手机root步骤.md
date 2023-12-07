# 小米手机安装 Magisk 获取 Root 权限指南

## 刷机，Root，Magisk，为什么？

### Root 意味着什么？

Root 意味着**自由**。

Root，指的是 root 用户。该用户对设备有**最高的权限**。获取 Root 权限，即修改系统，使得用户和应用能够以 root 用户的身份执行操作，也就是说，用户获得对设备的最高访问权，真正实现了“**我的设备我做主**”。

Root 权限的使用方式主要分为两类。一种是获取系统特权，常见应用如下：

- 利用文件管理器或破解工具自由备份、还原应用的数据和游戏进度。
- 利用系统权限禁用/隐藏应用，或禁止应用后台运行。
- 禁用，或在当前用户空间下卸载系统应用。
- 自由操纵应用的权限，例如禁止自启动。
- 使用内存修改器对游戏数据进行破解。
- 修改受保护的系统设置，例如无障碍服务。
- 修改系统内存，实现更改设备 MAC 地址保护隐私/绕过身份验证等。
- 修改隐藏的设置项，例如使状态栏上的时间精确到秒（这个一般不需要 Root 也能做到）。
- 执行自动化操作。

另一种，为**修改**系统。常见应用如下：

- 定制系统的开机动画。
- 彻底清除、替换系统应用。
- 将应用安装为系统应用。
- 修改内核选项。
- 修改系统构建信息，以实现修改设备的制造商、机型等信息。
- 对系统核心进行破解，以移除应用覆盖安装时的版本和签名检测（对破解游戏比较有用）。
- 调校充电速度等行为。
- 对硬件超频以压榨性能。
- 注入系统进程，以便调整第三方应用的界面、行为。

同样，Root 意味着**风险**。

- 若对恶意软件授予 Root 权限，其将具有非常大的破坏力。
- Root 权限使用时不谨慎，或因为各类天灾人祸，会导致系统损坏与数据丢失。
- 系统更新变得麻烦。若原厂镜像未备份或系统被修改，设备将无法直接接受增量更新，**需要刷机才能升级系统**。

### 我需不需要 Root？

是否需要 Root 取决于你需要进行的操作类型。

如果你的需求在 `adb shell` 下，或使用 `adb` 授权就能够完成（**系统特权**型中的大多数均属于此类），则很可能不需要 Root。如今，更加流行一些免 Root 获得系统特权的权宜之计（例如 [Shizuku API](https://shizuku.rikka.app/zh-hans/)）。相比于 Root，这种方式的风险小得多，更值得提倡。

如果你需要**修改系统**，或从事应用/游戏破解、Android 核心破解等工作，则你需要 Root。

### 为什么是 Magisk？

传统的 Root 权限方案是 SuperSU，该方案主要通过修改系统[分区](https://ak-ioi.com/763-preintro-android-bootmode/#general-partitions) `/system` 来安装 Root 权限。

Magisk 是一个较新的方案，主要优势如下：

- \#️⃣ 轻量化修改。相比于 SuperSU，其只修改比系统分区小得多 Boot 分区。因此，刷机过程要快很多，移除 Root 权限并还原原厂镜像容易得多。
- 🚫 无系统（Systemless）方式。Magisk 不修改系统分区，使得设备接受后续系统更新要容易很多。
- 🧩 模块（Modules）。Magisk 提供许多使用无系统方式修改系统的模块。
- 💧 隐藏（MagiskHide）。Magisk 内置了对其他应用隐藏 Magisk 和 Root 权限的工具，这使得**对 Root 权限敏感的游戏、银行等软件仍然能正常使用**（要求 ≤v23.0 或为 Alpha 版，Android ≤ 11，其他情况下有替代方案）。
- ⚡ 一次性刷机方案。Magisk 的安装只需要一次刷机就能完成，不使用第三方 Recovery 系统。这使得第三方 Recovery 不支持某一设备的问题得到解决，且对系统的安全性影响比较小。

对于较新的设备，Magisk 方案还具有风险极小的特点，具体如下：

- ✅ 无设备支持问题。Magisk 具有对 Android 系统的通用支持，而非对某特定机型的支持，无须寻找适合你的机型的版本，更不用担心找错版本。
- 🔧 仅对 Boot 分区进行修改。这意味着刷机修改能在数秒内完成，且 Fastboot 模式下，**你始终可以在刷入 Boot 镜像前先进行“试用”，确保刷入后系统不会爆掉**。
- 🔒 不使用第三方 Recovery。避免覆盖原厂 Recovery，使得**遇到严重问题 Fastboot 无法正常刷机的情况下，也能通过 Recovery 刷原厂镜像还原**。也使得 Root 对系统安全性的影响降到最低。
- 🗑️ 一键卸载。系统更新前，可以一键将被修改的 Boot 镜像恢复原厂，以正常接受增量系统更新（注：OnePlus 设备检测到 Magisk 后，会自动下载全量更新包，故不需要卸载 Magisk 即可进行系统更新）。

### 为什么刷机？

如果早些时候（2014 年左右）你接触过 Root 权限的获取，你可能会知道许多“**一键 Root**”等免刷机的 Root 权限获取软件，有的系统甚至直接允许用户打开 Root 权限。为什么如今获取 Root 如此麻烦？为什么刷机风险这么大，却又说刷机其实是最明智的选择？

原因之一，是如今“一键 Root”等工具已经不好用了。

这类软件往往使用**系统漏洞**进行破解。事实上，这是一个很大的安全性问题，因为不只是一键 Root 工具可以使用漏洞，其他的任何软件都可以，而一旦恶意软件获取 Root 权限，Android 权限管理对其就形同虚设。如今，随着安全漏洞的修复，此类工具自然也就越来越难用了。

然而，刷机却不利用奇技淫巧，具有**理论可行性**，因而成为了公认的“通解通法”。

原因之二，也是最重要的原因，就是“**权力越大，责任越大**”。我们常说，如果一个设备制造商允许用户刷机并给了教程，那它确实是在支持用户折腾设备；如果设备制造商直接允许在设置中开启 Root 权限，那么它是在给维修点刷业绩。正因如此，我强烈反对使用人工代刷服务来获取 Root 权限。

获取 Root 权限**并非一劳永逸**。由于 Root 权限意味着设备最高访问权，一旦后续使用 Root 权限时不谨慎，系统就可能被弄坏。此时，必须使用刷机方式才能修复设备，而使用“一键 Root”工具的人，往往不具备刷机的知识和技能，因此设备只能被送去维修，或者报废。使用刷机方法获取 Root 的过程中，机主锻炼了自身的技能，并已经下载到或者备份好了原厂镜像。只有这样，机主才算是真正拿到了“搞机资格证”。

刷机会不会清除数据？刷机会不会清除数据？

刷机本身不清除数据。但是，下面几种情况需要清空数据。

- 用正常 Fastboot 方式解锁 Bootloader，会一并清除数据。（通常，这只需要做一次）
- 安装第三方操作系统，通常要自行清空数据，否则系统无法正常工作。
- 获取 Root 权限后，不当修改系统数据、禁用系统组件，设备出现无法开机、无限重启的问题。

各种各样的刷机事故也会导致需要清除数据。因此，开始前，请**对重要数据做好备份**。

## 一定能成功吗？

一般是的。但是下面是一些有可能发生的问题。

- 使用版本不对的 Boot 镜像，系统不能正常启动。
- Magisk 版本对当前 Android 版本不支持，系统不能正常启动。（这种情况发生后可自行撤销更改）
- 网上找不到版本合适的全量更新包。（购机前可事先考证。请注意，官网上的更新包肯能不是最新的）
- **此设备登录了非你本人的 HeyTap 账户且开启了查找设备。**（这种情况请不要解锁 Bootloader 刷机，否则会导致设备被锁，输入账户的密码才能解锁）

## 准备工作

### 如果需要，学好基础知识

[[基础预科\] ADB、Android 终端、Android 用户权限](https://ak-ioi.com/714-preintro-adb/)

[[基础预科\] Android 分区、启动模式、Fastboot](https://ak-ioi.com/763-preintro-android-bootmode/)

### 确认设备如何强制关机

开始刷机操作前，请确认自己知道如何强制关机或重启设备，**并且已经尝试成功过**。常见方法有这些：

- 拔掉充电器，然后拆除内置电池，将会关机。（适用于电池可拆卸的设备）
- 长按电源按钮 10s，强制重启。（适用于较老的设备）
- 同时按住电源和音量上按钮，保持 10s，待屏幕熄灭或感受到振动后立即放开，即为强制关机。（适用于较新的设备）

### 确认如何从关机状态进入 Fastboot

请确认自己知道如何从关机状态下进入 Fastboot 模式，**并且已经尝试成功过**。

有些文章会告诉你可以通过 USB 调试从开机状态下重启进入 Fastboot。**请不要仅仅满足于这么做**，因为若刷机中途失误，你可能必须直接进入 Fastboot 进行修复，而无法开机，再通过 USB 调试进入。

~~你看，这篇文章的“准备工作”章节就根本没要求你打开 USB 调试。~~

对于 OnePlus 设备，具体有两种情况。

较老设备：

| 操作     | 按键组合               | 功能             |
| -------- | ---------------------- | ---------------- |
| 关机长按 | 电源 + 音量上          | Recovery 模式    |
| 关机长按 | 电源 + 音量下          | Fastboot 模式    |
| 关机长按 | 电源 + 音量上 + 音量下 | 无法启动[待考证] |

较新设备：

| 操作     | 按键组合               | 功能                                                         |
| -------- | ---------------------- | ------------------------------------------------------------ |
| 关机长按 | 电源 + 音量上          | 正常启动                                                     |
| 关机长按 | 电源 + 音量下          | I. 若 Bootloader 未解锁，则 Recovery 模式 II. 若 Bootloader 已解锁，则 Fastboot 模式 |
| 关机长按 | 电源 + 音量上 + 音量下 | Fastboot 模式                                                |

![img](https://ak-ioi.com/wp-content/uploads/2022/07/26bd642a6eccbddd637df0706c793d0b.png)

▲ OnePlus 6T 的 Fastboot 界面实拍。请注意 START 的意思是重启进入正常系统。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/7fc3b36510f40e67fb14dabfd14c4aa1.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/afb1562ff69786c1ee717fbdde54e6c3.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/3cb9d19cf7487cd4ed132b6b7d1e6842.png)

▲ 效果图。此界面可执行几个简单的操作。按音量键选择要进行的操作，电源键确认。

注：如果你的机型无法退出 Fastboot 模式，请参照强制关机的方法。

### 确认 USB 接触良好

接触良好的 USB 接口和数据线是刷机的基础。若刷机过程中连接断开，将产生无法开机的后果（重新刷入受损的分区可以恢复）。

建议使用 Type-C 接口的 USB 集线器，刷机过程中不要在集线器上插拔设备。

提示：Fastboot 刷入 Boot 分区，大约需要 2.5s。

### 安装 ADB 环境

若电脑上没有 ADB，请先安装。方法参照[此处](https://ak-ioi.com/714-preintro-adb/#install-adb)。

你安装的 ADB 中应该会有 `fastboot.exe`，否则寄。

安装后，在命令行中执行命令 `fastboot --version` 验证你的安装。[【搜索“Windows 命令行”】](https://www.bing.com/search?q=Windows+命令行&mkt=zh-CN)

### 允许 OEM 解锁

进入开发者选项，打开“允许 OEM 解锁”开关，按提示输入设备锁屏密码，以允许后续解锁 Bootloader。[【搜索“OnePlus 开启开发者选项”】](https://cn.bing.com/search?q=开发者选项&pglt=675)

此开关一般位于开发者选项第一屏内。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/d32401a884c5eedb19d42d7c3e24e194.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/414884ae2ad4c91e68c9320cfa3e3ee8.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/67aa876265a2f41ce33ae35d7112a8de.png)

注：**该操作并没有解锁 Bootloader**，只是允许解锁。

### 关闭系统自动更新

系统更新过程会移除已安装的 Magisk。为防止这种意外，应当禁止系统自动更新。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/ba570f0afdc03ea568afab831d37bc3a.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/68fb52056d39aa9f4d6450a7ac81b480.png)

### 确认云账户状态

如果设备已登录云账户且已经开启“查找设备”，请确保自己知道这个云账户的密码，并在解锁 Bootloader 前退出账户。

若没有退出，**则再次启动后设备会被锁定，输入云账户密码方可解锁**。

### 调整心态

刷机是有风险的操作。然而，对于 OnePlus 设备和 Magisk 方案，风险实际上极小。请放松心态。

刷机时，请选择安排不紧张的时间段，保证至少一小时的连续空闲时间，切忌仓促行事，否则容易犯错。

操作过程中，时刻记住，设备不会被轻易搞坏，即使搞坏了大概率也能自己救。由于采用 Magisk 方案，你可以告诉自己任何更改前，都有机会先“试用”待刷的镜像，观察其能否正常工作（本文章也会让你这么干）。

本文章会告诉你一些常见的故障如何处理。请看下文每个步骤后的“快速故障排除”表。

## 概览

Magisk 要修改 Boot 镜像，然而，在没有 Root 权限时，并没有办法直接提取 Boot 镜像，也无法将修改的镜像直接写入设备。因此，我们必须先从系统更新全量包中提取镜像，交给 Magisk App 进行“修补”，然后自己刷入。

这只是概览，不要直接对着操作。预计用时假设操作者是新手，但操作顺利。

- 安装 Magisk App

   

  5分钟

  - 🎇 选择合适的 Magisk 版本 2分钟
  - 🔰 下载并安装 App 3分钟
  - 👀 查看 Ramdisk 是否为“是”，确认是否受支持 0分钟

- 从全量包提取原厂镜像

   

  16-23分钟

  - 💻 下载全量包（尽可能选择一致的版本） 15分钟
  - 🪛 若版本不一致，将下载的全量包通过 Recovery 刷入 0-7分钟
  - 🧵 取出全量包中的 Boot 镜像 1分钟

- 解锁 Bootloader

   

  6分钟

  - ⭕ 进入 Fastboot 0分钟
  - 🔌 安装驱动，调试 Fastboot 连接 2分钟
  - 🔓 发起解锁命令并确认 1分钟
  - ⭕ 重启设备，待数据清除完毕并开机一次 2分钟
  - 👀 检查解锁状态 1分钟

- 测试原厂镜像

   

  4分钟

  - ⭕ 进入 Fastboot 0分钟
  - 🪄 传入你提取的原厂镜像进行试用 1分钟
  - ✅ 确认设备工作正常 3分钟

- 修补镜像

   

  6分钟

  - 🔰 重新安装 Magisk App 2分钟
  - 🩹 利用 Magisk App 修补镜像 3分钟
  - ⏏️ 导出新镜像 1分钟

- 试用镜像并确认安装

   

  5分钟

  - ⭕ 进入 Fastboot 0分钟
  - 🪄 传入修补后的镜像进行试用 1分钟
  - ✅ 确认设备工作正常 3分钟
  - ⚡ 确认安装 1分钟
  - ⭕ 重启设备 0分钟

- 开机体验

   

  1分钟

  - ✨ 打开需要 Root 权限的应用，或安装模块，开始使用

共计 43-50 分钟。

请注意，接下来请按照下面的指示进行操作，不要中断。教程未要求重启时，请勿自行重启。

选择确认安装前，设备的系统并没有受到更改。

若要中断 Magisk 的安装，只须断开 USB 连接，重启设备，然后卸载 Magisk App。

若安装后需要恢复，建议直接使用 Recovery 模式刷入官方全量包。

## 安装 Magisk App

### 选择合适的 Magisk 版本

过时内容提醒：目前功能最强大的 Magisk 版本或许是 [Magisk Delta](https://huskydg.github.io/magisk-files/intro.html)。

对于一般的用户，建议使用 Magisk 稳定版或 Magisk Alpha。

选择版本原则如下：

- 若无特殊需求，尽量选择稳定版与较新版本。
- Android 11 或更高版本的用户，**不得**选择稳定版 v23.0 或更低版本。
- 如果你知道 Zygisk 是什么并且需要，必须选择稳定版 v24.0 或更高版本，或 Magisk Alpha。
- 如果你需要使用 Magisk 的隐身斗篷 MagiskHide（不可与 Zygisk 共存，不能工作于 Android 12 或更高），必须选择稳定版 v23.0 或更低版本，或 Magisk Alpha。
  提示：如果你使用 Zygisk，那么存在 MagiskHide 的替代方案，选择版本时你不需要考虑这一条。
- 如果对稳定性要求高，请选择稳定版的某一版本。

[Magisk 稳定版仓库](https://github.com/topjohnwu/Magisk/releases) [Magisk Alpha 下载](https://h1335344215.gitee.io/magisk-alpha/)

下载到合适的 APK 文件后，将其传输至手机完成安装。

### 查看支持情况

打开 Magisk App，观察主页上的参数。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/c8349a6fd5a83cf586470fb8497e0826.png)

**若 Ramdisk 一栏为“是”，则你的设备可以安装 Magisk**。提示：目前没有已知的 OnePlus 设备存在不支持问题，且 Ramdisk 在 Android 11 之后被强制要求，故后续也不会出现类似问题。

| 快速故障排除                                                 |
| ------------------------------------------------------------ |
| **Q：Ramdisk 显示“否”，能否继续？**                          |
| A：不建议继续。这里可能存在误检测情况，但目前已知的误检测只会发生在小米设备上。 |

## 从全量包提取原厂镜像

### 下载全量包

先打开系统设置，查看你设备的系统版本号。

在网络上搜索 <你的设备名称> + “官方固件”，找到**对应版本**的固件并下载。若没有找到对应版本，尽量下载更新的版本；如果还是没有，请找到与当前版本尽可能接近的版本。

注：目前官方网站上版本不全。可以找一找民间的下载。

| 快速故障排除                  |
| ----------------------------- |
| **Q：应当去哪里找全量包？**   |
| A：没有固定答案，请自行搜索。 |

### 刷入全量包（可选）

若你的全量包版本比当前系统版本新，或者与当前系统版本相差太远，为减少出问题的可能性，可以先用 Recovery 模式刷入当前全量包，将系统变为该版本。[【搜索“OnePlus 刷入官方固件”】](https://cn.bing.com/search?q=OnePlus+刷入官方固件)

### 提取 Boot 镜像

将全量包解压，将得到若干个 zip 压缩包。请逐一查看，找出含有 `boot.img` 文件的压缩包并解压出来。

## 解锁 Bootloader

### 连接 Fastboot

将设备关机，启动进入 Fastboot 模式，然后使用数据线连接至电脑（操作顺序请勿颠倒）。

在命令行中执行命令 `fastboot devices`，查看设备是否连接并识别。

```plain
C:\Users\[redacted]>fastboot devices
0123456789ABCDEF        fastboot
```

上述命令无输出的解决方法上述命令无输出的解决方法

1. 打开 Windows 设备管理器。[【搜索“Windows 设备管理器”】](https://cn.bing.com/search?q=Windows+设备管理器)
2. 找到无法识别的 “Android” 设备，右键，选择“更新驱动程序”。
   ![img](https://ak-ioi.com/wp-content/uploads/2022/01/a463fd7bd3b6112ad0e9b5d592ad249d.png)
3. 选择“浏览我的电脑以查找驱动程序”“让我从计算机的可用驱动程序列表中选取”。
4. 选择 Android Composite ADB Interface。
   ![img](https://ak-ioi.com/wp-content/uploads/2022/01/899bb798ba9c71f84aa28197132bc2c1.png)
   如果这一步系统找不到驱动程序，则系统存在 ADB 驱动缺失问题。请[搜索“adb 驱动缺失”](https://cn.bing.com/search?q=adb+驱动缺失)，然后像安装 ADB 驱动一样安装 Fastboot 的驱动。
5. 完成后，将看到设备为可用状态。
   ![img](https://ak-ioi.com/wp-content/uploads/2022/01/10daec1a01797c254f88a9a0b98071c3.png)
6. 重新执行 `fastboot devices`，将能够看到设备。

**若能够看到设备已连接，则说明连接成功**。

| 快速故障排除                                                |
| ----------------------------------------------------------- |
| **Q：始终无法检测到设备。**                                 |
| A：请按上面说明安装驱动。如果仍然遇到问题，请自行搜索解决。 |

### 发送解锁命令

请注意，**解锁 Bootloader 将清空你的用户数据**。请对重要内容做好备份。

解锁后**不建议重新锁定**。若设备镜像未恢复原厂状态，这会导致无法开机。

连接好 Fastboot 模式下的设备，运行命令 `fastboot flashing unlock`。

此时设备上将弹出警告文字，**请仔细阅读全部文字**（以你设备上显示的文字为准）。读完后，按音量键，使得 UNLOCK THE BOOTLOADER 被选中，然后按电源键确认。完成后，电脑上将显示 OKAY 字样。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/20eea79cdf7c5c3cdf502d624af39e52.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/484fee31bef766186dcc6b0874eccc44.png)

接下来请看 Fastboot 界面上的 DEVICE STATE。请确保显示 unlocked。

| 快速故障排除                                                 |
| ------------------------------------------------------------ |
| **Q：无法解锁，显示 Permission Denied。**                    |
| A：请确保已经在设置中开启“允许 OEM 解锁”。若不是 OnePlus 手机，解锁会更加麻烦，请参考该品牌的官方说明。 |
| **Q：解锁是否会对数据安全造成威胁？**                        |
| A：一定程度上会（具体表现为设备加密失效，设备丢失后数据更容易被窃取）。请慎重对待。 |
| **Q：如何重新锁定？**                                        |
| A：`fastboot flashing relock`。然而一旦修改过系统，不建议重新锁定。 |

### 重启清空数据

完成后，运行命令 `fastboot reboot`（或在手机上选择操作 START）重启。

接下来，手机会先重启进入 Recovery 模式以清空数据。完成后，手机将再次重启，这一次重启会花费比往常更多的时间。重启后，请再次完成手机的初次使用设置。

然后不妨进入开发者选项（你需要重新启用开发者选项）看一眼。此时，**“允许 OEM 解锁”设置的开关应当为开启状态并变为灰色，下方显示字样“引导加载程序已解锁”**。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/6b4dd192e6295907dac026becb45afaa.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/e5224d4279703e2846b3f79f1fe0c74a.png)

安装 Magisk 后，这个灰色开关可能会恢复原样，但改变其状态并不能改变 Bootloader 的解锁状态。

这是 Magisk 为了避免系统及应用检测到设备已被解锁（处于“不安全”状态）而采取的措施。

| 快速故障排除                                                 |
| ------------------------------------------------------------ |
| **Q：开发者选项中的 OEM 解锁开关状态不正常。**               |
| A：这可能不是大问题。请以 Fastboot 界面上的 DEVICE STATE 为准。 |
| **Q：重启大概需要多久？**                                    |
| A：根据系统预编译的程度，30s 至 5min 不等。如果超过 10min，则为不正常状况，请强制重启。 |

## 测试原厂镜像

在开始修改原厂镜像前，我们应当先试试你拿到的“原厂”Boot 镜像能否正常工作，特别是其版本与你系统版本不一致时。

### 原厂镜像试用启动

将设备关机，启动进入 Fastboot 模式，然后使用数据线连接至电脑（操作顺序请勿颠倒）。

运行命令 `fastboot boot <boot 镜像文件>`，将会把此镜像传输至手机。手机会暂时地使用这一镜像进行启动，而不会直接将其刷入。你将会看到手机先回到带有“Fastboot Mode”字样的 Logo 界面，然后播放开机动画，进入系统。

```plain
C:\Users\[redacted]>fastboot boot "E:\__my_workspace\BrushMachine\Oneplus 9R\[redacted]\boot-20220710.img"
Sending 'boot.img' (98304 KB)                      OKAY [  2.271s]
Booting                                            OKAY [  0.169s]
Finished. Total time: 2.490s
```

![img](https://ak-ioi.com/wp-content/uploads/2022/07/f8c4e010b19b8856cc157b7ea0f06bf8.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/5f9e4877151caaf7f35c91ddf6cb2566.png)

注意，开机动画显示异常、开机时间比正常开机长、开机后的卡顿比正常情况长、开机后一段时间不显示锁屏等，**都不是正常现象**。如果出现这类情况，说明此镜像不能正常工作。

请注意区分 `fastboot boot` 和 `fastboot flash boot`。

- 前者是试用启动，只是暂时地用镜像启动设备，而不会修改设备。
- 后者是刷入镜像，会将镜像直接写入 Boot 分区。

| 快速故障排除                                                 |
| ------------------------------------------------------------ |
| **Q：错误 Permission Denied。**                              |
| A：请再次检查 Bootloader 是否已解锁。                        |
| **Q：错误 Unknown Command。**                                |
| A：你的设备不支持试用启动。如果你头铁，请跳过这一步继续（可能需要同时参考其他教程）。 |
| **Q：错误 is not a boot image。**                            |
| A：请检查传入的镜像是否正确。                                |

### 检查是否工作正常

请依次检查这些硬件是否正常工作。

- 显示与触屏
- 屏幕指纹（如果有）
- 重力/加速度传感器
- 摄像头
- 麦克风
- WiFi 连接
- 移动数据连接
- 扬声器
- 耳机接口（如果有）
- 静音开关（如果有）

请确保通知栏、导航等系统界面功能正常。

**如果出现任何异常，都请返回重新下载合适的镜像**，不要继续操作。

| 快速故障排除                                                 |
| ------------------------------------------------------------ |
| **Q：试用启动期间是否会保存我产生的数据？**                  |
| A：会。除 Boot 镜像是临时的以外，试用启动与正常启动没有其他区别。 |

## 修补镜像

如果上述测试一切正常，你可以选择重启设备，也可以直接在试用状态下继续。现在，使用 Magisk App 修补你的原厂镜像。

### 重新安装 Magisk App

由于前面清空过数据，Magisk App 已经无了。请将你下载的 APK 传输到手机重新安装。

### 修补镜像

将你的原厂镜像传输到手机中。

打开 Magisk App，点击“安装”，选择“选择并修补一个文件”，完成镜像修补。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/bf3c6ced542cea9e7273a7a154b8aa4a.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/0f90c3bee3bad3617e471403a167354e.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/b04323b76496a875b5da58535a118c44.png)
![img](https://ak-ioi.com/wp-content/uploads/2022/07/4db68e32a616f5fade75119f72b22625.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/dd11e4c0a68d476eaa2b3a2e2334f5ba.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/86e518c1126a65e1121553835086e2d7.png)

修补后的镜像存在 `/sdcard/Download/` 下。请对其进行重命名或移动，然后传输至电脑。**请仍然保管好修补前的镜像，并做好区分以防混淆**。

| 快速故障排除                   |
| ------------------------------ |
| **Q：要不要选择修补 vbmeta？** |
| A：一般是不需要的。            |

## 试用镜像并确认安装

接下来，我们测试修补后的镜像是否正常工作。如果正常工作，接下来可以直接用 Magisk App 确认安装，不需要自行刷入。

### 修补后镜像试用

将设备关机，启动进入 Fastboot 模式，然后使用数据线连接至电脑（操作顺序请勿颠倒）。

运行命令 `fastboot boot <boot 修补后镜像文件>`，使用修补后镜像启动。此次启动，你的系统将暂时具有 Magisk。

### 检查是否工作正常

先参照上文章节，检查设备各种功能是否工作正常。

完成后，打开 Magisk App，主页上将检测出 Magisk 版本。

| 快速故障排除                                                 |
| ------------------------------------------------------------ |
| **Q：设备不能正常启动。**                                    |
| A：这说明你的 Magisk 版本与 Android 版本不兼容，请使用更新的版本。 |
| **Q：Magisk 检测不到版本。**                                 |
| A：这说明你的设备不支持 Magisk。                             |

### 确认安装

确认一切无误后，点击 Magisk App 主页上的“安装”，此时将能够选择“直接安装”选项。选择该选项完成安装即可。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/c30c09813bc0fca2f652002cef084f8d.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/f6fa03daed5a29993172f2ced989e95d.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/14cecd665dbd8256aff5ad12371479e3.png)

完成后重启，就正式完成了安装。

## 附录：系统更新的方法

系统更新后不需要重新解锁，但需要重新刷入 Magisk。（设备支持 A/B 无缝系统更新的除外，见下文）

对于已安装 Magisk 需要更新系统的设备，可以通过某些手段从官方渠道下载更新包中的分包（大小约为全量包的一半），提取可靠的 `boot.img`。

此处关于提取全量包下载网址的说明以 OnePlus 9R 为例，其他设备情况不尽相同。

### 前置要求

- 设备已获取 Root 权限
- OnePlus 系统更新检测到 Magisk，决定下载全量包（系统更新界面此时会显示文件大小是好几 GB 而非几十 MB）

提示：如果你的系统安装了 Magisk 却没有自动下载全量包，请下载差量包后选择安装更新，更新失败后系统将改用全量包。

### 下载更新

请先确保关闭“夜间自动安装”。然后下载更新，直至下载完成。先不要选择安装。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/b8c7d6413a65b98566455870c2546746.png)

### 查询地址并下载分包

使用合适的文件管理器取出 `/data/data/com.oppo.ota/databases/ota.db`（或 `/data/data/com.oplus.ota/databases/ota.db`），复制到 `/sdcard/` 下，然后使用合适的 SQLite 查看器打开。另拷一份到电脑备用。

找到 `system_vendor` 包对应的行，然后找到 `url` 列，复制出单元格的内容。这就是包含 `boot.img` 的分包的下载地址。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/9cc6623b5dfd40a0cd12f1bf00ce53d5.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/5767c2d94582153360e0e623ca063d8d.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/4f3b7d1e7e09c058ddc7cb913bea3b08.png)

用浏览器访问该地址，下载分包，提取出其中的 `boot.img`。

### 镜像修补

将 `boot.img` 传输至手机进行修补，然后重新传输到电脑。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/bf3c6ced542cea9e7273a7a154b8aa4a.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/0f90c3bee3bad3617e471403a167354e.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/b04323b76496a875b5da58535a118c44.png)
![img](https://ak-ioi.com/wp-content/uploads/2022/07/4db68e32a616f5fade75119f72b22625.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/dd11e4c0a68d476eaa2b3a2e2334f5ba.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/86e518c1126a65e1121553835086e2d7.png)

### 安装更新

在手机上直接安装系统更新，待所有流程完成后，关机。

### 试用并确认

打开 Fastboot 模式，试用启动修补后的 `boot.img`。参照上文检查设备工作是否正常。

```plain
E:\__my_workspace\BrushMachine\Oneplus 9R\[redacted]>fastboot boot "E:\__my_workspace\BrushMachine\Oneplus 9R\[redacted]\magisk_patched-24308_rqYSN.img"
Sending 'boot.img' (98304 KB)                      OKAY [  2.276s]
Booting                                            OKAY [  0.165s]
Finished. Total time: 2.495s
```

![img](https://ak-ioi.com/wp-content/uploads/2022/07/f8c4e010b19b8856cc157b7ea0f06bf8.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/5f9e4877151caaf7f35c91ddf6cb2566.png)

若无问题，打开 Magisk App 确认安装。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/3d1271629c542ae32b083471cd0fb11f.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/d2fe78d3913c17fb1dbdbff1b6e137aa.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/ad47467d81e0946526bc56916373b76b.png)

## 附录：A/B 无缝系统更新

此类系统更新可以在后台静默执行。更新完后，重启即可立即体验新版本。

此类系统更新完成后，请先不要重启。打开 Magisk App，点击“安装”，选择“安装到未使用的槽位（OTA 后）”，然后重启即可使用。

## 附录：隐藏 Magisk 和 Root

Magisk 和 Root 好用好玩之处固然多，然而有的应用会检测用户的 Magisk 与 Root，若发现会警告用户甚至拒绝加载。为防止它们受到影响，需要对 Magisk 和 Root 进行隐藏。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/ff2fa6cc1f2c0eb83eae6b5996f59598.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/f08c7f6a0775e55c9842340b70d0c820.png)

过时内容提醒：目前隐藏 Magisk 和 Root 的最佳方法或许是使用非官方的 Magisk 版本 [Magisk Delta](https://huskydg.github.io/magisk-files/intro.html)。

### 卵用没有 - 隐藏 App

少数应用可能通过检测系统上的 Magisk App 来发现 Magisk（目前笔者暂未找到例子）。这种检测利用的是包名。通过使用 Magisk App 的隐藏功能，可以为 Magisk App 随机生成包名，重新安装。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/157b0a91bc44fc9df8d0a2ccc541190b.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/b714556c6b8a2142d88c8ad507a5be78.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/454d5afb5712ca871cdf966e5bcc14e1.png)

伪装应用的名称一般不影响效果。

### 隐身斗篷 - MagiskHide

- 不可与 Zygisk 同时使用
- 支持 Android：≤11
- Magisk：≤v23.0 或 Alpha

MagiskHide 是 Magisk 官方提供的 Root 隐藏工具，但目前已经从稳定版中移除，Alpha 版也停止对其维护。

在 Magisk 设置中，可启用 MagiskHide 开关。接下来，打开排除列表（对于稳定版 ≤v23.0，从主页切换到“超级用户”选项卡，顶部会出现“MagiskHide”菜单），选择你**需要对其隐藏** Magisk 的应用。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/157b0a91bc44fc9df8d0a2ccc541190b.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/2a7ce22440870a193bb4ffbf928f3c41.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/b1cbbd18a7575430c470f99ff00177d9.png)

点击应用图标，可以打开其进程列表。建议对所有进程开启，否则隐藏可能无效。

### 君子声明 - DenyList

- 必须与 Zygisk 同时使用
- 从 Magisk 修改中排除 - 不可对该应用使用 Xposed 等注入，同时 su 也不会被注入，从而一般应用不会检测到 Root 报错
- 本身不提供隐藏措施 - 应用仍然能通过查找二进制文件、判断系统属性等方法检测
- 支持 Android：≥6
- Magisk：≥v24.0 或 Alpha

Zygisk 模式下，Magisk 的所有更改通过均通过向应用进程中注入实现。对于 DenyList 中的应用，Magisk 不会进行注入，故该应用也不会检测到 su 文件，使用一般检测方法不会检测 Root。然而，该模式“本身不提供任何隐藏措施”，应用理论上可以通过其他方法检测。

DenyList 中的应用，也无法通过基于 Magisk 的 LSPosed 等框架进行注入。

在 Magisk 设置中，启用“遵循排除列表”开关。接下来，打开排除列表，选择你**需要对其排除 Magisk 注入**的应用进程。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/157b0a91bc44fc9df8d0a2ccc541190b.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/325e1ddc8563d72177714ac7b4802165.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/07f8b507162150c9a40852ccd6100458.png)

### 我全都要 - Shamiko

- 第三方 Magisk 模块
- 必须与 Zygisk 同时使用
- 目标应用仍能接受 Xposed 等框架的注入。
- 像 MagiskHide 一样提供基本的 Root 隐藏措施。
- 支持 Android：≥6
- Magisk：≥v24.0 或 Alpha

[下载 Shimako](https://github.com/LSPosed/LSPosed.github.io)

这是 Zygisk 环境下 MagiskHide 的替代品（来自 LSPosed Developers），可谓两全其美之法。使用此模块不需要安装 LSPosed。

将下载的 zip 作为 Magisk 模块安装。随后进入 Magisk 设置，关闭“遵循排除列表”开关即可。仍然需要在排除列表界面中选择你**需要对其隐藏** Magisk 的应用。

![img](https://ak-ioi.com/wp-content/uploads/2022/07/968d68cd4c0444db093066071e5c6d6f.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/75ede6593b46729c4b282fa70e627c53.png) ![img](https://ak-ioi.com/wp-content/uploads/2022/07/1e0ef97a55ec8c7be7443cc940e9b44f.png)

## 附录：救砖常见方法

刷机或使用 Root 不当可能造成系统被破坏无法启动，手机变得如同板砖一样，这种情况被称为“变砖”。

### Magisk 模块导致

Fastboot 模式下，用原 Boot 镜像试用启动，然后重启到安全模式，Magisk 会禁用所有模块。

### 系统被修改损坏

使用 Recovery 刷入全量包，即可还原系统修改。

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