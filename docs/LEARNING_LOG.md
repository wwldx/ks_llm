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

