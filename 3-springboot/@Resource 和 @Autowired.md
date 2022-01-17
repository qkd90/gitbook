# @Resource 和 @Autowired

@Resource 是 *JSR-250* 规范的一部分

说到 @Resource 大家肯定会想到 @Autowired， 至于两者的区别， 大部门分童鞋都知道。


@Resource 的作用和 @Autowired 一样，只不过 @Autowired 是按 byType 自动注入，而 @Resource 默认按 byName 自动注入，而且还提供了 name 和 type 两个属性，其含义也容易理解，分别按 byName 和 byType 注入。

如果两个属性都没有提供的话，则根据属性名称注入，我理解的是 byName，还有地方说是通过反射机制使用 byName自动注入。

![img](https://pic2.zhimg.com/80/v2-7a9749258c9344f8458a8782ab86e2b5_720w.jpg)

我们先来看看 @Autowired 的测试情况。

![img](https://pic2.zhimg.com/v2-fe6daaa1a5eb5f50f4f85b132b45ce6d_r.jpg)

我通过在 SpringTest 类的 Main 方法中，创建基于注解的容器对象 AnnotationConfigApplicationContext 并初始化和启动 Spring 容器，通过调用 getBean 方法获取 UserService 对象并调用 getUser 方法。spring.xml 配置文件中配置了两个 UserDao 接口的实现类 UserDaoImpl0 和 UserDaoImpl1，打印了简单的一句话。结果肯定显而易见，报错了。

![img](https://pic2.zhimg.com/v2-e6486aea06d8d4fe18fd5c92c34b1f41_r.jpg)

我在 spring.xml 中配置了两个实现类，默认按 byType 注入，发现多个，根据 byName注入，无法找到 name 为 userDao 的 bean，所以报错了，接下来修改属性名，再看。

![img](https://pic2.zhimg.com/v2-7fd96ab0d97a38e0beb02a8c44d31e1d_r.jpg)

这次同样的步骤，默认按 byType 注入，发现多个，根据 byName 注入，找到 name 为 userDaoImpl0 的 Bean。成功执行。

![img](https://pic3.zhimg.com/v2-efad5f6840b0f28bd03527f034a14ae6_r.jpg)

接下来看看 @Resource 的情况，请看下图配置，我注释掉了 spring.xml 中的一个实现类的声明。

![img](https://pic1.zhimg.com/v2-f5298d22c75fb9e39b7690bab4478660_r.jpg)

注意 UserServiceImpl 中声明的属性 userDao，在 spring.xml 配置文件中没有这个属性对应的 Bean，@Resource 没有配置 name 和 type 的情况下，结果是什么呢？现在大家猜一下执行成功还是失败。

![img](https://pic2.zhimg.com/v2-093003f697d803c1c6116c96851717ed_r.jpg)

是的，没有报错，你猜对了吗？那好现在我们把 UserServiceImpl 中的属性名称再改一下。

![img](https://pic2.zhimg.com/v2-d09d801db304498d59260a6d055e4a55_r.jpg)

我把属性改为在 spring.xml 中存在的 Bean，userDaoImpl1，然后我们再来看看结果，毫无疑问结果肯定是没有报错。

![img](https://pic3.zhimg.com/v2-ee53ae6f1a422647d3071a86dcf505e2_r.jpg)

那好，按照以上测试结果来看，当 @Resource 没有提供 name 和 type 属性的时候，如果 byName 没有找到对应的 Bean 时，则会根据依赖属性的类型去 Spring 容器中查找是否有提供了其他类型相同的 Bean，如果有则自动注入，如果没有则报错。当然如果根据 byName 找到了则直接注入。接下来，我们再来看看，name 和 type 的情况。

![img](https://pic3.zhimg.com/v2-f5255f8b124fd5b31abe3da3c4943a82_r.jpg)

我在 UserServiceImpl 中添加了 @Resource 的 name 属性 为 userDaoImpl0，那么现在如果执行，结果是否会报错？

![img](https://pic2.zhimg.com/v2-8ef7f93a593e6064446cf726777914a9_r.jpg)

是的报错了，因为我的 spring.xml 中注释了 userDaoImpl0 的声明，所以在使用 name 属性查找时，无法找到对应的 Bean，所以直接报错，没有再次去通过类型到 Spring 容器中查找。接下来我们再看看使用存在 spring.xml 中配置的 Bean的情况。

![img](https://pic1.zhimg.com/v2-cbc5140b01e3a48ce304588d774f721c_r.jpg)

我使用了 userDaoImpl1 这个 Bean，那结果显而易见，肯定没有问题。

![img](https://pic4.zhimg.com/v2-65a8430af82dffe60d2230f547a09e2f_r.jpg)

type 属性我就不用演示了吧，和 name 属性是一样，如果同时提供了 name 和 type 的话，那就必须两个都要匹配才能注入依赖，否则就会注入失败。总算把 @Resource 注解搞明白了，之前一直以为 @Resource 注解就是默认 byName 装配，不知道里面还有这么多弯弯绕呢。下篇文章我会从源码角度带大家看看，当不提供 name 和 type时，Spring 是怎样根据类型查找容器里面相同类型的属性。