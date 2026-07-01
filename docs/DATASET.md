# Explorer LLM-Rec Competition 数据集说明

数据集主页：https://huggingface.co/datasets/OpenOneRec/Explorer_LLM_Rec_Competition

## 数据源区分

目前要区分两类数据：

1. Hugging Face 全量/公开数据源：
   - 地址：https://huggingface.co/datasets/OpenOneRec/Explorer_LLM_Rec_Competition
   - 页面标注约 17.2GB。
   - 包含用户多域行为、内容元信息、semantic id 映射和通用知识数据。

2. 比赛操作手册下载的本地精调数据包：
   - 本地路径：`dataset/`
   - 当前落盘大小：约 436MB。
   - 文件形态：12 个 `.jsonl`，可直接用于万擎“模型定制 -> 模型精调 -> 新建精调任务”的数据集选择。

两者不是矛盾。17.2GB 指 Hugging Face 上更完整的数据源；当前本地 `dataset/` 更像平台精调任务使用的整理/裁剪数据包。

两类数据都不应提交到 Git。统一建议下载到本地：

```text
datasets/Explorer_LLM_Rec_Competition/
dataset/
```

## 本地精调数据包概览

2026-07-01 快速统计：

| 文件 | 行数 | 大小 | 用途初判 |
| --- | ---: | ---: | --- |
| `懂推荐1.jsonl` | 5,426 | 100MB | R3 推荐 CoT 样本 |
| `懂推荐2.jsonl` | 5,442 | 100MB | R3 推荐 CoT 样本 |
| `懂推荐3.jsonl` | 5,372 | 100MB | R3 推荐 CoT 样本 |
| `懂推荐4.jsonl` | 2,964 | 54MB | R3 推荐 CoT 样本 |
| `懂用户.jsonl` | 2,892 | 73MB | R2/用户兴趣演化相关样本 |
| `懂物料part1-7.jsonl` | 10,384 | 约 8MB | R0/R1 物料理解或 token grounding 样本 |
| 合计 | 32,480 | 436MB | 精调平台数据包 |

`懂推荐1-4` 合计 19,204 行，和万擎页面中“懂推荐”约 19000 样本数一致。由于每条推荐样本 prompt 平均约 8k 字符、response 平均约 1.4k 字符，全选预计费用约 400 元是合理的，不适合第一轮 baseline 全量验证。

## 精调成本建议

官方优惠券约 1500 元时，建议先做分级 baseline：

1. `smoke`: 100 条 `懂推荐`，验证上传、训练、评测流程。
2. `small`: 500-1000 条，观察 loss 和输出格式是否正常。
3. `medium`: 2000-5000 条，开始比较数据配比。
4. 全量 `懂推荐` 只在确认 pipeline、格式和评测收益后再跑。

如果万擎平台不能在页面内按行数采样，可以本地生成子集 jsonl，再上传为单独数据集。

## Hugging Face 主要目录

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
- `dataset/`
- `data/`
- `outputs/`
- `*.parquet`
- `*.jsonl`
- `*.arrow`
- `*.safetensors`
- 模型 checkpoint
