一、开发前置要求:

```
1.docker
2.docker配置过远程连接
```

## 1.idea安装docker插件

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202304181135460.png)

## 2.

1）、编辑配置
2）、填远程docker地址
3）、连接成功，会列出远程docker容器和镜像
![在这里插入图片描述](https://img-blog.csdnimg.cn/52ee2adf7d24446aa0869fb898c0d16a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6L-b5Ye755qE56iL5bqP54y_fg==,size_20,color_FFFFFF,t_70,g_se,x_16)
连接成功，会列出远程docker容器和镜像
![在这里插入图片描述](https://img-blog.csdnimg.cn/86bdf3f2828248978a88462feb47b610.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6L-b5Ye755qE56iL5bqP54y_fg==,size_13,color_FFFFFF,t_70,g_se,x_16)

# 二、新建项目

1.创建springboot项目
项目结构图
![在这里插入图片描述](https://img-blog.csdnimg.cn/0a9441bfb447465e938cf42736c8c279.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6L-b5Ye755qE56iL5bqP54y_fg==,size_9,color_FFFFFF,t_70,g_se,x_16)

## step1、配置pom文件

```java
<?xml version="1.0" encoding="UTF-8"?>  
<project xmlns="http://maven.apache.org/POM/4.0.0"  
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">  
    <modelVersion>4.0.0</modelVersion>  
  
    <groupId>docker-demo</groupId>  
    <artifactId>com.demo</artifactId>  
    <version>1.0-SNAPSHOT</version>  
    <parent>  
        <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-parent</artifactId>  
        <version>2.0.2.RELEASE</version>  
        <relativePath />  
    </parent>  
  
    <properties>  
         <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  
         <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>  
         <docker.image.prefix>com.demo</docker.image.prefix>  
         <java.version>1.8</java.version>  
    </properties>  
    <build>  
        <plugins>  
          <plugin>  
            <groupId>org.springframework.boot</groupId>  
            <artifactId>spring-boot-maven-plugin</artifactId>  
          </plugin>  
        <plugin>  
           <groupId>com.spotify</groupId>  
           <artifactId>docker-maven-plugin</artifactId>  
           <version>1.0.0</version>  
           <configuration>  
              <dockerDirectory>src/main/docker</dockerDirectory>  
              <resources>  
                <resource>  
                    <targetPath>/</targetPath>  
                    <directory>${project.build.directory}</directory>  
                    <include>${project.build.finalName}.jar</include>  
                </resource>  
              </resources>  
           </configuration>  
        </plugin>  
        <plugin>  
            <artifactId>maven-antrun-plugin</artifactId>  
            <executions>  
                 <execution>  
                     <phase>package</phase>  
                    <configuration>  
                        <tasks>  
                            <copy todir="src/main/docker" file="target/${project.artifactId}-${project.version}.${project.packaging}"></copy>  
                        </tasks>  
                     </configuration>  
                    <goals>  
                        <goal>run</goal>  
                    </goals>  
                    </execution>  
            </executions>  
        </plugin>  
  
       </plugins>  
    </build>  
<dependencies>  
    <dependency>  
        <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-web</artifactId>  
    </dependency>  
    <dependency>  
  <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-starter-test</artifactId>  
        <scope>test</scope>  
    </dependency>  
    <dependency>  
        <groupId>log4j</groupId>  
        <artifactId>log4j</artifactId>  
        <version>1.2.17</version>  
    </dependency>  
</dependencies>  
</project>  
12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879
```

## step2、在src/main目录下创建docker目录，并创建Dockerfile文件

```java
FROM openjdk:8-jdk-alpine  
ADD *.jar app.jar  
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]  
123
```

## step3、在resource目录下创建application.properties文件

```java
logging.config=classpath:logback.xml  
logging.path=/home/developer/app/logs/  
server.port=8990
123
```

## step4、创建DockerApplication文件

```java
@SpringBootApplication  
public class DockerApplication {  
    public static void main(String[] args) {  
        SpringApplication.run(DockerApplication.class, args);  
    }  
}  
123456
```

## step5、创建DockerController文件

```java
@RestController  
public class DockerController {  
    static Log log = LogFactory.getLog(DockerController.class);  
  
    @RequestMapping("/")  
    public String index() {  
        log.info("Hello Docker!");  
        return "Hello Docker!";  
    }  
}  
12345678910
```

## step6、增加配置

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202304181128057.png)
命令解释：
Image tag : 指定镜像名称和tag，镜像名称为 docker-demo，tag为v1.0.0
Bind ports : 绑定宿主机端口到容器内部端口。格式为[宿主机端口]:[容器内部端口]
Bind mounts : 将宿主机目录挂到到容器内部目录中。格式为[宿主机目录]:[容器内部目录]。
这个springboot项目会将日志打印在容器 /home/developer/app/logs/ 目录下，将宿主机目录挂载到容器内部目录后，那么日志就会持久化容器外部的宿主机目录中。

**该配置等同于执行命令**：

```shell
docker build -t v1.0.0 . && docker run -p 8080:8080 -v /home/developer/app/logs/:/home/developer/app/logs/ --name docker-hello v1.0.0 
```

## step7、Maven打包

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202304181128523.png)

## step8、运行

![在这里插入图片描述](https://raw.githubusercontent.com/qkd90/figureBed/main/202304181128570.png)
先pull基础镜像，然后再打包镜像，并将镜像部署到远程docker运行
![在这里插入图片描述](https://img-blog.csdnimg.cn/7137ec0f794049e3937ddc24fdb4c796.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA6L-b5Ye755qE56iL5bqP54y_fg==,size_13,color_FFFFFF,t_70,g_se,x_16)

这里我们可以看到镜像名称为docker-demo:1.1，docker容器为docker-server

![image-20230418114953297](https://raw.githubusercontent.com/qkd90/figureBed/main/202304181149348.png)

添加maven goal清理不要的包

```
clean package -U -DskipTests
```



## step9、运行成功

![图片](https://raw.githubusercontent.com/qkd90/figureBed/main/202304181128732.png)
自此，通过IDEA 部署springboot项目到docker成功！可以在浏览器进行应用访问。难以想象，部署一个Javaweb项目竟然如此简单方便！