## 简介

Anaconda是一个用于科学计算的Python发行版，支持Linux, Mac, Windows,包含了众多流行的科学计算、数据分析的Python包。

## 配置方法

### Anaconda 配置

Anaconda 安装包可以到 http://mirrors.aliyun.com/anaconda/archive/ 下载。

Linux用户可以通过修改用户目录下的 `.condarc` 文件。

Windows 用户无法直接创建名为 `.condarc` 的文件，可先执行 `conda config --set show_channel_urls yes` 生成该文件之后再修改。

注：由于更新过快难以同步，我们不同步`pytorch-nightly`, `pytorch-nightly-cpu`, `ignite-nightly`这三个包。

```
channels:
  - defaults
show_channel_urls: true
default_channels:
  - http://mirrors.aliyun.com/anaconda/pkgs/main
  - http://mirrors.aliyun.com/anaconda/pkgs/r
  - http://mirrors.aliyun.com/anaconda/pkgs/msys2
custom_channels:
  conda-forge: http://mirrors.aliyun.com/anaconda/cloud
  msys2: http://mirrors.aliyun.com/anaconda/cloud
  bioconda: http://mirrors.aliyun.com/anaconda/cloud
  menpo: http://mirrors.aliyun.com/anaconda/cloud
  pytorch: http://mirrors.aliyun.com/anaconda/cloud
  simpleitk: http://mirrors.aliyun.com/anaconda/cloud
```

即可添加 Anaconda Python 免费仓库。

配置完成可运行 `conda clean -i` 清除索引缓存。

Miniconda 安装包可以到 http://mirrors.aliyun.com/anaconda/miniconda/ 下载。

## conda相关命令

### 升级Anaconda

```
conda update conda #基本升级
conda update anaconda #大的升级
conda update anaconda-navigator //update最新版本的anaconda-navigator
```

查看当前版本信息

```
conda info
```



## 卸载Anaconda

### windows:

由于Anaconda的安装文件都包含在一个目录中，所以直接将该目录删除即可。删除整个Anaconda目录：

计算机控制面板->程序与应用->卸载 //windows

或者

找到C:\ProgramData\Anaconda3\Uninstall-Anaconda3.exe执行卸载

### ubuntu:

rm -rf anaconda //ubuntu

最后，建议清理下.bashrc中的Anaconda路径。

#  conda环境使用基本命令

conda update -n base conda #update最新版本的conda
conda create -n xxxx python=3.5 #创建python3.5的xxxx虚拟环境

conda deactivate #关闭环境
conda env list #显示所有的虚拟环境
conda info --envs #显示所有的虚拟环境

# 查看指定包可安装版本信息命令

查看tensorflow各个版本：（查看会发现有一大堆TensorFlow源，但是不能随便选，选择可以用查找命令定位）

anaconda search -t conda tensorflow

查看指定包可安装版本信息命令:

anaconda show <USER/PACKAGE>

查看指定anaconda/tensorflow版本信息

anaconda show tensorflow

输出结果会提供一个下载地址，使用下面命令就可指定安装1.8.0版本tensorflow

conda install --channel https://conda.anaconda.org/anaconda tensorflow=1.8.0

# 6. 更新，卸载安装包

conda list #查看已经安装的文件包
conda list -n xxx #指定查看xxx虚拟环境下安装的package
conda update xxx #更新xxx文件包
conda uninstall xxx #卸载xxx文件包

# 7. 删除虚拟环境

conda remove -n xxxx --all //创建xxxx虚拟环境

# 8. 清理（conda瘦身）

conda clean就可以轻松搞定！第一步：通过conda clean -p来删除一些没用的包，这个命令会检查哪些包没有在包缓存中被硬依赖到其他地方，并删除它们。第二步：通过conda clean -t可以将删除conda保存下来的tar包。

conda clean -p //删除没有用的包
conda clean -t //删除tar包
conda clean -y --all //删除所有的安装包及cache

# 9. 复制/重命名/删除env环境

Conda是没有重命名环境的功能的, 要实现这个基本需求, 只能通过愚蠢的克隆-删除的过程。
切记不要直接mv移动环境的文件夹来重命名, 会导致一系列无法想象的错误的发生!

//克隆oldname环境为newname环境
conda create --name newname --clone oldname
//彻底删除旧环境
conda remove --name oldname --all

### 注意：必须在base环境下进行以上操作，否则会出现各种莫名的问题。

# 10. conda自动开启/关闭激活

conda activate #默认激活base环境
conda activate xxx #激活xxx环境
conda deactivate #关闭当前环境
conda config --set auto_activate_base false #关闭自动激活状态
conda config --set auto_activate_base true #关闭自动激活状态

## 11. Conda 安装本地包

有时conda或pip源下载速度太慢，install a过程中会中断连接导致压缩包下载不全，
此时，我们可以用浏览器等工具先下载指定包再用conda或pip进行本地安装

\#pip 安装本地包

#### pip install ～/Downloads/a.whl

\#conda 安装本地包

#### conda install --use-local ~/Downloads/a.tar.bz2

## 11. 解决conda/pip install 下载速度慢

### conda数据源管理

```python
#显示目前conda的数据源有哪些
conda config --show channels

# ⚠️ 会清空现有 channels（确认后再用）
conda config --remove-key channels   

#添加数据源
conda config --add channels defaults
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/win-64
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/win-64
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/win-64
conda config --set show_channel_urls yes

#删除数据源
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
```

### 各大镜像

### 清华conda镜像

注：由于更新过快难以同步，我们不同步pytorch-nightly,pytorch-nightly-cpu,ignite-nightly这三个包。

```python
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --set show_channel_urls yes
```


完整配置：

```
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  deepmodeling: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/
```



```python
北外conda镜像

conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/
#Conda Forge
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/conda-forge/
#msys2（可略）
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/msys2/
#bioconda（可略）
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/bioconda/
#menpo（可略）
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/menpo/
#pytorch
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/pytorch/

for legacy win-64（可略）
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/peterjc123/
conda config --set show_channel_urls yes
```

```
中科大conda镜像
由于合规性，Anaconda 源目前已经无限期停止服务。
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/msys2/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/menpo/
conda config --set show_channel_urls yes
```

#获取版本号
conda --version 或 conda -V

#检查更新当前conda
conda update conda

#查看当前存在哪些虚拟环境
conda env list 或 conda info -e

#Create env
#Create env with python 3.7 and pip
conda create --name whatwhale python=3.7 pip
#Activate env
#Activate by name

conda activate whatwhale
#Deactivate env
conda deactivate
#Removing an environment
#Remove environment by name

# remove env
#conda env remove --name whatwhale
# verify
conda env list

#查看--安装--更新--删除包

conda list：
conda search package_name# 查询包
conda install package_name
conda install package_name=1.5.0
conda update package_name
conda remove package_name
阿里conda镜像
channels:
  - defaults
show_channel_urls: true
default_channels:
  - http://mirrors.aliyun.com/anaconda/pkgs/main
  - http://mirrors.aliyun.com/anaconda/pkgs/r
  - http://mirrors.aliyun.com/anaconda/pkgs/msys2
    custom_channels:
    conda-forge: http://mirrors.aliyun.com/anaconda/cloud
    msys2: http://mirrors.aliyun.com/anaconda/cloud
    bioconda: http://mirrors.aliyun.com/anaconda/cloud
    menpo: http://mirrors.aliyun.com/anaconda/cloud
    pytorch: http://mirrors.aliyun.com/anaconda/cloud
    simpleitk: http://mirrors.aliyun.com/anaconda/cloud

 

## pip数据源管理

\#显示目前pip的数据源有哪些
pip config list
pip config list --[user|global] # 列出用户|全局的设置
pip config get global.index-url # 得到这key对应的value 如：https://mirrors.aliyun.com/pypi/simple/

\# 添加
pip config set key value
\#添加数据源：例如, 添加USTC中科大的源：
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
\#添加全局使用该数据源
pip config set global.trusted-host https://mirrors.ustc.edu.cn/pypi/web/simple

\# 删除
pip config unset key
\# 例如
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

\#搜索
pip search flask #搜素flask安装包

\# 升级pip
pip install pip -U

 

### 记录一下pip国内源

阿里云 http://mirrors.aliyun.com/pypi/simple/
中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
豆瓣(douban) http://pypi.douban.com/simple/
清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/

## pip安装包管理

工具：anaconda prompt

`conda activate tongue 可以切换环境`

pip list #列出当前缓存的包
pip purge #清除缓存
pip remove #删除对应的缓存
pip help #帮助
pip install xxx #安装xxx包
pip uninstall xxx #删除xxx包
pip show xxx #展示指定的已安装的xxx包
pip check xxx #检查xxx包的依赖是否合适

 

# pip和conda批量导出、安装组件(requirements.txt)

pip批量导出包含环境中所有组件的requirements.txt文件

pip freeze > requirements.txt

pip批量安装requirements.txt文件中包含的组件依赖

pip install -r requirements.txt

[conda](https://so.csdn.net/so/search?q=conda)批量导出包含环境中所有组件的requirements.txt文件

conda list -e > requirements.txt

conda批量安装requirements.txt文件中包含的组件依赖

conda install --yes --file requirements.txt

