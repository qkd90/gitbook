# Lombok 注解

## 1.概述

本文讲解注解如下：

```
@RequiredArgsConstructor
```

2.

### 2.1@RequiredArgsConstructor

```java
@RestController
@RequestMapping("alarm/configs")
@RequiredArgsConstructor
public class AlarmConfigController {
    //这里必须是final,若不使用final,用@NotNull注解也是可以的
    private final AlarmConfigService alarmConfigService;
...
}
```

spring推荐写法

```java
@RestController
@RequestMapping("alarm/configs")
public class AlarmConfigController {
    private final AlarmConfigService alarmConfigService;
 
    @Autowired
    public AlarmConfigController(AlarmConfigService alarmConfigService) {
        this.alarmConfigService = alarmConfigService;
    }
...
}
```

