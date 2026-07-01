# Explorer LLM-Rec Competition 数据集说明

数据集主页：https://huggingface.co/datasets/OpenOneRec/Explorer_LLM_Rec_Competition

## 定位

这是快手探索者 LLM-Rec 挑战赛使用的数据源。数据来自真实推荐场景，包含用户多域行为、内容元信息、semantic id 映射和通用知识数据。

数据总量约 17.2GB，不应提交到 Git。统一下载到本地：

```text
datasets/Explorer_LLM_Rec_Competition/
```

## 主要目录

根据 Hugging Face 数据集页面：

- `OneReason_UserProfile/`
  - 用户多域历史行为记录。
  - 页面显示约 500k rows。
  - 每行对应匿名用户样本，不包含原始 uid。

- `OneReason_Pid2Sid/`
  - `pid -> semantic id` 映射。
  - semantic id 对应论文中的 itemic pattern 三段 sub-token。

- `OneReason_Pid2Caption/`
  - `pid -> caption` 映射。
  - 可用于 R0 感知、caption grounding、数据清洗和 prompt 构造。

- `OneReason_Pid2Tag/`
  - `pid -> tag/category` 映射。
  - 可用于用户画像摘要、数据分析和负采样/分层评估。

- `OneReason_General/`
  - 通用知识/通用能力相关数据。
  - 用于缓解过拟合推荐格式、保留通用指令能力。

- `demo/`
  - 小型样例和 baseline/demo 脚本，建议优先下载。

## Domain 与 itemic token

论文和数据集中的 domain 对应关系：

| 数据域 | itemic begin token |
| --- | --- |
| video/video | `<|video_begin|>` |
| video/ad | `<|ad_begin|>` |
| goods/product | `<|prod_begin|>` |
| live | `<|living_begin|>` |

标准 itemic pattern 形态：

```text
<|domain_begin|><a_xxxx><b_xxxx><c_xxxx>
```

## 下载方式

先下载 demo：

```bash
mkdir -p datasets/Explorer_LLM_Rec_Competition
huggingface-cli download OpenOneRec/Explorer_LLM_Rec_Competition \
  --repo-type dataset \
  --include "demo/**" \
  --local-dir datasets/Explorer_LLM_Rec_Competition
```

下载全量数据：

```bash
huggingface-cli download OpenOneRec/Explorer_LLM_Rec_Competition \
  --repo-type dataset \
  --local-dir datasets/Explorer_LLM_Rec_Competition
```

如果本地没有 `huggingface-cli`，可先安装：

```bash
python -m pip install -U huggingface_hub
```

## 数据使用建议

第一阶段先做数据审计：

- 样本总数和各 domain 样本数。
- 每条样本历史长度分布。
- target 数量和目标 domain 分布。
- itemic token 正则合法性。
- `pid` 是否能 join 到 `sid/caption/tag`。
- target 是否出现在 `<think>` 中，避免答案泄漏。
- CoT 中引用的 itemic tokens 是否来自用户历史，避免 hallucination。

第二阶段构造训练样本：

- `unCoT`: 用户画像 + 历史行为 -> target itemic tokens。
- `R3 CoT`: 用户画像 + 历史行为 -> `<think>画像抽象/兴趣展开/转移判断</think>` + target itemic tokens。
- `R2`: 用户时间线 -> 高置信兴趣演化链。
- `R1`: source item -> 一跳 relation bridge -> follow-up itemic token。

## 不要提交的数据

以下路径和文件应保持本地或服务器侧，不进入 Git：

- `datasets/`
- `data/`
- `outputs/`
- `*.parquet`
- `*.jsonl`
- `*.arrow`
- `*.safetensors`
- 模型 checkpoint

