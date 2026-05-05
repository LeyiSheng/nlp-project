#!/usr/bin/env python3
"""Write PART2_SUMMARY.md from generated Part 2 artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import DATASETS, MODEL_SUBFOLDERS


PROMPT_STRATEGIES = ("zero_shot", "few_shot", "cot", "react")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", default="results/part2")
    parser.add_argument("--output", default="PART2_SUMMARY.md")
    return parser.parse_args()


def load_metrics(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def pct(value) -> str:
    if value is None:
        return "pending"
    return f"{100 * float(value):.1f}%"


def metric_table(title: str, root: Path, runs: tuple[str, ...] | list[str], datasets: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.append("| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for run in runs:
        for dataset in datasets:
            metrics = load_metrics(root / run / f"{dataset}_metrics.json")
            if metrics is None:
                lines.append(f"| {run} | {dataset} | pending | pending | pending | pending | pending |")
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        run,
                        dataset,
                        str(metrics.get("total", "pending")),
                        str(metrics.get("skipped_unreachable", "pending")),
                        pct(metrics.get("success_rate")),
                        pct(metrics.get("feasibility")),
                        pct(metrics.get("optimality")),
                    ]
                )
                + " |"
            )
    lines.append("")
    return lines


def failure_highlights(path: Path) -> list[str]:
    if not path.exists():
        return ["## Failure Patterns", "", "Failure analysis is pending. Run `python part2/analyze_failures.py`.", ""]
    analysis = json.loads(path.read_text(encoding="utf-8"))
    aggregate = {}
    for item in analysis.get("runs", {}).values():
        root = item["root"]
        counts = aggregate.setdefault(root, {})
        for key, value in item["counts"].items():
            counts[key] = counts.get(key, 0) + value
    lines = ["## Failure Patterns", ""]
    lines.append("| Group | out_of_bounds | obstacle | invalid_action | feasible_not_goal | non_optimal_success |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for root, counts in sorted(aggregate.items()):
        lines.append(
            "| "
            + " | ".join(
                [
                    root,
                    str(counts.get("out_of_bounds", 0)),
                    str(counts.get("obstacle", 0)),
                    str(counts.get("invalid_action", 0)),
                    str(counts.get("feasible_not_goal", 0)),
                    str(counts.get("non_optimal_success", 0)),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("Representative examples are written to `results/part2/failure_analysis.md`.")
    lines.append("")
    return lines


def main() -> int:
    args = parse_args()
    root = Path(args.results_root)
    datasets = list(DATASETS)
    lines = [
        "# PPNL Part 2 Summary",
        "",
        "This report compares Part 1 fine-tuned Seq2Seq models with Part 2 prompting strategies using the same single-goal executor metrics: success rate, feasibility, and optimality.",
        "",
        "Prompting uses official OpenAI API model `gpt-5-mini`, temperature `0`, and deterministic reachable samples of 100 examples per dataset with seed `2026`.",
        "",
    ]
    lines.extend(metric_table("Fine-Tuned Models: Full Test Sets", root / "finetuned", MODEL_SUBFOLDERS, datasets))
    lines.extend(metric_table("Fine-Tuned Models: Prompt Samples", root / "finetuned_samples", MODEL_SUBFOLDERS, datasets))
    lines.extend(metric_table("Prompting Strategies: Prompt Samples", root / "prompting", PROMPT_STRATEGIES, datasets))
    lines.extend(failure_highlights(root / "failure_analysis.json"))
    lines.extend(
        [
            "## Notes",
            "",
            "- `evaluate/evaluate_sg.py` is the canonical evaluator for all reported metrics.",
            "- Full Seq2Seq OOD prediction can be slow on CPU; use `--device cuda` and tune `--batch-size` on GPU machines.",
            "- Missing cells marked `pending` mean the corresponding prediction/evaluation artifact has not been generated yet.",
            "",
        ]
    )
    Path(args.output).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
