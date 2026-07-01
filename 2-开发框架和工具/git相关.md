# 1. Git 是什么

Git 是一个分布式版本控制系统，用来记录代码修改历史、支持多人协作、分支开发、版本回退和代码合并。Git 官方文档把文件状态分为三个核心阶段：**已修改 modified**、**已暂存 staged**、**已提交 committed**；理解这三个状态，是掌握 Git 的关键。

简单理解：

```
工作区 Working Directory
  ↓ git add
暂存区 Staging Area / Index
  ↓ git commit
本地仓库 Local Repository
  ↓ git push
远程仓库 Remote Repository
```

------

# 2. 常用术语

| 术语        | 含义                               |
| ----------- | ---------------------------------- |
| 工作区      | 你本地正在编辑的代码目录           |
| 暂存区      | 准备提交的文件集合                 |
| 本地仓库    | 本机 `.git` 目录保存的完整版本历史 |
| 远程仓库    | Gogs/GitLab/GitHub 上的仓库        |
| commit      | 一次代码提交记录                   |
| branch      | 分支                               |
| master/main | 主分支                             |
| origin      | 默认远程仓库名称                   |
| clone       | 克隆远程仓库到本地                 |
| pull        | 拉取远程代码并合并到当前分支       |
| push        | 推送本地提交到远程                 |
| merge       | 合并分支                           |
| rebase      | 变基，让提交历史更线性             |
| conflict    | 合并冲突                           |
| tag         | 标签，常用于版本发布               |

------

# 3. 安装与初始化配置

## 3.1 检查 Git 是否安装

```
git --version
```

如果能看到版本号，说明 Git 已安装。

------

## 3.2 配置用户名和邮箱

这是提交记录里显示的作者信息。

```
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

查看配置：

```
git config --global --list
```

查看当前项目配置：

```
git config --local --list
```

------

## 3.3 推荐基础配置

```
# 设置默认编辑器，可选
git config --global core.editor "vim"

# Windows 下建议打开路径中文显示
git config --global core.quotepath false

# 设置默认拉取策略，二选一
git config --global pull.rebase false
```

如果团队希望提交历史更线性，也可以使用：

```
git config --global pull.rebase true
```

`git pull` 本质上会先执行 `fetch`，再根据配置执行 `merge` 或 `rebase`；如果本地和远程分支都产生了新提交，就需要明确使用 `--rebase` 或 `--no-rebase` 等方式处理分叉历史。

------

# 4. 获取代码仓库

## 4.1 克隆远程仓库

```
git clone http://gogs.sinocare.com/SinoHealth/glucose-wave.git
```

克隆后进入目录：

```
cd glucose-wave
```

`git clone` 会创建一个新的本地目录，并生成远程跟踪分支；默认情况下也会创建名为 `origin` 的远程仓库配置。

------

## 4.2 查看远程仓库地址

```
git remote -v
```

示例输出：

```
origin  http://gogs.sinocare.com/SinoHealth/glucose-wave.git (fetch)
origin  http://gogs.sinocare.com/SinoHealth/glucose-wave.git (push)
```

------

## 4.3 修改远程仓库地址

HTTP 地址：

```
git remote set-url origin http://gogs.sinocare.com/SinoHealth/glucose-wave.git
```

SSH 地址：

```
git remote set-url origin git@gogs.sinocare.com:SinoHealth/glucose-wave.git
```

查看是否修改成功：

```
git remote -v
```

Git 官方文档中，“远程仓库”是协作的核心概念，日常需要掌握添加、删除、查看、修改远程仓库以及推送/拉取数据等操作。

------

# 5. 日常开发基本流程

## 5.1 查看当前状态

```
git status
```

简洁版：

```
git status -s
```

常见状态：

```
M  文件已修改
A  文件已添加
D  文件已删除
?? 未跟踪文件
```

------

## 5.2 查看具体修改内容

查看所有未暂存修改：

```
git diff
```

查看已经 `git add` 到暂存区的修改：

```
git diff --cached
```

查看某个文件的修改：

```
git diff src/main.py
```

------

## 5.3 添加文件到暂存区

添加单个文件：

```
git add src/main.py
```

添加当前目录下所有修改：

```
git add .
```

添加所有修改、删除、新增文件：

```
git add -A
```

------

## 5.4 提交代码

```
git commit -m "fix: 修复血糖数据同步异常"
```

推荐提交信息格式：

```
类型: 简短描述
```

常用类型：

| 类型     | 含义                   |
| -------- | ---------------------- |
| feat     | 新功能                 |
| fix      | 修复 bug               |
| docs     | 文档修改               |
| style    | 格式调整，不影响逻辑   |
| refactor | 重构                   |
| test     | 测试相关               |
| chore    | 构建、依赖、脚本等杂项 |
| perf     | 性能优化               |

示例：

```
git commit -m "feat: 新增血糖趋势图"
git commit -m "fix: 修复登录 token 过期问题"
git commit -m "docs: 更新部署说明"
```

------

## 5.5 推送到远程仓库

```
git push origin master
```

第一次推送新分支时：

```
git push -u origin feature/login
```

`-u` 的作用是建立当前本地分支和远程分支的跟踪关系，以后可以直接执行：

```
git push
git pull
```

`branch.<name>.merge` 与 `branch.<name>.remote` 这类配置会影响 `fetch`、`pull`、`rebase`、`push` 等命令默认使用哪个上游分支。

------

# 6. 分支操作

## 6.1 查看分支

查看本地分支：

```
git branch
```

查看远程分支：

```
git branch -r
```

查看所有分支：

```
git branch -a
```

查看当前分支：

```
git branch --show-current
```

------

## 6.2 创建分支

```
git branch feature/login
```

创建并切换到新分支：

```
git switch -c feature/login
```

老版本 Git 也可以用：

```
git checkout -b feature/login
```

分支的核心作用是让你从主线开发中分离出来，在不影响主分支的情况下独立完成新功能或修复。

------

## 6.3 切换分支

```
git switch master
```

或：

```
git checkout master
```

------

## 6.4 删除分支

删除本地分支：

```
git branch -d feature/login
```

强制删除本地分支：

```
git branch -D feature/login
```

删除远程分支：

```
git push origin --delete feature/login
```

------

## 6.5 分支命名规范

推荐：

```
feature/功能名
bugfix/问题名
hotfix/紧急修复名
release/版本号
test/测试内容
```

示例：

```
feature/glucose-chart
bugfix/login-token-expired
hotfix/push-error
release/v1.2.0
```

------

# 7. 拉取远程代码

## 7.1 fetch：只下载，不合并

```
git fetch origin
```

查看远程更新后，可以再决定是否合并。

PyCharm 官方文档也强调，`fetch` 会下载远程新提交，但不会直接修改你的本地工作代码，所以它是一种比较安全的同步方式。

------

## 7.2 pull：下载并合并

```
git pull origin master
```

等价于大致执行：

```
git fetch origin
git merge origin/master
```

如果你们团队使用 rebase：

```
git pull --rebase origin master
```

`git pull` 的官方说明是：把远程仓库的修改合并到当前分支；更准确地说，它会先运行 `git fetch`，然后根据配置执行 `merge` 或 `rebase`。

------

## 7.3 推荐拉取习惯

每天开始开发前：

```
git switch master
git pull origin master
```

开发自己的功能分支前：

```
git switch master
git pull origin master
git switch -c feature/xxx
```

功能开发过程中同步主分支：

```
git fetch origin
git merge origin/master
```

或者：

```
git fetch origin
git rebase origin/master
```

------

# 8. 推送代码

## 8.1 推送当前分支

```
git push
```

如果当前分支还没有关联远程分支：

```
git push -u origin feature/xxx
```

------

## 8.2 推送到指定分支

```
git push origin master
git push origin feature/login
```

------

## 8.3 强制推送：慎用

```
git push --force
```

更安全一点：

```
git push --force-with-lease
```

不要随便对公共分支执行强制推送，尤其是：

```
master
main
develop
release/*
```

`git push --force` 可能覆盖远程引用；官方文档也提示，`--force` 作用范围可能影响多个被推送的引用，因此团队协作中必须谨慎使用。

------

# 9. 合并分支

## 9.1 merge 合并

假设你在 `master` 分支，要合并 `feature/login`：

```
git switch master
git pull origin master
git merge feature/login
```

如果没有冲突，提交合并结果：

```
git push origin master
```

Git 官方分支章节使用的典型流程就是：从主线切出功能分支、在功能分支开发、完成后再合并回主线。

------

## 9.2 rebase 变基

假设你在功能分支：

```
git switch feature/login
git fetch origin
git rebase origin/master
```

rebase 的作用是把你的本地提交“移动”到最新的目标分支后面，让提交历史更直线。

常见场景：

```
master:        A---B---C
feature:           \---D---E

rebase 后:

master:        A---B---C
feature:               \---D'---E'
```

官方文档说明，rebase 默认会把提交重新应用到新的基础之上；对于复杂合并历史，还存在 `--rebase-merges` 等选项。

------

## 9.3 merge 和 rebase 怎么选

| 场景                     | 推荐          |
| ------------------------ | ------------- |
| 合并功能到主分支         | merge         |
| 自己的功能分支同步主分支 | rebase        |
| 多人共用的公共分支       | 不建议 rebase |
| 已经推送给别人使用的分支 | 谨慎 rebase   |
| 想保留完整分支历史       | merge         |
| 想提交历史简洁           | rebase        |

------

# 10. 解决冲突

## 10.1 什么情况下会冲突

常见原因：

```
两个人改了同一个文件的同一行
一个人删除文件，另一个人修改文件
两个分支都修改了同一块逻辑
```

------

## 10.2 冲突文件长什么样

```
<<<<<<< HEAD
这是你当前分支的内容
=======
这是被合并分支的内容
>>>>>>> feature/login
```

你需要手动改成最终想要的内容，例如：

```
这是最终保留的内容
```

------

## 10.3 命令行解决冲突流程

执行合并：

```
git merge feature/login
```

出现冲突后查看：

```
git status
```

打开冲突文件，手动处理 `<<<<<<<`、`=======`、`>>>>>>>`。

处理完后：

```
git add 冲突文件
git commit
```

如果是 rebase 过程中冲突：

```
git add 冲突文件
git rebase --continue
```

放弃 rebase：

```
git rebase --abort
```

放弃 merge：

```
git merge --abort
```

------

## 10.4 PyCharm 解决冲突

PyCharm 可以直接做 Git 的提交、推送、分支合并和冲突处理；JetBrains 官方文档也说明 PyCharm 内置 Git 集成，并提供专门的 Git 工具窗口。

常用操作路径：

```
底部 Git / Commit 工具窗口
右上角分支名
Git 菜单
```

解决冲突时，PyCharm 通常会出现：

```
Accept Yours
Accept Theirs
Merge
```

含义：

| 操作          | 含义             |
| ------------- | ---------------- |
| Accept Yours  | 保留当前分支内容 |
| Accept Theirs | 保留对方分支内容 |
| Merge         | 手动合并两边内容 |

------

# 11. 撤销与回滚

这一章最容易误操作，务必注意。

Git 官方文档明确提醒，撤销操作中有些动作无法完全恢复，尤其是会修改工作区或丢弃提交的命令，需要谨慎使用。

------

## 11.1 撤销工作区修改

撤销某个文件的未提交修改：

```
git restore src/main.py
```

撤销所有未提交修改：

```
git restore .
```

老写法：

```
git checkout -- src/main.py
```

------

## 11.2 取消暂存

已经执行了 `git add`，但不想提交：

```
git restore --staged src/main.py
```

取消所有暂存：

```
git restore --staged .
```

------

## 11.3 修改最近一次 commit 信息

```
git commit --amend
```

如果只是改提交信息：

```
git commit --amend -m "fix: 修复推送失败问题"
```

官方文档也把 `git commit --amend` 作为常见的“撤销/修正最近一次提交”的方式。

------

## 11.4 回退到上一个提交，但保留代码修改

```
git reset --soft HEAD~1
```

效果：

```
撤销 commit
保留暂存区内容
代码还在
```

------

## 11.5 回退到上一个提交，保留工作区修改

```
git reset --mixed HEAD~1
```

或：

```
git reset HEAD~1
```

效果：

```
撤销 commit
撤销 git add
代码还在工作区
```

------

## 11.6 强制回退并丢弃修改：危险

```
git reset --hard HEAD~1
```

效果：

```
撤销 commit
丢弃暂存区修改
丢弃工作区修改
```

`git reset --hard` 会同时影响 HEAD、暂存区和工作区，如果使用错误可能导致工作丢失；官方文档也特别提醒该选项有丢失工作的风险。

------

## 11.7 用 revert 安全回滚线上提交

如果代码已经推送到远程，尤其是 `master` 分支，推荐用：

```
git revert 提交ID
```

示例：

```
git revert a1b2c3d
```

它会生成一个新的提交，用来抵消之前的提交。

适合：

```
线上回滚
公共分支回滚
多人协作分支回滚
```

不建议在公共分支上随便：

```
git reset --hard
git push --force
```

------

# 12. 查看历史记录

## 12.1 查看提交历史

```
git log
```

简洁模式：

```
git log --oneline
```

图形化查看：

```
git log --oneline --graph --decorate --all
```

查看某个文件历史：

```
git log -- src/main.py
```

------

## 12.2 查看某次提交详情

```
git show 提交ID
```

示例：

```
git show a1b2c3d
```

------

## 12.3 查看某个文件是谁改的

```
git blame src/main.py
```

------

# 13. stash 临时保存

## 13.1 使用场景

你正在写代码，但突然需要切换分支修 bug，这时可以先把当前未提交修改临时存起来。

------

## 13.2 保存当前修改

```
git stash
```

带说明保存：

```
git stash push -m "临时保存登录功能修改"
```

------

## 13.3 查看 stash 列表

```
git stash list
```

------

## 13.4 恢复最近一次 stash

恢复并保留 stash 记录：

```
git stash apply
```

恢复并删除 stash 记录：

```
git stash pop
```

恢复指定 stash：

```
git stash apply stash@{1}
```

------

## 13.5 删除 stash

删除指定记录：

```
git stash drop stash@{0}
```

清空所有 stash：

```
git stash clear
```

Git 官方文档把 stash 用于“暂存当前修改、清理工作区”，并和 `git clean` 一起归在工作区清理相关工具中。

------

# 14. 清理未跟踪文件

查看会删除哪些文件：

```
git clean -n
```

删除未跟踪文件：

```
git clean -f
```

删除未跟踪文件和目录：

```
git clean -fd
```

连 `.gitignore` 忽略的文件也删除：

```
git clean -fdx
```

官方文档说明，`git clean -f -d` 会删除未跟踪文件和目录；默认不会删除被 `.gitignore` 忽略的文件，如果加 `-x` 则会连忽略文件一起删除。

危险程度：

| 命令             | 风险                 |
| ---------------- | -------------------- |
| `git clean -n`   | 安全，只预览         |
| `git clean -f`   | 删除未跟踪文件       |
| `git clean -fd`  | 删除未跟踪文件和目录 |
| `git clean -fdx` | 高危，连忽略文件也删 |

------

# 15. 标签 tag 操作

## 15.1 查看标签

```
git tag
```

------

## 15.2 创建轻量标签

```
git tag v1.0.0
```

------

## 15.3 创建带说明的标签

```
git tag -a v1.0.0 -m "发布 1.0.0 版本"
```

------

## 15.4 推送标签

推送单个标签：

```
git push origin v1.0.0
```

推送所有标签：

```
git push origin --tags
```

------

## 15.5 删除标签

删除本地标签：

```
git tag -d v1.0.0
```

删除远程标签：

```
git push origin --delete tag v1.0.0
```

Git 标签常用于标记重要历史点，例如版本发布点 `v1.0`、`v2.0` 等。

------

# 16. `.gitignore` 使用规范

## 16.1 作用

`.gitignore` 用来告诉 Git 哪些文件不需要纳入版本管理。

常见不提交内容：

```
编译产物
日志文件
本地配置
IDE 临时文件
依赖缓存
密钥文件
数据库文件
```

------

## 16.2 Python 项目示例

```
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtualenv
venv/
.env/
.venv/

# PyCharm
.idea/

# Logs
*.log

# Build
dist/
build/
*.egg-info/

# Env
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

注意：如果文件已经被 Git 跟踪，后来再加到 `.gitignore` 里不会自动取消跟踪。

取消跟踪但保留本地文件：

```
git rm --cached .env
```

提交修改：

```
git add .gitignore
git commit -m "chore: 更新 gitignore"
```

------

# 17. 远程账号、密码和凭据处理

你之前遇到的是这类问题：

```
fatal: unable to access 'http://gogs.sinocare.com/...':
The requested URL returned error: 500
```

如果账号刚改过密码，本地 Git/PyCharm/Windows 里可能还缓存着旧凭据。

------

## 17.1 查看当前远程地址

```
git remote -v
```

如果是 HTTP：

```
http://gogs.sinocare.com/xxx/xxx.git
```

那就需要用户名密码或 token。

如果是 SSH：

```
git@gogs.sinocare.com:xxx/xxx.git
```

那就依赖 SSH key。

------

## 17.2 删除 Git 凭据缓存

Git 官方提供了 `git credential` 接口，`reject` 动作可以让已配置的凭据助手删除匹配的已存储凭据。

Windows Git Bash 可以执行：

```
printf "protocol=http\nhost=gogs.sinocare.com\n\n" | git credential reject
```

如果你的远程地址是 HTTPS：

```
printf "protocol=https\nhost=gogs.sinocare.com\n\n" | git credential reject
```

------

## 17.3 Windows 凭据管理器删除

打开：

```
控制面板
  → 凭据管理器
    → Windows 凭据
```

删除类似条目：

```
gogs.sinocare.com
git:http://gogs.sinocare.com
git:https://gogs.sinocare.com
```

然后重新 push：

```
git push origin master
```

这时应该会重新提示输入用户名和新密码。

------

## 17.4 PyCharm 删除密码

PyCharm 的密码管理入口：

```
File
  → Settings
    → Appearance & Behavior
      → System Settings
        → Passwords
```

JetBrains 官方文档说明，PyCharm 并没有完全独立的密码仓库，而是使用系统原生密码管理或 KeePass；如果远程资源的凭据变了，需要到对应的密码存储中更新。

如果使用 KeePass，可以在这个页面找到：

```
Clear
```

用于清除已有密码数据库中的密码。PyCharm 的 Git 远程密码策略也在同一路径配置：`Appearance and Behavior | System Settings | Passwords`。

------

## 17.5 PyCharm 里管理远程仓库地址

路径：

```
Git
  → Manage Remotes
```

可以添加、修改、删除远程仓库地址。JetBrains 官方文档也说明，可以通过 `Git | Manage Remotes` 管理远程仓库，并可在 Push Dialog 中编辑远程地址。

------

# 18. PyCharm 常用 Git 操作

## 18.1 查看修改文件

```
Alt + 0
打开 Commit 工具窗口
```

里面可以看到：

```
Modified
Unversioned Files
Deleted
```

PyCharm 官方文档说明，Commit 工具窗口可以查看已修改、新增、未跟踪文件，并可以从这里添加文件到 Git。

------

## 18.2 提交代码

路径：

```
Commit 工具窗口
  → 勾选文件
  → 输入 commit message
  → Commit
```

如果要提交并推送：

```
Commit and Push
```

JetBrains 文档说明，提交是把本地修改记录到项目历史中，推送是把提交发布到远程仓库，让其他人可以获取。

------

## 18.3 拉取代码

路径：

```
Git
  → Pull
```

或者：

```
右上角分支名
  → Update
```

PyCharm 的 Pull 会先下载远程数据，再把变化整合到当前工作副本；Update Project 可以按设置选择 merge 或 rebase。

------

## 18.4 推送代码

路径：

```
Git
  → Push
```

快捷键常见为：

```
Ctrl + Shift + K
```

------

## 18.5 切换分支

路径：

```
右下角/右上角分支名
  → 选择分支
  → Checkout
```

------

# 19. 常见错误处理

## 19.1 push 被拒绝：non-fast-forward

错误类似：

```
rejected
non-fast-forward
fetch first
```

原因：远程分支比你本地新。

处理：

```
git pull --rebase origin master
git push origin master
```

如果冲突，解决冲突后：

```
git add .
git rebase --continue
git push origin master
```

------

## 19.2 账号密码错误：401 / 403

常见原因：

```
密码错误
token 过期
没有仓库权限
本地缓存了旧密码
```

处理：

```
git remote -v
printf "protocol=http\nhost=gogs.sinocare.com\n\n" | git credential reject
```

然后删除 Windows 凭据管理器里的 Gogs 记录，再重新 push。

------

## 19.3 服务器 500

错误：

```
The requested URL returned error: 500
```

可能原因：

```
Gogs 服务端异常
仓库服务错误
账号权限异常
反向代理异常
服务端 hook 执行失败
```

你本地可以先验证：

```
git remote -v
git ls-remote origin
```

如果 `git ls-remote origin` 也报 500，多半不是代码冲突，而是服务端或认证链路问题。

------

## 19.4 当前有未提交修改，无法切换分支

错误类似：

```
Your local changes would be overwritten by checkout
```

处理方式 1：提交

```
git add .
git commit -m "wip: 临时提交"
git switch other-branch
```

处理方式 2：stash

```
git stash push -m "临时保存"
git switch other-branch
```

回来后恢复：

```
git stash pop
```

处理方式 3：丢弃修改，慎用

```
git restore .
```

------

## 19.5 冲突后想完全放弃合并

放弃 merge：

```
git merge --abort
```

放弃 rebase：

```
git rebase --abort
```

------

## 19.6 不小心提交了敏感文件

例如提交了：

```
.env
config.yaml
private.key
```

如果还没 push：

```
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit --amend
```

如果已经 push，需要联系团队处理历史记录，不能只靠 `.gitignore`。

------

# 20. 推荐团队开发流程

## 20.1 功能开发流程

```
# 1. 切到主分支
git switch master

# 2. 拉最新代码
git pull origin master

# 3. 创建功能分支
git switch -c feature/glucose-chart

# 4. 开发代码
# ...

# 5. 查看修改
git status
git diff

# 6. 添加并提交
git add .
git commit -m "feat: 新增血糖趋势图"

# 7. 同步主分支
git fetch origin
git rebase origin/master

# 8. 推送功能分支
git push -u origin feature/glucose-chart
```

然后在 Gogs/GitLab 上发起合并请求，或者由负责人合并到 `master`。

------

## 20.2 紧急修复流程

```
git switch master
git pull origin master
git switch -c hotfix/login-token

# 修改代码
git add .
git commit -m "hotfix: 修复登录 token 失效问题"

git push -u origin hotfix/login-token
```

合并后打标签：

```
git switch master
git pull origin master
git tag -a v1.2.1 -m "发布 v1.2.1 热修复版本"
git push origin v1.2.1
```

------

# 21. 高危命令清单

这些命令执行前要特别小心：

| 命令                 | 风险                   |
| -------------------- | ---------------------- |
| `git reset --hard`   | 丢弃工作区和暂存区修改 |
| `git clean -fd`      | 删除未跟踪文件和目录   |
| `git clean -fdx`     | 连忽略文件也删除       |
| `git push --force`   | 可能覆盖远程分支       |
| `git branch -D`      | 强制删除本地分支       |
| `git rebase`         | 会重写提交历史         |
| `git commit --amend` | 会改写最近一次提交     |

安全替代：

| 目标             | 更安全命令                        |
| ---------------- | --------------------------------- |
| 回滚公共分支提交 | `git revert`                      |
| 临时保存修改     | `git stash`                       |
| 预览清理内容     | `git clean -n`                    |
| 强推个人分支     | `git push --force-with-lease`     |
| 查看历史         | `git log --oneline --graph --all` |

------

# 22. 常用命令速查表

## 仓库

```
git clone 仓库地址
git init
git remote -v
git remote add origin 仓库地址
git remote set-url origin 新地址
```

## 状态

```
git status
git status -s
git diff
git diff --cached
```

## 提交

```
git add .
git add -A
git commit -m "提交说明"
git commit --amend
```

## 分支

```
git branch
git branch -a
git switch 分支名
git switch -c 新分支名
git branch -d 分支名
git branch -D 分支名
```

## 拉取

```
git fetch origin
git pull origin master
git pull --rebase origin master
```

## 推送

```
git push origin master
git push -u origin feature/xxx
git push origin --delete feature/xxx
```

## 合并

```
git merge 分支名
git rebase origin/master
git merge --abort
git rebase --abort
git rebase --continue
```

## 回滚

```
git restore 文件名
git restore .
git restore --staged 文件名
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
git revert 提交ID
```

## 历史

```
git log
git log --oneline
git log --oneline --graph --decorate --all
git show 提交ID
git blame 文件名
```

## stash

```
git stash
git stash push -m "说明"
git stash list
git stash apply
git stash pop
git stash drop stash@{0}
git stash clear
```

## tag

```
git tag
git tag v1.0.0
git tag -a v1.0.0 -m "发布 v1.0.0"
git push origin v1.0.0
git push origin --tags
git tag -d v1.0.0
git push origin --delete tag v1.0.0
```

------

# 23. 建议你们团队统一的规范

## 23.1 分支规范

```
master/main：稳定主分支
develop：开发集成分支，可选
feature/*：功能分支
bugfix/*：普通 bug 修复
hotfix/*：线上紧急修复
release/*：发布分支
```

------

## 23.2 提交规范

推荐：

```
feat: 新增功能
fix: 修复问题
docs: 修改文档
style: 调整格式
refactor: 代码重构
test: 增加测试
chore: 工程配置
perf: 性能优化
```

示例：

```
git commit -m "feat: 新增设备绑定功能"
git commit -m "fix: 修复血糖数据上传失败"
git commit -m "refactor: 重构用户登录逻辑"
```

------

## 23.3 合并规范

建议：

```
个人分支可以 rebase
公共分支不要 rebase
master/main 禁止直接 force push
上线回滚优先用 revert
每次 push 前先 pull/rebase 最新代码
```

------

## 23.4 提交前检查清单

提交前执行：

```
git status
git diff
```

确认：

```
没有提交无关文件
没有提交密码、token、密钥
没有提交本地配置
没有提交编译产物
提交信息清楚
代码能正常运行
```

------

# 24. 结合你当前 PyCharm/Gogs 的建议

你现在用的是 PyCharm，远程地址是：

```
http://gogs.sinocare.com/SinoHealth/glucose-wave.git
```

建议你按这个顺序处理日常问题：

```
git remote -v
git status
git pull --rebase origin master
git push origin master
```

如果密码改了，优先做：

```
1. PyCharm → Settings → Appearance & Behavior → System Settings → Passwords
2. Windows → 控制面板 → 凭据管理器 → Windows 凭据
3. 删除 gogs.sinocare.com / git:http://gogs.sinocare.com
4. 重新 git push
```

如果公司允许，长期建议把 HTTP 改成 SSH：

```
git remote set-url origin git@gogs.sinocare.com:SinoHealth/glucose-wave.git
```

这样以后不会频繁受账号密码变更影响。

## Windows Git 凭据

控制面板 → 凭据管理器 → Windows 凭据

jetbrains保存的凭据使用的是Windows 凭据，修改这里就可以修改凭据

