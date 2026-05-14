# PPNL Part 2 Pipeline

This folder contains the reproducible Part 2 workflow for OOD executor evaluation, failure analysis, and prompting comparisons.

## Setup

Install dependencies from the repository root:

```bash
/home/vipuser/miniconda3/bin/python -m pip install -r requirements.txt
```

Prompting requires an official OpenAI key:

```bash
export OPENAI_API_KEY=...
```

## One Command

```bash
bash part2/run_all_part2.sh
```

Useful overrides:

```bash
PYTHON_BIN=/home/vipuser/miniconda3/bin/python DEVICE=cuda BATCH_SIZE=16 bash part2/run_all_part2.sh
OPENAI_MODEL=gpt-5-mini SAMPLE_SIZE=100 SEED=2026 bash part2/run_all_part2.sh
```

If no CUDA driver is available, Seq2Seq inference falls back to CPU and full OOD evaluation can be slow.

## Step-by-Step

Create deterministic prompting samples:

```bash
/home/vipuser/miniconda3/bin/python part2/sample_prompt_sets.py
```

Generate fine-tuned predictions:

```bash
/home/vipuser/miniconda3/bin/python part2/predict_seq2seq.py \
  --model-subfolder t5-base-sg6x6 \
  --test-data single_goal/1_goals_test_unseen_7x7_samples.json \
  --output results/part2/finetuned/t5-base-sg6x6/unseen_7x7_predictions.json \
  --device auto \
  --batch-size 8
```

Evaluate predictions with the canonical executor:

```bash
/home/vipuser/miniconda3/bin/python part2/run_executor_eval.py --predictions-root results/part2/finetuned
```

### Part 1: pretrained models (no fine-tuning)

Compare fine-tuned weights against the **original** HuggingFace checkpoints on the same four
single-goal test splits. This downloads `t5-small`, `t5-base`, and `facebook/bart-base` once
(unless already cached).

```bash
/home/vipuser/miniconda3/bin/python part2/run_pretrained_baseline.py \
  --device cuda \
  --batch-size 8
```

Single backbone / smoke test:

```bash
/home/vipuser/miniconda3/bin/python part2/run_pretrained_baseline.py \
  --models pretrained-t5-base \
  --datasets seen_6x6 \
  --limit 32 \
  --device cuda
```

Outputs live under `results/part1_pretrained_baseline/` with `*_metrics.json` and
`pretrained_baseline_summary.md`.

You can also call `part2/predict_seq2seq.py` directly with `--hf-model-id t5-base` (omit `--model-subfolder`).

Run prompting on sampled sets:

```bash
/home/vipuser/miniconda3/bin/python part2/run_prompting.py \
  --samples-dir results/part2/prompt_samples \
  --model gpt-5-mini \
  --strategies zero_shot few_shot cot react \
  --output-dir results/part2/prompting
```

Aggregate failures and refresh the report:

```bash
/home/vipuser/miniconda3/bin/python part2/analyze_failures.py
/home/vipuser/miniconda3/bin/python part2/make_part2_report.py
```

## Decoding Ablation

The decoding ablation varies only the Seq2Seq generation beam size while keeping
model weights, datasets, and executor metrics fixed. This tests whether greedy
decoding is the bottleneck for the fine-tuned models.

```bash
/home/vipuser/miniconda3/bin/python part2/run_decoding_ablation.py \
  --device cuda \
  --batch-size 16 \
  --beams 1 3 5 10
```

For a quick smoke test:

```bash
/home/vipuser/miniconda3/bin/python part2/run_decoding_ablation.py \
  --models t5-base-sg6x6 \
  --datasets unseen_7x7 \
  --beams 1 3 \
  --limit 20 \
  --device auto
```

See `part2/DECODING_ABLATION_PLAN.md` for the experimental plan.

### Plot decoding ablation figures

After `run_decoding_ablation.py` finishes and writes `decoding_ablation_summary.json`:

```bash
/home/vipuser/miniconda3/bin/python part2/plot_decoding_ablation.py
```

Figures are saved under `results/part2/decoding_ablation/figures/` as PNG and PDF
(grouped **bar charts**: x-axis beam size, colored bars for each model).

## Outputs

- `results/part2/finetuned/`: full-test fine-tuned predictions, metrics, and details.
- `results/part2/finetuned_samples/`: fine-tuned predictions and metrics on the same 100-example samples used for prompting.
- `results/part2/prompting/`: prompting predictions, raw responses, metrics, and details.
- `results/part2/decoding_ablation/`: beam-search ablation predictions, metrics, details, and summary tables.
- `results/part2/decoding_ablation/figures/`: PNG/PDF plots from `plot_decoding_ablation.py`.
- `results/part2/failure_analysis.*`: aggregated failure counts and representative examples.
- `results/part1_pretrained_baseline/`: pretrained (no fine-tune) Part 1 baselines on full test splits.
- `PART2_SUMMARY.md`: final report table; pending cells are filled once metrics files exist.
