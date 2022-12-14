### 设置保护分支

把认为哪个个分支不想让别人动，就把这个分支设置为保护分支，并且只有授权的用户才可以向这个分支推送代码

 

在实际使用过程中，我们通常会保持 master 分支稳定，用于生产环境的版本发布，**只有授权的用户**才可以向 master 合并代码。

要实现此功能，我们需要将 master 设置为保护分支，并**授权什么用户**可以向 master 用户推送代码。


使用 root 用户点击 git_test 仓库页面左下角的 Settings

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648364.png)

 

 

 进入设置页面，选择设置菜单栏下面的 Repository 选项

 

![img](https://img2020.cnblogs.com/blog/1137246/202003/1137246-20200330234216247-1291484502.png)

 

 

 进入 repository 设置页面

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648674.png)

 

 

 

展开 Protected Branches 

![img](https://img2020.cnblogs.com/blog/1137246/202003/1137246-20200331232459561-522112756.png)

 

 

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648372.png)

 

设置完成后，在仓库分支页面，可看到 master 分支后面出现一个绿色的 protected 标记。意味着master分支被保护

 ![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200401000819103-1082655780.png)

 

 

 

 

只有master角色可以合并申请到master分支，才可以push代码到master分支，对于master分支操作，只有master才可以做

admin是master身份

dev没有权限往master分支push推送代码，也没有权限往master合并申请

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648539.png)

 

 

 

 

ci-node1 对应master

ci-node2对应dev用户

 

此时我们再尝试在 ci-node2 上推送 master 分支到 GitLab

 在dev分支 切换到master分支

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git branch
* dev
  master

[root@ci-node2 git_test]# git checkout master
Switched to branch 'master'
Your branch is up-to-date with 'origin/master'
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

创建新文件，然后提交，在ci-node2客户端推送

 

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# touch ci-node2
[root@ci-node2 git_test]# git add .
[root@ci-node2 git_test]# git commit -m "commit ci-node2 on ci-node2"
[master 2bd2e88] commit ci-node2 on ci-node2
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 ci-node2
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

报错 

我们发现此时我们已经不能在 ci-node2 上向 GitLab 上推送 master 分支，因为我们ci-node2 绑定的是 dev 用户，dev 用户属于 developer 角色，

master 分支不允许 developer角色向其推送内容。



![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git push -u origin master
Counting objects: 2, done.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 234 bytes | 0 bytes/s, done.
Total 2 (delta 1), reused 0 (delta 0)
remote: GitLab: You are not allowed to push code to protected branches on this project.
To 192.168.31.11:test/git_test.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'git@192.168.31.11:test/git_test.git
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

 

例子2

在dev分支

```
[root@ci-node2 git_test]# git branch
* dev
  master
```

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# ll
total 4
-rw-r--r-- 1 root root 21 Mar 30 00:11 a
-rw-r--r-- 1 root root  0 Mar 30 00:34 dev
-rw-r--r-- 1 root root  0 Mar 30 00:11 master
-rw-r--r-- 1 root root  0 Mar 30 00:11 test
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

创建一个文件 然后提交

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# touch ci-node2
[root@ci-node2 git_test]# ll
total 4
-rw-r--r-- 1 root root 21 Mar 30 00:11 a
-rw-r--r-- 1 root root  0 Apr  1 23:05 ci-node2
-rw-r--r-- 1 root root  0 Mar 30 00:34 dev
-rw-r--r-- 1 root root  0 Mar 30 00:11 master
-rw-r--r-- 1 root root  0 Mar 30 00:11 test
[root@ci-node2 git_test]# git add .
[root@ci-node2 git_test]# git commit -m "touch ci-node2 file on dev branch"
[dev be5cdbe] touch ci-node2 file on dev branch
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 ci-node2
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

推送到dev用户

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git push -u origin dev
Counting objects: 2, done.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 247 bytes | 0 bytes/s, done.
Total 2 (delta 1), reused 0 (delta 0)
remote: 
remote: To create a merge request for dev, visit:
remote:   http://192.168.31.11/test/git_test/merge_requests/new?merge_request%5Bsource_branch%5D=dev
remote: 
To 192.168.31.11:test/git_test.git
   a0e7b8d..be5cdbe  dev -> dev
Branch dev set up to track remote branch dev from origin.
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

推上去了

![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200402000439576-1777914479.png)

 

切换到master分支

 

```
[root@ci-node2 git_test]# git checkout master
Switched to branch 'master'
```

把dev分支合并到master 分支

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git merge dev
Updating cc7da0e..be5cdbe
Fast-forward
 ci-node2 | 0
 dev      | 0
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 ci-node2
 create mode 100644 dev
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

推送到master分支

报错原因 因为ci-node2 公钥绑定gitlab dev用户上 ，gitlab上设置dev用户是开发者，开发者没有权限推送到master

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git push -u origin master
Total 0 (delta 0), reused 0 (delta 0)
remote: GitLab: You are not allowed to push code to protected branches on this project.
To 192.168.31.11:test/git_test.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'git@192.168.31.11:test/git_test.git'
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

回到ci-node1 上 推master分支

 

```
[root@ci-node1 git_test]# git push -u gitlab master
Branch master set up to track remote branch master from gitlab.
Everything up-to-date
```

ci-node2 上做了修改 推送了仓库内容，ci-node1现在本地仓库和远程仓库 内容 不一致，导致以上情况

 

这时候需要 用git fetch命令

 

 

### git fetch 使用

上面我们在 ci-node2 向 gitlab 上的远程仓库推送了新的内容，此时对于 ci-node1 上的 git_test 仓库来说，它的远程仓库已经更新，所以需要将这些更新取回本地，这时就需 要用到 git fetch 命令。

fetch到本地，然后合并，再推送

 

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node1 git_test]# git fetch
remote: Counting objects: 4, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 1), reused 0 (delta 0)
Unpacking objects: 100% (4/4), done.
From 192.168.31.11:test/git_test
 * [new branch]      dev        -> gitlab/dev
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

合并  把更新内容合并到本地

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node1 git_test]# git merge gitlab/dev
Updating cc7da0e..be5cdbe
Fast-forward
 ci-node2 | 0
 dev      | 0
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 ci-node2
 create mode 100644 dev
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

有ci-node2文件

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node1 git_test]# ll
total 4
-rw-r--r-- 1 root root 21 Mar 21 23:53 a
-rw-r--r-- 1 root root  0 Apr  2 23:49 ci-node2
-rw-r--r-- 1 root root  0 Apr  2 23:49 dev
-rw-r--r-- 1 root root  0 Mar 21 18:31 master
-rw-r--r-- 1 root root  0 Mar 18 00:20 test
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

再推送 

推成功了

 

```
[root@ci-node1 git_test]# git push -u gitlab master
Total 0 (delta 0), reused 0 (delta 0)
To 192.168.31.11:test/git_test.git
   cc7da0e..be5cdbe  master -> master
Branch master set up to track remote branch master from gitlab.
```

 

再看看gitlab 有ci-node2文件

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648664.png)

 现在ci-node1 客户端上 对ci-node2 文件追加内容 ，提交

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node1 git_test]# echo "222" >> ci-node2 

[root@ci-node1 git_test]# git add .
[root@ci-node1 git_test]# git commit -m "modify ci-node2 file on master branch"
[master b5692cb] modify ci-node2 file on master branch
 1 file changed, 1 insertion(+)
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

再推送

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node1 git_test]# git push -u gitlab master
Counting objects: 3, done.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 273 bytes | 0 bytes/s, done.
Total 3 (delta 1), reused 0 (delta 0)
To 192.168.31.11:test/git_test.git
   be5cdbe..b5692cb  master -> master
Branch master set up to track remote branch master from gitlab
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

推送成功再去看看 gitlab，推上来了，dev用户推不上来，ci-node1 可以推上来，ci-node1 公钥绑定的是root用户 admin用户，

ci-node2 公钥绑定要dev用户，我们设置master分支只有master角色才能推送

![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200403001736677-1484631658.png)

 

 

###  不让dev用户推到master分支，dev用户只能推到dev分支上，做完还可以提个申请，申请把代码合并到master

 

 

切换到dev分支

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git branch
  dev
* master
[root@ci-node2 git_test]# git checkout dev
Switched to branch 'dev'
Your branch is up-to-date with 'origin/dev'.
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

 

 

 

我们创建一个文件 ci-node2 然后提交 推送到gitlab 上的dev用户

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# touch ci-node2
[root@ci-node2 git_test]# ll
total 4
-rw-r--r-- 1 root root 21 Mar 30 00:11 a
-rw-r--r-- 1 root root  0 Apr  4 18:36 ci-node2
-rw-r--r-- 1 root root  0 Mar 30 00:34 dev
-rw-r--r-- 1 root root  0 Mar 30 00:11 master
-rw-r--r-- 1 root root  0 Mar 30 00:11 test

[root@ci-node2 git_test]# git add .
[root@ci-node2 git_test]# git commit -m "touch ci-node2 file on dev branch"
[dev 30de0f6] touch ci-node2 file on dev branch
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 ci-node2
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

 

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

```
[root@ci-node2 git_test]# git remote
origin
[root@ci-node2 git_test]# git push -u origin dev
Counting objects: 2, done.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 247 bytes | 0 bytes/s, done.
Total 2 (delta 1), reused 0 (delta 0)
remote: 
remote: To create a merge request for dev, visit:
remote:   http://192.168.31.11/test/git_test/merge_requests/new?merge_request%5Bsource_branch%5D=dev
remote: 
To 192.168.31.11:test/git_test.git
   a0e7b8d..30de0f6  dev -> dev
Branch dev set up to track remote branch dev from origin.
```

![复制代码](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648532.gif)

 

 

 

在gitlab登录dev用户 在dev分支上做了改动 ，然后可以在web界面提交合并申请 把dev分支合并到master分支

dev分支上收到推送的ci-node2文件

 

![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200404184114742-1109077375.png)

 

 

 

出现界面填信息

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648542.png)

 

 

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648545.png)

 

 

然后退出来，登录root用户 发现合并请求

 

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648822.png)

 

 

 

![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200404191122785-1754606763.png)

 

 

 

 这里可以看合并了什么东西 有什么改变

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648012.png)

 

 没有问题就merge

![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200404192643685-702295651.png)

 



 

点完merge以后，他会告诉你 已经合并过来了

![img](https://raw.githubusercontent.com/qkd90/figureBed/main/202212121648709.png)

 



 再看看 master分支的仓库 ci-node2 合并进来master

![img](https://img2020.cnblogs.com/blog/1137246/202004/1137246-20200404193014553-17945860.png)

 

 没有权限推送到master，你可以在提合并申请，合并申请有合并内容，