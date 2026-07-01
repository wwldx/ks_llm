# 快手探索者 LLM-Rec 挑战赛项目

本仓库用于整理快手探索者 LLM-Rec 挑战赛资料、论文笔记、数据下载说明和后续训练代码。

## 重要入口

- 比赛官网：https://ks-llmrec.streamlake.com/
- 万擎赛事平台文档：https://www.streamlake.com/document/WANQING/mq57afym1d7p20atnau
- FAQ：https://docs.qingque.cn/d/home/eZQAVR10RNyGdtIrSA08YFfr5?identityId=275VOohv2EV
- 数据集：https://huggingface.co/datasets/OpenOneRec/Explorer_LLM_Rec_Competition
- 竞赛基座模型：https://huggingface.co/OpenOneRec/OneReason-0.8B-pretrain-competition
- OneReason 论文：https://arxiv.org/abs/2606.06260

## 当前已保存资料

- `OneReason Technical Report English arxiv.pdf`：arXiv 英文原文，108 页。
- `OneReason Technical Report 中文完整版.pdf`：同学使用 CodeBuddy 翻译的中文版本，供辅助阅读。
- `OneReason英文原文阅读指南.md`：按英文原文页码组织的阅读路线和比赛落地建议。
- `docs/COMPETITION_INFO.md`：比赛入口、时间、算力领取和待确认信息。
- `docs/DATASET.md`：Hugging Face 数据集结构、字段理解和下载方式。

## 当前关键信息

- 当前日期：2026-07-01，比赛已于 2026-07-01 00:00 启动。
- 首期算力资源领取：2026-07-01 10:00，通过万擎控制台弹窗领取。
- 常规资源领取：每周三上午 10:00。
- 参赛前置事项：完成万擎平台实名认证，加入赛事沟通群。
- 初赛基座：`OpenOneRec/OneReason-0.8B-pretrain-competition`。
- 数据源：`OpenOneRec/Explorer_LLM_Rec_Competition`，约 17.2GB，不应提交到 Git。

## 建议目录

```text
.
├── docs/                         # 比赛资料、数据说明、项目状态
├── scripts/                      # 后续下载、清洗、训练脚本
├── configs/                      # 后续训练配置
├── datasets/                     # 本地数据目录，已被 .gitignore 忽略
└── outputs/                      # 本地实验输出，已被 .gitignore 忽略
```

## 第一阶段行动

1. 完成万擎实名认证并领取算力。
2. 下载 Hugging Face 数据集的 `demo/`，先跑通样例。
3. 下载全量数据到 `datasets/Explorer_LLM_Rec_Competition/`。
4. 写数据审计脚本：样本量、domain 分布、token 合法性、历史长度、target 泄漏检查。
5. 跑通官方 baseline SFT。
6. 构造第一版 `unCoT` 直接推荐样本。
7. 小比例加入 R3 CoT 样本，扫描 CoT/unCoT 配比。

