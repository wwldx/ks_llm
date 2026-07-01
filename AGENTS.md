# Project Work Rules

## Project Purpose

本项目用于参加快手探索者 LLM-Rec 挑战赛，整理官方资料、OneReason 论文理解、数据下载说明、训练脚本和实验记录。

## Main Directories

- `/Users/wwl_mac/Desktop/2026春季第四学期/快手LLM-搜索比赛/`: 项目根目录。
- `docs/`: 比赛资料、数据说明、持续上下文和决策记录。
- `datasets/`: 本地数据目录，不提交到 Git。
- `outputs/`: 本地实验输出目录，不提交到 Git。
- `scripts/`: 后续脚本目录。
- `configs/`: 后续训练配置目录。

## Commands

- Run: Unknown, 官方 baseline/demo 下载后补充。
- Test: Unknown, 训练/数据脚本创建后补充。
- Lint/typecheck: Unknown。
- Git status: `git status --short --branch`

## File Rules

- 不要把 17GB Hugging Face 数据集、模型权重、训练输出提交到 Git。
- 论文 PDF 可以保留在仓库中，但后续大模型 checkpoint 不应提交。
- 比赛时间、平台规则、下载链接更新时，同步更新 `README.md`、`docs/COMPETITION_INFO.md` 和 `docs/DATASET.md`。

## Agent Workflow

- Start by reading this file and `docs/AGENT_STATE.md`.
- If decisions matter, read `docs/DECISIONS.md`.
- If learning context matters, read `docs/LEARNING_LOG.md`.
- Before finishing substantial work, update `docs/AGENT_STATE.md`.

