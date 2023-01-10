# Kubernetes 测试网络

该项目将Hyperledger框架重新建立为云原生应用程序。

从2.0版开始，Hyperledger引入了test-network项目作为运行 Fabric 网络的加速器和学习资源。 除了为操作模式提供了学习指南，测试网络还为Fabric 社区，通过可工作的本地系统快速上手，编写智能合约并进行开发简单的区块链应用程序。

作为基于 docker-compose 的测试网络的补充，本指南提供了等效的 Fabric 网络适用于运行示例应用程序和链码，开发网关和链码即服务应用程序，并将 CI 和部署流程与统一的容器框架 -Kubernetes 协调起来。

与 Fabric 类似，Kubernetes 引入了陡峭的学习曲线，并呈现出令人眼花缭乱的操作阵列和灵活性。 在本指南中，我们将概述 ./network脚本，提供对 [Fabric CA 部署指南]（https://hyperledger-fabric-ca.readthedocs.io/en/latest/deployguide/ca-deploy.html）的补充，并构建一个参考模型，以便在 Kubernetes 上进行实际的生产部署。

## 1.目标

- 提供简单、_one click_活动来运行 Fabric 测试网络。
- 提供在 Kubernetes 上部署_production style_网络的参考指南。
- 为开发链码、网关和区块链应用程序提供_cloud ready_平台。
- 提供对 Fabric [CA 操作和部署] （https://hyperledger-fabric-ca.readthedocs.io/en/latest/deployguide/ca-deploy.html） 指南的 Kube 补充。
- 支持过渡到[链码即服务]（https://hyperledger-fabric.readthedocs.io/en/latest/cc_service.html）。
- 支持从内部 Docker 守护程序到 [外部链码]（https://hyperledger-fabric.readthedocs.io/en/latest/cc_launcher.html）构建器的转换。
- 在任何 Kube 上运行。

## 2.准备工作

1.安装docker

2.安装kubectl

3.安装kind

4.安装jq

## 3.快速开始

Create a local Kubernetes cluster:

```shell
./network kind
```

启动网络，创建通道，并部署[basic-asset-transfer](../asset-transfer-basic) 智能合约: 

```shell
./network up
./network channel create
./network chaincode deploy
```

Invoke and query chaincode:

```shell
./network chaincode invoke '{"Args":["CreateAsset","1","blue","35","tom","1000"]}' 
./network chaincode query '{"Args":["ReadAsset","1"]}'
```

Access the blockchain with a [REST API](https://github.com/hyperledger/fabric-samples/tree/main/asset-transfer-basic/rest-api-typescript): 

```
./network rest-easy
```

Tear down the test network: 

```shell
./network down 
```

Tear down the cluster: 

```shell
./network unkind
```


## 4.网络拓扑结构

Kube 测试网络在一个专门的排序节点和两个peer节点之间建立了联盟。对网络的参与通过渠道进行管理，交易通过以下方式asset-transfer-basic，提交到区块链分类账调用 
_Chaincode-as-a-Service_ 在共享的 Kubernetes namespace上运行 .

![Test Network](https://github.com/hyperledger/fabric-samples/raw/main/test-network-k8s/docs/images/test-network.png)
