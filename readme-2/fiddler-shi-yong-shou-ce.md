# fiddler使用手册

## fiddler使用手册

测试前端过程中，经常需要验证各种功能状态、不同数据层级等返回后的展示效果。一般会通过以下三种方式进行测试：

1.构造满足条件的测试数据；（耗时费力）

2.修改数据库；（前提需要了解数据库数据存储、沟通成本高）

3.通过网络代理截获返回的数据进行修改。（成本低、即时修改即时测试、不需要打扰后端修改数据库）

综合，第三种方式较方便且灵活。最近在用抓包工具fiddler，以下通过fiddler介绍如何修改response返回结果。

第一步：下载fiddler的最新版本；

运行fiddler之后测试要调试的页面是否可以捕获，刷新页面后左边列表会实时显示目前http请求的条目。如图红色部分

![](https://img2018.cnblogs.com/blog/1190329/201907/1190329-20190712115848227-762039500.png)

第二步：开启断点捕获数据：

点击菜单栏按钮【Rules】—【automatic Breakpoints】-【After Response】，意思是要在请求返回后修改返回结果。

这个时候开始刷新页面，会发现页面卡着不动，Fiddler左边的转台框http请求前出现红色框框，这个时候说明配置成功；找到需要修改的接口，如果没有，这个时候在命令行中输入【go】命令放行，直到要修改的接口出来。

![](https://img2018.cnblogs.com/blog/1190329/201907/1190329-20190712115909503-913320232.png)

接口找到后，查看右侧response的选项卡【Transformer】，记住当前选中的编码格式，默认【chunked Transfer-Encoding】是选中的，去掉之后下方【HTTP Compression】选中在【GZIP Encoding】上的，没有的话最好，要记住选项，我们在这里统一勾选【no Compression】意思是不压缩，如果不点你的代码没办法修改是乱码的。修改完之后记得是要点回来的，重新压缩在发送。

![](https://img2018.cnblogs.com/blog/1190329/201907/1190329-20190712115928209-86934487.png)

第三步：然后点击【Textview】修改需要的返回结果。

![](https://img2018.cnblogs.com/blog/1190329/201907/1190329-20190712115944001-1006024641.png)

第四步：修改完成后，第二步中选项卡【Transformer】的编码格式要重新设置回去，重新压缩在发送。点击【Run to Completion】。

第五步：验证页面是否按照修改预期展示。

## fiddler如何只抓取指定浏览器的包

在实际工作中，常常会抓取浏览器的数据，其加载的数据较多，不好区分，不知道其是哪个是需要抓取的数据，所以就需抓取指定浏览器的数据，这样就能很清晰知道数据的来源。

步骤一：

打开fiddler，再打开浏览器

步骤二：

点击下图中的捕捉按钮，按钮处的文案将显示成"pick target"，拖动鼠标至特定浏览器页面并放开鼠标，此时浏览器名称及占用端口号将显示在捕捉按钮之后

![](https://img-blog.csdnimg.cn/20190603140428725.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTIxMDYzMDY=,size_16,color_FFFFFF,t_70)

![](https://img-blog.csdnimg.cn/20190603140504569.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTIxMDYzMDY=,size_16,color_FFFFFF,t_70)

