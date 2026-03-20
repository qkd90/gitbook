## 更换国内源

https://hf-mirror.com/

## Dataset

### 文本标记化

模型无法处理原始文本，因此你需要将文本转换为数字。标记化提供了一种通过将文本分割成称为*tokens*的单个单词来实现此目的的方法。Tokens 最终会被转换为数字。

查看 Hugging Face 课程第二章的 [标记器](https://hugging-face.cn/course/chapter2/4#pt) 部分，了解更多关于标记化和不同标记化算法的信息。

**1**. 首先加载 [rotten_tomatoes](https://hugging-face.cn/datasets/rotten_tomatoes) 数据集和与预训练 [BERT](https://hugging-face.cn/bert-base-uncased) 模型对应的标记器。使用与预训练模型相同的标记器很重要，因为你希望确保文本以相同的方式进行分割。

```
from transformers import AutoTokenizer
from datasets import load_dataset

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
dataset = load_dataset("cornell-movie-review-data/rotten_tomatoes", split="train")
```

**2**. 在数据集的第一行 `text` 上调用你的标记器

```
tokenizer(dataset[0]["text"])
{'input_ids': [101, 1103, 2067, 1110, 17348, 1106, 1129, 1103, 6880, 1432, 112, 188, 1207, 107, 14255, 1389, 107, 1105, 1115, 1119, 112, 188, 1280, 1106, 1294, 170, 24194, 1256, 3407, 1190, 170, 11791, 5253, 188, 1732, 7200, 10947, 12606, 2895, 117, 179, 7766, 118, 172, 15554, 1181, 3498, 6961, 3263, 1137, 188, 1566, 7912, 14516, 6997, 119, 102],
 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
```

标记器返回一个包含三个项的字典

- `input_ids`：表示文本中标记的数字。
- `token_type_ids`：如果存在多个序列，指示标记属于哪个序列。
- `attention_mask`：指示标记是否应该被屏蔽。

这些值实际上是模型输入。

**3**. 标记化整个数据集最快的方法是使用 [map()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.map) 函数。此函数通过将标记器应用于批量示例而不是单个示例来加速标记化。将 `batched` 参数设置为 `True`

```
def tokenization(example):
    return tokenizer(example["text"])

dataset = dataset.map(tokenization, batched=True)
```

**4**. 设置数据集格式以与你的机器学习框架兼容

PyTorch

隐藏 Pytorch 内容

使用 [set_format()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.set_format) 函数将数据集格式设置为与 PyTorch 兼容

```
dataset.set_format(type="torch", columns=["input_ids", "token_type_ids", "attention_mask", "label"])
dataset.format['type']
'torch'
```

TensorFlow

隐藏 TensorFlow 内容

使用 [to_tf_dataset()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.to_tf_dataset) 函数将数据集格式设置为与 TensorFlow 兼容。你还需要从 🤗 Transformers 导入一个 [数据整理器](https://hugging-face.cn/docs/transformers/main_classes/data_collator#transformers.DataCollatorWithPadding)，将不同长度的序列组合成一个等长批次。

```
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="tf")
tf_dataset = dataset.to_tf_dataset(
    columns=["input_ids", "token_type_ids", "attention_mask"],
    label_cols=["label"],
    batch_size=2,
    collate_fn=data_collator,
    shuffle=True
)
```

**5**. 数据集现在已准备好与你的机器学习框架进行训练！

## 重采样音频信号

音频输入像文本数据集一样需要被分成离散的数据点。这被称为*采样*；采样率告诉你在每秒捕获了多少语音信号。确保你的数据集的采样率与用于预训练模型的采样率匹配非常重要。如果采样率不同，预训练模型可能在你的数据集上表现不佳，因为它无法识别采样率的差异。

**1**. 首先加载 [MInDS-14](https://hugging-face.cn/datasets/PolyAI/minds14) 数据集、[Audio](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Audio) 特征和与预训练 [Wav2Vec2](https://hugging-face.cn/facebook/wav2vec2-base-960h) 模型对应的特征提取器

```
from transformers import AutoFeatureExtractor
from datasets import load_dataset, Audio

feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")
dataset = load_dataset("PolyAI/minds14", "en-US", split="train")
```

**2**. 索引到数据集的第一行。当你调用数据集的 `audio` 列时，它会自动解码和重采样。

```
audio = dataset[0]["audio"]
print(audio)
<datasets.features._torchcodec.AudioDecoder object at 0x11642b6a0>
audio.get_all_samples().sample_rate
8000
```

**3**. 阅读数据集卡片非常有用，可以为你提供大量关于数据集的信息。快速查看 MInDS-14 数据集卡片可知其采样率为 8kHz。同样，你可以从模型卡片中获取模型的许多详细信息。Wav2Vec2 模型卡片显示它是在 16kHz 语音音频上采样的。这意味着你需要对 MInDS-14 数据集进行上采样以匹配模型的采样率。

使用 [cast_column()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.cast_column) 函数，并将 [Audio](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Audio) 特征中的 `sampling_rate` 参数设置为上采样音频信号。现在当你调用 `audio` 列时，它会被解码并重采样到 16kHz。

```
dataset = dataset.cast_column("audio", Audio(sampling_rate=16_000))
audio = dataset[0]["audio"]
print(audio)
<datasets.features._torchcodec.AudioDecoder object at 0x11642b6a0>
audio.get_all_samples().sample_rate
16000
```

**4**. 使用 [map()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.map) 函数将整个数据集重采样到 16kHz。此函数通过将特征提取器应用于批量示例而不是单个示例来加速重采样。将 `batched` 参数设置为 `True`

```
def preprocess_function(examples):
    audio_arrays = [x.get_all_samples().data for x in examples["audio"]]
    inputs = feature_extractor(
        audio_arrays, sampling_rate=feature_extractor.sampling_rate, max_length=16000, truncation=True
    )
    return inputs

dataset = dataset.map(preprocess_function, batched=True)
```

**5**. 数据集现在已准备好与你的机器学习框架进行训练！

### 应用数据增强

对图像数据集最常见的预处理是*数据增强*，这是一个在不改变数据含义的情况下对图像引入随机变化的过程。这可能意味着改变图像的颜色属性或随机裁剪图像。你可以自由使用任何你喜欢的数据增强库，而 🤗 Datasets 将帮助你将数据增强应用于你的数据集。

**1**. 首先加载 [Beans](https://hugging-face.cn/datasets/AI-Lab-Makerere/beans) 数据集、`Image` 特征和与预训练 [ViT](https://hugging-face.cn/google/vit-base-patch16-224-in21k) 模型对应的特征提取器

```
from transformers import AutoFeatureExtractor
from datasets import load_dataset, Image

feature_extractor = AutoFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")
dataset = load_dataset("AI-Lab-Makerere/beans", split="train")
```

**2**. 索引到数据集的第一行。当你调用数据集的 `image` 列时，底层的 PIL 对象会自动解码为图像。

```
dataset[0]["image"]
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x500 at 0x7FE5A047CC70>
```

大多数图像模型都期望图像处于 RGB 模式。Beans 图像已经处于 RGB 模式，但如果你的数据集包含其他模式的图像，你可以使用 [cast_column()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.cast_column) 函数将模式设置为 RGB。

```
dataset = dataset.cast_column("image", Image(mode="RGB"))
```

**3**. 现在让我们将数据增强应用于你的图像。🤗 Datasets 支持任何增强库，在本例中我们将使用 Albumentations。

[Albumentations](https://albumentations.ai/) 是一个流行的图像增强库，它提供了一系列[丰富的变换](https://albumentations.ai/docs/reference/supported-targets-by-transform/)，包括空间级别变换、像素级别变换和混合级别变换。

安装 Albumentations

```
pip install albumentations
```

**4**. 使用 Albumentations 创建一个典型的数据增强管道

```
import albumentations as A
import numpy as np
from PIL import Image

transform = A.Compose([
    A.RandomCrop(height=256, width=256, pad_if_needed=True, p=1),
    A.HorizontalFlip(p=0.5),
    A.ColorJitter(p=0.5)
])
```

**5**. 由于 🤗 Datasets 使用 PIL 图像，而 Albumentations 期望 NumPy 数组，因此你需要在格式之间进行转换。

```
def albumentations_transforms(examples):
    # Apply Albumentations transforms
    transformed_images = []
    for image in examples["image"]:
        # Convert PIL to numpy array (OpenCV format)
        image_np = np.array(image.convert("RGB"))
        
        # Apply Albumentations transforms
        transformed_image = transform(image=image_np)["image"]
        
        # Convert back to PIL Image
        pil_image = Image.fromarray(transformed_image)
        transformed_images.append(pil_image)
    
    examples["pixel_values"] = transformed_images
    return examples
```

**6**. 使用 [with_transform()](https://hugging-face.cn/docs/datasets/v4.0.0/en/package_reference/main_classes#datasets.Dataset.with_transform) 应用变换

```
dataset = dataset.with_transform(albumentations_transforms)
dataset[0]["pixel_values"]
```

**在使用 🤗 Datasets 时，与 Albumentations 结合的关键点：**

- 在应用变换之前将 PIL 图像转换为 NumPy 数组
- Albumentations 返回一个字典，其中转换后的图像在“image”键下
- 转换后将结果转换回 PIL 格式

**7**. 数据集现在已准备好与你的机器学习框架进行训练！



