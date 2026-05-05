# Part 1 Summary: Baseline Fine-tuning on Single-Goal 6x6

## 做了什么

在 PPNL benchmark 的单目标 6x6 网格上，微调了三个 Seq2Seq 模型来生成动作序列（up/down/left/right）。

三个模型用完全相同的超参数训练：
- learning_rate=1e-4, batch_size=1, gradient_accumulation=410
- AdaFactor optimizer, constant schedule, no warmup
- early_stopping patience=30, eval every 50 steps
- 训练集 16,032 条，验证集 2,004 条

## 最终结果（Dev 集 + Executor 评估）

| 模型 | Epoch | 训练时间 | Success | Feasibility | Optimality | Trainer exact_match |
|------|:-----:|----------|--------|-------------|------------|:------:|
| T5-small | 120 | 20.6h | **92.7%** | 92.9% | 92.6% | 95.0% |
| T5-base | 55 | 17.4h | **96.3%** | 96.5% | 96.3% | 95.1% |
| BART-base | 83 | 13.1h | **87.0%** | 95.4% | 86.7% | 82.4% |

GPU 总用时：51.1h（三卡并行，墙钟约 20h）

## 关键发现

1. **T5-base 效果最好**：96.3% success rate，几乎完美。T5 的 relative position encoding 对空间关系建模天然有优势。

2. **T5-small 接近大模型**：92.7% success，说明这个任务对模型规模要求不高。

3. **BART 明显落后**：87.0% success，比 T5 差 5-9 个点。BART 用绝对位置编码 + encoder-decoder 各一层 cross-attention，对空间推理的归纳偏置不如 T5。

4. **所有模型 feasibility 都很高**：动作序列几乎都在合法范围内，说明模型学会了规则（避开障碍、不出界）。

## 文件位置（服务器）

```
/data_sdf/lxf/ppnl-spatial-temporal-reasoning/
├── single_goal/                    ← 原始数据
│   ├── 1_train_set_6x6_samples.json       (16,032 条)
│   ├── 1dev_set_6x6_samples.json          (2,004 条)
│   ├── 1_goals_test_seen_6x6_samples.json (2,004 条)
│   ├── 1_goals_test_unseen_5x5_samples.json    (OOD)
│   ├── 1_goals_test_unseen_7x7_samples.json    (OOD)
│   └── 1_goals_test_unseen_6x6more_obstacles_samples.json (OOD)
└── train/
    ├── T5/runs/t5-small-sg6x6/     ← T5-small 权重 (94 checkpoints, 22G)
    ├── T5/runs/t5-base-sg6x6/      ← T5-base 权重  (43 checkpoints, 36G)
    └── BART/runs/bart-base-sg6x6/  ← BART 权重     (48 checkpoints, 26G)
```

---

# Part 2 工作指引

## 目标（占分 50%）

1. **Failure case 分析（5%）**：找出微调模型在哪些情况下出错（出界、撞障碍、路径过长等）
2. **提出改进方案（45%）**：用 prompting 策略（zero-shot / few-shot / CoT / ReAct）在无需训练的情况下解决路径规划，并测试 OOD 泛化

## 具体步骤

### Step 1: 生成 Part 1 模型的测试集预测
用三个模型的最佳 checkpoint 在 **test 集和 OOD 集**上生成预测，跑 executor 拿到 baseline 数据。

```bash
# 在服务器上运行，每个模型对每个测试集生成预测
cd /data_sdf/lxf/ppnl-spatial-temporal-reasoning
# 使用 evaluate/evaluate_sg.py 评估所有 split
```

需要评估的数据集：
- `1_goals_test_seen_6x6_samples.json` (ID test)
- `1_goals_test_unseen_5x5_samples.json` (OOD)
- `1_goals_test_unseen_7x7_samples.json` (OOD)
- `1_goals_test_unseen_6x6more_obstacles_samples.json` (OOD)

### Step 2: Failure case 分析
从 executor 输出中提取失败样本，分类：
- 出界错误 (out_of_bounds)
- 撞障碍 (obstacle)
- 无效动作 (invalid_action)
- 到达但非最优路径

### Step 3: Prompting 实验
用 SiliconCloud API (Qwen3.5-4B) 测试以下策略：
- **Zero-shot**: 直接给 NL 描述，让模型输出动作序列
- **Few-shot**: 给 3-5 个训练样例作为上下文
- **Chain-of-Thought**: 让模型先写出推理过程再输出动作
- **ReAct**: 让模型交替思考和行动

Prompt 模板在 `ICL/` 目录下。

### Step 4: 对比分析
把 prompting 结果和 Part 1 微调结果放在一起对比：
- ID 6x6 上的表现
- OOD (5x5, 7x7, dense 6x6) 上的泛化能力
- 推理过程的可解释性

### Step 5: 写报告
报告结构：Abstract → Introduction → Related Work → Methodology → Experiments → Results → Conclusion

## API 信息

- 提供商：SiliconCloud
- 模型：Qwen/Qwen3.5-4B
- API Key：sk-chnbfwgwwmlpbviowcqtighcmjmrnxmktqepffbqpiihsskh
- 文档：https://docs.siliconflow.cn/
