# 部署fabric网络教程

## 一、生成网络配置

```
cryptogen generate --config ./crypto-config-orderer.yaml
cryptogen generate --config ./crypto-config-org1.yaml
cryptogen generate --config ./crypto-config-org2.yaml
```

创世区块的配置和生成

```
configtxgen -profile TwoOrgsGenesis -channelID ChannelDefaults -outputBlock orderer.genesis.block

```

## 二、配置和操作 Raft 排序服务

## 2.1 概念概述

有关排序概念的高级概述以及受支持的排序服务实现（包括 Raft）如何在高级别的工作，请查看我们关于[排序服务](https://hyperledger-fabric.readthedocs.io/en/release-2.4/orderer/ordering_service.html)的概念文档。

要了解设置排序节点的过程，请查看我们关于[排序服务规划的](https://hyperledger-fabric.readthedocs.io/en/release-2.4/deployorderer/ordererplan.html)文档。

## 2.2 配置

一个 Raft 集群配置在两个地方：

- **本地配置**：管理节点特定方面，例如 TLS 通信、复制行为和文件存储。
- **通道配置**：定义相应通道的 Raft 集群的成员资格，以及协议特定的参数，如心跳频率、领导者超时等。

Raft 节点使用 TLS pinning 相互识别，因此为了冒充 Raft 节点，攻击者需要获取其 TLS 证书的私钥。因此，如果没有有效的 TLS 配置，就无法运行 Raft 节点。

回想一下，每个通道都有自己运行的 Raft 协议实例。因此，必须在其所属的每个通道的配置中引用 Raft 节点，方法是将其服务器和客户端 TLS 证书（`PEM`格式）添加到通道配置中。这确保了当其他节点收到来自它的消息时，它们可以安全地确认发送消息的节点的身份。

以下部分`configtx.yaml`显示了通道中的三个 Raft 节点（也称为“consenters”）：

```
       Consenters:
            - Host: raft0.example.com
              Port: 7050
              ClientTLSCert: path/to/ClientTLSCert0
              ServerTLSCert: path/to/ServerTLSCert0
            - Host: raft1.example.com
              Port: 7050
              ClientTLSCert: path/to/ClientTLSCert1
              ServerTLSCert: path/to/ServerTLSCert1
            - Host: raft2.example.com
              Port: 7050
              ClientTLSCert: path/to/ClientTLSCert2
              ServerTLSCert: path/to/ServerTLSCert2
```

创建通道配置块时，该`configtxgen`工具会读取 TLS 证书的路径，并将路径替换为证书的相应字节。

注意：可以在不影响其他节点的情况下动态地从通道中删除和添加排序节点，该过程在下面的重新配置部分中描述。



### 2.2.1 本地配置

`orderer.yaml`有两个与 Raft 订购者相关的配置部分：

**Cluster**，它决定了 TLS 通信配置。和 **共识**，它决定了预写日志和快照的存储位置。

**集群参数：**

默认情况下，Raft 服务与面向客户端的服务器（用于发送事务或拉取块）在同一 gRPC 服务器上运行，但可以将其配置为具有单独的 gRPC 服务器和单独的端口。

这对于您希望由组织 CA 颁发的 TLS 证书但仅由集群节点用于相互通信以及由公共 TLS CA 为面向客户端的 API 颁发的 TLS 证书的情况很有用。

- `ClientCertificate`, `ClientPrivateKey`: 客户端 TLS 证书和对应私钥的文件路径。
- `ListenPort`: 集群监听的端口。它必须与`consenters[i].Port`Channel 配置中的相同。如果为空，则端口与订购者通用端口相同（`general.listenPort`）
- `ListenAddress`：集群服务正在监听的地址。
- `ServerCertificate`, `ServerPrivateKey`: TLS 服务器证书密钥对，当集群服务在单独的 gRPC 服务器（不同端口）上运行时使用。

注意：`ListenPort`, `ListenAddress`, `ServerCertificate`,`ServerPrivateKey`必须同时设置或取消设置。如果它们未设置，它们会从通用 TLS 部分继承，例如. 禁用通用 TLS 时：`general.tls.{privateKey, certificate}`

- 使用`ListenPort`与订购者通用端口不同的端口
- 在通道配置中正确配置 TLS 根 CA。

还有一些隐藏的配置参数`general.cluster`可用于进一步微调集群通信或复制机制：

- `SendBufferSize`：调节出口缓冲区中的消息数量。
- `DialTimeout`, `RPCTimeout`: 指定创建连接和建立流的超时时间。
- `ReplicationBufferSize`：可以为每个用于从其他集群节点复制块的内存缓冲区分配的最大字节数。每个通道都有自己的内存缓冲区。默认`20971520`为`20MB`.
- `PullTimeout`：排序节点在中止之前等待接收块的最长时间。默认为五秒。
- `ReplicationRetryTimeout`：排序节点将在两次连续尝试之间等待的最长时间。默认为五秒。
- `ReplicationBackgroundRefreshInterval`: 两次连续尝试复制此节点添加到的现有通道之间的时间，或此节点过去无法复制的通道之间的时间。默认为五分钟。
- `TLSHandshakeTimeShift`：如果排序节点的 TLS 证书过期并且没有及时更换（参见下面的 TLS 证书轮换），它们之间的通信将无法建立，并且无法向排序服务发送新的交易。为了从这种情况中恢复，可以使排序节点之间的 TLS 握手考虑将时间向后移动一个给定的数量，该数量配置为`TLSHandshakeTimeShift`. 此设置仅在使用单独的集群侦听器时适用。如果集群服务共享 orderer 的主 gRPC 服务器，则改为`TLSHandshakeTimeShift`在`General.TLS`部分中指定。

**共识参数：**

- `WALDir`：预写日志的`etcd/raft`存储位置。每个频道都有自己的以频道 ID 命名的子目录。
- `SnapDir`：指定`etcd/raft`存储快照的位置。每个频道都有自己的以频道 ID 命名的子目录。

还有两个隐藏的配置参数可以通过将它们添加到共识部分来设置`orderer.yaml`：

- `EvictionSuspicion`：通道驱逐怀疑的累积时间段，触发节点从其他节点拉块并查看它是否已被驱逐出通道以确认其怀疑。如果怀疑得到确认（检查的块不包含节点的 TLS 证书），则节点会停止对该通道的操作。A node suspects its channel eviction when it doesn't know about any elected leader nor can be elected as leader in the channel. 默认为 10 分钟。
- `TickIntervalOverride`：如果设置，此值将优先于在此排序节点是同意者的所有通道中配置的滴答间隔。设置此值时应非常小心，因为排序器之间的滴答间隔不匹配可能会导致一个或多个通道的仲裁丢失。



### 2.2.2 通道配置

除了（已经讨论过的）同意者之外，Raft 通道配置还有一个`Options`与协议特定的旋钮相关的部分。当前无法在节点运行时动态更改这些值。该节点必须重新配置并重新启动。

唯一的例外是`SnapshotIntervalSize`，它可以在运行时进行调整。

注意：建议避免更改以下值，因为错误配置可能导致根本无法选举领导者的状态（即，如果 `TickInterval`和`ElectionTick`非常低）。无法选举领导者的情况是不可能解决的，因为领导者需要做出改变。由于存在此类危险，我们建议不要在大多数用例中调整这些参数。

- `TickInterval`  Node.Tick：两次调用之间的时间间隔。
- `ElectionTick`：`Node.Tick`两次选举之间必须通过的调用次数。也就是说，如果一个follower在`ElectionTick`过去之前没有收到当前任期leader的任何消息，它将成为候选人并开始选举。
- `ElectionTick`必须大于`HeartbeatTick`。
- `HeartbeatTick`：`Node.Tick`心跳之间必须通过的调用次数。也就是说，领导者会发送心跳消息以保持其领导地位`HeartbeatTick`。
- `MaxInflightBlocks`：限制乐观复制阶段的最大动态追加块数。
- `SnapshotIntervalSize`：定义拍摄快照的字节数。



## 2.3重新配置

Raft orderer 支持动态（即，在为通道提供服务时）添加和删除节点，只要一次只添加或删除一个节点。请注意，在您尝试重新配置之前，您的集群必须是可操作的并且能够达成共识。例如，如果您有三个节点，而两个节点发生故障，您将无法重新配置集群以删除这些节点。同样，如果在具有三个节点的通道中有一个故障节点，则不应尝试轮换证书，因为这会引发第二个故障。作为一条规则，你不应该尝试对 Raft 同意者进行任何配置更改，例如添加或删除同意者，或者轮换同意者的证书，除非所有同意者都在线且健康。

如果您决定更改这些参数，建议仅在维护周期内尝试进行此类更改。当一个节点关闭时在只有几个节点的集群中尝试配置时，最有可能出现问题。例如，如果您的同意者集中有三个节点并且其中一个已关闭，则意味着您有三分之二的节点处于活动状态。如果在此状态下将集群扩展到四个节点，则四个节点中只有两个处于活动状态，这不是仲裁。第四个节点将无法加入，因为节点只能加入正常运行的集群（除非集群的总大小为一或两个）。

因此，通过将一个由三个节点组成的集群扩展到四个节点（而只有两个节点还活着），您实际上会被卡住，直到原始离线节点复活。

将新节点添加到排序服务：

1. **确保拥有新节点的 orderer 组织是通道上的 orderer 组织之一**。如果 orderer 组织不是管理员，则该节点将无法作为跟随者拉块或加入同意者集。
2. **启动新的排序节点**。有关如何部署排序节点的信息，请查看[排序服务的规划](https://hyperledger-fabric.readthedocs.io/en/release-2.4/deployorderer/ordererdeploy.html)。请注意，当您使用`osnadmin`CLI 创建和加入频道时，您无需在启动节点时指向配置块。
3. **使用`osnadmin`CLI 将第一个排序者添加到通道**。有关更多信息，请查看[创建频道](https://hyperledger-fabric.readthedocs.io/en/release-2.4/create_channel/create_channel_participation.html#step-two-use-the-osnadmin-cli-to-add-the-first-orderer-to-the-channel)教程。
4. **等待 Raft 节点**从现有节点复制其证书已添加到的所有通道的块。当一个排序节点被添加到一个通道时，它被添加为一个“跟随者”，在这种状态下它可以复制块，但不属于积极服务于通道的“同意者集”的一部分。当节点完成复制块时，它的状态应该从“onboarding”变为“active”。请注意，“活动”排序节点仍然不是同意者集的一部分。
5. **将新的排序节点添加到同意集**。有关更多信息，请查看[创建频道](https://hyperledger-fabric.readthedocs.io/en/release-2.4/create_channel/create_channel_participation.html#step-three-join-additional-ordering-nodes)教程。

可以在节点本身运行时将已经运行（并且已经参与某些通道）的节点添加到通道。为此，只需将节点的证书添加到通道的通道配置中。节点会自主检测自己加入新通道（这里默认为五分钟，但如果希望节点更快检测到新通道，请重启节点），并将从通道中的 orderer 中拉取通道块，然后启动该链的 Raft 实例。

成功完成后，可以更新通道配置以包含新 Raft orderer 的端点。

要从通道的同意者集中删除排序节点，请使用命令从通道中删除其端点和证书。有关更多信息，请查看[从现有渠道添加或删除订购者](https://hyperledger-fabric.readthedocs.io/en/release-2.4/create_channel/create_channel_participation.html#add-or-remove-orderers-from-existing-channels)。`osnadmin channel remove`

一旦从通道中删除了一个排序节点，其他排序节点将停止在已删除通道的上下文中与已删除的排序节点通信。他们可能仍在其他渠道上进行交流。

从通道中删除的节点会立即或在`EvictionSuspicion`时间过去（默认为 10 分钟）后自动检测其删除，并关闭该通道上的 Raft 实例。

如果打算完全删除节点，请在关闭节点之前将其从所有通道中删除。



### 2.3.1 排序节点的 TLS 证书轮换

所有 TLS 证书都有一个由颁发者确定的到期日期。这些到期日期的范围从发行之日起 10 年到短短几个月，因此请咨询您的发行人。在到期日期之前，您需要在节点本身和节点加入的每个通道上轮换这些证书。

**注意：**如果 TLS 证书的公钥保持不变，则无需发布通道配置更新。

对于节点参与的每个通道：

1. 使用新证书更新通道配置。
2. 在节点的文件系统中替换其证书。
3. 重启节点。

因为一个节点只能有一个 TLS 证书密钥对，节点将无法在更新过程中为其未添加新证书的通道提供服务，从而降低容错能力。因此， **证书轮换过程一旦开始，就应该尽快完成。**

如果由于某种原因 TLS 证书的轮换已开始但无法在所有通道中完成，建议将 TLS 证书轮换回原来的状态并稍后尝试轮换。



### 2.3.2 证书到期相关认证

每当具有过期日期的身份（例如基于 x509 证书的身份）的客户端向 orderer 发送交易时，orderer 都会检查其身份是否已过期，如果是，则拒绝交易提交。

`General.Authentication.NoExpirationChecks`但是，可以通过启用`orderer.yaml`.

这应该仅在管理员证书已过期的极端情况下进行，因此无法发送配置更新以用更新的证书替换管理员证书，因为现有管理员签署的配置事务现在是因为过期而被拒绝。更新频道后，建议改回默认配置，强制对身份进行过期检查。



### 2.3.3 指标

有关操作服务的描述以及如何设置它，请查看 [我们关于操作服务的文档](https://hyperledger-fabric.readthedocs.io/en/release-2.4/operations_service.html)。

有关操作服务收集的指标列表，请查看我们[关于指标的参考材料](https://hyperledger-fabric.readthedocs.io/en/release-2.4/metrics_reference.html)。

虽然您优先考虑的指标与您的特定用例和配置有很大关系，但您可能需要特别监控两个指标：

- `consensus_etcdraft_is_leader`：标识集群中的哪个节点当前是领导者。如果没有节点有这个集合，你就失去了仲裁。
- `consensus_etcdraft_data_persist_duration`: 表示对 Raft 集群的持久预写日志的写入操作需要多长时间。为了协议安全，消息必须持久保存，并`fsync`在适当的情况下调用，然后才能与同意者集共享。如果该值开始攀升，则该节点可能无法参与共识（这可能导致该节点甚至网络的服务中断）。
- `consensus_etcdraft_cluster_size`和`consensus_etcdraft_active_nodes`：这些通道指标有助于跟踪“活动”节点（听起来，与集群中的节点总数相比，这些节点是当前对集群做出贡献的节点）。如果活动节点的数量低于集群中的大多数节点，则仲裁将丢失，并且排序服务将停止处理通道上的块。

## 三、Fabric-CA介绍

3.1搭建fabric-ca过程：

fabric-ca包括两个应用程序，一个是fabric-ca-client, 一个是fabric-ca-server。我们这里使用docker镜像，编译好后看镜像hyperledger/fabric-ca

```
docker image ls|grep fabric-ca
```

镜像里面同时包含fabric-ca-client和fabric-ca-server程序

## 1. 启动fabric-ca-server

在hyperledger/fabric-ca镜像中启动fabric-ca-server程序。使用以下yaml文件，通过docker-compose启动，注意的是FABRIC_CA_SERVER_CSR_HOSTS变量，需要设置为实际运行fabric-ca-server的主机名

```
$ cat tls-server-compose.yaml

version: "3.9"
services:
  ca-tls:
    container_name: ca-tls
    image: hyperledger/fabric-ca
    command: sh -c 'fabric-ca-server start -d -b ca-tls-admin:ca-tls-adminpw --port 7052'
    environment:
      # CA Server的工作路径
      - FABRIC_CA_SERVER_HOME=/tmp/tls
      # 启动fabric-ca-server和fabric-ca-client之间的tls通讯
      - FABRIC_CA_SERVER_TLS_ENABLED=true
      # 证书中的CN字段
      - FABRIC_CA_SERVER_CSR_CN=ca-tls
      # 证书适用范围
      - FABRIC_CA_SERVER_CSR_HOSTS=localhost
      - FABRIC_CA_SERVER_DEBUG=true
    volumes:
      - ca-tls:/tmp/tls
    ports:
      - 7052:7052

volumes:
   ca-tls:
```

运行fabric-ca-server

```
docker-compose -f tls-server-compose.yaml up -
```

第一次启动server后，在FABRIC_CA_SERVER_HOME下面有server的配置文件：fabric-ca-server-config.yaml。

我们可根据实际需要修改即可，本例中相关的修改如下：

```
csr:
   names:
      - C: CN
        ST: "Cheng Du"
        L:
        O: MHTech
        OU:

# 开启这个功能，允许fabric-ca-sever删除已经注册的用户，一般在开发环境中使用
cfg:
  identities:
    allowremove: true
```

修改后，把FABRIC_CA_SERVER_HOME目录下除fabric-ca-server-config.yaml的所有文件都删掉，重新启动server。

启动后，我们可以看到FABRIC_CA_SERVER_HOME目录下有以下文件:

```
# ls -1

IssuerPublicKey
IssuerRevocationPublicKey
ca-cert.pem
fabric-ca-server-config.yaml
fabric-ca-server.db
msp
tls-cert.pem
```

我们只需要关注几个文件：

- ca-cert.pem。是自签名的根证书文件，本ca的根证书 ，就是它，fabric-ca-server启动时生成
- tls-cert.pem。由ca-cert.pem签发的证书，是fabric-ca-server的tls通讯证书，当fabric-ca-client向fabirc-ca-server发起tls通讯请求时，fabric-ca-server就展示tls-cert.pem证书，fabric-ca-client接下来验证该证书的有效性即可（fabric-ca-client持有ca-cert.pem根证书即可验证）

我们看看证书的内容是否符合预期，尤其关注下我们自己修改的那部分

```
$ keytool -printcert -file ca-cert.pem

Owner: CN=ca-tls, O=MHTech, ST=Cheng Du, C=CN
Issuer: CN=ca-tls, O=MHTech, ST=Cheng Du, C=CN
Serial number: 60bfcf507e7a22ab875415593e0b47132acf8ef5
Valid from: Mon Oct 04 16:02:00 CST 2021 until: Tue Sep 30 16:02:00 CST 2036
Certificate fingerprints:
     MD5:  F9:21:E0:81:8C:DB:4C:55:7D:D3:C5:68:81:17:16:6A
     SHA1: 0C:0D:E3:C8:86:03:92:8A:0D:95:9B:3A:EF:46:08:29:7C:68:2E:0E
     SHA256: B8:2F:B6:10:7C:D0:0D:1D:9A:1A:1B:D1:84:32:50:F7:EE:9E:CD:7A:41:92:AB:51:12:3B:15:E4:36:A0:63:40
Signature algorithm name: SHA256withECDSA
Subject Public Key Algorithm: 256-bit EC key
Version: 3

Extensions:

#1: ObjectId: 2.5.29.19 Criticality=true
BasicConstraints:[
  CA:true
  PathLen:1
]

#2: ObjectId: 2.5.29.15 Criticality=true
KeyUsage [
  Key_CertSign
  Crl_Sign
]

#3: ObjectId: 2.5.29.17 Criticality=false
SubjectAlternativeName [
  IPAddress: 0.0.0.0
]

#4: ObjectId: 2.5.29.14 Criticality=false
SubjectKeyIdentifier [
KeyIdentifier [
0000: D4 9E B9 03 A1 4E 70 49   01 24 94 28 9B A7 F7 D0  .....NpI.$.(....
0010: 5E 17 FE 9C                                        ^...
]
]
```

## 2. 颁发admin证书

申请证书由fabric-ca-client发起。

> fabric-ca-client也可以由镜像启动，但在实际过程中，由于需要频繁操作fabric-ca-client。本文中直接使用二进制方式启动。

证书的申请过程一共经过两个步骤：register和enroll

```
fabric-ca-client register ...
fabric-ca-client enroll ...
```

- register是登记注册用户的过程
- enroll是实际颁发用户证书的过程

但并不是任何人都可以发起register和enroll命令的，必须得是admin账户。

在启动server的时候，我们注意到命令为：

```
fabric-ca-server start -d -b admin-ca-orgA:admin-ca-orgApw --port 7152
```

其中-b参数指定了初始的admin账户。即server启动的时候，已经通过命令行register了初始admin账户：用户名为admin-ca-orgA，密码为admin-ca-orgApw。

我们接下来得获得admin的实际证书，即enroll过程

### 2.1 设置FABRIC_CA_CLIENT_HOME路径

在使用fabric-ca-client之前，得先设置FABRIC_CA_CLIENT_HOME变量，用于指定fabric-ca-client的工作路径。

```
export FABRIC_CA_CLIENT_HOME=$PWD
```

### 2.2 准备tls通讯证书

之前提到server和client之前开启了tls通讯，server的证书文件是tls-cert.pem。当client发起tls通讯的时候，需要认证server所提供的tls-cert.pem证书的有效性。这就要求client端拥有ca的根证书ca-cert.pem

把fabric-ca-server中FABRIC_CA_SERVER_HOME目录下的ca-cert.pem拷贝到fabic-ca-client端指定目录下，如果是想从server的docker镜像中拷贝出来，则使用

```
docker cp <server path> <client path>
```

### 2.3 获取admin的证书

创建tls-admin目录，发起enroll动作

```
./fabric-ca-client enroll -d -u https://admin-ca-orgA:admin-ca-orgApw@127.0.0.1:7152 --tls.certfiles ./admin-ca/orgA/root-orgA.crt  --mspdir  ./admin-ca/orgA/msp
```

- tls.certfiles指定了从server端获取的ca-cert.pem，在本地重命名为root-orgA.crt
- mspdir指定即将获取的证书保存路径

查看client端证书保存目录，注意新生成的admin证书。其中的keystore目录，保存着证书私钥。signcerts目录，保存着证书文件

```
orgA
├── msp
│   ├── IssuerPublicKey
│   ├── IssuerRevocationPublicKey
│   ├── cacerts
│   │   └── 127-0-0-1-7152.pem
│   ├── keystore
│   │   └── ea095793e88af32fee9c0e7d3e2b11387933abbb44c66b97ce6e9414ed1c7d10_sk
│   ├── signcerts
│   │   └── cert.pem
│   └── user
└── root-orgA.crt
```

查看下证书内容，可能有些内容并不符合你需要，修改FABRIC_CA_CLIENT_HOME目录下的fabric-ca-client-config.yaml文件，添加一下内容，注意其中hosts尤其关键，该字段描述生成的证书能在哪些机器使用，具体就不展开讲了，感兴趣的同学可以自行搜索x509的SubjectAlternativeName字段含义

```
tls:
  certfiles: ./tls-root-cert.pem

csr:
  names:
    - C: CN
      ST: Cheng Du
      L:
      O: MHTech
      OU:
  hosts:
    - localhost
```

如果修改了fabric-ca-client-config.yaml文件，需要重新执行enroll, 获取证书

```
./fabric-ca-client enroll -d -u https://admin-ca-orgA:admin-ca-orgApw@127.0.0.1:7152 --tls.certfiles ./admin-ca/orgA/root-orgA.crt  --mspdir  ./admin-ca/orgA/msp
```

检查下最终生成的证书

```
$ keytool -printcert -file cert.pem

Owner: CN=ca-tls-admin, OU=client, O=MHTech, ST=Cheng Du, C=CN
Issuer: CN=ca-tls, O=MHTech, ST=Cheng Du, C=CN
Serial number: 349def492795485465b1144db4fbede63173521
Valid from: Mon Oct 04 16:55:00 CST 2021 until: Tue Oct 04 17:24:00 CST 2022
Certificate fingerprints:
     MD5:  47:62:B5:CF:A1:B3:4F:4F:33:10:F7:82:A3:2A:CE:71
     SHA1: 66:FE:30:8F:D5:08:58:CC:CC:F5:30:4A:81:CF:FA:4E:4D:5D:F5:81
     SHA256: 15:8F:1A:F7:6F:F4:C1:F7:47:DD:BF:44:0B:89:E7:56:24:04:04:98:B9:EA:66:19:7A:B0:CF:6F:F2:A1:CB:96
Signature algorithm name: SHA256withECDSA
Subject Public Key Algorithm: 256-bit EC key
Version: 3

Extensions:

#1: ObjectId: 2.5.29.35 Criticality=false
AuthorityKeyIdentifier [
KeyIdentifier [
0000: D7 6D 43 EC 23 28 88 41   10 44 43 24 94 C2 EB 83  .mC.#(.A.DC$....
0010: F3 95 CA F1                                        ....
]
]

#2: ObjectId: 2.5.29.19 Criticality=true
BasicConstraints:[
  CA:false
  PathLen: undefined
]

#3: ObjectId: 2.5.29.15 Criticality=true
KeyUsage [
  DigitalSignature
]

#4: ObjectId: 2.5.29.17 Criticality=false
SubjectAlternativeName [
  DNSName: localhost
]

#5: ObjectId: 2.5.29.14 Criticality=false
SubjectKeyIdentifier [
KeyIdentifier [
0000: 8E DF ED 55 F9 57 80 2B   8F 7C 0B F7 4F 6A 22 59  ...U.W.+....Oj"Y
0010: 58 96 97 9A                                        X...
]
]
```

## 3. 颁发orderer, peer, user证书

admin证书到手，那我们就可以通过admin颁发证书了。在fabric环境中，orderer, peer和user都需要颁发证书，操作过程都是一样的

我们通过admin颁发一个orderer证书为例:

```
./fabric-ca-client register -d --id.name orderer1-orgA --id.secret orderer1-orgAPW --id.type orderer -u https://127.0.0.1:7152 --tls.certfiles ./admin-ca/orgA/root-orgA.crt  --mspdir  ./admin-ca/orgA/msp

./fabric-ca-client enroll -d -u https://orderer1-orgA:orderer1-orgAPW@127.0.0.1:7152 --tls.certfiles ./admin-ca/orgA/root-orgA.crt  --mspdir  ./tmp
```

## 小结

要正确使用fabirc-ca， 需要对证书格式，CA的工作原理有所了解。本文篇幅有限，不可能面面俱到，建议大家先去了解PKI的相关背景知识，尤其是证书的工作原理，再来操作fabric-ca, 则会顺利很多

