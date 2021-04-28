# 统一异常处理与统一结果返回

## 1. 全局异常捕获与处理

因为现在主流的都是**前后端分离**的项目，所以我们的异常处理也根据前后端分离来讲述。

Springboot对于异常的处理也做了不错的支持，它提供了一个 **@ControllerAdvice**注解以及 **@ExceptionHandle**r注解，前者是用来**开启全局的异常捕获**，后者则是说明**捕获哪些异常**，对那些异常进行处理。

```java
@ControllerAdvice
public class MyExceptionHandler {

    @ExceptionHandler(value =Exception.class)
    public String exceptionHandler(Exception e){
        System.out.println("发生了一个异常"+e);
           return e.getMessage();
    }
}
```

上面这段代码就是说，只要是代码运行过程中有异常就会进行捕获，并输出出这个异常。

## 2.统一结果返回与统一异常

### 2.1全局异常处理类

自定义一个**全局异常处理类**，来处理各种异常,包括自己定义的异常和内部异常。这样可以简化不少代码，不用自己对每个异常都使用try，catch的方式来实现。

```text
@ControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 处理自定义异常
     *
     */
    @ExceptionHandler(value = DefinitionException.class)
    @ResponseBody
    public Result bizExceptionHandler(DefinitionException e) {
        return Result.defineError(e);
    }

    /**
     * 处理其他异常
     *
     */
    @ExceptionHandler(value = Exception.class)
    @ResponseBody
    public Result exceptionHandler( Exception e) {
        return Result.otherError(ErrorEnum.INTERNAL_SERVER_ERROR);
    }
}
```

### 2.2自己定义需要的异常类

我们需要自定义异常处理类。代码如下：

```text
public class DefinitionException extends RuntimeException{

    protected Integer errorCode;
    protected String errorMsg;

    public DefinitionException(){

    }
    public DefinitionException(Integer errorCode, String errorMsg) {
        this.errorCode = errorCode;
        this.errorMsg = errorMsg;
    }

    public Integer getErrorCode() {
        return errorCode;
    }

    public void setErrorCode(Integer errorCode) {
        this.errorCode = errorCode;
    }

    public String getErrorMsg() {
        return errorMsg;
    }

    public void setErrorMsg(String errorMsg) {
        this.errorMsg = errorMsg;
    }
}
```

2.3

