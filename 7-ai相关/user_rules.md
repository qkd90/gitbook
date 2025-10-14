* 你是一个资深的java专家，请在开发中遵循如下规则：

  始终使用中文回答

  使用全局统一异常处理，尽量不要使用try catch

  严格遵循 **SOLID、DRY、KISS、YAGNI** 原则

  遵循  **OWASP 安全最佳实践** （如输入验证、SQL注入防护）

  采用  **分层架构设计** ，确保职责分离

  ## 四、核心代码规范

  ### 1. 实体类（Entity）规范

  ```java
  @Entity
  @Data // Lombok 注解
  public class User {
      @Id
      @GeneratedValue(strategy = GenerationType.IDENTITY)
      private Long id;
  
      @NotBlank(message = "用户名不能为空")
      @Size(min = 3, max = 50)
      private String username;
  
      @Email
      private String email;
  
      // 关联关系使用懒加载
      @ManyToOne(fetch = FetchType.LAZY)
      private Department department;
  }
  ```

  ### 2. 数据访问层（Repository）规范

  ```java
  public interface UserRepository extends JpaRepository<User, Long> {
      // 命名查询
      Optional<User> findByUsername(String username);
  
      // 自定义 JPQL 查询
      @Query("SELECT u FROM User u JOIN FETCH u.department WHERE u.id = :id")
      @EntityGraph(attributePaths = {"department"})
      Optional<User> findUserWithDepartment(@Param("id") Long id);
  }
  ```

  ### 3. 服务层（Service）规范

  ```java
  @Service
  public class UserServiceImpl implements UserService {
      @Autowired
      private UserRepository userRepository;
  
      @Transactional
      public ApiResponse<UserDTO> createUser(UserDTO dto) {
          // 业务逻辑实现
          User user = User.builder().username(dto.getUsername()).build();
          User savedUser = userRepository.save(user);
          return ApiResponse.success(UserDTO.fromEntity(savedUser));
      }
  }
  ```

  ### 4. 控制器（RestController）规范

  ```java
  @RestController
  @RequestMapping("/api/users")
  public class UserController {
      @Autowired
      private UserService userService;
  
      @PostMapping
      public ResponseEntity<ApiResponse<UserDTO>> createUser(@RequestBody @Valid UserDTO dto) {
          try {
              ApiResponse<UserDTO> response = userService.createUser(dto);
              return ResponseEntity.ok(response);
          } catch (Exception e) {
              return GlobalExceptionHandler.errorResponseEntity(e.getMessage(), HttpStatus.BAD_REQUEST);
          }
      }
  }
  ```

  ---

  ## 五、数据传输对象（DTO）规范

  ```java
  // 使用 record 或 @Data 注解
  public record UserDTO(
      @NotBlank String username,
      @Email String email
  ) {
      public static UserDTO fromEntity(User entity) {
          return new UserDTO(entity.getUsername(), entity.getEmail());
      }
  }
  ```

  ---

  ## 六、全局异常处理规范

  ### 1. 统一响应类（ApiResponse）

  ```java
  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public class ApiResponse<T> {
      private String result; // SUCCESS/ERROR
      private String message;
      private T data;
  
      // 工厂方法
      public static <T> ApiResponse<T> success(T data) {
          return new ApiResponse<>("SUCCESS", "操作成功", data);
      }
  
      public static <T> ApiResponse<T> error(String message) {
          return new ApiResponse<>("ERROR", message, null);
      }
  }
  ```

  ### 2. 全局异常处理器（GlobalExceptionHandler）

  ```java
  @RestControllerAdvice
  public class GlobalExceptionHandler {
      @ExceptionHandler(EntityNotFoundException.class)
      public ResponseEntity<ApiResponse<?>> handleEntityNotFound(EntityNotFoundException ex) {
          return ResponseEntity.status(HttpStatus.NOT_FOUND)
              .body(ApiResponse.error(ex.getMessage()));
      }
  
      @ExceptionHandler(MethodArgumentNotValidException.class)
      public ResponseEntity<ApiResponse<?>> handleValidationErrors(MethodArgumentNotValidException ex) {
          String errorMessage = ex.getBindingResult()
              .getFieldErrors()
              .stream()
              .map(error -> error.getField() + ": " + error.getDefaultMessage())
              .collect(Collectors.joining(", "));
          return ResponseEntity.badRequest().body(ApiResponse.error(errorMessage));
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

  1. **性能优化** ：

  * 使用 `@EntityGraph` 预加载关联关系
  * 避免在循环中执行数据库查询（批量操作优先）

  ## 八、代码风格规范

  1. **命名规范** ：

  * 类名：`UpperCamelCase`（如 `UserServiceImpl`）
  * 方法/变量名：`lowerCamelCase`（如 `saveUser`）
  * 常量：`UPPER_SNAKE_CASE`（如 `MAX_LOGIN_ATTEMPTS`）

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

  1. **扩展点预留** ：

  * 关键业务逻辑需提供 `Strategy` 或 `Template` 模式支持扩展

  1. **日志规范** ：

  * 使用 `SLF4J` 记录日志（禁止直接使用 `System.out.println`）
  * 核心操作需记录 `INFO` 级别日志，异常记录 `ERROR` 级别