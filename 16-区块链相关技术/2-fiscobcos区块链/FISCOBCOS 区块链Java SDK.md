# FISCO BCOS 区块链Java SDK

Java SDK 提供了访问 FISCO BCOS 节点的Java API，支持节点状态查询、部署和调用合约等功能，基于Java SDK可开发区块链应用

> **主要特性**
>
> - 提供 [合约编译](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/quick_start.html#solidityjava) ，将Solidity合约文件转换成Java合约文件
> - 提供 [Java SDK API](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/api.html),提供访问FISCO BCOS [JSON-RPC](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/api.html) 的功能，并支持预编译（Precompiled）合约调用
> - 提供 [自定义构造和发送交易功能](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/assemble_transaction.html)
> - 提供 [AMOP](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/amop.html) 功能
> - 支持 [事件推送](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/event_sub.html)
> - 支持 [ABI解析](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/abi.html)
> - 提供 [账户管理](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/key_tool.html) 接口

- [快速入门](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/quick_start.html)
- [配置说明](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/configuration.html)
- [基于ABI和BIN调用合约](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/assemble_transaction.html)
- [集成外部签名服务调用合约](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/remote_sign_assemble_transaction.html)
- [交易的组装与发送详解](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/make_transaction.html)
- [交易回执解析](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/transaction_decode.html)
- [AMOP 功能](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/amop.html)
- [合约事件推送](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/event_sub.html)
- [ABI解析](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/abi.html)
- [远程调用接口](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/api.html)
- [账户管理](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/key_tool.html)
- [密码学模块](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/sdk/java_sdk/crypto.html)
- [Java SDK JavaDoc](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/javadoc/index.html)

## 账户管理

FISCO BCOS 使用账户来标识和区分每一个独立的用户。在采用公私钥体系的区块链系统里，每一个账户对应一对公钥和私钥。其中，账户的账户名为该账户的公钥经哈希等安全单向性算法计算后得到的字符串地址，即**账户地址**。

TBaaS 可托管私钥，用户需要新增或者导入已有私钥来参与链共识。私钥以群组维度展示，页面可以切换群组。



