# OneReason Technical Report 英文原文阅读指南

本指南对应英文 arXiv 原文：

- 本地文件：`OneReason Technical Report English arxiv.pdf`
- 官方页面：https://arxiv.org/abs/2606.06260
- 官方 PDF：https://arxiv.org/pdf/2606.06260

英文原文共 108 页，本地同学翻译版共 94 页，页码不要混用。英文版的正文是英文，但附录里大量 prompt 示例保留中文，并附英文翻译。

## 0. 先抓住论文主线

这篇论文不是单纯讲“用大模型做推荐”，而是在回答一个很具体的问题：

> 为什么推荐模型加上 `<think>` 之后不一定更准？怎样让 thinking mode 真正超过 non-thinking mode？

论文答案是两步：

1. 先让 itemic token 有语义，即 perception / grounding。
2. 再训练推荐场景特有的认知推理，即 compression + reasoning + transition judgement。

对应到比赛，最重要的不是完整复现它的 578B token 预训练或复杂 RL，而是学习它怎么构造 SFT/RFT 数据。

## 1. 术语速查

`itemic token / itemic pattern`

一个物品不是用原始 ID 表示，而是表示成：

```text
<|domain_begin|><a_xxxx><b_xxxx><c_xxxx>
```

`domain` 可以是 `video`、`prod`、`ad`、`living` 等。三个 sub-token 来自 RQ-KMeans codebook，用来承载粗到细的物品语义。

`thinking mode`

模型先输出 `<think>...</think>` 推理，再输出推荐 itemic tokens。

`non-thinking mode / unCoT`

模型不输出推理，直接输出推荐 itemic tokens。

`CoT`

Chain-of-Thought。本文中的 CoT 不是数学题步骤，而是推荐推理链：压缩用户历史、枚举兴趣方向、判断下一步最可能转移到哪里。

`R0-R3`

- R0: Perception，理解单个 itemic token 的语义。
- R1: Derivation，理解 item-to-item 的一跳关系。
- R2: Evolution，理解用户兴趣随时间演化。
- R3: Recommendation，综合画像和历史做下一物品预测。

`RFT`

Rejection Sampling Fine-tuning。让 RL/teacher 生成很多轨迹，只保留命中目标或高质量的轨迹，再拿这些成功样本继续 SFT。比赛中比完整 RL/MOPD 更现实。

`MOPD`

Multi-Teacher On-Policy Distillation。多个单域 teacher 通过 on-policy token-level advantage 蒸馏到一个 student。复杂度高，适合后期理解，不适合第一版方案。

## 2. 今晚阅读路线

目标：读完后你应该能回答三件事：

1. OneReason 为什么认为推荐推理必须先做 itemic-text grounding？
2. R3 推荐 CoT 到底怎么构造？
3. 比赛第一版数据/SFT 应该怎么做，哪些复杂技术先不碰？

建议总耗时 3.5 到 4.5 小时。

### 第一轮：抓论文骨架，40 分钟

读：

- p1 Abstract
- p4-p7 Introduction
- p7 Reasoning Design Philosophy
- p8-p11 Benchmark Design

重点问题：

- 为什么 OneRec-Think/OpenOneRec 里 thinking mode 没有稳定超过 non-thinking mode？
- 作者从多模态 LLM 得到什么启发？
- 为什么推荐推理是 abductive reasoning，而不是 deductive reasoning？
- R0/R1/R2/R3 分别在诊断什么能力？

读完要记住：

- 推荐没有唯一正确答案，用户意图也不可直接观测。
- 好的推荐 CoT 应该做三件事：选择相关行为、压缩成兴趣状态、建模兴趣转移。
- 论文所有训练设计都围绕 R0-R3 展开。

### 第二轮：重点读 SFT，70 分钟

读：

- p20-p31 SFT Pipeline
- p85-p88 D.1 SFT Data and Itemic-Token Perception
- p88-p99 D.2 Cognitive-Reasoning Data Construction
- p99-p106 D.3 Recommendation CoT Construction

这是今晚最关键部分。

重点问题：

- R0 为什么同时保留 CoT caption 和 unCoT caption？
- R1 的目标为什么不是 generic similarity，而是 source-to-follow-up bridge？
- R2 的逻辑链过滤为什么这么严格？
- R3 的三阶段 CoT 是什么？

R3 要背下来：

1. `Persona Abstraction`
   - 把用户画像和长历史压缩成软 persona state。
   - 注意它不是硬标签，不能机械套“游戏用户”“家庭主妇”。

2. `Interest Expansion`
   - 不要立刻押一个答案。
   - 先列 A/B/C 几个有证据的兴趣方向。
   - 论文发现扩展宽度不能太大，`n in {1,3,5}` 往往比 10/20 好。

3. `Transition Inference`
   - 比较每个方向的证据强度、近期性、连续性、persona 兼容性、目标域兼容性。
   - 最后承诺最可能的方向。

比赛启发：

- 第一版 SFT 不要只做“历史 -> target token”。
- 应该混入一部分 R3 CoT 样本，训练模型学会压缩和筛选证据。
- CoT 不能泄漏 target 标题、target token 或 target-only 实体。

### 第三轮：看预训练，不钻细节，35 分钟

读：

- p11-p20 Pre-Training Pipeline
- p80-p85 C. Pre-Training Details，只看数据样例和 mixture 结构

重点问题：

- itemic tokenizer 是怎么来的？
- 四粒度预训练数据分别解决什么？
- 为什么 user granularity 是最终 integrator？

四粒度数据：

- `Token granularity`: 让 sub-token 有层级语义。
- `Item granularity`: itemic pattern 和 caption/QA 对齐。
- `Relational granularity`: item-to-item 转移带自然语言解释。
- `User granularity`: 用户画像 + 多域行为 + 时间线。

比赛启发：

- 你们大概率做不了完整预训练。
- 但可以借鉴它的数据清洗原则：caption 粗粒化、去掉过细 OCR/ASR/型号/日期噪声、保留类别/品牌/IP/卖点/人群。
- 如果官方给 item metadata/caption，可以构造 R0/R1/R2/R3 式增强 SFT 样本。

### 第四轮：读 RL/RFT/MOPD，45 分钟

读：

- p31-p44 RL Pipeline
- p37 Rejection Sampling Fine-tuning
- p38-p42 Multi-Teacher On-Policy Distillation
- p42-p44 Comparison and Discussions

阅读优先级：

1. 先理解 `specialize-then-unify`。
2. 再理解 RFT 为什么提升 large-K recall。
3. 最后粗看 MOPD，不用硬啃公式。

关键结论：

- mixed-domain RL 会互相干扰。
- single-domain RL 能更好激活 thinking。
- RFT 通过只保留成功轨迹，能让 thinking mode 更稳定超过 non-thinking mode。
- MOPD 会同时增强 thinking 和 non-thinking，但更复杂，也可能吸收弱 CoT 噪声。

比赛启发：

- 如果你同学说的 `opd` 是 MOPD，先知道它是什么即可。
- 第一阶段更现实的是 RFT：模型生成多条，筛选命中/高质量结果，回灌训练。
- 不要一上来做完整 GRPO/MOPD，调试成本高。

### 第五轮：读评测和实验，45 分钟

读：

- p44-p50 CoT Analysis Indicators
- p50-p55 Experiments
- p52-p55 Non-Thinking Gains from Thinking Supervision

重点问题：

- CoT 是否真的帮了最终预测，论文怎么测？
- 为什么 SFT 的 CoT 可能让 target log-likelihood 下降？
- 为什么 RFT 后 CoT 才真正变有用？
- CoT/unCoT 混合比例为什么不能盲目全 CoT？

四个 CoT 分析指标：

- `Delta LL`: 加 CoT 后，ground-truth target 的 log-likelihood 是否升高。
- `log-likelihood progression`: 推理片段越多，target 似然是否逐步上升。
- `item legality`: CoT 里引用的 itemic pattern 是否在 item catalog 中合法。
- `history grounding`: CoT 引用的合法 item 是否真的出现在用户历史里。

比赛启发：

- 训练样本质量不能只看文字流畅。
- 要写脚本检查：
  - token 格式合法性；
  - CoT 中引用 token 是否来自历史；
  - target token 是否泄漏在 `<think>` 里；
  - 生成答案是否在目标域；
  - CoT 是否过长。

### 第六轮：部署和相关工作，20 分钟

读：

- p55-p57 Deployment
- p57-p59 Related Works
- p59 Conclusion
- p67-p69 Deployment Details 可略读

重点看：

- `Fast-Slow Thinking` 架构。
- nearline OneReason 负责慢推理召回，online OneRec 负责实时。
- 低活跃用户收益最大，因为 OneReason 能用语义和有限行为补全兴趣。

比赛里这部分不是直接实现重点，但有助于理解为什么它不是纯实时模型。

## 3. 可以先跳过的内容

今晚如果时间紧，先跳过：

- p60-p66 References。
- p66 Author List。
- RL 里的所有公式细节，先理解目标和结论即可。
- MOPD 的重要性采样公式、reverse-KL 公式。
- A.2 OneReason for OneRec 的工程蒸馏细节。

不要跳过：

- p7 Reasoning Design Philosophy。
- p20-p31 SFT Pipeline。
- p99-p106 R3 Recommendation CoT Construction。
- p52-p55 Non-Thinking Gains from Thinking Supervision。

## 4. 读论文时的标注方式

建议你每读一节，在旁边只写三类笔记：

`Claim`

作者提出了什么判断，例如：

- Thinking fails when itemic tokens are not grounded.
- Recommendation reasoning is abductive.
- CoT supervision can improve non-thinking decoding in some domains.

`Evidence`

作者用什么实验或表格支撑，例如：

- Table 2: 四粒度预训练消融。
- Table 9: SFT/Mix-RL/Single-RL/RFT/MOPD 对比。
- Figure 23: SFT CoT 的 Delta LL 为负，RFT 后为正。
- Table 17/Figure 25: CoT/unCoT 混合比例影响 non-thinking。

`Action`

对比赛有什么动作，例如：

- 构造 R3 CoT 数据。
- 扫 CoT/unCoT 比例。
- 做 token 合法性和 target 泄漏检查。
- 后期做 RFT，而不是先做 MOPD。

## 5. 论文对比赛的直接方案

### 第一版 baseline

目标：先跑通官方训练评测。

数据：

- 官方 train data。
- 直接格式：`user profile + history -> target itemic tokens`。
- 不加复杂 CoT。

训练：

- LoRA SFT 优先。
- 先拿到可提交结果。

### 第二版 CoT SFT

目标：借鉴 R3 recommendation CoT。

数据格式：

```text
System: 你擅长理解用户画像、跨场景行为和 itemic tokens，请根据输入信息归纳该用户的目标内容。
User: 用户画像 + 多域历史
Assistant:
<think>
画像抽象；兴趣方向 A/B/C；权衡证据强度、近期性、目标域兼容性；最终判断最可能方向。
</think>
target itemic tokens
```

质量规则：

- `<think>` 里可以引用历史 itemic tokens。
- `<think>` 里不能出现 target itemic tokens。
- 不允许编造历史中不存在的行为。
- 不允许只写“用户喜欢游戏/美食”这种泛化结论，要尽量到具体 IP、功能、场景、风格。

比例：

- 不要全 CoT。
- 从 `20%-40% CoT + 60%-80% unCoT` 开始扫。
- 不同目标域可以分别扫比例。

### 第三版 R2/R1 增强

目标：让模型更会做兴趣演化和一跳转移。

R1 样本：

- 输入一个 source item。
- 输出一段 source-to-follow-up bridge，再输出 target itemic token。

R2 样本：

- 输入用户时间线。
- 输出高置信兴趣演化链。
- 如果没有真实演化链，返回空数组，不要强行解释。

重点复用 p95 的 11 条逻辑链过滤原则：

- 顺序互换测试。
- 认知增量测试。
- 行为修正/收敛。
- 交互深度变化。
- 时间密度测试。
- 非普适性测试。
- 触发源测试。
- 强因果排他性测试。
- 证据闭环。
- 禁止读心。

### 第四版 RFT

目标：把模型自己发现的成功轨迹回灌。

流程：

1. 用当前模型对 dev/train split 生成多条候选。
2. 根据 target 命中、合法性、格式、history grounding 筛选。
3. 保留成功 CoT + answer。
4. 混入 SFT 继续训练。

这比直接做 MOPD 更适合比赛前中期。

## 6. 今晚读完后的自测题

读完以后你应该能口头回答：

1. 为什么“推荐 CoT”不是数学题 CoT？
2. R0/R1/R2/R3 分别对应什么数据样本？
3. `Persona Abstraction -> Interest Expansion -> Transition Inference` 每一步在防什么问题？
4. 为什么 RFT 后 thinking mode 才更稳定？
5. 为什么 CoT 数据可以提升 non-thinking，但不能无限加？
6. 你们队明天第一版数据构造应该怎么做？

如果这些能答出来，这篇论文对比赛的主要价值就读到了。

## 7. 最小可执行清单

明天拿到数据后优先做：

- [ ] 统计各 domain 样本量、target 数量、历史长度分布。
- [ ] 检查 itemic token 正则合法性。
- [ ] 跑通官方 baseline SFT。
- [ ] 构造 unCoT 推荐样本。
- [ ] 构造少量 R3 CoT 样本。
- [ ] 写 target 泄漏检查。
- [ ] 写 history grounding 检查。
- [ ] 扫 CoT/unCoT 混合比例。
- [ ] 对高活跃/低活跃用户分层看效果。
- [ ] 如果时间允许，做 rejection sampling fine-tuning。

