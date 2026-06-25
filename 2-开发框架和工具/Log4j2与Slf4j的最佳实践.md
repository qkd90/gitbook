# Log4j2 与 Slf4j 的最佳实践

## 基本关系

Slf4j 是日志门面，负责提供统一 API；Log4j2 是日志实现，负责真正输出日志。业务代码中应优先使用 Slf4j API，底层通过依赖和配置选择 Log4j2、Logback 等具体实现。

```java
private static final Logger log = LoggerFactory.getLogger(UserService.class);
```

推荐做法：

- 业务代码只依赖 `org.slf4j.Logger` 和 `org.slf4j.LoggerFactory`。
- 日志实现统一由项目依赖管理，不要在不同模块混用多套实现。
- 输出日志时使用占位符，不要使用字符串拼接。
- 异常日志要把异常对象作为最后一个参数传入。

## 常用依赖

Spring Boot 默认使用 Logback。如果要切换到 Log4j2，一般需要排除默认日志并引入 Log4j2 starter。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-log4j2</artifactId>
</dependency>
```

## 日志级别

| 级别 | 使用场景 |
| --- | --- |
| `trace` | 极细粒度调试，生产环境一般关闭 |
| `debug` | 开发和测试阶段定位流程、参数 |
| `info` | 关键业务节点、启动完成、任务完成 |
| `warn` | 可恢复异常、降级、重试、配置缺失 |
| `error` | 需要人工关注的异常、数据不一致、外部服务不可用 |

## 推荐写法

### 使用占位符

```java
log.info("用户登录成功，userId={}, account={}", userId, account);
```

不要这样写：

```java
log.info("用户登录成功，userId=" + userId + ", account=" + account);
```

### 异常日志保留堆栈

```java
try {
    orderService.submit(orderId);
} catch (Exception e) {
    log.error("订单提交失败，orderId={}", orderId, e);
    throw e;
}
```

如果只打印 `e.getMessage()`，后续排查时会缺少调用栈。

### 控制敏感信息

日志中不要输出明文密码、身份证、手机号、token、密钥。确实需要定位时，应脱敏处理。

```java
log.info("发送验证码，phone={}", maskPhone(phone));
```

## Log4j2 配置示例

`log4j2-spring.xml`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Properties>
        <Property name="LOG_PATTERN">%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n</Property>
        <Property name="LOG_PATH">logs</Property>
    </Properties>

    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="${LOG_PATTERN}"/>
        </Console>

        <RollingFile name="File"
                     fileName="${LOG_PATH}/app.log"
                     filePattern="${LOG_PATH}/app-%d{yyyy-MM-dd}-%i.log.gz">
            <PatternLayout pattern="${LOG_PATTERN}"/>
            <Policies>
                <TimeBasedTriggeringPolicy/>
                <SizeBasedTriggeringPolicy size="100 MB"/>
            </Policies>
            <DefaultRolloverStrategy max="30"/>
        </RollingFile>
    </Appenders>

    <Loggers>
        <Logger name="org.springframework" level="info"/>
        <Root level="info">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="File"/>
        </Root>
    </Loggers>
</Configuration>
```

## 生产建议

- 日志文件按天和大小滚动，避免单文件过大。
- 保留周期根据磁盘容量和审计要求设置，一般保留 7 到 30 天。
- 错误日志、访问日志、业务审计日志可以拆分文件，方便检索。
- 容器环境优先输出到标准输出，再由日志采集组件统一收集。
- 调试 SQL、HTTP 请求体等高频日志时，要评估性能和敏感数据风险。

## 常见问题

### 多个日志实现冲突

现象：启动时提示多个 binding，或者日志重复输出。

排查：

```bash
mvn dependency:tree | grep -E "slf4j|logback|log4j"
```

处理方式是保留一套日志实现，排除多余依赖。

### 日志没有输出到文件

重点检查：

- 配置文件名称是否为 `log4j2-spring.xml`。
- 配置文件是否放在 `src/main/resources`。
- 运行目录是否有 `logs` 目录写入权限。
- 当前 profile 是否覆盖了日志配置。
