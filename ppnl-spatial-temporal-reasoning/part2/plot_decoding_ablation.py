#!/usr/bin/env python3
"""Plot decoding (beam-search) ablation results from decoding_ablation_summary.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from matplotlib.ticker import MultipleLocator

from common import REPO_ROOT


DATASET_LABELS = {
    "seen_6x6": "Seen 6×6",
    "unseen_5x5": "Unseen 5×5",
    "unseen_7x7": "Unseen 7×7",
    "more_obstacles": "More obstacles",
}

MODEL_LABELS = {
    "t5-small-sg6x6": "T5-small",
    "t5-base-sg6x6": "T5-base",
    "bart-base-sg6x6": "BART-base",
}

MODEL_ORDER = ("t5-small-sg6x6", "t5-base-sg6x6", "bart-base-sg6x6")
DATASET_ORDER = ("seen_6x6", "unseen_5x5", "unseen_7x7", "more_obstacles")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--summary",
        default="results/part2/decoding_ablation/decoding_ablation_summary.json",
        help="Path to decoding_ablation_summary.json",
    )
    p.add_argument(
        "--out-dir",
        default="results/part2/decoding_ablation/figures",
        help="Directory for PNG/PDF outputs",
    )
    p.add_argument("--dpi", type=int, default=200)
    p.add_argument(
        "--full-y",
        action="store_true",
        help="Use 0--100%% on y-axis; default is 50--100%% with 5%% grid spacing.",
    )
    return p.parse_args()


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Summary not found: {path}. Run run_decoding_ablation.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def nest(rows: list[dict]) -> dict[tuple[str, str], dict[int, dict]]:
    """Build (model, dataset) -> beam -> full summary row."""
    out = defaultdict(dict)
    for r in rows:
        out[(r["model"], r["dataset"])][int(r["beam"])] = r
    return out


def plot_metric(
    rows: list[dict],
    metric_key: str,
    title: str,
    ylabel: str,
    out_path: Path,
    dpi: int,
    *,
    full_y: bool,
) -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    nested = nest(rows)
    beams = sorted({int(r["beam"]) for r in rows})
    n_beams = len(beams)
    n_models = len(MODEL_ORDER)
    x = np.arange(n_beams, dtype=float)
    # Total group width ~0.72; each model gets a slice
    total_width = 0.72
    bar_width = total_width / n_models

    fig, axes = plt.subplots(2, 2, figsize=(10, 7.2), sharex=True)
    fig.suptitle(title, fontsize=12, fontweight="bold")
    axes_flat = axes.flatten()

    colors = {"t5-small-sg6x6": "#1f77b4", "t5-base-sg6x6": "#ff7f0e", "bart-base-sg6x6": "#2ca02c"}

    for ax, ds in zip(axes_flat, DATASET_ORDER):
        for model_idx, model in enumerate(MODEL_ORDER):
            offset = bar_width * (model_idx - (n_models - 1) / 2)
            heights = []
            for b in beams:
                cell = nested.get((model, ds), {}).get(b)
                heights.append(100.0 * float(cell[metric_key]) if cell is not None else float("nan"))
            ax.bar(
                x + offset,
                heights,
                bar_width,
                label=MODEL_LABELS[model],
                color=colors[model],
                edgecolor="white",
                linewidth=0.6,
            )
        ax.set_title(DATASET_LABELS[ds])
        if full_y:
            ax.set_ylim(0, 100)
        else:
            ax.set_ylim(50, 100)
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.grid(True, axis="y", alpha=0.3, which="major")
        ax.set_xticks(x)
        ax.set_xticklabels([str(b) for b in beams])

    for ax in axes[1, :]:
        ax.set_xlabel("Beam size")
    for ax in axes[:, 0]:
        ax.set_ylabel(ylabel)

    handles, labels = axes_flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.02), frameon=True)
    plt.tight_layout(rect=(0, 0.06, 1, 0.96))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path.with_suffix(".png"), dpi=dpi, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path.with_suffix('.png')} and .pdf")


def main() -> int:
    args = parse_args()
    root = REPO_ROOT
    summary_path = Path(args.summary)
    if not summary_path.is_absolute():
        summary_path = root / summary_path
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = root / out_dir

    rows = load_rows(summary_path)

    plot_metric(
        rows,
        "success_rate",
        "Decoding ablation: success rate vs. beam size",
        "Success (%)",
        out_dir / "decoding_ablation_success",
        args.dpi,
        full_y=args.full_y,
    )
    plot_metric(
        rows,
        "feasibility",
        "Decoding ablation: feasibility vs. beam size",
        "Feasibility (%)",
        out_dir / "decoding_ablation_feasibility",
        args.dpi,
        full_y=args.full_y,
    )
    plot_metric(
        rows,
        "optimality",
        "Decoding ablation: optimality vs. beam size",
        "Optimality (%)",
        out_dir / "decoding_ablation_optimality",
        args.dpi,
        full_y=args.full_y,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
