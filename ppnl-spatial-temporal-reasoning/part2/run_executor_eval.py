#!/usr/bin/env python3
"""Run the canonical single-goal executor evaluator for Part 2 outputs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import DATASETS, MODEL_SUBFOLDERS, REPO_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions-root", default="results/part2/finetuned")
    parser.add_argument("--output-root", default=None, help="Defaults to --predictions-root.")
    parser.add_argument("--dataset-root", default=None, help="Use sampled JSONs from this directory instead of full datasets.")
    parser.add_argument("--models", nargs="+", default=list(MODEL_SUBFOLDERS))
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS))
    parser.add_argument("--strict", action="store_true", help="Fail when an expected predictions file is missing.")
    return parser.parse_args()


def dataset_paths(dataset_root: str | None) -> dict[str, Path]:
    if dataset_root is None:
        return DATASETS
    root = Path(dataset_root)
    return {key: root / f"{key}_sample.json" for key in DATASETS}


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


def main() -> int:
    args = parse_args()
    predictions_root = Path(args.predictions_root)
    output_root = Path(args.output_root) if args.output_root else predictions_root
    paths = dataset_paths(args.dataset_root)

    missing = []
    for model in args.models:
        for dataset_key in args.datasets:
            test_data = paths[dataset_key]
            predictions = predictions_root / model / f"{dataset_key}_predictions.json"
            if not predictions.exists():
                missing.append(str(predictions))
                print(f"missing predictions: {predictions}")
                continue
            if not test_data.exists():
                raise SystemExit(f"missing test data: {test_data}")
            out_dir = output_root / model
            run_eval(
                predictions=predictions,
                test_data=test_data,
                details=out_dir / f"{dataset_key}_details.csv",
                metrics=out_dir / f"{dataset_key}_metrics.json",
            )

    if missing and args.strict:
        raise SystemExit("missing expected predictions:\n" + "\n".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
