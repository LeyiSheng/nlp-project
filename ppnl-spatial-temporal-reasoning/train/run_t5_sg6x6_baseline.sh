#!/usr/bin/env bash
set -euo pipefail

MODEL_SIZE="${1:-small}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "${MODEL_SIZE}" in
  small)
    CONFIG="configs/train_t5_small_sg6x6.json"
    OUTPUT_DIR="${REPO_ROOT}/train/T5/runs/t5-small-sg6x6"
    ;;
  base)
    CONFIG="configs/train_t5_base_sg6x6.json"
    OUTPUT_DIR="${REPO_ROOT}/train/T5/runs/t5-base-sg6x6"
    ;;
  *)
    echo "Usage: $0 [small|base]" >&2
    exit 2
    ;;
esac

python "${REPO_ROOT}/train/convert.py" "${REPO_ROOT}/single_goal/1_train_set_6x6_samples.json" single
python "${REPO_ROOT}/train/convert.py" "${REPO_ROOT}/single_goal/1dev_set_6x6_samples.json" single
python "${REPO_ROOT}/train/convert.py" "${REPO_ROOT}/single_goal/1_goals_test_seen_6x6_samples.json" single

cd "${REPO_ROOT}/train/T5"
export PPNL_TRAIN_FILE="./transformers_cache/1_train_set_6x6_samples.json"
export PPNL_DEV_FILE="./transformers_cache/1dev_set_6x6_samples.json"
export PPNL_TEST_FILE="./transformers_cache/1_goals_test_seen_6x6_samples.json"

python main.py "${CONFIG}"

python "${REPO_ROOT}/evaluate/evaluate_sg.py" \
  "${OUTPUT_DIR}/predictions_predict_test.json" \
  "${REPO_ROOT}/single_goal/1_goals_test_seen_6x6_samples.json" \
  --details "${OUTPUT_DIR}/sg6x6_eval_details.csv" \
  --json | tee "${OUTPUT_DIR}/sg6x6_executor_metrics.json"
