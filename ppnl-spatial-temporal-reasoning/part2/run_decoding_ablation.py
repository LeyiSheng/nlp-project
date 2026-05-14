#!/usr/bin/env python3
"""Run beam-search decoding ablations for fine-tuned PPNL Seq2Seq models.

This script reuses the existing Part 2 prediction and executor-evaluation
pipeline. It varies only generation-time decoding parameters, so it does not
retrain any model.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import DATASETS, MODEL_SUBFOLDERS, REPO_ROOT, load_json, write_json
from predict_seq2seq import DEFAULT_MODEL_ID


DEFAULT_BEAMS = (1, 3, 5, 10)

DEFAULT_LOCAL_MODEL_PATHS = {
    "t5-small-sg6x6": Path(
        "/data_sdf/lxf/ppnl-spatial-temporal-reasoning_old/train/T5/runs/t5-small-sg6x6/checkpoint-4650"
    ),
    "t5-base-sg6x6": Path(
        "/data_sdf/lxf/ppnl-spatial-temporal-reasoning_old/train/T5/runs/t5-base-sg6x6/checkpoint-2100"
    ),
    "bart-base-sg6x6": Path(
        "/data_sdf/lxf/ppnl-spatial-temporal-reasoning_old/train/BART/runs/bart-base-sg6x6/checkpoint-2950"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument(
        "--use-local-checkpoints",
        action="store_true",
        help="Load local best checkpoints under ppnl-spatial-temporal-reasoning_old instead of Hugging Face Hub.",
    )
    parser.add_argument("--models", nargs="+", default=list(MODEL_SUBFOLDERS), choices=MODEL_SUBFOLDERS)
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS), choices=list(DATASETS))
    parser.add_argument("--beams", nargs="+", type=int, default=list(DEFAULT_BEAMS))
    parser.add_argument("--output-root", default="results/part2/decoding_ablation")
    parser.add_argument("--dataset-root", default=None, help="Use sampled JSONs from this directory instead of full datasets.")
    parser.add_argument("--device", default="auto", help="'auto', 'cpu', 'cuda', or cuda device like cuda:0")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--limit", type=int, help="Optional smoke-test limit per dataset.")
    parser.add_argument("--skip-existing", action="store_true", help="Reuse existing prediction files.")
    parser.add_argument("--eval-only", action="store_true", help="Only run executor evaluation for existing predictions.")
    parser.add_argument("--predict-only", action="store_true", help="Only generate predictions; skip executor evaluation.")
    return parser.parse_args()


def dataset_paths(dataset_root: str | None) -> dict[str, Path]:
    if dataset_root is None:
        return DATASETS
    root = Path(dataset_root)
    return {key: root / f"{key}_sample.json" for key in DATASETS}


def prepare_test_data(source: Path, dataset_key: str, output_root: Path, limit: int | None) -> Path:
    """Return an evaluator-compatible test-data path.

    When --limit is used, prediction and evaluation must see the same truncated
    file; otherwise evaluate_sg.py will reject the size mismatch.
    """
    if limit is None:
        return source

    limited_dir = output_root / "_limited_data"
    limited_path = limited_dir / f"{dataset_key}_limit{limit}.json"
    if not limited_path.exists():
        samples = load_json(source)[:limit]
        write_json(limited_path, samples)
    return limited_path


def prediction_path(output_root: Path, beam: int, model: str, dataset_key: str) -> Path:
    return output_root / f"beam_{beam}" / model / f"{dataset_key}_predictions.json"


def metrics_path(output_root: Path, beam: int, model: str, dataset_key: str) -> Path:
    return output_root / f"beam_{beam}" / model / f"{dataset_key}_metrics.json"


def details_path(output_root: Path, beam: int, model: str, dataset_key: str) -> Path:
    return output_root / f"beam_{beam}" / model / f"{dataset_key}_details.csv"


def run_prediction(args: argparse.Namespace, beam: int, model: str, dataset_key: str, test_data: Path, output: Path) -> None:
    if args.eval_only:
        return
    if args.skip_existing and output.exists():
        print(f"skip existing predictions: {output}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(REPO_ROOT / "part2" / "predict_seq2seq.py"),
        "--model-subfolder",
        model,
        "--test-data",
        str(test_data),
        "--output",
        str(output),
        "--device",
        args.device,
        "--batch-size",
        str(args.batch_size),
        "--max-new-tokens",
        str(args.max_new_tokens),
        "--num-beams",
        str(beam),
    ]
    if args.use_local_checkpoints:
        model_path = DEFAULT_LOCAL_MODEL_PATHS[model]
        if not model_path.exists():
            raise SystemExit(f"missing local checkpoint: {model_path}")
        cmd[2:2] = ["--model-path", str(model_path)]
    else:
        cmd[2:2] = ["--model-id", args.model_id]
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def run_eval(predictions: Path, test_data: Path, details: Path, metrics: Path) -> None:
    details.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(REPO_ROOT / "evaluate" / "evaluate_sg.py"),
        str(predictions),
        str(test_data),
        "--details",
        str(details),
        "--json",
    ]
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    parsed = json.loads(result.stdout)
    metrics.write_text(json.dumps(parsed, indent=2) + "\n", encoding="utf-8")
    print(f"evaluated {predictions} -> {metrics}")


def pct(value) -> str:
    return f"{100 * float(value):.1f}%"


def collect_summary(output_root: Path, beams: list[int], models: list[str], datasets: list[str]) -> list[dict]:
    rows = []
    for beam in beams:
        for model in models:
            for dataset_key in datasets:
                path = metrics_path(output_root, beam, model, dataset_key)
                if not path.exists():
                    continue
                metrics = json.loads(path.read_text(encoding="utf-8"))
                rows.append(
                    {
                        "beam": beam,
                        "model": model,
                        "dataset": dataset_key,
                        "total": metrics["total"],
                        "skipped_unreachable": metrics["skipped_unreachable"],
                        "success_rate": metrics["success_rate"],
                        "feasibility": metrics["feasibility"],
                        "optimality": metrics["optimality"],
                    }
                )
    return rows


def write_summary(output_root: Path, rows: list[dict]) -> None:
    write_json(output_root / "decoding_ablation_summary.json", rows)

    lines = [
        "# Decoding Ablation Summary",
        "",
        "| Beam | Model | Dataset | Total | Skipped | Success | Feasibility | Optimality |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["beam"]),
                    row["model"],
                    row["dataset"],
                    str(row["total"]),
                    str(row["skipped_unreachable"]),
                    pct(row["success_rate"]),
                    pct(row["feasibility"]),
                    pct(row["optimality"]),
                ]
            )
            + " |"
        )
    lines.append("")
    (output_root / "decoding_ablation_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.eval_only and args.predict_only:
        raise SystemExit("--eval-only and --predict-only cannot be used together.")

    output_root = Path(args.output_root)
    paths = dataset_paths(args.dataset_root)
    beams = sorted(set(args.beams))

    for beam in beams:
        if beam < 1:
            raise SystemExit(f"beam size must be >= 1, got {beam}")
        for model in args.models:
            for dataset_key in args.datasets:
                source_data = paths[dataset_key]
                if not source_data.exists():
                    raise SystemExit(f"missing dataset: {source_data}")
                test_data = prepare_test_data(source_data, dataset_key, output_root, args.limit)
                predictions = prediction_path(output_root, beam, model, dataset_key)
                metrics = metrics_path(output_root, beam, model, dataset_key)
                details = details_path(output_root, beam, model, dataset_key)

                run_prediction(args, beam, model, dataset_key, test_data, predictions)
                if not args.predict_only:
                    if not predictions.exists():
                        raise SystemExit(f"missing predictions for eval: {predictions}")
                    run_eval(predictions, test_data, details, metrics)

    if not args.predict_only:
        rows = collect_summary(output_root, beams, args.models, args.datasets)
        write_summary(output_root, rows)
        print(f"wrote summary under {output_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
