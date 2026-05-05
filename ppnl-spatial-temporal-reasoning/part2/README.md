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

## Outputs

- `results/part2/finetuned/`: full-test fine-tuned predictions, metrics, and details.
- `results/part2/finetuned_samples/`: fine-tuned predictions and metrics on the same 100-example samples used for prompting.
- `results/part2/prompting/`: prompting predictions, raw responses, metrics, and details.
- `results/part2/failure_analysis.*`: aggregated failure counts and representative examples.
- `PART2_SUMMARY.md`: final report table; pending cells are filled once metrics files exist.
