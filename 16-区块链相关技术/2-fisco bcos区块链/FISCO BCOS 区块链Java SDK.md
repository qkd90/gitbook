# FISCO BCOS 区块链Java SDK

Java SDK 提供了访问 FISCO BCOS 节点的Java API，支持节点状态查询、部署和调用合约等功能，基于Java SDK可开发区块链应用，目前支持[FISCO BCOS 2.0+](https://fisco-bcos-documentation.readthedocs.io/zh_CN/v3.0.0/docs/change_log/index.html)。

注解

v2.0+版本的java-sdk仅支持v2.0+版本FISCO BCOS区块链，若区块链版本是v3.0+,请使用v3.0+版本java-sdk，具体参考 [这里](https://fisco-bcos-doc.readthedocs.io/zh_CN/latest/docs/develop/sdk/java_sdk/index.html)

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