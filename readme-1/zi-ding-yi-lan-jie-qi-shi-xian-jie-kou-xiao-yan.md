# 自定义拦截器实现接口校验

## **自定义拦截器实现比较简单。分为两步：**

* 1.通过implements HandlerInterceptor来实现自定义拦截器。
* 2.通过 implements WebMvcConfigurer来注册自定义拦截器即可。

## 1. pom.xml

```text
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.0.3.RELEASE</version>
</parent>

<dependencies>
    <dependency> 
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

## 2.自定义拦截器 SessionInterceptor.java

新建文件SessionInterceptor.java，每一个拦截器有需要实现的 HandlerInterceptor 接口，这个接口有三个方法，每个方法会在请求调用的不同时期完成，因为我们需要在接口调用之前拦截请求判断是否登陆，所以这里需要使用 preHandle 方法，在里面写验证逻辑，最后返回 true 或者 false，确定请求是否合法。记住加 @Component 注解，另外需要在下一步的 WebConfigurer类中注入自定义拦截器。

```text
package com.example.chengying.service;


import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * 自定义拦截器，实现校验用户是否登陆，未登录返回错误信息：尚未登陆。登陆成功则放行
 * @author tan90
 * @date 2021-04-26
 */
@Component
@Slf4j

@RestControllerAdvice
public class InterceptorVerification {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        log.info("=============进入拦截器了=======================");
        String authorization = request.getHeader("Authorization");
        if(StringUtils.isEmpty(authorization)){
            log.info("调用接口拦截验证登陆信息不存在，说明状态为未登陆！");
            throw new BizException(CodeMsg.NOT_LOGIN_YET);
        }else{
            UserInfo userInfo = null;
            try {
                userInfo = JwtUtil.parseAccessToken(authorization);
                String account = userInfo.getAccount();
                log.info("调用接口拦截验证登陆信息account:{}存在，说明状态为已登陆！",account);
                return true;
            } catch (Exception e) {
                throw new BizException(CodeMsg.HEADER_TRANSFER_EXCEPTION,e.getMessage());
            }
        }
    }
    //请求处理后，渲染ModelAndView前调用
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        log.info("=============进入拦截器,请求处理后,渲染ModelAndView前调用。=================================");
    }
    //渲染ModelAndView后调用
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        log.info("=============进入拦截器,渲染ModelAndView后调用。=================================");
    }
}
```

