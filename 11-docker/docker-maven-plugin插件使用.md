pom文件配置

```html
			<plugin>
                <groupId>io.fabric8</groupId>
                <artifactId>docker-maven-plugin</artifactId>
                <version>0.40.3</version>
                <configuration>
                    <!--这一部分是为了实现对远程docker容器的控制-->
                    <!--docker主机地址,用于完成docker各项功能,注意是tcp不是http!-->
                    <dockerHost>tcp://192.168.18.17:2375</dockerHost>
                    <!--这一部分是为了实现docker镜像的构建和推送-->
                    <!--镜像相关配置,支持多镜像-->
                    <images>
                        <!-- 单个镜像配置 -->
                        <image>
                            <!--镜像名(含版本号)-->
                            <name>trasen/trasenchain:${project.version}</name>
                            <!--别名:用于容器命名和在docker-compose.yml文件只能找到对应名字的配置-->
                            <alias>trasenchain${project.version}</alias>
                            <!--镜像build相关配置-->
                            <build>
                                <!--使用dockerFile文件-->
                                <dockerFileDir>${project.basedir}</dockerFileDir>
                                <ports>
                                    <port>9999</port>
                                </ports>
                                <cleanup>
                                </cleanup>

                            </build>
                            <!--容器run相关配置-->
                            <run>
                                <!--配置运行时容器命名策略为:别名,如果不指定则默认为none,即使用随机分配名称-->
                                <namingStrategy>alias</namingStrategy>
                            </run>
                        </image>
                    </images>
                </configuration>
                <executions>
                    <execution>
                        <id>docker-build</id>
                        <!-- 绑定mvn install阶段，当执行mvn install时 就会执行docker build 和docker push-->
                        <phase>install</phase>
                        <goals>
                            <goal>build</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
```

