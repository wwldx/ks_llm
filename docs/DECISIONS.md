# Decisions

Continuity schema: 0.1

## 2026-06-30 - 使用英文原文作为主要论文依据

Decision: 以 `OneReason Technical Report English arxiv.pdf` 为准，中文翻译版仅作辅助阅读。

Reason:

- 中文版本由同学用 CodeBuddy 翻译，可能存在术语误译和页码差异。
- 英文 arXiv 原文共 108 页，中文译文共 94 页。

Impact:

- 阅读指南和后续引用按英文原文页码组织。

## 2026-07-01 - 数据集不提交到 Git

Decision: Hugging Face 数据集下载到 `datasets/Explorer_LLM_Rec_Competition/`，通过 `.gitignore` 排除。

Reason:

- 官方数据集约 17.2GB，不适合进入 Git 仓库。
- 后续训练输出和模型 checkpoint 体积也会很大。

Impact:

- 仓库只保存文档、脚本、配置和小型示例。
- 大数据和模型权重保留在本地或训练平台。

