#!/usr/bin/env python3
"""Batch evaluator for single-goal PPNL action sequences."""

import argparse
import csv
import json
import re
from collections import deque
from pathlib import Path


ACTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


def load_json_or_jsonl(path):
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def load_predictions(path):
    path = Path(path)
    if path.suffix.lower() in {".json", ".jsonl"}:
        data = load_json_or_jsonl(path)
        if isinstance(data, dict):
            for key in ("predictions", "outputs", "data"):
                if key in data:
                    data = data[key]
                    break
        predictions = []
        for item in data:
            if isinstance(item, str):
                predictions.append(item)
            elif isinstance(item, dict):
                value = None
                for key in (
                    "generated",
                    "prediction",
                    "predicted",
                    "output",
                    "plan",
                    "agent_as_a_point",
                    "target",
                ):
                    if key in item:
                        value = item[key]
                        break
                if isinstance(value, list):
                    value = value[0] if value else ""
                predictions.append(value or "")
            else:
                predictions.append("")
        return predictions
    return path.read_text(encoding="utf-8").splitlines()


def parse_actions(action_text):
    action_text = action_text.lower()
    words = re.findall(r"[a-z]+", action_text)
    if all(word in ACTIONS for word in words):
        return words, []

    compact = "".join(words)
    actions = []
    invalid = []
    pos = 0
    action_names = sorted(ACTIONS, key=len, reverse=True)
    while pos < len(compact):
        matched = None
        for action in action_names:
            if compact.startswith(action, pos):
                matched = action
                break
        if matched:
            actions.append(matched)
            pos += len(matched)
        else:
            invalid.append(compact[pos])
            pos += 1
    return actions, invalid


def find_cell(grid, value):
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == value:
                return row_idx, col_idx
    raise ValueError(f"cell value {value} not found")


def shortest_distance(grid, start, goal):
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (row, col), distance = queue.popleft()
        if (row, col) == goal:
            return distance
        for d_row, d_col in ACTIONS.values():
            nxt = (row + d_row, col + d_col)
            if (
                0 <= nxt[0] < len(grid)
                and 0 <= nxt[1] < len(grid[0])
                and grid[nxt[0]][nxt[1]] != 1
                and nxt not in visited
            ):
                visited.add(nxt)
                queue.append((nxt, distance + 1))
    return None


def execute(grid, actions):
    position = find_cell(grid, 2)
    goal = find_cell(grid, 3)
    trace = [position]

    for action in actions:
        d_row, d_col = ACTIONS[action]
        nxt = (position[0] + d_row, position[1] + d_col)
        if not (0 <= nxt[0] < len(grid) and 0 <= nxt[1] < len(grid[0])):
            return {
                "feasible": False,
                "success": False,
                "end": position,
                "error": "out_of_bounds",
                "trace": trace,
            }
        if grid[nxt[0]][nxt[1]] == 1:
            return {
                "feasible": False,
                "success": False,
                "end": position,
                "error": "obstacle",
                "trace": trace,
            }
        position = nxt
        trace.append(position)

    return {
        "feasible": True,
        "success": position == goal,
        "end": position,
        "error": "",
        "trace": trace,
    }


def evaluate_item(sample, prediction):
    grid = sample["world"]
    actions, invalid_tokens = parse_actions(prediction)
    start = find_cell(grid, 2)
    goal = find_cell(grid, 3)
    optimal_len = shortest_distance(grid, start, goal)
    if invalid_tokens:
        result = {
            "feasible": False,
            "success": False,
            "end": start,
            "error": "invalid_action",
            "trace": [start],
        }
    else:
        result = execute(grid, actions)
    action_len = len(actions)
    optimal = result["success"] and optimal_len is not None and action_len == optimal_len

    return {
        "prediction": prediction,
        "actions": " ".join(actions),
        "action_count": action_len,
        "optimal_length": optimal_len,
        "success": result["success"],
        "feasible": result["feasible"],
        "optimal": optimal,
        "end": list(result["end"]),
        "error": result["error"],
    }


def rate(rows, key):
    if not rows:
        return 0.0
    return sum(1 for row in rows if row[key]) / len(rows)


def write_details(path, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "idx",
                "success",
                "feasible",
                "optimal",
                "action_count",
                "optimal_length",
                "end",
                "error",
                "actions",
                "prediction",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate single-goal up/down/left/right predictions."
    )
    parser.add_argument("predictions", help="JSON/JSONL/TXT model outputs, aligned by row.")
    parser.add_argument("test_data", help="Single-goal sample JSON with world grids.")
    parser.add_argument("--details", help="Optional CSV path for per-example results.")
    parser.add_argument("--json", action="store_true", help="Print metrics as JSON.")
    args = parser.parse_args()

    predictions = load_predictions(args.predictions)
    samples = load_json_or_jsonl(args.test_data)
    if len(predictions) != len(samples):
        raise SystemExit(
            f"prediction/test size mismatch: {len(predictions)} vs {len(samples)}"
        )

    rows = []
    skipped = 0
    for idx, (sample, prediction) in enumerate(zip(samples, predictions)):
        if (
            "Goal not reachable" in sample.get("agent_as_a_point", "")
            or shortest_distance(sample["world"], find_cell(sample["world"], 2), find_cell(sample["world"], 3)) is None
        ):
            skipped += 1
            continue
        row = evaluate_item(sample, prediction)
        row["idx"] = idx
        rows.append(row)

    metrics = {
        "total_input": len(samples),
        "total": len(rows),
        "skipped_unreachable": skipped,
        "success_rate": rate(rows, "success"),
        "feasibility": rate(rows, "feasible"),
        "optimality": rate(rows, "optimal"),
    }

    if args.details:
        write_details(args.details, rows)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        for key, value in metrics.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
