

## 简介

**CGMformer** 是一个基于 **Transformer 架构的深度学习模型**，用于从连续血糖监测（Continuous Glucose Monitoring, CGM）数据中学习个体的血糖动态。它最初来自 YurunLu/CGMformer 仓库，是科研项目复现/本地测试版本（你这个 repo 是 fork 版）。[GitHub+1](https://github.com/qkd90/CGMformer)

原论文说明它通过自监督预训练学习血糖变化模式，然后可用于多个下游任务，如糖尿病检测、非糖尿病分型、饮食影响预测等。

CGMformer 的设计初衷是：

✔ 学习和捕捉 CGM 数据中长期依赖的血糖趋势；
 ✔ 构建个体隐含的血糖动态表示，具有迁移能力；
 ✔ 利用预训练模型在下游任务上提升效果（例如分类或预测）。[OUP Academic](https://academic.oup.com/nsr/article/12/5/nwaf039/8005967?utm_source=chatgpt.com)

Transformer 类似于 NLP 里的模型，对时间序列“tokenize”并做自监督学习（类似 BERT 的 masked-learning）。[EurekAlert!](https://www.eurekalert.org/news-releases/1074837?utm_source=chatgpt.com)

## 仓库结构（关键部分）

从你的仓库里主要文件可以看到

```
CGMFormer/                # 主模型
CGMformer_C/              # 带临床数据结合的模型
CGMformer_type/           # 非糖尿病亚型分析
CGMformer_Diet/           # 饮食影响预测模型
Data/                     # 示例/待处理的数据
*.ipynb                   # 数据处理和可视化 notebook
*.py                      # 脚本用于预训练、分类、回归等任务
```

## 程序

| 文件                        | 作用                      |
| --------------------------- | ------------------------- |
| `run_pretrain_CGMFormer.py` | 预训练 CGMformer          |
| `run_clustering.py`         | 获取 embedding / 聚类示例 |
| `run_labels_classify.py`    | 分类标签任务              |
| `run_regression.py`         | 回归任务                  |
| `processing_811_data.ipynb` | 数据预处理示例            |
| `build_vocab.ipynb`         | 构建 token 化字典         |

## 运行方式

按 notebook `processing_811_data.ipynb` 预处理你的 CGM 数据，生成 `input_ids` 等格式（token 化值）

```python
python processing_811_data.py --input_data your_cgm_data.csv --output_data processed_data.json
```

### 推理（inference）并生成嵌入向量：

这一步会生成模型的输出（血糖预测值或 embedding）。

```
python run_clustering.py \
    --checkpoint_path D:/github/CGMformer/cgm_ckp \
    --data_path processed_data.json \
    --save_path output/
```

这里的 `run_clustering.py` 会将预训练模型应用到 **`processed_data.json`** 数据集上，生成血糖预测的嵌入表示或聚类结果，并保存在 `output/` 目录下。

### 分类/回归任务推理：

如果你要进行分类或回归任务，可以运行以下命令：

```
python run_labels_classify.py \
    --checkpoint_path D:/github/CGMformer/cgm_ckp \
    --train_path train_data.json \
    --test_path processed_data.json \
    --output_path output/
```

这个命令会根据你指定的 **test 数据** 文件 `processed_data.json` 来进行推理，**不涉及训练**，结果会被保存在 `output/` 目录下。

**结果分析**

推理后，结果将保存在 `output/` 目录中。你可以查看输出结果：

- 如果你执行的是聚类（embedding 提取）任务，输出结果通常会包含每个样本的 embedding 向量或聚类标签。
- 如果你执行的是分类/回归任务，输出将会是模型的预测结果，例如血糖水平预测、糖尿病风险分类等。

## Data目录

不同来源的 CGM 数据 → 经过 CGMformer 编码 → 得到的特征向量

| 文件名              | 数据来源             |
| ------------------- | -------------------- |
| multicenter_vec.csv | 全国多中心真实数据   |
| zhao_vec.csv        | Zhao 等人的研究数据  |
| Colas_vec.csv       | Colas 等人的研究数据 |
