#!/usr/bin/env python3
"""Run OpenAI prompting baselines for sampled PPNL Part 2 data."""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from common import ACTIONS, DATASETS, REPO_ROOT, extract_action_sequence, find_cell, load_json, parse_actions, write_json


STRATEGIES = ("zero_shot", "few_shot", "cot", "react")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples-dir", default="results/part2/prompt_samples")
    parser.add_argument("--output-dir", default="results/part2/prompting")
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--base-url", default=None, help="Optional OpenAI-compatible base URL.")
    parser.add_argument("--strategies", nargs="+", default=list(STRATEGIES), choices=STRATEGIES)
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS))
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--react-turns", type=int, default=3)
    parser.add_argument("--limit", type=int, help="Optional smoke-test limit per dataset.")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls.")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def load_prompt(name: str) -> str:
    return (REPO_ROOT / "ICL" / "prompts" / name).read_text(encoding="utf-8").strip()


def build_prompt(strategy: str, task: str) -> str:
    if strategy == "zero_shot":
        return (
            "Provide only a sequence of actions to navigate the world and reach the goal. "
            "Use only these tokens separated by spaces: up, down, left, right.\n"
            "(0,0) is the upper-left corner. Rows increase downward and columns increase to the right.\n"
            "###\n"
            f"Task: {task}\n"
            "Actions:"
        )
    if strategy == "few_shot":
        prompt = load_prompt("few-shot-prompts-single_goal_5.txt")
        return f"{prompt}\n###\nTask: {task}\nActions:"
    if strategy == "cot":
        prompt = load_prompt("CoT-SG.txt")
        return f"{prompt}\nTask: {task}\nActions:"
    if strategy == "react":
        prompt = load_prompt("react-prompt.txt")
        return (
            f"{prompt}\n###\nTask: {task}\n"
            "Thought 1: Think briefly about the shortest feasible path.\n"
            "Act 1:"
        )
    raise ValueError(strategy)


def make_client(args: argparse.Namespace):
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required for prompting experiments.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("Missing dependency: install openai>=1.0.0 before running prompting.") from exc

    kwargs = {}
    if args.base_url:
        kwargs["base_url"] = args.base_url
    return OpenAI(**kwargs)


def chat_completion(client, args: argparse.Namespace, messages: list[dict[str, str]]) -> str:
    last_error = None
    for attempt in range(args.retries):
        try:
            kwargs = {
                "model": args.model,
                "messages": messages,
                "max_completion_tokens": args.max_tokens,
            }
            if args.temperature is not None:
                kwargs["temperature"] = args.temperature
            try:
                response = client.chat.completions.create(**kwargs)
            except Exception as exc:
                if "temperature" not in str(exc).lower():
                    raise
                kwargs.pop("temperature", None)
                response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as exc:
            last_error = exc
            wait = min(60, 2**attempt)
            print(f"API call failed on attempt {attempt + 1}/{args.retries}: {exc}; sleeping {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"API call failed after {args.retries} attempts: {last_error}")


def execute_from_position(grid: list[list[int]], actions: list[str], start: tuple[int, int]) -> tuple[list[str], str, tuple[int, int], str]:
    position = start
    executed = []
    for step, action in enumerate(actions, start=1):
        if action not in ACTIONS:
            return executed, "invalid_action", position, f"Action '{action}' is invalid."
        d_row, d_col = ACTIONS[action]
        nxt = (position[0] + d_row, position[1] + d_col)
        if not (0 <= nxt[0] < len(grid) and 0 <= nxt[1] < len(grid[0])):
            return (
                executed,
                "out_of_bounds",
                position,
                f"After {step - 1} executed steps, I am at {position}. The next action leaves the grid.",
            )
        if grid[nxt[0]][nxt[1]] == 1:
            return (
                executed,
                "obstacle",
                position,
                f"After {step - 1} executed steps, I am at {position}. The next action hits an obstacle at {nxt}.",
            )
        executed.append(action)
        position = nxt
    if grid[position[0]][position[1]] == 3:
        return executed, "success", position, f"Performing the action sequence leads to {position}. The task has been solved."
    return executed, "not_solved", position, f"Performing the action sequence leads to {position}. The task has not been solved yet."


def run_direct_strategy(client, args: argparse.Namespace, strategy: str, sample: dict) -> dict:
    prompt = build_prompt(strategy, sample["nl_description"])
    response = chat_completion(client, args, [{"role": "user", "content": prompt}])
    prediction = extract_action_sequence(response)
    return {
        "raw_response": response,
        "prediction": prediction,
        "prompt": prompt,
    }


def run_react_strategy(client, args: argparse.Namespace, sample: dict) -> dict:
    task = sample["nl_description"]
    grid = sample["world"]
    position = find_cell(grid, 2)
    executed_all: list[str] = []
    transcript = []

    first_prompt = build_prompt("react", task)
    messages = [{"role": "user", "content": first_prompt}]
    for turn in range(1, args.react_turns + 1):
        response = chat_completion(client, args, messages)
        actions = parse_actions(extract_action_sequence(response))
        executed, status, position, observation = execute_from_position(grid, actions, position)
        executed_all.extend(executed)
        transcript.append(
            {
                "turn": turn,
                "response": response,
                "actions": " ".join(actions),
                "executed": " ".join(executed),
                "status": status,
                "observation": observation,
            }
        )
        if status == "success":
            break
        messages.append({"role": "assistant", "content": response})
        messages.append(
            {
                "role": "user",
                "content": (
                    f"Obs {turn}: {observation}\n"
                    f"Continue from current position {position}. Respond with Thought {turn + 1} and Act {turn + 1}."
                ),
            }
        )

    return {
        "raw_response": transcript[-1]["response"] if transcript else "",
        "prediction": " ".join(executed_all),
        "prompt": first_prompt,
        "react_transcript": transcript,
    }


def load_existing(path: Path) -> list[dict]:
    if path.exists():
        return load_json(path)
    return []


def run_strategy_dataset(client, args: argparse.Namespace, strategy: str, dataset_key: str) -> None:
    sample_path = Path(args.samples_dir) / f"{dataset_key}_sample.json"
    samples = load_json(sample_path)
    if args.limit is not None:
        samples = samples[: args.limit]

    out_path = Path(args.output_dir) / strategy / f"{dataset_key}_predictions.json"
    rows = [] if args.overwrite else load_existing(out_path)
    done = {row.get("sample_idx") for row in rows}

    for sample_idx, sample in enumerate(samples):
        if sample_idx in done:
            continue
        if strategy == "react":
            result = run_react_strategy(client, args, sample)
        else:
            result = run_direct_strategy(client, args, strategy, sample)

        row = {
            "sample_idx": sample_idx,
            "idx": sample.get("part2_original_idx", sample_idx),
            "english": sample["nl_description"],
            "ground_truth": sample.get("agent_as_a_point", ""),
            "prediction": result["prediction"],
            "world": sample["world"],
            "model": args.model,
            "strategy": strategy,
            "raw_response": result["raw_response"],
        }
        if strategy == "react":
            row["react_transcript"] = result["react_transcript"]
        rows.append(row)
        write_json(out_path, rows)
        print(f"{strategy}/{dataset_key}: {len(rows)}/{len(samples)}")
        if args.sleep:
            time.sleep(args.sleep)


def main() -> int:
    args = parse_args()
    client = make_client(args)
    for strategy in args.strategies:
        for dataset_key in args.datasets:
            run_strategy_dataset(client, args, strategy, dataset_key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
