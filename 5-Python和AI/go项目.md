# Codex 自定义指令

这个仓库以 Go 微服务为主，核心规范来自根目录 `README.md`、`开发快速上手指南【boot-1.10.x】.md`、`.golangci.yml`，以及各服务目录中的既有实现。你的目标是在最小改动前提下完成需求，并严格遵守仓库当前代码风格和分层约定。

## 工作总则

- 先读同目录、同模块、同服务的现有实现，再开始改代码。优先遵循“最近的兄弟文件”的稳定写法。
- 先匹配现有模式，再考虑抽象优化。不要引入与当前服务不一致的新架构、新库、新封装习惯。
- 默认做局部修改，不做与需求无关的重构，不顺手重命名大批符号，不调整无关文件。
- 文档规范和现有代码有冲突时：优先遵循当前服务中已稳定落地的实现；涉及跨模块公共约定时，再回到根目录规范文档。
- 保留现有中文业务语义、`dc` 标签、接口摘要和注释风格。新增内容要与现有文件一致。
- 生成注释里面不要加1、2、3...类似步骤数字标签

## 仓库与分层约定

- 服务实现位于 `apps/<service>/internal/`。
- RPC/公共接口定义位于根目录 `api/` 相关模块；若修改跨服务调用协议，必须同步修改协议定义和调用方。
- 分层保持清晰：
  - `internal/api/<module>/`: 控制器，仅处理入参、鉴权上下文、调用 logic、组装返回。
  - `internal/logic/logic.go`: 业务接口定义与服务获取函数。
  - `internal/logic/impl/`: 业务实现。
  - `internal/model/dto/`: logic 层输入输出。
  - `internal/model/vo/`: API/RPC 输入输出。
  - `internal/model/entity/`: 数据库实体或 Mongo 文档映射。
  - `internal/public/*`: 本服务公共常量、枚举、缓存 key、工具。
- 不要把业务逻辑塞进 controller。复杂逻辑、数据库访问、事件发送都应放在 `logic/impl`。
- 仅当某模块已经稳定使用 DAO 层时才沿用；对现有服务，优先遵循本地模式。很多服务直接在 `logic/impl` 中用 `frame.Model` / `mongo.Coll`，不要为了“更分层”新建一层 DAO。

## 命名规范

- Logic 接口命名：`I<Service>`，例如 `ISportRecord`。
- Logic 获取函数：`func SportRecord() ISportRecord`。
- Logic 实现结构体：`s<Service>`，例如 `sSportRecord`。
- Logic 实现需在 `init()` 中注册：`frame.RegisterService[logic.IService](...)`。
- DTO 统一使用 `Inp` / `Out` 后缀。
- VO 统一使用 `Req` / `Res` 后缀。
- API/RPC 请求对象命名要体现业务含义，不要使用含糊的通用名字。
- 常见函数命名遵循仓库约定：
  - `List`: 无分页列表
  - `Page`: 分页查询
  - `Detail`: 单条详情
  - `Save` / `Submit`: 新增或保存
  - `Add`: 仅新增
  - `Update`: 仅更新
  - `Remove`: 逻辑删除
  - `Delete`: 物理删除
  - `Import` / `Export` / `Download` / `BatchXxx`

## API / RPC 规范

- API 请求结构体通常内嵌 `frame.Meta`，并声明 `path`、`method`、`summary`、`auth`、`rpc`、`version` 等标签。
- Controller 保持轻量：
  - 从 `ctx` 或工具函数中补齐 `userId` / `accountId` / 家庭成员上下文
  - 调用 logic
  - 组装返回
- 对象转换优先使用 `frame.Scan` 或 `frame.ScanTo`。不要大段手写字段拷贝，除非存在结构差异或特殊转换。
- 若相邻代码已使用 `_ = frame.Scan(...)` 忽略错误，可保持一致；若转换结果不稳定或字段差异明显，必须显式处理错误或补手动字段。
- 跨服务调用统一使用 `frame.Client(...).ContentJson().Rpc(...)`。不要新增 Feign 风格调用。

## Context、参数与返回值

- `ctx context.Context` 必须是业务方法的第一个参数。
- 除非需要返回 `nil`、修改原对象、或对象很大，否则优先使用值参数和值返回；但如果当前模块已经稳定使用指针风格，优先与本模块保持一致。
- 不要无故把所有入参和返回值改成指针。

## 数据访问规范

- ORM 查询优先使用 `frame.Model(ctx, &entity.X{})` 的链式写法。
- Mongo 查询优先使用 `mongo.Coll(cc.TABLE_NAME)`，过滤条件使用 `bson.M`。
- Mongo 表常量优先复用 `common/consts` 中现有定义，通常以 `cc` 别名导入。
- Redis key 必须集中定义，禁止在业务代码里直接拼接 key；优先复用 `internal/public/caches` 或统一常量定义。
- SQL 简单 CRUD 用 ORM；复杂联表或模板化 SQL 才使用集中管理的 SQL 常量。
- 查询条件复杂且会复用时，抽成小的 filter/helper 函数；简单查询不要过度抽象。
- 新增字段时，保持 `json` / `bson` / `orm` / `dc` 标签风格与相邻实体一致。

## ID、时间与业务常量

- 字符串主键优先使用 `frame.GetId()`；如果当前集合明确使用 Mongo `ObjectID`，则遵循现有集合写法。
- 时间处理优先复用当前模块已有常量或 helper，例如 `layout := "2006-01-02 15:04:05"`。
- 涉及业务日期边界时，优先遵循相邻代码的时区约定。`sino-health` 中大量逻辑使用 `Asia/Shanghai`，不要混用 UTC 或本地默认时区。
- 重复出现的业务字符串、指标 ID、topic/tag、状态值，优先提取为常量；全局常量放 `common/consts`，服务内常量放 `internal/public/consts` 或本文件 `const` 块。

## 错误处理与日志

- 所有错误都必须处理。不要静默吞错，除非是仓库里已明确接受的模式，如无害的 `frame.Scan` 结果忽略。
- 业务错误优先使用项目已有错误体系，例如 `errors.NewCode(...)`；普通错误使用 `fmt.Errorf` / `errors.New`。
- `fmt.Errorf` 消息不要以标点结尾，和仓库 lint 规则保持一致。
- 日志统一优先使用 `frame.Log().Infof / Warningf / Errorf / Debugf`，并传 `ctx`。
- 不要在新代码中继续引入标准库 `log`、`slog` 或 `fmt.Println` 作为正式日志方案，除非所在文件已明确使用且改动范围只允许局部保持。
- `Infof`/`Errorf` 这类格式化日志必须保证占位符和参数匹配，避免 `govet` 报错。

## 事件、消息队列与异步

- 发送事件、Kafka、RocketMQ、延迟消息时，优先复用现有 `common/event` 能力和已有 topic/tag 常量。
- 新增消费者时，按现有模式实现 `Meta()` 和 `Handle()`，并在 `init()` 中注册。
- 谨慎使用 goroutine。优先复用现有模式；涉及上下文、panic 恢复、超时或资源释放时必须明确处理。
- 若当前服务已有同步/异步顺序要求，严格沿用，不要随意并行化。

## 代码风格

- 统一使用 `gofmt -w`。不要引入与仓库现状不一致的格式化工具风格。
- 代码必须至少通过 `typecheck`、`govet`、`errcheck`、`staticcheck` 这类基础检查的预期约束。
- `.golangci.yml` 明确关注的点包括：
  - 不忽略重要错误
  - 避免错误的格式化字符串
  - 避免可疑的变量遮蔽
  - 保持静态检查可通过
- 只在确有价值时加注释。注释重点解释业务原因、兼容逻辑、时区/数据源/事件顺序等，不写“给变量赋值”这类低信息注释。

## 修改策略

- 改接口时，先查：
  - controller
  - `logic.go` 接口
  - `logic/impl`
  - DTO/VO
  - router 绑定
  - 相关 entity / 常量 / RPC 协议
- 新增接口时，优先复制同模块最相近接口的组织方式，再做最小差异修改。
- 修改已有行为时，优先保持旧字段、旧路径、旧响应结构兼容，除非需求明确要求破坏性变更。
- 若当前工作区已有未提交改动，默认视为有效上下文，不要回退或覆盖与任务无关的用户改动。

## 验证与交付

- 改动完成后，至少做与改动范围匹配的本地验证：
  - `gofmt -w <files>`
  - `go test ./apps/<service>/...` 或最小必要的包级验证
- 如果测试因运行时配置初始化而无法直接执行，至少做可编译验证，例如目标包的 `go test -c`，并在结论里明确说明限制。
- 最终说明只写：
  - 改了什么
  - 验证了什么
  - 还有什么限制或风险

## 禁止事项

- 不要引入新的架构层、统一响应封装、依赖注入框架、ORM 封装或工具库，除非仓库已经在该模块稳定使用。
- 不要擅自改公共常量值、MQ topic/tag、缓存 key、RPC path、数据库表名。
- 不要把无关文件一起格式化或重写。
- 不要把局部需求扩展成大范围“顺手治理”。

## 执行优先级

当你不确定如何实现时，按以下优先级决策：

1. 当前目录下最相似文件的写法
2. 当前服务内其他模块的稳定写法
3. 根目录 `README.md`
4. 根目录 `开发快速上手指南【boot-1.10.x】.md`
5. 仅在以上都缺失时，使用保守的 Go 最佳实践
