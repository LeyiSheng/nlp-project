#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-/home/vipuser/miniconda3/bin/python}"
DEVICE="${DEVICE:-auto}"
BATCH_SIZE="${BATCH_SIZE:-8}"
OPENAI_MODEL="${OPENAI_MODEL:-gpt-5-mini}"
SAMPLE_SIZE="${SAMPLE_SIZE:-100}"
SEED="${SEED:-2026}"

MODELS=(t5-small-sg6x6 t5-base-sg6x6 bart-base-sg6x6)
DATASET_KEYS=(seen_6x6 unseen_5x5 unseen_7x7 more_obstacles)
DATASET_PATHS=(
  single_goal/1_goals_test_seen_6x6_samples.json
  single_goal/1_goals_test_unseen_5x5_samples.json
  single_goal/1_goals_test_unseen_7x7_samples.json
  single_goal/1_goals_test_unseen_6x6more_obstacles_samples.json
)
PROMPT_STRATEGIES=(zero_shot few_shot cot react)

"${PYTHON_BIN}" part2/sample_prompt_sets.py \
  --output-dir results/part2/prompt_samples \
  --sample-size "${SAMPLE_SIZE}" \
  --seed "${SEED}"

for model in "${MODELS[@]}"; do
  for i in "${!DATASET_KEYS[@]}"; do
    key="${DATASET_KEYS[$i]}"
    data="${DATASET_PATHS[$i]}"
    "${PYTHON_BIN}" part2/predict_seq2seq.py \
      --model-subfolder "${model}" \
      --test-data "${data}" \
      --output "results/part2/finetuned/${model}/${key}_predictions.json" \
      --device "${DEVICE}" \
      --batch-size "${BATCH_SIZE}"
  done
done

"${PYTHON_BIN}" part2/run_executor_eval.py \
  --predictions-root results/part2/finetuned \
  --output-root results/part2/finetuned \
  --strict

for model in "${MODELS[@]}"; do
  for key in "${DATASET_KEYS[@]}"; do
    "${PYTHON_BIN}" part2/predict_seq2seq.py \
      --model-subfolder "${model}" \
      --test-data "results/part2/prompt_samples/${key}_sample.json" \
      --output "results/part2/finetuned_samples/${model}/${key}_predictions.json" \
      --device "${DEVICE}" \
      --batch-size "${BATCH_SIZE}"
  done
done

"${PYTHON_BIN}" part2/run_executor_eval.py \
  --predictions-root results/part2/finetuned_samples \
  --output-root results/part2/finetuned_samples \
  --dataset-root results/part2/prompt_samples \
  --strict

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is required before running prompting experiments." >&2
  exit 2
fi

"${PYTHON_BIN}" part2/run_prompting.py \
  --samples-dir results/part2/prompt_samples \
  --model "${OPENAI_MODEL}" \
  --strategies "${PROMPT_STRATEGIES[@]}" \
  --output-dir results/part2/prompting

"${PYTHON_BIN}" part2/run_executor_eval.py \
  --predictions-root results/part2/prompting \
  --output-root results/part2/prompting \
  --dataset-root results/part2/prompt_samples \
  --models "${PROMPT_STRATEGIES[@]}" \
  --strict

"${PYTHON_BIN}" part2/analyze_failures.py \
  --roots results/part2/finetuned results/part2/finetuned_samples results/part2/prompting \
  --output-json results/part2/failure_analysis.json \
  --output-md results/part2/failure_analysis.md

"${PYTHON_BIN}" part2/make_part2_report.py \
  --results-root results/part2 \
  --output PART2_SUMMARY.md
