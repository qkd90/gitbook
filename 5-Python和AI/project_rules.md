## 总要求

你是一个资深的java专家，请在开发中遵循如下规则：
始终使用中文回答
使用全局统一异常处理和@SneakyThrows处理异常，不要使用try catch
严格遵循阿里的java语法规则
遵循  OWASP 安全最佳实践（如输入验证、SQL注入防护）
采用分层架构设计，确保职责分离

不需要生成技术文档，只在我需要你生成的时候生成

## 1.项目技术栈

* **框架** ：Spring Boot 3.x + Java 21
* **依赖** ：satoken,mybatisplus
* 核心：Spring Web, Spring Data JPA, Lombok
* 数据库： mysql
* 其他：


  ## 2.分层架构原则

  | 层级           | 职责                                | 约束条件                                                     |
  | -------------- | ----------------------------------- | ------------------------------------------------------------ |
  | **Controller** | 处理 HTTP 请求与响应，定义 API 接口 | - 禁止直接操作数据库``- 必须通过 Service 层调用              |
  | **Service**    | 业务逻辑实现，事务管理，数据校验    | - 必须通过 Repository 访问数据库``- 返回 DTO 而非实体类（除非必要） |
  | **Repository** | 数据持久化操作，定义数据库查询逻辑  |                                                              |
  | **domain**     | 数据库表结构映射对象                | - 仅用于数据库交互``- 禁止直接返回给前端（需通过 DTO 转换）  |

## 3.核心代码规范

### 1. 实体类（Entity）规范

```java
/**
 * AI任务实体类
 *
 * @author trasen
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("ai_task")
public class AiTask extends BaseEntity {

    /**
     * 任务ID
     */
    @TableId
    private Long taskId;

    /**
     * 任务唯一标识码
     */
    private String taskCode;

    /**
     * 任务类型（0:视频和文字-数字人 1:视频和文字-合成任务, 2:音频与静音视频-合成任务 3:豆包 4:声动人像）
     */
    private String taskType;

    /**
     * 任务状态（0:待处理, 1:处理中, 2:已完成, 3:失败）
     */
    private String status;

    /**
     * 任务处理消息
     */
    private String message;

    /**
     * 要合成的文本内容
     */
    private String text;

    /**
     * 输入视频URL
     */
    private String videoUrl;

    /**
     * 输入音频URL
     */
    private String audioUrl;

    /**
     * 用户上传的人脸参考图 URL
     */
    private String refImageUrl;

    /**
     * 输入视频时长
     */
    private Integer videoDuration;

    /**
     * 输入音频时长
     */
    private Integer audioDuration;

    /**
     * 生成的视频文件路径
     */
    private String videoPath;

    /**
     * OSS存储URL
     */
    private String ossUrl;

    /**
     * OSS文件ID
     */
    private String ossId;

    /**
     * 文件名
     */
    private String fileName;

    /**
     * 完成时间
     */
    private String completionTime;

    /**
     * 外部任务ID
     */
    private String externalTaskId;

    /**
     * 字幕任务id
     */
    private String subtitleJobId;

    /**
     * 视频描述文本提示
     */
    @JsonProperty("text_prompt")
    private String textPrompt;

    /**
     * 图片URL（上传接口返回的URL）
     */
    @JsonProperty("image_file")
    private String imageFile;

    /**
     * 视频时长(秒)
     */
    private Integer duration;

    /**
     * 视频分辨率
     */
    private String resolution;

    /**
     * 是否固定摄像机
     */
    @JsonProperty("camera_fixed")
    private boolean cameraFixed;

    /**
     * 阿里云智能媒体参数
     * 保存整个timeline配置信息，用于后续的视频制作和编辑任务
     * 存储格式为JSON字符串，包含视频轨道和音频轨道的详细配置
     */
    private String timeline;

    /**
     * 封面URL
     */
    private String coverUrl;

    /**
     * 调用的模型
     */
    private String model;

    /**
     * 逻辑删除（0正常 1删除）
     */
    private String isDeleted;
}
```

### 2. 数据访问层（Repository）规范

```java

```

### 3. 服务层（Service）规范

```java
/**
 * AI任务服务接口
 *
 * @author renq@trasen.cn
 */
public interface AiTaskService {

    /**
     * 创建任务
     *
     * @param aiTask 任务信息
     * @return 任务ID
     */
    Long createTask(AiTask aiTask);

    /**
     * 更新任务状态
     *
     * @param taskId  任务ID
     * @param status  任务状态
     * @param message 处理消息
     * @param ossUrl  OSS URL
     */
    void updateTaskStatus(Long taskId, String status, String message, String ossUrl);

    /**
     * 根据任务ID查询任务
     *
     * @param taskId 任务ID
     * @return 任务信息
     */
    AiTask getTaskById(Long taskId);

    /**
     * 根据任务ID查询任务并验证权限
     * 验证任务是否属于当前登录用户
     *
     * @param taskId 任务ID
     * @return 任务信息，如果任务不存在或不属于当前用户则返回null
     */
    AiTask getTaskByIdWithPermissionCheck(Long taskId);

    /**
     * 处理视频和文字-数字人 异步任务
     *
     * @param taskId 任务ID
     */
    void processDigitalTask(Long taskId);

    /**
     * 处理视频和文字-合成任务 异步任务
     *
     * @param taskId 任务ID
     */
    void processVideoTextTask(Long taskId);

    /**
     * 音频与静音视频-合成任务 异步任务
     *
     * @param taskId 音频合成任务ID
     */
    void processAudioVideoTask(Long taskId);

    /**
     * 查询当前用户的任务列表
     *
     * @param aiTask    查询参数
     * @param pageQuery 分页参数
     * @return 任务列表
     */
    TableDataInfo<AiTask> queryTaskList(AiTask aiTask, PageQuery pageQuery);

    /**
     * 校验用户是否有数据权限
     *
     * @param taskId 任务id
     */
    void checkUserDataScope(Long taskId);
}
```

### 4. 控制器（Controller）规范

```java
/**
 * 任务
 *
 * @author renq@trasen.cn
 */
@Slf4j
@Validated
@RequiredArgsConstructor
@RestController
@RequestMapping("/task")
public class AiTaskController extends BaseController {

    private final AiTaskService aiTaskService;

    /**
     * 查询当前用户的任务列表
     *
     * @param aiTask    查询参数
     * @param pageQuery 分页参数
     * @return 任务列表
     */
    @GetMapping("/list")
    public TableDataInfo<AiTask> list(AiTask aiTask, PageQuery pageQuery) {
        // 调用服务层方法查询任务列表，用户ID在Service层获取
        return aiTaskService.queryTaskList(aiTask, pageQuery);
    }

    /**
     * 根据任务ID查询任务详情
     *
     * @param taskId 任务ID
     * @return 任务详情
     */
    @GetMapping("/detail/{taskId}")
    public RequestResponse<AiTask> getInfo(@PathVariable("taskId") Long taskId) {
        // 判断任务是否存在
        AiTask aiTask = aiTaskService.getTaskById(taskId);
        if (aiTask == null) {
            return RequestResponse.fail("任务不存在");
        }

        // 查询是否有权限
        aiTaskService.checkUserDataScope(taskId);
        // 调用服务层方法查询任务详情，同时进行权限检查
        return RequestResponse.ok(aiTaskService.getTaskById(taskId));
    }
}
```

---

## 五、数据传输对象（DTO）规范

```java

```

---

## 六、全局异常处理规范

### 1. 统一响应类（ApiResponse）

```java
/**
 * 操作消息提醒
 *
 * @author renq@trasen.cn
 */
@Data
@NoArgsConstructor
public class RequestResponse<T> implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    /**
     * 成功
     */
    public static final int SUCCESS = 200;

    /**
     * 失败
     */
    public static final int FAIL = 500;

    private int code;

    private String msg;

    private T data;

    public static <T> RequestResponse<T> ok() {
        return restResult(null, SUCCESS, "操作成功");
    }

    public static <T> RequestResponse<T> ok(T data) {
        return restResult(data, SUCCESS, "操作成功");
    }

    public static <T> RequestResponse<T> ok(String msg) {
        return restResult(null, SUCCESS, msg);
    }

    public static <T> RequestResponse<T> ok(String msg, T data) {
        return restResult(data, SUCCESS, msg);
    }

    public static <T> RequestResponse<T> fail() {
        return restResult(null, FAIL, "操作失败");
    }

    public static <T> RequestResponse<T> fail(String msg) {
        return restResult(null, FAIL, msg);
    }

    public static <T> RequestResponse<T> fail(T data) {
        return restResult(data, FAIL, "操作失败");
    }

    public static <T> RequestResponse<T> fail(String msg, T data) {
        return restResult(data, FAIL, msg);
    }

    public static <T> RequestResponse<T> fail(int code, String msg) {
        return restResult(null, code, msg);
    }

    /**
     * 返回警告消息
     *
     * @param msg 返回内容
     * @return 警告消息
     */
    public static <T> RequestResponse<T> warn(String msg) {
        return restResult(null, HttpStatus.WARN, msg);
    }

    /**
     * 返回警告消息
     *
     * @param msg 返回内容
     * @param data 数据对象
     * @return 警告消息
     */
    public static <T> RequestResponse<T> warn(String msg, T data) {
        return restResult(data, HttpStatus.WARN, msg);
    }

    private static <T> RequestResponse<T> restResult(T data, int code, String msg) {
        RequestResponse<T> r = new RequestResponse<>();
        r.setCode(code);
        r.setData(data);
        r.setMsg(msg);
        return r;
    }

    public static <T> Boolean isError(RequestResponse<T> ret) {
        return !isSuccess(ret);
    }

    public static <T> Boolean isSuccess(RequestResponse<T> ret) {
        return RequestResponse.SUCCESS == ret.getCode();
    }
}

```

### 2. 全局异常处理器（GlobalExceptionHandler）

```java
/**
 * 全局异常处理器
 *
 * @author Lion Li
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 请求方式不支持
     */
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public R<Void> handleHttpRequestMethodNotSupported(HttpRequestMethodNotSupportedException e,
                                                       HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求地址'{}',不支持'{}'请求", requestURI, e.getMethod());
        return R.fail(HttpStatus.HTTP_BAD_METHOD, e.getMessage());
    }

    /**
     * 业务异常
     */
    @ExceptionHandler(ServiceException.class)
    public R<Void> handleServiceException(ServiceException e, HttpServletRequest request) {
        log.error(e.getMessage());
        Integer code = e.getCode();
        return ObjectUtil.isNotNull(code) ? R.fail(code, e.getMessage()) : R.fail(e.getMessage());
    }

    /**
     * 认证失败
     */
    @ResponseStatus(org.springframework.http.HttpStatus.UNAUTHORIZED)
    @ExceptionHandler(SseException.class)
    public String handleNotLoginException(SseException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.debug("请求地址'{}',认证失败'{}',无法访问系统资源", requestURI, e.getMessage());
        return JsonUtils.toJsonString(R.fail(HttpStatus.HTTP_UNAUTHORIZED, "认证失败，无法访问系统资源"));
    }

    /**
     * servlet异常
     */
    @ExceptionHandler(ServletException.class)
    public R<Void> handleServletException(ServletException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求地址'{}',发生未知异常.", requestURI, e);
        return R.fail(e.getMessage());
    }

    /**
     * 业务异常
     */
    @ExceptionHandler(BaseException.class)
    public R<Void> handleBaseException(BaseException e, HttpServletRequest request) {
        log.error(e.getMessage());
        return R.fail(e.getMessage());
    }

    /**
     * 请求路径中缺少必需的路径变量
     */
    @ExceptionHandler(MissingPathVariableException.class)
    public R<Void> handleMissingPathVariableException(MissingPathVariableException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求路径中缺少必需的路径变量'{}',发生系统异常.", requestURI);
        return R.fail(String.format("请求路径中缺少必需的路径变量[%s]", e.getVariableName()));
    }

    /**
     * 请求参数类型不匹配
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public R<Void> handleMethodArgumentTypeMismatchException(MethodArgumentTypeMismatchException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求参数类型不匹配'{}',发生系统异常.", requestURI);
        return R.fail(String.format("请求参数类型不匹配，参数[%s]要求类型为：'%s'，但输入值为：'%s'", e.getName(), e.getRequiredType().getName(), e.getValue()));
    }

    /**
     * 找不到路由
     */
    @ExceptionHandler(NoHandlerFoundException.class)
    public R<Void> handleNoHandlerFoundException(NoHandlerFoundException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求地址'{}'不存在.", requestURI);
        return R.fail(HttpStatus.HTTP_NOT_FOUND, e.getMessage());
    }

    /**
     * 拦截未知的运行时异常
     */
    @ResponseStatus(org.springframework.http.HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler(IOException.class)
    public void handleRuntimeException(IOException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        if (requestURI.contains("sse")) {
            // sse 经常性连接中断 例如关闭浏览器 直接屏蔽
            return;
        }
        log.error("请求地址'{}',连接中断", requestURI, e);
    }

    /**
     * 拦截未知的运行时异常
     */
    @ExceptionHandler(RuntimeException.class)
    public R<Void> handleRuntimeException(RuntimeException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求地址'{}',发生未知异常.", requestURI, e);
        return R.fail(e.getMessage());
    }

    /**
     * 系统异常
     */
    @ExceptionHandler(Exception.class)
    public R<Void> handleException(Exception e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求地址'{}',发生系统异常.", requestURI, e);
        return R.fail(e.getMessage());
    }

    /**
     * 自定义验证异常
     */
    @ExceptionHandler(BindException.class)
    public R<Void> handleBindException(BindException e) {
        log.error(e.getMessage());
        String message = StreamUtils.join(e.getAllErrors(), DefaultMessageSourceResolvable::getDefaultMessage, ", ");
        return R.fail(message);
    }

    /**
     * 自定义验证异常
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public R<Void> constraintViolationException(ConstraintViolationException e) {
        log.error(e.getMessage());
        String message = StreamUtils.join(e.getConstraintViolations(), ConstraintViolation::getMessage, ", ");
        return R.fail(message);
    }

    /**
     * 自定义验证异常
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public R<Void> handleMethodArgumentNotValidException(MethodArgumentNotValidException e) {
        log.error(e.getMessage());
        String message = StreamUtils.join(e.getBindingResult().getAllErrors(), DefaultMessageSourceResolvable::getDefaultMessage, ", ");
        return R.fail(message);
    }

    /**
     * JSON 解析异常（Jackson 在处理 JSON 格式出错时抛出）
     * 可能是请求体格式非法，也可能是服务端反序列化失败
     */
    @ExceptionHandler(JsonParseException.class)
    public R<Void> handleJsonParseException(JsonParseException e, HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        log.error("请求地址'{}' 发生 JSON 解析异常: {}", requestURI, e.getMessage());
        return R.fail(HttpStatus.HTTP_BAD_REQUEST, "请求数据格式错误（JSON 解析失败）：" + e.getMessage());
    }

    /**
     * 请求体读取异常（通常是请求参数格式非法、字段类型不匹配等）
     */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public R<Void> handleHttpMessageNotReadableException(HttpMessageNotReadableException e, HttpServletRequest request) {
        log.error("请求地址'{}', 参数解析失败: {}", request.getRequestURI(), e.getMessage());
        return R.fail(HttpStatus.HTTP_BAD_REQUEST, "请求参数格式错误：" + e.getMostSpecificCause().getMessage());
    }

}
```

---

## 七、安全与性能规范

1. **输入校验** ：

* 使用 `@Valid` 注解 + JSR-303 校验注解（如 `@NotBlank`, `@Size`）
* 禁止直接拼接 SQL 防止注入攻击

1. **事务管理** ：

* `@Transactional` 注解仅标注在 Service 方法上
* 避免在循环中频繁提交事务

## 八、代码风格规范

1. **注释规范** ：

* 方法必须添加注释且方法级注释使用 Javadoc 格式
* 计划待完成的任务需要添加 `// TODO` 标记
* 存在潜在缺陷的逻辑需要添加 `// FIXME` 标记

1. **代码格式化** ：

* 使用 IntelliJ IDEA 默认的 Spring Boot 风格
* 禁止手动修改代码缩进（依赖 IDE 自动格式化）

## 十、扩展性设计规范

1. **接口优先** ：

* 服务层接口（`UserService`）与实现（`UserServiceImpl`）分离

1. **日志规范** ：

* 使用 `SLF4J` 记录日志（禁止直接使用 `System.out.println`）
* 核心操作需记录 `INFO` 级别日志，异常记录 `ERROR` 级别