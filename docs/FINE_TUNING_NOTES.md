# 万擎模型精调记录

更新时间：2026-07-01

## 当前操作状态

用户已根据比赛操作手册完成：

- 下载本地精调数据包到 `dataset/`。
- 在万擎平台进入 `模型定制 -> 模型精调 -> + 新建精调任务`。
- 已先创建一个试验任务。
- 第一次试验没有全选数据集，而是只选了部分数据做 baseline 验证。

## 成本观察

万擎页面中“懂推荐”数据集显示约 19,000 样本。全选后预计价格约 400 元。

本地统计与页面吻合：

- `懂推荐1.jsonl`: 5,426 行
- `懂推荐2.jsonl`: 5,442 行
- `懂推荐3.jsonl`: 5,372 行
- `懂推荐4.jsonl`: 2,964 行
- 合计：19,204 行

推荐样本很贵的原因：

- 平均 prompt 约 8k 字符，包含很长用户历史。
- 平均 response 约 1.4k 字符，包含 `<think>` 推理。
- 这是 R3 recommendation CoT 样本，单条 token 成本比 R0 物料理解样本高很多。

## Baseline 策略

先不要全量跑 19k `懂推荐`。

建议分四档：

1. `smoke`: 100 条，验证任务创建、数据格式、训练能否成功。
2. `small`: 500-1000 条，检查模型是否学会输出格式。
3. `medium`: 2000-5000 条，开始看评测趋势。
4. `full`: 全量 19k，只在前几档确认有效后再消耗预算。

## 数据选择建议

第一轮只想验证 baseline 时：

- 优先选少量 `懂推荐`，因为它最贴近最终 R3 推荐任务。
- 可少量混入 `懂物料`，帮助模型稳住 itemic token grounding。
- 不建议一开始大量加入 `懂用户`，它 prompt 很长，成本也不低，且更偏 R2/用户演化。

## 后续脚本建议

已提供本地采样脚本：

```bash
python3 scripts/make_finetune_subset.py --preset recommend --size 100
python3 scripts/make_finetune_subset.py --preset recommend --size 500
python3 scripts/make_finetune_subset.py --preset recommend --size 1000
python3 scripts/make_finetune_subset.py --preset material --size 500
```

默认输出到 `dataset_subsets/`，该目录已被 `.gitignore` 忽略。

建议生成：

- `dataset_subsets/recommend_smoke_100.jsonl`
- `dataset_subsets/recommend_small_500.jsonl`
- `dataset_subsets/recommend_small_1000.jsonl`
- `dataset_subsets/material_small_500.jsonl`

这些采样文件也应被 `.gitignore` 忽略，不进入 Git。
