# SpringCloud/Boot + Oauth2 集成短信登陆方案

登录框架有很多，Oauth2算是属于比较常用的一个框架了，诸如腾讯，阿里，字节跳动等产品登录都是使用Oauth2的。那么Oauth2怎么集成短信登陆和第三方登录呢？

最终我参考了这个作者的文章，把短信登录集成做好了，这个方案是属于非侵入式的解决方案，实现起来也相对来说简单。

#### 1.实现思路:

![实现流程图](https://upload-images.jianshu.io/upload_images/15637155-17bf19e87b11ca36.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1180/format/webp)

首先需要做一个Filter，用来拦截/oauth/token的请求，并增加auth_type用来区分登录方式。

```
public class IntegrationAuthenticationFilter extends GenericFilterBean implements ApplicationContextAware {

    private static final String AUTH_TYPE_PARM_NAME = "auth_type";

    private static final String OAUTH_TOKEN_URL = "/oauth/token";

    private Collection<IntegrationAuthenticator> authenticators;

    private ApplicationContext applicationContext;

    private RequestMatcher requestMatcher;

    public IntegrationAuthenticationFilter() {
        this.requestMatcher = new OrRequestMatcher(
                new AntPathRequestMatcher(OAUTH_TOKEN_URL, "GET"),
                new AntPathRequestMatcher(OAUTH_TOKEN_URL, "POST")
        );
    }

    @Bean
    public FilterRegistrationBean registrationBean(IntegrationAuthenticationFilter integrationAuthenticationFilter){
        FilterRegistrationBean registrationBean = new FilterRegistrationBean(integrationAuthenticationFilter);
        registrationBean.setEnabled(false);
        return registrationBean;
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        HttpServletResponse response = (HttpServletResponse) servletResponse;

        if (requestMatcher.matches(request)) {
            //设置集成登录信息
            IntegrationAuthentication integrationAuthentication = new IntegrationAuthentication();
            integrationAuthentication.setAuthType(request.getParameter(AUTH_TYPE_PARM_NAME));
            integrationAuthentication.setAuthParameters(request.getParameterMap());
            IntegrationAuthenticationContext.set(integrationAuthentication);
            try {
                //预处理
                this.prepare(integrationAuthentication);

                filterChain.doFilter(request, response);

                //后置处理
                this.complete(integrationAuthentication);
            } finally {
                IntegrationAuthenticationContext.clear();
            }
        } else {
            filterChain.doFilter(request, response);
        }
    }

    /**
     * 进行预处理
     *
     * @param integrationAuthentication
     */
    private void prepare(IntegrationAuthentication integrationAuthentication) {

        //延迟加载认证器
        if (this.authenticators == null || this.authenticators.isEmpty()) {
            synchronized (this) {
                Map<String, IntegrationAuthenticator> integrationAuthenticatorMap = applicationContext.getBeansOfType(IntegrationAuthenticator.class);
                if (integrationAuthenticatorMap != null) {
                    this.authenticators = integrationAuthenticatorMap.values();
                }
            }
        }

        if (this.authenticators == null || this.authenticators.isEmpty()) {
            this.authenticators = new ArrayList<>();
        }

        for (IntegrationAuthenticator authenticator : authenticators) {
            if (authenticator.support(integrationAuthentication)) {
                authenticator.prepare(integrationAuthentication);
            }
        }
    }

    /**
     * 后置处理
     *
     * @param integrationAuthentication
     */
    private void complete(IntegrationAuthentication integrationAuthentication) {
        for (IntegrationAuthenticator authenticator : authenticators) {
            if (authenticator.support(integrationAuthentication)) {
                authenticator.complete(integrationAuthentication);
            }
        }
    }

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.applicationContext = applicationContext;
    }
}
```

拦截器做完了，然后就到SmsAuthenticator了。（敲重点！！！ 这里面的代码才是实际上验证短信验证码是否正确的地方，所以必不可少）

```
@Component
public class SmsIntegrationAuthenticator extends AbstractPreparableIntegrationAuthenticator implements ApplicationEventPublisherAware {

    @Autowired
    private IUsersService usersService;

    @Autowired
    private ISmsMessageService smsMessageService;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private ApplicationEventPublisher applicationEventPublisher;

    private final static String SMS_AUTH_TYPE = "sms";

    @Override
    public Users authenticate(IntegrationAuthentication integrationAuthentication) {
        //获取密码，实际值是验证码
        String password = integrationAuthentication.getAuthParameter("password");
        //获取用户名，实际值是手机号
        String username = integrationAuthentication.getUsername();
        //发布事件，可以监听事件进行自动注册用户
        this.applicationEventPublisher.publishEvent(new SmsAuthenticateBeforeEvent(integrationAuthentication));
        //通过手机号码查询用户
        Users users = usersService.getUserByPhone(username);
        if (users != null) {
            //将密码设置为验证码
            users.setPassword(passwordEncoder.encode(password));
            //发布事件，可以监听事件进行消息通知
            this.applicationEventPublisher.publishEvent(new SmsAuthenticateSuccessEvent(integrationAuthentication));
        }
        return users;
    }

    @Override
    public void prepare(IntegrationAuthentication integrationAuthentication)   {
        String smsCode = integrationAuthentication.getAuthParameter("password");
        String username = integrationAuthentication.getAuthParameter("username");
        SmsMessage message = null;
        try {
            message = smsMessageService.validateCaptcha(username, Integer.parseInt(smsCode));
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (message==null) {
            throw new OAuth2Exception("验证码错误或已过期");
        }
    }

    @Override
    public boolean support(IntegrationAuthentication integrationAuthentication) {
        return SMS_AUTH_TYPE.equals(integrationAuthentication.getAuthType());
    }

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
        this.applicationEventPublisher = applicationEventPublisher;
    }
}
```

验证码验证的方法就不贴出来了，都是根据手机号和验证码去查询获取的。

### 好了，做完这两个步骤之后，还需要做什么呢？

#### 修改AuthorizationServerConfiguration里的代码，命名可能都不一样，不过这个类是继承AuthorizationServerConfigurerAdapter的，所以你们可以搜一下就清楚了。

找到代码位置

```
    @Override
    public void configure(AuthorizationServerSecurityConfigurer scurityConfigurer) {
        scurityConfigurer.tokenKeyAccess("permitAll()")
                .checkTokenAccess("permitAll()")
                .allowFormAuthenticationForClients()
                .addTokenEndpointAuthenticationFilter(integrationAuthenticationFilter);
    }
```

上面的代码是继承AuthorizationServerConfigurerAdapter必须实现的方法，在里面我们把Filter加上，这样刚刚写的Filter才能生效。

```
addTokenEndpointAuthenticationFilter(integrationAuthenticationFilter);
```

### 好了，代码贴的差不多了。短信登录可以说基本上完成了（如果集成微信，淘宝等登录方式也可以按照这个方案来实现）

### 现在就要测试一下能否可行了

我是使用Postman来测试接口的
{{ip}}:8080/oauth/token?username=手机号&password=验证码&grant_type=password&client_id=xxx&client_secret=xxx&auth_type=sms
最终出现这样的结果

验证码正确，用户也存在



image.png

验证码不正确



image.png

### 登录的请求基本没有变化，但是注意的是需要增加一个auth_type，这里面的值就是你拦截器里面写的值。

## 看到这里我相信大家都把短信登录集成到系统里面了，但是会出现一个问题。如果不加auth_type的话，随便输入什么密码都会登录成功，那么这里要怎么解决呢？

#### 其实非常简单，我们需要再实现一个PasswordIntegrationAuthenticator就好了，具体代码和SmsIntegrationAuthenticator差不多，但是验证用户的时候需要改成以下方式

```
 @Override
    public void prepare(IntegrationAuthentication integrationAuthentication) {
        BCryptPasswordEncoder bCryptPasswordEncoder = new BCryptPasswordEncoder();
        String username = integrationAuthentication.getAuthParameter("username");
        String password = integrationAuthentication.getAuthParameter("password");
        Users users = null;
        try {
            users = usersService.findByUid(username);
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (users == null) {
            throw new OAuth2Exception("用户不存在");
        }
        String userPwd = users.getPassword().substring(users.getPassword().lastIndexOf("}") + 1, users.getPassword().length());
        if (!bCryptPasswordEncoder.matches(password, userPwd)) {
            throw new OAuth2Exception("密码错误");
        }
    }
```

然后登录请求把auth_type加上，具体的值就是你们设置的那个，然后登录的时候就会走这个验证用户和密码合法性了。

最后，我得吐槽一下。。。 这鬼东西搞了我两天，终于弄好了！！

撒花*★,°*:.☆(￣▽￣)/$:*.°★* 。