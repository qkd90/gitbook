#### typora设置修改

Typora作为一款跨平台、有颜值的markdown编辑器， 除了上方被我吐槽的这两点， 基本上是一款非常令人满意的软件。

但是，就在昨天我用Typora来记录kafka的相关配置选项的时候发现了另外一个不太人性的地方， 默认展示渲染结果的宽度太窄了（github主题的最大宽度是860px， 你敢信💔？）。

```
#write{
    max-width: 860px;
    margin: 0 auto;
    padding: 20px 30px 40px 30px;
    padding-top: 20px;
    padding-bottom: 100px;
}
```

>   github.css

这种情况在你想贴一段代码， 或者加一个很多列的表格的时候尤为明显，导致本该一行显示的代码变成了两行显示或者表格区域下方多了一个x方向的滚动条，丑。 但是你翻遍Typora的配置项也找不到任何一个地方可以修改的地方。

PS.缩放字体也不行， 该丑的， 它还是丑。

不过好在Typora是用electron技术栈开发的软件，意味着你可以按下`F12`显示最熟悉的chrome控制台， 审查元素之后你就会发现（以github white主题为例）， css文件中指定了最大宽度， 而且， 还是860px。

虽然不太懂为什么要这么做， 但是接下来就是我们要做的事情。

1.  搜索安装目录下的github.css文件

>   linux下： ${TYPORA_HOME}/resources/app/style/themes/github.css

1.  修改`#white`下的`max-width`为你想要的宽度， 像素值或者百分比， 建议80%.

重启Typora即可。