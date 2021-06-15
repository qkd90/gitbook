### docker ps的结果很乱怎么办

docker ps是我们最常用的docker命令之一。用来查询当前运行中的容器，但是这个命令显示的结果很乱，如下图：

[![深度截图_选择区域_20190312095714.png](https://liyangweb.com/wp-content/uploads/emlog/201903/eca71552355850.png)](https://liyangweb.com/wp-content/uploads/emlog/201903/eca71552355850.png)

显示的内容分为6列，但是由于有些列的内容比较长，再加上电脑屏幕宽度有限，导致显示的内容发生了换行，看上去极其的混乱。我们可以通过format参数，来过滤一些不需要查看的列，这样就清晰多了。一般来说，创建时间我不太关心，默认执行的命令也不关心，docker ps查询出来的本来就是运行中的容器，所以容器状态我也不关心，那么我就隐藏掉这两列，命令如下：

```
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}"
```

![image-20210615141346728](C:\Users\rq\AppData\Roaming\Typora\typora-user-images\image-20210615141346728.png)

当然每次都敲这么长的命令是很让人头大的，那么我们可以创建一个命令别名

打开用户的命令别名配置文件 vim ~/.bashrc

在文件最后追加 

```
alias dockerps=’docker ps –format “table {{.ID}} {{.Image}} {{.Ports}} {{.Names}}”‘
```

重新加载配置，使别名生效 source ~/.bashrc

下面就可以用我们显示清晰的dockerps命令啦

![image-20210615141419428](C:\Users\rq\AppData\Roaming\Typora\typora-user-images\image-20210615141419428.png)

当然，如果你希望显示其他的列，那么请参考如下表格

[![fa571c3e6a754420bfd81a521dae5702.jpeg](https://liyangweb.com/wp-content/uploads/emlog/201903/8e881552357067.jpeg)](https://liyangweb.com/wp-content/uploads/emlog/201903/8e881552357067.jpeg)