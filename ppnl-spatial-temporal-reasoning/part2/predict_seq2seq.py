#!/usr/bin/env python3
"""Generate Seq2Seq predictions for single-goal PPNL test data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import MODEL_SUBFOLDERS, load_json, write_json


DEFAULT_MODEL_ID = "SheldonLI329/ppnl-baselines"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument(
        "--model-path",
        default=None,
        help="Optional local checkpoint directory. When set, --model-id and --model-subfolder are ignored for loading.",
    )
    parser.add_argument(
        "--hf-model-id",
        default=None,
        help=(
            "HuggingFace pretrained checkpoint id without fine-tuning "
            "(e.g. tiny, t5-small, facebook/bart-base). "
            "When set, --model-id and --model-subfolder are ignored for weight loading."
        ),
    )
    parser.add_argument(
        "--model-subfolder",
        default=None,
        choices=MODEL_SUBFOLDERS,
        help="Fine-tuned subfolder on HuggingFace Hub (required unless --model-path or --hf-model-id).",
    )
    parser.add_argument("--test-data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="auto", help="'auto', 'cpu', 'cuda', or cuda device like cuda:0")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=128, help="Generation max length for action output.")
    parser.add_argument("--num-beams", type=int, default=1)
    parser.add_argument("--limit", type=int, help="Optional smoke-test limit.")
    return parser.parse_args()


def resolve_device(device: str):
    import torch

    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device


def batched(items: list[str], batch_size: int):
    for start in range(0, len(items), batch_size):
        yield start, items[start : start + batch_size]


def main() -> int:
    args = parse_args()
    try:
        import torch
        from transformers import AutoConfig, AutoModelForSeq2SeqLM, AutoTokenizer
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency. Install project requirements plus transformers/datasets first."
        ) from exc

    samples = load_json(args.test_data)
    if args.limit is not None:
        samples = samples[: args.limit]

    questions = [sample["nl_description"] for sample in samples]
    device = resolve_device(args.device)

    if args.model_path:
        load_source = args.model_path
        load_kwargs = {}
    elif args.hf_model_id:
        load_source = args.hf_model_id
        load_kwargs = {}
    else:
        if not args.model_subfolder:
            raise SystemExit(
                "Provide --model-subfolder for Hub fine-tuned weights, "
                "or --model-path / --hf-model-id for local / pretrained loading."
            )
        load_source = args.model_id
        load_kwargs = {"subfolder": args.model_subfolder}

    config = AutoConfig.from_pretrained(load_source, **load_kwargs)
    if hasattr(config, "early_stopping"):
        config.early_stopping = False

    tokenizer = AutoTokenizer.from_pretrained(load_source, use_fast=True, **load_kwargs)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        load_source,
        **load_kwargs,
        config=config,
    )
    if hasattr(model.generation_config, "early_stopping"):
        model.generation_config.early_stopping = False
    model.to(device)
    model.eval()

    predictions: list[str] = []
    with torch.no_grad():
        for start, batch in batched(questions, args.batch_size):
            encoded = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=1024)
            encoded = {key: value.to(device) for key, value in encoded.items()}
            generated = model.generate(
                **encoded,
                max_length=args.max_new_tokens,
                num_beams=args.num_beams,
            )
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            predictions.extend(decoded)
            print(f"generated {min(start + len(batch), len(questions))}/{len(questions)}", flush=True)

    rows = []
    for idx, (sample, prediction) in enumerate(zip(samples, predictions)):
        rows.append(
            {
                "idx": sample.get("part2_original_idx", idx),
                "english": sample["nl_description"],
                "ground_truth": sample.get("agent_as_a_point", ""),
                "prediction": prediction,
                "world": sample["world"],
            }
        )
    write_json(args.output, rows)
    print(f"wrote {len(rows)} predictions to {Path(args.output)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
