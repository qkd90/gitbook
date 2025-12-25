## 先确认环境是否已经创建

在 **Anaconda Prompt**（推荐）或 **PowerShell** 打开后，执行：

```
conda env list
```

你会看到类似：

```
# conda environments:
#
base                  *  C:\Users\...\anaconda3
CGMformer                 C:\Users\...\anaconda3\envs\CGMformer
```

如果列表里 **有 `CGMformer`**，直接看下一步。
 如果 **没有**，先创建：

```
conda create -n CGMformer python=3.10 -y
```

## 切换到项目环境（关键一步）

```
conda activate CGMformer
```

切换成功后，命令行前面会变成：

```
(CGMformer) C:\Users\...
```

👉 这一步必须成功，否则你后面装包/跑脚本都在别的环境里。

------

## 在项目环境里执行你的命令

### 1️⃣ 升级 pip（建议）

```
python -m pip install -U pip setuptools wheel
```

### 2️⃣ 安装 PyTorch（CPU 版）

```
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
```

### 3️⃣ 安装项目依赖

```
cd D:\gitcode\CGMformer   # 切到你项目目录
pip install -r requirements.txt
```



## pycharm开发

安装包直接使用终端即可



pycharm终端命令：

安装依赖

```
pip install -r requirements.txt

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --proxy http://127.0.0.1:7890 --trusted-host pypi.tuna.tsinghua.edu.cn
```



## 下载安装最新版 Miniconda（官方 & 干净）

### 去官方页面（推荐）

👉 https://docs.conda.io/en/latest/miniconda.html

选择 **最新版**：

- **Windows**
- **Python 3.10**（⚠️ 强烈推荐 AI 项目用 3.10）
- 文件名类似：

```
Miniconda3-py310_24.x.x-Windows-x86_64.exe
```

> 不建议 3.12（很多 AI 依赖还没完全适配）

------

### 安装时的关键选项（非常重要）

双击安装 → 一路到选项页时：

✅ 勾选：

- ✔ **Add Miniconda3 to my PATH environment variable**
- ✔ **Register Miniconda3 as my default Python**

> 官方提示“不推荐加 PATH”，但**对 PyCharm / 终端 / AI 开发来说反而更省事**
>  （我们后面用 venv / conda env，不会污染）

------

### 安装完成后验证

打开 **PowerShell**（新窗口）：

```
conda --version
python --version
```

你应该看到类似：

```
conda 24.x.x
Python 3.10.x
```

------

## Miniconda 基础配置

### 初始化 conda（如果还没生效）

```
conda init powershell
```

然后 **关闭 PowerShell，重新打开**

------

### 清华镜像（如果你在国内）

```python
#清理所有镜像
conda config --remove-key channels

conda config --add channels defaults
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --set show_channel_urls yes
```

验证：

```
conda config --show channels
```

------

### 让 Miniconda 使用系统代理

```python
conda config --set proxy_servers.http  http://127.0.0.1:7890
conda config --set proxy_servers.https http://127.0.0.1:7890
```

如果你用的是 **socks5**（比如 10808），Conda 也可以这么写（不保证所有环境都支持得一样好，http 代理通常最省心）：

```
conda config --set proxy_servers.http  socks5://127.0.0.1:10808
conda config --set proxy_servers.https socks5://127.0.0.1:10808
```

取消代理（恢复直连）：

```
conda config --remove-key proxy_servers
```

### 为 AI 项目创建专用 conda 环境（最佳实践）

⚠️ **不要在 base 环境里开发 AI 项目**

```
conda create -n ai python=3.8 -y
conda activate ai
```

验证：

```
python --version
```

------

## 在 conda 环境里安装 AI 基础栈

### PyTorch（先装，避免依赖地狱）

#### CPU 版（最稳）

```
pip install torch torchvision torchaudio
```

#### GPU 版（NVIDIA + CUDA 11.7 / 12.x）

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```

验证：

```
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

------

### 常用 AI / 数据科学库

```
pip install numpy pandas scipy scikit-learn matplotlib tqdm transformers datasets accelerate torchmetrics
```

------

## 把 Miniconda / conda env 接入 PyCharm（关键一步）

#### PyCharm 直接用 conda env

1. 打开 **PyCharm**

2. `File → Settings → Python Interpreter`

3. 右上角 ⚙ → **Add Interpreter**

4. 选择 **Conda Environment**

5. 选：

   - Existing environment

   - Interpreter 路径：

     ```
     <Miniconda安装目录>\envs\ai\python.exe
     ```

示例：

```
C:\Users\xxx\miniconda3\envs\ai\python.exe
```

1. Apply / OK

✅ PyCharm 现在就完全用 conda 的 `ai` 环境了

------

## 方式 B：PyCharm 创建 conda env（可选）

步骤（大概）：

1. Settings → Project → Python Interpreter → Add Interpreter
2. 选 **Conda Environment**
3. 选 **Existing environment**
4. Conda executable 指到你的（很重要）：
   - `D:\miniconda-3.8\condabin\conda.bat`（优先）
   - 或 `D:\miniconda-3.8\Scripts\conda.exe`
5. Environment 选 `ai`

------

## 流程

```
Miniconda（只管理环境）
↓
conda create -n 项目名 python=3.10
↓
conda 安装 AI 包（torch / transformers / etc）
↓
PyCharm 指向该 conda env
```

------

## conda相关命令

切换环境

```python
conda activate ai #开启xxxx环境
```



根据配置文件安装依赖

```
conda install -r requirements.txt
```

