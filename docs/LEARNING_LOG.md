# Learning Log

Continuity schema: 0.1

## 2026-06-30 - OneReason 论文主线

### Key Understanding

- 推荐推理是 abductive reasoning，不是数学题式 deductive reasoning。
- OneReason 将能力拆成 R0 Perception、R1 Derivation、R2 Evolution、R3 Recommendation。
- R3 CoT 的核心结构是 Persona Abstraction、Interest Expansion、Transition Inference。

### Decisions

- 比赛第一阶段优先做 SFT 数据构造和数据审计。
- 完整 GRPO/MOPD 暂不作为第一版目标。

### Follow-ups

- 结合官方数据集实际字段，落地 unCoT 与 R3 CoT 样本构造脚本。

## 2026-07-01 - 官方数据集确认

### Key Understanding

- 数据源为 `OpenOneRec/Explorer_LLM_Rec_Competition`。
- 主要目录包括 `OneReason_UserProfile`、`OneReason_Pid2Sid`、`OneReason_Pid2Caption`、`OneReason_Pid2Tag`、`OneReason_General` 和 `demo`。
- 数据域和论文 itemic token begin token 对应：video、ad、prod、living。

### Decisions

- 先下载 demo，跑通格式，再下载全量。
- 全量数据放入 `datasets/`，不提交 Git。

### Follow-ups

- 拉取 demo 并检查文件格式。
- 写数据审计脚本。

## 2026-07-01 - 本地精调数据包与成本

### Key Understanding

- 操作手册下载到本地的 `dataset/` 是 436MB 的精调平台数据包，不是 Hugging Face 上约 17.2GB 的完整数据源。
- `懂推荐1-4` 合计 19,204 行，和万擎页面显示的“懂推荐”约 19000 样本一致。
- `懂推荐` 样本 prompt 和 response 都很长，全选预计约 400 元是合理现象。

### Decisions

- 第一轮 baseline 不全选 19k `懂推荐`。
- 先使用 100/500/1000 条子集做 smoke/small 实验。

### Follow-ups

- 写本地采样脚本生成可上传的小数据集。
- 记录每次万擎任务的数据选择、价格、训练配置和评测结果。
