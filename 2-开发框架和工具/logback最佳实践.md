



## logback过滤

### 场景

使用监控异常日志进行告警时，部分异常日志可能只是不需要告警，但无法通过编码去除时，可以通过不输出这类异常日志达到忽略告警的目的。

比如在系统中经常会出现断开的管道的相关问题，异常如下

> org.apache.catalina.connector.ClientAbortException: java.io.IOException: 断开的管道
> org.apache.catalina.connector.ClientAbortException: java.io.IOException: broken pipe
> [587ce8c8] Error [reactor.netty.ReactorNetty$InternalNettyException: java.nio.channels.ClosedChannelException] for HTTP GET "/xxxx", but ServerHttpResponse already committed (200 OK)

有因为使用框架的原因异常无法捕获，在不改源码的情况下可以通过是用日志过滤的方式处理。

### 日志过滤

基于logback的基础上引入jar包，不引入无法启动。

```
<!--日志过滤-->
<dependency>
    <groupId>org.codehaus.janino</groupId>
    <artifactId>commons-compiler</artifactId>
    <version>3.0.12</version>
</dependency>
<dependency>
    <groupId>org.codehaus.janino</groupId>
    <artifactId>janino</artifactId>
    <version>3.0.12</version>
</dependency>
```

添加过滤条件，过滤输出中含有某个字符串的信息

```xml
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
     <!--增加日志匹配处理-->
    <filter class="ch.qos.logback.core.filter.EvaluatorFilter">
        <!--匹配处理器-->
        <evaluator>
            <!-- 处理模式，默认为 ch.qos.logback.classic.boolex.JaninoEventEvaluator -->  
            <!-- 存在某个字符串则匹配成功 -->  
            <expression>return message.contains("broken pipe");</expression>
        </evaluator>
        <!--匹配则停止执行日志输出-->
        <OnMatch>DENY</OnMatch>
        <!--不匹配则往下执行-->
        <OnMismatch>ACCEPT</OnMismatch>
    </filter>
    <!--调用其他日志处理-->
    <appender-ref ref="KAFKA"/>
</appender>
```



## Logback 自定义灵活的日志过滤规则

当我们需要对日志的打印要做一些范围的控制的时候，通常都是通过为各个Appender设置不同的Filter配置来实现。在Logback中自带了两个过滤器实现：ch.qos.logback.classic.filter.LevelFilter和ch.qos.logback.classic.filter.ThresholdFilter，用户可以根据需要来配置一些简单的过滤规则，下面先简单介绍一下这两个原生的基础过滤器。

ch.qos.logback.classic.filter.LevelFilter过滤器的作用是通过比较日志级别来控制日志输出。



### 下面是一个只记录日志级别为ERROR的例子

```xml
<appender name="ERROR_APPENDER" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>logs/error.log</file>ds
    <filter class="ch.qos.logback.classic.filter.LevelFilter">
        <level>ERROR</level>
        <onMatch>ACCEPT</onMatch>
        <onMismatch>DENY</onMismatch>
    </filter>
    <encoder>
        <pattern>%-4relative [%thread] %-5level %logger{30} - %msg%n</pattern>
    </encoder>
</appender>
```

LevelFilter通过定义日志级别，并设置匹配与不匹配的处理策略来控制针对某个级别日志的输出策略。

当我们要设置多个不同级别的日志策略的时候，如果仅依靠这个过滤器，我们就要级联的定义多个filter来控制才能实现，显然不是很方便，所以此时我们就可以使用ch.qos.logback.classic.filter.ThresholdFilter过滤器来控制了。

比如下面的配置，实现了只记录WARN及以上级别的控制，比WARN级别低（如：INFO、DEBUG、TRACE）都不会记录。

```
<appender name="WARN_APPENDER" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>logs/warn_error.log</file>
    <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
        <level>WARN</level>
    </filter>
    <encoder>
        <pattern>%-4relative [%thread] %-5level %logger{30} - %msg%n</pattern>
    </encoder>
</appender>    
```

通过上述介绍的两个过滤器来控制日志的记录级别已经满足绝大部分的需求，但是可能还是会出现一些特殊情况，需要自定义复杂的过滤规则，比如想过滤掉一些框架中的日志，通过自带的几个过滤器已经无法完全控制，并且也不希望修改框架源码来实现。这个时候，我们就可以自己来实现过滤器，并配置使用。实现的方式也很简单，只需要实现Logback提供的ch.qos.logback.core.filter.Filter接口即可。



### 下面举一个简单的例子

```
public class MyFilter extends Filter<ILoggingEvent> {
    @Override
    public FilterReply decide(ILoggingEvent event) {
        if (event.getLevel() == Level.ERROR) {
            switch (event.getLoggerName()) {
                case "org.springframework.cloud.sleuth.instrument.web.ExceptionLoggingFilter":
                    return FilterReply.DENY;
            }
            return FilterReply.ACCEPT;
        }
        return FilterReply.DENY;
    }
}
```

上面过滤器的功能主要是通过重写decide，限制了org.springframework.cloud.sleuth.instrument.web.ExceptionLoggingFilter类输出ERROR级别的日志记录。在编写好自己的过滤器实现之后，只需要在Appender中配置使用就能实现自己需要的灵活过滤规则了：

```
<appender name="WARN_APPENDER" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>logs/warn_error.log</file>
    <filter class="com.didispace.log.filter.ExceptionClassFilter"></filter>
    <encoder>
        <pattern>%-4relative [%thread] %-5level %logger{30} - %msg%n</pattern>
    </encoder>
</appender>   
```

更多关于Logback过滤器的内容可参考[官方文档](http://logback.qos.ch/manual/filters.html)