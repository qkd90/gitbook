## 安装miniconda3



### 下载miniconda

清华镜像源下载类似：Miniconda3-py312_26.7.1-1-Linux-x86_64.sh

### 安装



配置环境变量：

```
source /mnt/datadisk0/miniconda3/bin/activate
```

检查：

```
conda --version
```

接着初始化 bash：

```
conda init bash
source ~/.bashrc
```

以后重新登录服务器就可以直接：

```
conda
```

如果你**不知道 Miniconda 到底安装在哪**，直接执行：

```
find / -type f -name conda 2>/dev/null | head -20
```

可能会返回：

```
/data/miniconda3/bin/conda
```

### 配置miniconda项目环境

**最适合项目隔离的方式**就是直接把 Conda 环境创建到项目目录下面，而不是统一放到 `~/miniconda3/envs/`。

假设你的项目目录是：

```
/data/icanfm
```

我建议这样配置：

```
cd /mnt/datadisk0/icanFM

# 创建项目专属环境目录
conda create -p /mnt/datadisk0/icanFM/.conda python=3.10 -y
```

创建完成后激活：

```
conda activate /mnt/datadisk0/icanFM/.conda
```

Conda 使用了 Anaconda 官方源，但还没有接受它的 Terms of Service。

最直接的解决方式就是按提示接受：

```
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

然后重新执行：

```
conda create -p /mnt/datadisk0/icanFM/.conda python=3.10 -y
```

创建完成后激活：

```
conda activate /mnt/datadisk0/icanFM/.conda
```

然后检查：

```
which python
python --version
```

之后你的目录大概会变成：

```
/mnt/datadisk0/icanFM/
├── .conda/          # Python/conda 环境
│   ├── bin/
│   ├── lib/
│   └── ...
├── requirements.txt
├── train.py
├── src/
└── ...
```

配置本地pycharm使用该服务器的python环境

```
/mnt/datadisk0/icanFM/.conda/bin/python3.10
```

安装项目依赖：

```
pip install -r requirements.txt
```

检查是否确实用了这个项目环境：

```
which python
```

正常应该输出：

```
/data/icanfm/.conda/bin/python
```

再检查：

```
python --version
pip --version
```

删除刚才创建环境：

```
rm -rf /mnt/datadisk0/icanFM/.conda
```

创建3.12环境

```
conda create -p /mnt/datadisk0/icanFM/.conda python=3.10 -y
conda activate /mnt/datadisk0/icanFM/.conda
```

