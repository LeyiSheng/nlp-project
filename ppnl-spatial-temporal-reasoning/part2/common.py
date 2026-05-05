#!/usr/bin/env python3
"""Shared utilities for PPNL Part 2 experiments."""

from __future__ import annotations

import json
import random
import re
from collections import deque
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]

DATASETS = {
    "seen_6x6": REPO_ROOT / "single_goal" / "1_goals_test_seen_6x6_samples.json",
    "unseen_5x5": REPO_ROOT / "single_goal" / "1_goals_test_unseen_5x5_samples.json",
    "unseen_7x7": REPO_ROOT / "single_goal" / "1_goals_test_unseen_7x7_samples.json",
    "more_obstacles": REPO_ROOT
    / "single_goal"
    / "1_goals_test_unseen_6x6more_obstacles_samples.json",
}

MODEL_SUBFOLDERS = ("t5-small-sg6x6", "t5-base-sg6x6", "bart-base-sg6x6")

ACTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


def load_json(path: str | Path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def find_cell(grid: list[list[int]], value: int) -> tuple[int, int]:
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == value:
                return row_idx, col_idx
    raise ValueError(f"cell value {value} not found")


def shortest_distance(grid: list[list[int]]) -> int | None:
    start = find_cell(grid, 2)
    goal = find_cell(grid, 3)
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


def is_reachable(sample: dict) -> bool:
    if "Goal not reachable" in sample.get("agent_as_a_point", ""):
        return False
    return shortest_distance(sample["world"]) is not None


def obstacle_count(grid: list[list[int]]) -> int:
    return sum(1 for row in grid for cell in row if cell == 1)


def sample_bucket(sample: dict) -> str:
    grid = sample["world"]
    distance = shortest_distance(grid)
    if distance is None:
        length_bucket = "unreachable"
    elif distance <= 4:
        length_bucket = "short"
    elif distance <= 8:
        length_bucket = "medium"
    else:
        length_bucket = "long"

    cells = len(grid) * len(grid[0])
    density = obstacle_count(grid) / cells
    density_bucket = "dense" if density >= 0.12 else "sparse"
    return f"{len(grid)}x{len(grid[0])}_{length_bucket}_{density_bucket}"


def stratified_sample(samples: list[dict], size: int, seed: int) -> list[dict]:
    reachable = [(idx, sample) for idx, sample in enumerate(samples) if is_reachable(sample)]
    if len(reachable) <= size:
        return [dict(sample, part2_original_idx=idx) for idx, sample in reachable]

    rng = random.Random(seed)
    buckets: dict[str, list[tuple[int, dict]]] = {}
    for item in reachable:
        buckets.setdefault(sample_bucket(item[1]), []).append(item)

    for items in buckets.values():
        rng.shuffle(items)

    bucket_names = sorted(buckets)
    selected: list[tuple[int, dict]] = []
    while len(selected) < size and any(buckets.values()):
        for name in bucket_names:
            if len(selected) >= size:
                break
            if buckets[name]:
                selected.append(buckets[name].pop())

    selected.sort(key=lambda item: item[0])
    return [dict(sample, part2_original_idx=idx) for idx, sample in selected]


def parse_actions(text: str) -> list[str]:
    words = re.findall(r"[a-z]+", text.lower())
    if all(word in ACTIONS for word in words):
        return words

    compact = "".join(words)
    actions = []
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
            pos += 1
    return actions


def extract_action_sequence(text: str) -> str:
    """Normalize plain, CoT, or ReAct text to an action-only sequence."""
    if not text:
        return ""

    candidates = []
    for marker in (
        "Therefore, my action sequence is:",
        "Therefore my action sequence is:",
        "action sequence is:",
        "Actions:",
        "Act:",
    ):
        if marker.lower() in text.lower():
            match = re.search(re.escape(marker), text, flags=re.IGNORECASE)
            if match:
                candidates.append(text[match.end() :])

    act_lines = re.findall(r"^Act\s+\d+\s*:\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE)
    candidates.extend(act_lines)
    candidates.append(text)

    best = max((parse_actions(candidate) for candidate in candidates), key=len, default=[])
    return " ".join(best)


def execute_action_prefix(grid: list[list[int]], actions: Iterable[str]) -> tuple[list[str], str, tuple[int, int]]:
    """Execute until the first invalid action and return the feasible prefix."""
    position = find_cell(grid, 2)
    executed: list[str] = []
    for action in actions:
        if action not in ACTIONS:
            return executed, "invalid_action", position
        d_row, d_col = ACTIONS[action]
        nxt = (position[0] + d_row, position[1] + d_col)
        if not (0 <= nxt[0] < len(grid) and 0 <= nxt[1] < len(grid[0])):
            return executed, "out_of_bounds", position
        if grid[nxt[0]][nxt[1]] == 1:
            return executed, "obstacle", position
        executed.append(action)
        position = nxt
    return executed, "", position


def dataset_key_from_path(path: str | Path) -> str:
    stem = Path(path).stem
    for key, known_path in DATASETS.items():
        if Path(path).resolve() == known_path.resolve() or stem == known_path.stem:
            return key
    return stem
