# 面试手册

1.一次完整的HTTP请求过程

```
对www.baidu.com这个网址进行DNS域名解析，得到对应的IP地址

根据这个IP，找到对应的服务器，发起TCP的三次握手

建立TCP连接后发起HTTP请求

服务器响应HTTP请求，浏览器得到html代码

浏览器解析html代码，并请求html代码中的资源（如js、css、图片等）（先得到html代码，才能去找这些资源）

浏览器对页面进行渲染呈现给用户

服务器关闭关闭TCP连接
```

2.java里面的多线程如何实现、线程安全如何实现、线程的工作区是哪里

```
Java多线程实现的方式有四种
1.继承Thread类，重写run方法
2.实现Runnable接口，重写run方法，实现Runnable接口的实现类的实例对象作为Thread构造函数的target
3.通过Callable和FutureTask创建线程
4.通过线程池创建线程
前面两种可以归结为一类：无返回值，原因很简单，通过重写run方法，run方式的返回值是void，所以没有办法返回结果
后面两种可以归结成一类：有返回值，通过Callable接口，就要实现call方法，这个方法的返回值是Object，所以返回的结果可以放在Object对象中

3.1 互斥（阻塞同步）同步（互斥是手段，同步是结果）
在JAVA中实现互斥同步手段有synchronized关键字以及java.util.concurrent包下的重入锁（ReentrantLock)。
3.2 非阻塞同步
先进行操作，如果没有其它线程争着用共享数据，那么操作就成功了，如果产生了冲突，那就采取其它的补偿措施。主要有volatile关键字以及使用原子类。
```

