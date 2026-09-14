# 区块链相关技术

## 章节定位

本章节记录联盟链相关实践，覆盖 Hyperledger Fabric 和 FISCO BCOS 的环境搭建、测试网络、节点/证书、智能合约与 Java SDK 调用。重点不是只把网络启动起来，而是能完整验证“身份配置 → 网络连通 → 合约/交易提交 → 查询结果”的闭环。

适用于需要了解联盟链基础、搭建开发测试环境、部署 Fabric 网络，或将 FISCO BCOS 接入 Java 服务的场景。

## 招聘准备入口

- [AI 与大数据招聘能力地图](./AI与大数据招聘能力地图.md)：将 Fabric、FISCO BCOS、证书、网络与 Java SDK 资料转成联盟链后端、可信数据平台和企业集成岗位的准备路径。

## 知识地图

```text
联盟链基础
├─ 账户、证书与组织
├─ 节点、网络与共识
├─ 通道、合约与交易
└─ SDK 调用与结果查询

Hyperledger Fabric
├─ Linux 环境与测试网络
├─ Peer、Orderer、Raft 与 Fabric CA
├─ Chaincode 与通道配置
└─ Hyperledger Cello 管理

FISCO BCOS
├─ 节点与控制台
└─ Java SDK、账户与合约调用
```

## 文档导航

| 路线 | 适合解决的问题 | 入口资料 |
| --- | --- | --- |
| Hyperledger Fabric 入门 | 理解 Peer、Orderer、通道、Chaincode 和证书 | [Fabric 章节说明](1-hyperledgerfabric区块链/README.md) |
| Fabric 测试环境 | 在 Linux 中安装基础工具、Docker、Go 并启动测试网络 | [Linux 搭建 Fabric 测试环境](1-hyperledgerfabric区块链/linux搭建fabirc的区块链测试环境.md)、[使用 Fabric 测试网络](1-hyperledgerfabric区块链/使用%20Fabric测试网络.md) |
| Fabric 网络与证书 | 配置网络、Raft 排序服务、Fabric CA 和证书 | [部署 Fabric 网络教程](1-hyperledgerfabric区块链/部署fabric网络教程.md) |
| Cello 管理 | 了解 Cello 架构与创建区块链系统的流程 | [Hyperledger Cello 使用手册](1-hyperledgerfabric区块链/Hyperledger%20Cello的rq使用手册.md) |
| FISCO BCOS Java 接入 | 使用账户、合约和 Java SDK 调用链能力 | [FISCO BCOS 章节说明](2-fiscobcos区块链/README.md)、[FISCO BCOS 区块链 Java SDK](2-fiscobcos区块链/FISCOBCOS%20区块链Java%20SDK.md) |

## 推荐学习与实践路径

1. **先明确链的边界**：理解联盟链中的组织、账户/证书、节点、共识、合约和 SDK 分别解决什么问题。
2. **选择一条技术路线**：Fabric 侧先从 Linux 测试网络开始；FISCO BCOS 侧先从节点/控制台与 Java SDK 的关系开始。两套平台的配置、证书和 SDK 不混用。
3. **跑通最小闭环**：记录网络版本、节点状态、证书/账户配置位置，完成一次合约或交易调用并立即查询结果。
4. **再进入部署与管理**：Fabric 继续学习网络配置、Raft、Fabric CA 和 Cello；FISCO BCOS 继续完善 Java SDK 的账户、合约和异常处理。
5. **保留可排查证据**：每次操作记录命令、配置变更、节点/容器状态、交易标识和查询结果，便于复现问题。

## 实践检查清单

- 节点、容器或进程是否正常运行，端口和网络是否可达。
- 组织、账户和证书是否匹配当前网络；证书路径、私钥和连接配置不能混用。
- 合约部署、交易提交和交易查询是否使用同一网络、通道和账户上下文。
- SDK 连接是否使用了正确的节点地址、证书和合约标识。
- 交易“提交成功”后，是否已通过查询确认状态与业务数据。
- 示例、日志和文档不记录私钥、真实账户凭据或生产连接信息。

## 常见问题定位顺序

1. 先看节点/容器状态与网络连通性。
2. 再核对版本、配置文件、通道和证书路径。
3. 然后确认合约已部署、调用账户有权限、SDK 连接的是目标网络。
4. 最后分别核对交易提交结果与查询结果，避免将“请求已发送”误判为“数据已上链”。

## 后续维护方向

- 新增实践文章应标注平台和版本、前置软件、拓扑/组织边界、配置修改点与验证步骤。
- 网络部署、证书轮换和合约升级需附带回滚或恢复说明，并明确测试环境与生产环境的差异。
- 长命令或多节点操作应提供预期现象和失败排查入口，方便后来者按步骤确认状态。
