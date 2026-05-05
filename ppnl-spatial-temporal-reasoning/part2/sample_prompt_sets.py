#!/usr/bin/env python3
"""Create deterministic reachable samples for Part 2 prompting."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import DATASETS, load_json, shortest_distance, stratified_sample, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="results/part2/prompt_samples")
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--seed", type=int, default=2026)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    manifest = {
        "seed": args.seed,
        "sample_size": args.sample_size,
        "datasets": {},
    }

    for key, path in DATASETS.items():
        samples = load_json(path)
        sampled = stratified_sample(samples, args.sample_size, args.seed)
        for sample in sampled:
            sample["part2_shortest_distance"] = shortest_distance(sample["world"])
        out_path = output_dir / f"{key}_sample.json"
        write_json(out_path, sampled)
        manifest["datasets"][key] = {
            "source": str(path),
            "output": str(out_path),
            "source_count": len(samples),
            "sample_count": len(sampled),
        }
        print(f"{key}: sampled {len(sampled)} from {len(samples)} -> {out_path}")

    write_json(output_dir / "manifest.json", manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
