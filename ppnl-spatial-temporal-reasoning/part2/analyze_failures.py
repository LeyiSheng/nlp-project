#!/usr/bin/env python3
"""Aggregate Part 2 executor details into failure-pattern summaries."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from common import write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roots", nargs="+", default=["results/part2/finetuned", "results/part2/prompting"])
    parser.add_argument("--output-json", default="results/part2/failure_analysis.json")
    parser.add_argument("--output-md", default="results/part2/failure_analysis.md")
    parser.add_argument("--examples-per-kind", type=int, default=3)
    return parser.parse_args()


def boolish(value: str) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def classify(row: dict) -> str:
    if boolish(row.get("success")) and not boolish(row.get("optimal")):
        return "non_optimal_success"
    if boolish(row.get("success")):
        return "success"
    error = row.get("error") or ""
    if error:
        return error
    if boolish(row.get("feasible")):
        return "feasible_not_goal"
    return "unknown_failure"


def parse_detail_path(path: Path) -> tuple[str, str, str]:
    run_name = path.parent.name
    dataset = path.name.removesuffix("_details.csv")
    root_name = path.parent.parent.name
    return root_name, run_name, dataset


def read_details(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def make_analysis(paths: list[Path], examples_per_kind: int) -> dict:
    analysis = {
        "runs": {},
        "examples": defaultdict(list),
    }
    for path in paths:
        root_name, run_name, dataset = parse_detail_path(path)
        rows = read_details(path)
        key = f"{root_name}/{run_name}/{dataset}"
        counts = Counter(classify(row) for row in rows)
        analysis["runs"][key] = {
            "root": root_name,
            "run": run_name,
            "dataset": dataset,
            "total": len(rows),
            "counts": dict(sorted(counts.items())),
        }
        for row in rows:
            kind = classify(row)
            if kind == "success":
                continue
            ex_key = f"{key}/{kind}"
            if len(analysis["examples"][ex_key]) < examples_per_kind:
                analysis["examples"][ex_key].append(
                    {
                        "idx": row.get("idx"),
                        "kind": kind,
                        "action_count": row.get("action_count"),
                        "optimal_length": row.get("optimal_length"),
                        "end": row.get("end"),
                        "actions": row.get("actions"),
                        "prediction": row.get("prediction"),
                    }
                )
    analysis["examples"] = dict(analysis["examples"])
    return analysis


def write_markdown(path: Path, analysis: dict) -> None:
    lines = ["# Part 2 Failure Analysis", ""]
    lines.append("| Run | Total | out_of_bounds | obstacle | invalid_action | feasible_not_goal | non_optimal_success |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for key, item in sorted(analysis["runs"].items()):
        counts = item["counts"]
        lines.append(
            "| "
            + " | ".join(
                [
                    key,
                    str(item["total"]),
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
    lines.append("## Representative Examples")
    lines.append("")
    for key, examples in sorted(analysis["examples"].items()):
        lines.append(f"### {key}")
        for ex in examples:
            lines.append(
                f"- idx={ex['idx']}, actions={ex['actions']!r}, "
                f"optimal_length={ex['optimal_length']}, end={ex['end']}, prediction={ex['prediction']!r}"
            )
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    paths: list[Path] = []
    for root in args.roots:
        paths.extend(sorted(Path(root).glob("*/*_details.csv")))
    if not paths:
        raise SystemExit("No details CSV files found. Run executor evaluation first.")
    analysis = make_analysis(paths, args.examples_per_kind)
    write_json(args.output_json, analysis)
    write_markdown(Path(args.output_md), analysis)
    print(f"wrote {args.output_json} and {args.output_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
