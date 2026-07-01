# Agent State

Continuity schema: 0.1

## Current Focus

快手探索者 LLM-Rec 挑战赛项目资料整理与启动准备。

## Completed

- 下载并保存 OneReason 英文 arXiv 原文 PDF。
- 保存同学提供的中文翻译版 PDF。
- 编写 `OneReason英文原文阅读指南.md`。
- 初始化 Git 仓库并推送到 `git@github.com:wwldx/ks_llm.git`。
- 补充比赛官网、数据集、时间线、算力领取和数据下载说明。
- 用户已按比赛操作手册下载精调数据包到 `dataset/`，当前落盘约 436MB，合计 32,480 行 jsonl。
- 记录万擎精调页面的成本观察：`懂推荐` 约 19,000 样本，全选预计约 400 元。

## Next

- 用本地 `dataset/` 小样本跑通万擎精调 baseline。
- 创建数据审计脚本，检查 domain 分布、token 合法性、join 覆盖率、history 长度和 target 泄漏。
- 创建本地采样脚本，生成 100/500/1000 条 `懂推荐` 子集，控制精调预算。
- 之后视需要下载 Hugging Face 全量数据到 `datasets/Explorer_LLM_Rec_Competition/`，不要提交到 Git。

## Open Questions

- 初赛/复赛/决赛完整截止日期仍需从官网或群公告确认。
- 正式提交格式和每日评测次数需以万擎平台最新文档为准。
- 是否允许把官方原始样本发给外部 GPT/Gemini API 进行蒸馏，需要向赛事群确认。

## Verification

- `git status --short --branch` 在 2026-06-30 显示本地 `main` 跟踪 `origin/main`。
- Hugging Face 数据集页面已确认为 `OpenOneRec/Explorer_LLM_Rec_Competition`。
- 2026-07-01 本地 `dataset/` 统计：`du -sh dataset` 为 436MB，`wc -l dataset/*.jsonl` 合计 32,480 行。
