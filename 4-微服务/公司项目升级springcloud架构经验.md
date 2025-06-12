# 公司项目升级springcloud架构经验

## 1.无法访问jakarta.servlet.ServletException

1、Redis配置变化\
Redis配置对比2.x版本，在spring下多了一个data层级，如下所示：

2、日志配置变化\
日志配置主要是日志的大小和保存历史等配置项和2.x版本不同，3.x版本增加了logback节点，如下所示：

三、代码变化\
1、mysql的依赖替换成 mysql-connector-j\
如下所示

```
    <!-- jdbc -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <!-- mysql -->
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <scope>runtime</scope>
    </dependency>
```

2、javax.servlet包替换为jakarta.servlet\
涉及的类包括ServletRequest、HttpServletRequest、ServletResponse、HttpServletResponse等，如下图所示：

3、javax.validation包替换为jakarta.validation\
涉及的注解包括@Valid、@NotNUll、@NotBlank、@NotEmpty等。

4、其他javax相关的包替换\
javax.persistence.\* -> jakarta.persistence.\*\
javax.annotation.\* -> jakarta.annotation.\*\
javax.transaction.\* -> jakarta.transaction.\*

5、允许跨域设置由addAllowedOrigin替换为addAllowedOriginPattern\
import org.springframework.context.annotation.Bean;\
import org.springframework.context.annotation.Configuration;\
import org.springframework.web.cors.CorsConfiguration;\
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;\
import org.springframework.web.filter.CorsFilter;\
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;\
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;\
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/\*\*

* 配置注册
*
* @author ldy
* @date 2024/03/06
*   @since V1.0.1\
    \*/\
    @Configuration\
    public class WebConfig implements WebMvcConfigurer {

    @Override\
    public void addResourceHandlers(ResourceHandlerRegistry registry) {\
    registry.addResourceHandler("/\*\*").addResourceLocations("classpath:/static/");\
    }

    private CorsConfiguration buildConfig() {\
    CorsConfiguration corsConfiguration = new CorsConfiguration();\
    //corsConfiguration.addAllowedOrigin("_");_\
    _corsConfiguration.addAllowedOriginPattern("_");\
    corsConfiguration.setAllowCredentials(true);\
    corsConfiguration.addAllowedHeader("_");_\
    _corsConfiguration.addAllowedMethod("_");\
    return corsConfiguration;\
    }

    @Bean\
    public CorsFilter corsFilter() {\
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();\
    source.registerCorsConfiguration("/\*\*", buildConfig());\
    return new CorsFilter(source);\
    }

}\
6、Spring MVC 和 WebFlux的URL匹配更改\
从 Spring Framework 6.0 开始，尾部斜杠匹配配置选项已为 deprecated，其默认值设置为 false。

简单来说，就是比如以前@GetMapping("/list")这样的控制器，可以通过 /list 和 /list/ 两个路径都能访问到，现在只能通过 /list 访问。

调用python接口的开发者要注意，因为python的开发者习惯在路径最后加个斜杠，java的开发者几乎不会去加，如果调用接口的时候默认都在最后加了斜杠的话，那么springboot升级后，后台将会报请求的资源路径不存在的错误。部署之前需要前端排查一下，要么后端加上包含最后有斜杠的路由，要么前端去掉斜杠后访问接口。

四、mybatis-plus依赖包替换\
如果使用了mybatis-plus的话需要将mybatis-plus-boot-starter依赖包替换成mybatis-plus-spring-boot3-starter,如果用到了代码生成器mybatis-plus-generator的话，还要同时升级代码生成器的依赖包，我这里升级到3.5.5版本，升级前后对比如下：

升级前：

```
    <!-- mybatis plus -->
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-boot-starter</artifactId>
        <version>3.4.1</version>
    </dependency>
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-support</artifactId>
        <version>2.3.3</version>
    </dependency>
    <!-- mybatis plus 代码生成器依赖 -->
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-generator</artifactId>
        <version>3.4.1</version>
    </dependency>
```

升级后：

```
    <!-- mybatis plus -->
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
        <version>3.5.5</version>
    </dependency>
 
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-support</artifactId>
        <version>2.3.3</version>
    </dependency>
    <!-- mybatis plus 代码生成器依赖 -->
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-generator</artifactId>
        <version>3.5.5</version>
    </dependency>
```

注意：升级后代码生成工具类也需要修改后才能用，代码生成工具类参考

springboot3.x集成mybatis-plus代码生成工具\
https://blog.csdn.net/LDY1016/article/details/142848395

同时，原xxxMapper代码里面的注解建议使用@Mapper，原实体类代码 extends Model 部分替换为implements Serializable，因为代码生成工具生成的是这样，为了保持代码的一致性，建议修改。

还需要删除原实体类里面的下列方法，如果原来有的话：

```
@Override
protected Serializable pkVal() {
    return this.id;
}
```

五、swagger2升级到swagger3\
springboot3.x集成SpringDoc Swagger3-CSDN博客\
文章浏览阅读71次。swagger3未授权访问的路径主要包括和。本人提供的解决方案就是通过过滤器的方式对请求进行验证，请求的时候需要在链接后面加上我们自定义的token参数，通过验证token判断是否是合法的访问，注意，添加过滤器后需要在启动类上加上。\
https://blog.csdn.net/LDY1016/article/details/136502829

六、集成nacos踩坑\
springboot3.x集成nacos踩坑，并实现多环境配置-CSDN博客\
springboot3.x集成Nacos首先需要将Nacos从1.x升级到2.x，建议直接安装2.x版本，手动将1.x的配置信息迁移到2.x中，先并行一段时间，待全部迁移完成稳定运行之后再停掉1.x，升级和安装、操作请查看官方文档。完成前面的工作之后，正常情况下nacos的集成就算成功了，但是，并没有想象的那么顺利，我们启动项目，意外发生了，控制台报错，项目启动失败！对应的是 Spring Boot 3.x 版本，版本。对应的是 Spring Boot 2.x 版本，版本。\
https://blog.csdn.net/LDY1016/article/details/136502907

七、其他踩坑记录\
springboot2.x升级到3.x后restTemplate请求微信接口报错412 Precondition Failed: \[no body] 问题解决\
https://blog.csdn.net/LDY1016/article/details/143050807

springboot3.x使用@NacosValue无法获取配置信息问题解决\
https://blog.csdn.net/LDY1016/article/details/143116113
