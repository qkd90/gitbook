# 使用 Fabric 测试网络

下载 Hyperledger Fabric Docker 映像和示例后，您可以使用 `fabric-samples`存储库中提供的脚本部署测试网络。测试网络用于通过在本地机器上运行节点来了解 Fabric。开发人员可以使用该网络来测试他们的智能合约和应用程序。该网络旨在仅用作教育和测试的工具，而不是作为如何建立网络的模型。一般来说，不鼓励对脚本进行修改，这可能会破坏网络。它基于不应用作部署生产网络的模板的有限配置：

- 它包括两个对等组织和一个排序组织。
- 为简单起见，配置了单节点 Raft 排序服务。
- 为降低复杂性，未部署 TLS 证书颁发机构 (CA)。所有证书均由根 CA 颁发。
- 示例网络使用 Docker Compose 部署 Fabric 网络。由于节点在 Docker Compose 网络中是隔离的，因此未将测试网络配置为连接到其他正在运行的 Fabric 节点。

要了解如何在生产中使用 Fabric，请参阅部署生产网络章节。

## 在你开始之前

在您可以运行测试网络之前，您需要在您的环境中安装 Fabric Samples。并且根据开始手册安装所需软件。

## 启动测试网络

`test-network`您可以在存储库的目录中找到启动网络的脚本`fabric-samples`。使用以下命令导航到测试网络目录：

```
cd fabric-samples/test-network
```

在此目录中，您可以找到一个带注释的脚本 ，`network.sh`它使用本地计算机上的 Docker 映像建立了一个 Fabric 网络。您可以运行 以打印脚本帮助文本：`./network.sh -h`

```shell
Usage:
  network.sh <Mode> [Flags]
    Modes:
      up - Bring up Fabric orderer and peer nodes. No channel is created
      up createChannel - Bring up fabric network with one channel
      createChannel - Create and join a channel after the network is created
      deployCC - Deploy a chaincode to a channel (defaults to asset-transfer-basic)
      down - Bring down the network

    Flags:
    Used with network.sh up, network.sh createChannel:
    -ca <use CAs> -  Use Certificate Authorities to generate network crypto material
    -c <channel name> - Name of channel to create (defaults to "mychannel")
    -s <dbtype> - Peer state database to deploy: goleveldb (default) or couchdb
    -r <max retry> - CLI times out after certain number of attempts (defaults to 5)
    -d <delay> - CLI delays for a certain number of seconds (defaults to 3)
    -i <imagetag> - Docker image tag of Fabric to deploy (defaults to "latest")
    -cai <ca_imagetag> - Docker image tag of Fabric CA to deploy (defaults to "latest")
    -verbose - Verbose mode

    Used with network.sh deployCC
    -c <channel name> - Name of channel to deploy chaincode to
    -ccn <name> - Chaincode name.
    -ccl <language> - Programming language of the chaincode to deploy: go (default), java, javascript, typescript
    -ccv <version>  - Chaincode version. 1.0 (default), v2, version3.x, etc
    -ccs <sequence>  - Chaincode definition sequence. Must be an integer, 1 (default), 2, 3, etc
    -ccp <path>  - File path to the chaincode.
    -ccep <policy>  - (Optional) Chaincode endorsement policy using signature policy syntax. The default policy requires an endorsement from Org1 and Org2
    -cccg <collection-config>  - (Optional) File path to private data collections configuration file
    -cci <fcn name>  - (Optional) Name of chaincode initialization function. When a function is provided, the execution of init will be requested and the function will be invoked.

    -h - Print this message

 Possible Mode and flag combinations
   up -ca -r -d -s -i -cai -verbose
   up createChannel -ca -c -r -d -s -i -cai -verbose
   createChannel -c -r -d -verbose
   deployCC -ccn -ccl -ccv -ccs -ccp -cci -r -d -verbose

 Examples:
   network.sh up createChannel -ca -c mychannel -s couchdb -i 2.0.0
   network.sh createChannel -c channelName
   network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-javascript/ -ccl javascript
   network.sh deployCC -ccn mychaincode -ccp ./user/mychaincode -ccv 1 -ccl javascript
```

从`test-network`目录内部，运行以下命令以从之前的任何运行中删除任何容器或工件：

```
./network.sh down
```

执行结果如下;

```shell
Using docker and docker-compose
Stopping network
Decomposing compose-test-net.yaml
[+] Running 8/8
 ⠿ Container orderer.example.com          Removed                                                                                                                             0.0s
 ⠿ Container cli                          Removed                                                                                                                             0.0s
 ⠿ Container peer0.org1.example.com       Removed                                                                                                                             0.1s
 ⠿ Container peer0.org2.example.com       Removed                                                                                                                             0.1s
 ⠿ Volume compose_peer0.org2.example.com  Removed                                                                                                                             0.0s
 ⠿ Volume compose_orderer.example.com     Removed                                                                                                                             0.0s
 ⠿ Volume compose_peer0.org1.example.com  Removed                                                                                                                             0.0s
 ⠿ Network fabric_test                    Removed                                                                                                                            18.1s
Decomposing compose-couch.yaml
service "peer0.org1.example.com" has neither an image nor a build context specified: invalid compose project
Decomposing compose-ca.yaml
[+] Running 1/0
 ⠿ compose  Warning: No resource found to remove                                                                                                                              0.0s
Error: No such volume: docker_orderer.example.com
Error: No such volume: docker_peer0.org1.example.com
Error: No such volume: docker_peer0.org2.example.com
Removing remaining containers
bcdcb140f1da
8f05496899c7
Removing generated chaincode docker images
Untagged: dev-peer0.org2.example.com-basic_1.0-dee2d612e15f5059478b9048fa4b3c9f792096554841d642b9b59099fa0e04a4-308602e1b42899c349e52c36c8f00dea32c141acb8851b0e809ca9e2543355c0:latest
Deleted: sha256:41656aa052b03be2c10697b6d382da7dc929e72980ca97268ccec875bdeb12ed
Deleted: sha256:2706edf3aae75e78f00ddfe5bfb1c508ad2e34268b209997eecb8abb49953434
Deleted: sha256:146e016d3c05b012c7a37c4f520d95a7a9099320fc6d1fac8fa24746074d8017
Deleted: sha256:d51a2c6c352ca0fa0979ac9eda7493abfeafe2891d1ecea3e3e4eabfd47e67c5
Untagged: dev-peer0.org1.example.com-basic_1.0-dee2d612e15f5059478b9048fa4b3c9f792096554841d642b9b59099fa0e04a4-56aae3ced9c0f8ca473609d4ac62394b30c6863da4d58757901cc5df53260f8b:latest
Deleted: sha256:7b2bdad1fb1a65774c59f50a6f9c36c6374a2f6b1d607d88724d2eea574c48b2
Deleted: sha256:3aab780836902483140fd7121d3f992efc05ed75409aa373f1c931cd9112e893
Deleted: sha256:7f74ca8748f36a1a8334a1038a0d1e276602d8ff603efd2b599d9be5952599af
Deleted: sha256:6883574dc562eb25423442c9dea7dea7f2a903e3a2acf0a90ddac46213ec8bff
"docker kill" requires at least 1 argument.
See 'docker kill --help'.

Usage:  docker kill [OPTIONS] CONTAINER [CONTAINER...] [flags]

Kill one or more running containers

```

然后，您可以通过发出以下命令来启动网络。如果您尝试从另一个目录运行脚本，您将遇到问题：

```
./network.sh up
```

输出结果如下：

```shell
Using docker and docker-compose
Starting nodes with CLI timeout of '5' tries and CLI delay of '3' seconds and using database 'leveldb' with crypto from 'cryptogen'
LOCAL_VERSION=2.4.2
DOCKER_IMAGE_VERSION=2.4.2
/usr/local/bin/cryptogen
Generating certificates using cryptogen tool
Creating Org1 Identities
+ cryptogen generate --config=./organizations/cryptogen/crypto-config-org1.yaml --output=organizations
org1.example.com
+ res=0
Creating Org2 Identities
+ cryptogen generate --config=./organizations/cryptogen/crypto-config-org2.yaml --output=organizations
org2.example.com
+ res=0
Creating Orderer Org Identities
+ cryptogen generate --config=./organizations/cryptogen/crypto-config-orderer.yaml --output=organizations
+ res=0
Generating CCP files for Org1 and Org2
[+] Running 8/8
 ⠿ Network fabric_test                      Created                                                                                                                           0.0s
 ⠿ Volume "compose_peer0.org1.example.com"  Created                                                                                                                           0.0s
 ⠿ Volume "compose_peer0.org2.example.com"  Created                                                                                                                           0.0s
 ⠿ Volume "compose_orderer.example.com"     Created                                                                                                                           0.0s
 ⠿ Container peer0.org2.example.com         Started                                                                                                                         143.7s
 ⠿ Container orderer.example.com            Started                                                                                                                         143.7s
 ⠿ Container peer0.org1.example.com         Started                                                                                                                         175.7s
 ⠿ Container cli                            Started                                                                                                                         164.0s
CONTAINER ID        IMAGE                                                  COMMAND                  CREATED             STATUS                      PORTS                                                                    NAMES
bfa8a2233fc1        hyperledger/fabric-tools:latest                        "/bin/bash"              2 minutes ago       Up Less than a second                                                                                cli
0913eee6eb8d        hyperledger/fabric-peer:latest                         "peer node start"        3 minutes ago       Up 48 seconds               0.0.0.0:7051->7051/tcp, 0.0.0.0:9444->9444/tcp                           peer0.org1.example.com
681c4690bd4f        hyperledger/fabric-orderer:latest                      "orderer"                3 minutes ago       Up About a minute           0.0.0.0:7050->7050/tcp, 0.0.0.0:7053->7053/tcp, 0.0.0.0:9443->9443/tcp   orderer.example.com
e958e215c64d        hyperledger/fabric-peer:latest                         "peer node start"        3 minutes ago       Up About a minute           0.0.0.0:9051->9051/tcp, 7051/tcp, 0.0.0.0:9445->9445/tcp                 peer0.org2.example.com
85ef17999799        milvusdb/milvus:v2.0.0-rc5-hotfix1-20210901-9e0b2cc    "/tini -- milvus run…"   14 minutes ago      Up 11 minutes               0.0.0.0:19530->19530/tcp                                                 milvus-standalone
664870f87586        minio/minio:RELEASE.2020-12-03T00-03-10Z               "/usr/bin/docker-ent…"   16 minutes ago      Up 12 minutes (unhealthy)   9000/tcp                                                                 milvus-minio
b4e0a3fa6394        redis                                                  "docker-entrypoint.s…"   21 hours ago        Up 21 hours                 0.0.0.0:6379->6379/tcp                                                   redis
6a9c1efe4511        quay.io/coreos/etcd:v3.5.0                             "etcd -advertise-cli…"   21 hours ago        Up 21 hours                 2379-2380/tcp                                                            milvus-etcd
1a85cef803d5        redis:latest                                           "docker-entrypoint.s…"   5 days ago          Exited (137) 21 hours ago   0.0.0.0:6379->6379/tcp                                                   vigorous_jepsen
a657006e4082        redis                                                  "docker-entrypoint.s…"   5 days ago          Exited (0) 5 days ago                                                                                distracted_jepsen
ce7709c31b4f        mongo:latest                                           "docker-entrypoint.s…"   6 days ago          Exited (0) 22 hours ago                                                                              gracious_carson
ff67c37ac26f        redis                                                  "docker-entrypoint.s…"   6 days ago          Exited (0) 5 days ago                                                                                quizzical_mcclintock
36682cbfed20        registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g   "/bin/sh -c '/home/o…"   9 days ago          Exited (137) 21 hours ago   0.0.0.0:1521->1521/tcp                                                   oracle
f1e50266b633        redis                                                  "docker-entrypoint.s…"   4 weeks ago         Exited (255) 2 weeks ago    0.0.0.0:6379->6379/tcp                                                   redis-test
b5e32ad315c2        continuumio/anaconda3                                  "/bin/bash"              3 months ago        Exited (137) 3 months ago                                                                            anaconda
```

### 测试网络的组成部分

部署测试网络后，您可能需要一些时间来检查其组件。运行以下命令以列出您机器上运行的所有 Docker 容器。您应该看到`network.sh`脚本创建的三个节点：

```
docker ps -a
```

与 Fabric 网络交互的每个节点和用户都需要属于一个组织才能参与网络。测试网络包括两个对等组织 Org1 和 Org2。它还包括一个维护网络订购服务的单一订购者组织。

[对等](https://hyperledger-fabric.readthedocs.io/en/release-2.4/peers/peers.html)点是任何 Fabric 网络的基本组件。对等点存储区块链分类帐并在交易提交到分类帐之前验证交易。Peers 运行包含用于管理区块链分类账上资产的业务逻辑的智能合约。

网络中的每个对等点都需要属于一个组织。在测试网络中，每个组织都运行一个对等点，`peer0.org1.example.com` 并且`peer0.org2.example.com`.

每个 Fabric 网络还包括一个[订购服务](https://hyperledger-fabric.readthedocs.io/en/release-2.4/orderer/ordering_service.html)。虽然对等方验证交易并将交易块添加到区块链分类帐中，但它们不会决定交易的顺序或将它们包含到新块中。在分布式网络上，对等点可能彼此远离，并且对何时创建事务没有共同的看法。就交易顺序达成共识是一个代价高昂的过程，会给对等方带来开销。

排序服务允许对等点专注于验证交易并将它们提交到分类帐。排序节点收到来自客户端的背书交易后，他们就交易的顺序达成共识，然后将它们添加到块中。然后将块分发到对等节点，这些节点将块添加到区块链分类帐中。

示例网络使用由 orderer 组织运营的单节点 Raft 排序服务。您可以看到在您的机器上运行的排序节点为`orderer.example.com`. 虽然测试网络仅使用单个节点订购服务，但生产网络将有多个订购节点，由一个或多个订购者组织运营。不同的排序节点将使用 Raft 共识算法来就整个网络的交易顺序达成一致。

## 创建频道

现在我们的机器上运行了 peer 和 orderer 节点，我们可以使用脚本为 Org1 和 Org2 之间的事务创建 Fabric 通道。通道是特定网络成员之间的私有通信层。频道只能由受邀加入频道的组织使用，并且对网络的其他成员不可见。每个通道都有一个单独的区块链分类帐。被邀请的组织将其对等节点“加入”通道以存储通道分类帐并验证通道上的交易。

您可以使用该`network.sh`脚本在 Org1 和 Org2 之间创建一个通道，并将它们的对等方加入该通道。运行以下命令以创建一个默认名称为 mychannel 的频道：

```shell
./network.sh createChannel
```

如果命令成功，您可以在日志中看到以下消息：

```shell
Using docker and docker-compose
Creating channel 'mychannel'.
If network is not up, starting nodes with CLI timeout of '5' tries and CLI delay of '3' seconds and using database 'leveldb
Using docker and docker-compose
Generating channel genesis block 'mychannel.block'
/usr/local/fabric/scripts/fabric-samples/bin/configtxgen
+ configtxgen -profile TwoOrgsApplicationGenesis -outputBlock ./channel-artifacts/mychannel.block -channelID mychannel
2022-02-23 16:28:48.632 CST 0001 INFO [common.tools.configtxgen] main -> Loading configuration
2022-02-23 16:28:48.648 CST 0002 INFO [common.tools.configtxgen.localconfig] completeInitialization -> orderer type: etcdraft
2022-02-23 16:28:48.649 CST 0003 INFO [common.tools.configtxgen.localconfig] completeInitialization -> Orderer.EtcdRaft.Options unset, setting to tick_interval:"500ms" election_tick:10 heartbeat_tick:1 max_inflight_blocks:5 snapshot_interval_size:16777216
2022-02-23 16:28:48.649 CST 0004 INFO [common.tools.configtxgen.localconfig] Load -> Loaded configuration: /usr/local/fabric/scripts/fabric-samples/test-network/configtx/configtx.yaml
2022-02-23 16:28:48.650 CST 0005 INFO [common.tools.configtxgen] doOutputBlock -> Generating genesis block
2022-02-23 16:28:48.650 CST 0006 INFO [common.tools.configtxgen] doOutputBlock -> Creating application channel genesis block
2022-02-23 16:28:48.651 CST 0007 INFO [common.tools.configtxgen] doOutputBlock -> Writing genesis block
+ res=0
Creating channel mychannel
Using organization 1
+ osnadmin channel join --channelID mychannel --config-block ./channel-artifacts/mychannel.block -o localhost:7053 --ca-file /usr/local/fabric/scripts/fabric-samples/test-network/organizations/ordererOrganizations/example.com/tlsca/tlsca.example.com-cert.pem --client-cert /usr/local/fabric/scripts/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.crt --client-key /usr/local/fabric/scripts/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.key
+ res=0
Status: 201
{
        "name": "mychannel",
        "url": "/participation/v1/channels/mychannel",
        "consensusRelation": "consenter",
        "status": "active",
        "height": 1
}

Channel 'mychannel' created
Joining org1 peer to the channel...
Using organization 1
+ peer channel join -b ./channel-artifacts/mychannel.block
+ res=0
2022-02-23 16:28:54.777 CST 0001 INFO [channelCmd] InitCmdFactory -> Endorser and orderer connections initialized
2022-02-23 16:28:54.866 CST 0002 INFO [channelCmd] executeJoin -> Successfully submitted proposal to join channel
Joining org2 peer to the channel...
Using organization 2
+ peer channel join -b ./channel-artifacts/mychannel.block
+ res=0
2022-02-23 16:28:57.929 CST 0001 INFO [channelCmd] InitCmdFactory -> Endorser and orderer connections initialized
2022-02-23 16:28:57.963 CST 0002 INFO [channelCmd] executeJoin -> Successfully submitted proposal to join channel
Setting anchor peer for org1...
Using organization 1
Fetching channel config for channel mychannel
Using organization 1
Fetching the most recent configuration block for the channel
+ peer channel fetch config config_block.pb -o orderer.example.com:7050 --ordererTLSHostnameOverride orderer.example.com -c mychannel --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/tlsca/tlsca.example.com-cert.pem
2022-02-23 08:28:58.165 UTC 0001 INFO [channelCmd] InitCmdFactory -> Endorser and orderer connections initialized
2022-02-23 08:28:58.170 UTC 0002 INFO [cli.common] readBlock -> Received block: 0
2022-02-23 08:28:58.170 UTC 0003 INFO [channelCmd] fetch -> Retrieving last config block: 0
2022-02-23 08:28:58.172 UTC 0004 INFO [cli.common] readBlock -> Received block: 0
+ configtxlator proto_decode --input config_block.pb --type common.Block --output config_block.json
Decoding config block to JSON and isolating config to Org1MSPconfig.json
+ jq '.data.data[0].payload.data.config' config_block.json
Generating anchor peer update transaction for Org1 on channel mychannel
+ jq '.channel_group.groups.Application.groups.Org1MSP.values += {"AnchorPeers":{"mod_policy": "Admins","value":{"anchor_peers": [{"host": "peer0.org1.example.com","port": 7051}]},"version": "0"}}' Org1MSPconfig.json
+ configtxlator proto_encode --input Org1MSPconfig.json --type common.Config --output original_config.pb
+ configtxlator proto_encode --input Org1MSPmodified_config.json --type common.Config --output modified_config.pb
+ configtxlator compute_update --channel_id mychannel --original original_config.pb --updated modified_config.pb --output config_update.pb
+ configtxlator proto_decode --input config_update.pb --type common.ConfigUpdate --output config_update.json
+ jq .
++ cat config_update.json
+ echo '{"payload":{"header":{"channel_header":{"channel_id":"mychannel", "type":2}},"data":{"config_update":{' '"channel_id":' '"mychannel",' '"isolated_data":' '{},' '"read_set":' '{' '"groups":' '{' '"Application":' '{' '"groups":' '{' '"Org1MSP":' '{' '"groups":' '{},' '"mod_policy":' '"",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Endorsement":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '}' '},' '"values":' '{' '"MSP":' '{' '"mod_policy":' '"",' '"value":' null, '"version":' '"0"' '}' '},' '"version":' '"0"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '},' '"write_set":' '{' '"groups":' '{' '"Application":' '{' '"groups":' '{' '"Org1MSP":' '{' '"groups":' '{},' '"mod_policy":' '"Admins",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Endorsement":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '}' '},' '"values":' '{' '"AnchorPeers":' '{' '"mod_policy":' '"Admins",' '"value":' '{' '"anchor_peers":' '[' '{' '"host":' '"peer0.org1.example.com",' '"port":' 7051 '}' ']' '},' '"version":' '"0"' '},' '"MSP":' '{' '"mod_policy":' '"",' '"value":' null, '"version":' '"0"' '}' '},' '"version":' '"1"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '}}}}'
+ configtxlator proto_encode --input config_update_in_envelope.json --type common.Envelope --output Org1MSPanchors.tx
2022-02-23 08:28:58.404 UTC 0001 INFO [channelCmd] InitCmdFactory -> Endorser and orderer connections initialized
2022-02-23 08:28:58.426 UTC 0002 INFO [channelCmd] update -> Successfully submitted channel update
Anchor peer set for org 'Org1MSP' on channel 'mychannel'
Setting anchor peer for org2...
Using organization 2
Fetching channel config for channel mychannel
Using organization 2
Fetching the most recent configuration block for the channel
+ peer channel fetch config config_block.pb -o orderer.example.com:7050 --ordererTLSHostnameOverride orderer.example.com -c mychannel --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/ordererOrganizations/example.com/tlsca/tlsca.example.com-cert.pem
2022-02-23 08:28:58.596 UTC 0001 INFO [channelCmd] InitCmdFactory -> Endorser and orderer connections initialized
2022-02-23 08:28:58.600 UTC 0002 INFO [cli.common] readBlock -> Received block: 1
2022-02-23 08:28:58.600 UTC 0003 INFO [channelCmd] fetch -> Retrieving last config block: 1
2022-02-23 08:28:58.605 UTC 0004 INFO [cli.common] readBlock -> Received block: 1
Decoding config block to JSON and isolating config to Org2MSPconfig.json
+ configtxlator proto_decode --input config_block.pb --type common.Block --output config_block.json
+ jq '.data.data[0].payload.data.config' config_block.json
Generating anchor peer update transaction for Org2 on channel mychannel
+ jq '.channel_group.groups.Application.groups.Org2MSP.values += {"AnchorPeers":{"mod_policy": "Admins","value":{"anchor_peers": [{"host": "peer0.org2.example.com","port": 9051}]},"version": "0"}}' Org2MSPconfig.json
+ configtxlator proto_encode --input Org2MSPconfig.json --type common.Config --output original_config.pb
+ configtxlator proto_encode --input Org2MSPmodified_config.json --type common.Config --output modified_config.pb
+ configtxlator compute_update --channel_id mychannel --original original_config.pb --updated modified_config.pb --output config_update.pb
+ configtxlator proto_decode --input config_update.pb --type common.ConfigUpdate --output config_update.json
+ jq .
++ cat config_update.json
+ echo '{"payload":{"header":{"channel_header":{"channel_id":"mychannel", "type":2}},"data":{"config_update":{' '"channel_id":' '"mychannel",' '"isolated_data":' '{},' '"read_set":' '{' '"groups":' '{' '"Application":' '{' '"groups":' '{' '"Org2MSP":' '{' '"groups":' '{},' '"mod_policy":' '"",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Endorsement":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '}' '},' '"values":' '{' '"MSP":' '{' '"mod_policy":' '"",' '"value":' null, '"version":' '"0"' '}' '},' '"version":' '"0"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '},' '"write_set":' '{' '"groups":' '{' '"Application":' '{' '"groups":' '{' '"Org2MSP":' '{' '"groups":' '{},' '"mod_policy":' '"Admins",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Endorsement":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '}' '},' '"values":' '{' '"AnchorPeers":' '{' '"mod_policy":' '"Admins",' '"value":' '{' '"anchor_peers":' '[' '{' '"host":' '"peer0.org2.example.com",' '"port":' 9051 '}' ']' '},' '"version":' '"0"' '},' '"MSP":' '{' '"mod_policy":' '"",' '"value":' null, '"version":' '"0"' '}' '},' '"version":' '"1"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '}}}}'
+ configtxlator proto_encode --input config_update_in_envelope.json --type common.Envelope --output Org2MSPanchors.tx
2022-02-23 08:28:58.838 UTC 0001 INFO [channelCmd] InitCmdFactory -> Endorser and orderer connections initialized
2022-02-23 08:28:58.858 UTC 0002 INFO [channelCmd] update -> Successfully submitted channel update
Anchor peer set for org 'Org2MSP' on channel 'mychannel'
Channel 'mychannel' joined

```

您还可以使用通道标志创建具有自定义名称的通道。例如，以下命令将创建一个名为 channel1 的通道：

```shell
./network.sh createChannel -c channel1
```

通道标志还允许您通过指定不同的通道名称来创建多个通道。创建`mychannel`和`channel1`之后，您可以使用以下命令创建名为 channel2 的第二个通道：

```
./network.sh createChannel -c channel2
```

**注意：**确保通道名称应用以下限制：

- 仅包含小写 ASCII 字母数字、点“.”和破折号“-”
- 少于 250 个字符
- 以字母开头

如果您想在一个步骤中启动网络并创建通道，您可以同时使用`up`和`createChannel`模式：

```
./network.sh up createChannel
```

## 在通道上启动链码

创建通道后，您可以开始使用智能合约与通道账本进行交互。智能合约包含管理区块链分类账上资产的业务逻辑。网络成员运行的应用程序可以调用智能合约在分类账上创建资产，以及更改和转移这些资产。应用程序还查询智能合约以读取分类帐上的数据。

为确保交易有效，使用智能合约创建的交易通常需要由多个组织签署才能提交到通道账本。多重签名是 Fabric 信任模型不可或缺的一部分。要求对交易进行多次背书可以防止通道上的一个组织篡改其对等方的分类帐或使用未经同意的业务逻辑。要签署交易，每个组织都需要在其对等方上调用和执行智能合约，然后对交易的输出进行签名。如果输出一致并且已经被足够多的组织签名，则交易可以提交到账本。指定通道上需要执行智能合约的集合组织的策略称为背书策略，

在 Fabric 中，智能合约以称为链码的包的形式部署在网络上。链码安装在组织的对等节点上，然后部署到通道，然后可以用于支持交易并与区块链分类帐交互。在将链码部署到通道之前，通道的成员需要就建立链码治理的链码定义达成一致。当所需数量的组织同意时，可以将链码定义提交到通道，并且可以使用链码。

使用`network.sh`创建通道后，您可以使用以下命令在通道上启动链代码：

```
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go
```

该`deployCC`子命令将安装**资产转移（基本）**链代码 `peer0.org1.example.com`，`peer0.org2.example.com`然后将链代码部署到使用通道标志指定的通道上（或者`mychannel` 如果未指定通道）。如果您是第一次部署链代码，脚本将安装链代码依赖项。您可以使用语言标志 ,`-l`来安装链代码的 Go、typescript 或 javascript 版本。`asset-transfer-basic`您可以在目录的文件夹中找到资产转移（基本）链代码`fabric-samples` 。此文件夹包含示例链代码，这些链代码作为示例提供，并被教程用于突出显示 Fabric 功能。

## 与网络交互

启动测试网络后，您可以使用`peer`CLI 与您的网络进行交互。CLI 允许您从`peer`CLI 调用已部署的智能合约、更新通道或安装和部署新的智能合约。

确保您从`test-network`目录中操作。如果您按照说明[安装示例、二进制文件和 Docker 映像](https://hyperledger-fabric.readthedocs.io/en/release-2.4/install.html)，您可以在 存储库的文件夹中找到`peer`二进制文件。使用以下命令将这些二进制文件添加到您的 CLI 路径：`bin` `fabric-samples`

```
export PATH=${PWD}/../bin:$PATH
```

您还需要设置`FABRIC_CFG_PATH`指向存储库中的`core.yaml`文件`fabric-samples`：

```
export FABRIC_CFG_PATH=$PWD/../config/
```

您现在可以设置允许您将`peer` CLI 作为 Org1 操作的环境变量：

```
# Environment variables for Org1

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

和`CORE_PEER_TLS_ROOTCERT_FILE`环境`CORE_PEER_MSPCONFIGPATH`变量指向`organizations`文件夹中的 Org1 加密材料。

如果您曾经安装和启动资产转移（基本）链代码，您可以调用(Go) 链代码的函数来将初始资产列表放在账本上（例如，如果使用 TypeScript 或 JavaScript，您将调用各个链码的功能）。`./network.sh deployCC -ccl go``InitLedger``./network.sh deployCC -ccl javascript``InitLedger`

运行以下命令以使用资产初始化分类帐。（注意 CLI 不访问 Fabric Gateway 对等体，因此必须指定每个背书对等体。）

```
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"function":"InitLedger","Args":[]}'
```

如果成功，您应该会看到类似于以下示例的输出：

```
-> INFO 001 Chaincode invoke successful. result: status:200
```

您现在可以从 CLI 查询分类帐。运行以下命令以获取已添加到您的频道分类帐的资产列表：

```
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

如果成功，您应该看到以下输出：

```
[
  {"ID": "asset1", "color": "blue", "size": 5, "owner": "Tomoko", "appraisedValue": 300},
  {"ID": "asset2", "color": "red", "size": 5, "owner": "Brad", "appraisedValue": 400},
  {"ID": "asset3", "color": "green", "size": 10, "owner": "Jin Soo", "appraisedValue": 500},
  {"ID": "asset4", "color": "yellow", "size": 10, "owner": "Max", "appraisedValue": 600},
  {"ID": "asset5", "color": "black", "size": 15, "owner": "Adriana", "appraisedValue": 700},
  {"ID": "asset6", "color": "white", "size": 15, "owner": "Michel", "appraisedValue": 800}
]
```

当网络成员想要转移或更改分类帐上的资产时，会调用链码。使用以下命令通过调用资产转移（基本）链码来更改账本上资产的所有者：

```
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"function":"TransferAsset","Args":["asset6","Christopher"]}'
```

如果命令成功，您应该会看到以下响应：

```
2019-12-04 17:38:21.048 EST [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
```

因为资产转移（基本）链码的背书策略要求交易由 Org1 和 Org2 签名，所以链码调用命令需要针对两者 `peer0.org1.example.com`并`peer0.org2.example.com`使用`--peerAddresses` 标志。由于为网络启用了 TLS，因此该命令还需要使用该`--tlsRootCertFiles`标志为每个对等方引用 TLS 证书。

调用链码后，我们可以使用另一个查询来查看调用如何更改区块链分类帐上的资产。由于我们已经查询了 Org1 节点，我们可以借此机会查询运行在 Org2 节点上的链码。设置以下环境变量以作为 Org2 运行：

```
# Environment variables for Org2

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org2MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:9051
```

您现在可以查询运行在以下位置的资产转移（基本）链代码`peer0.org2.example.com`：

```
peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset6"]}'
```

结果将显示`"asset6"`已转移到 Christopher：

```
{"ID":"asset6","color":"white","size":15,"owner":"Christopher","appraisedValue":800}
```



## 关闭网络

使用完测试网络后，可以使用以下命令关闭网络：

```
./network.sh down
```

该命令将停止并删除节点和链码容器，删除组织加密材料，并从 Docker Registry 中删除链码映像。该命令还会从以前的运行中删除通道工件和 docker 卷，以便您在遇到任何问题时再次运行。`./network.sh up`



