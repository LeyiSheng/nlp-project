# PPNL Part 2 Summary

This report compares Part 1 fine-tuned Seq2Seq models with Part 2 prompting strategies using the same single-goal executor metrics: success rate, feasibility, and optimality.

Prompting uses official OpenAI API model `gpt-5-mini`, temperature `0`, and deterministic reachable samples of 100 examples per dataset with seed `2026`.

## Fine-Tuned Models: Full Test Sets

| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| t5-small-sg6x6 | seen_6x6 | 1992 | 12 | 95.5% | 95.6% | 95.4% |
| t5-small-sg6x6 | unseen_5x5 | 3701 | 49 | 94.9% | 94.9% | 94.8% |
| t5-small-sg6x6 | unseen_7x7 | 3744 | 6 | 54.5% | 86.3% | 54.1% |
| t5-small-sg6x6 | more_obstacles | 4141 | 359 | 81.7% | 81.7% | 81.6% |
| t5-base-sg6x6 | seen_6x6 | 1992 | 12 | 95.8% | 96.0% | 95.8% |
| t5-base-sg6x6 | unseen_5x5 | 3701 | 49 | 95.1% | 95.1% | 95.1% |
| t5-base-sg6x6 | unseen_7x7 | 3744 | 6 | 54.5% | 88.2% | 54.2% |
| t5-base-sg6x6 | more_obstacles | 4141 | 359 | 82.9% | 83.0% | 82.8% |
| bart-base-sg6x6 | seen_6x6 | 1992 | 12 | 86.1% | 95.1% | 85.5% |
| bart-base-sg6x6 | unseen_5x5 | 3701 | 49 | 91.7% | 95.4% | 91.7% |
| bart-base-sg6x6 | unseen_7x7 | 3744 | 6 | 48.2% | 89.6% | 47.3% |
| bart-base-sg6x6 | more_obstacles | 4141 | 359 | 13.6% | 24.1% | 13.3% |

## Fine-Tuned Models: Prompt Samples

| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| t5-small-sg6x6 | seen_6x6 | 100 | 0 | 82.0% | 82.0% | 82.0% |
| t5-small-sg6x6 | unseen_5x5 | 100 | 0 | 79.0% | 80.0% | 79.0% |
| t5-small-sg6x6 | unseen_7x7 | 100 | 0 | 49.0% | 80.0% | 49.0% |
| t5-small-sg6x6 | more_obstacles | 100 | 0 | 59.0% | 59.0% | 59.0% |
| t5-base-sg6x6 | seen_6x6 | 100 | 0 | 84.0% | 84.0% | 83.0% |
| t5-base-sg6x6 | unseen_5x5 | 100 | 0 | 80.0% | 80.0% | 80.0% |
| t5-base-sg6x6 | unseen_7x7 | 100 | 0 | 49.0% | 85.0% | 49.0% |
| t5-base-sg6x6 | more_obstacles | 100 | 0 | 65.0% | 65.0% | 65.0% |
| bart-base-sg6x6 | seen_6x6 | 100 | 0 | 63.0% | 78.0% | 63.0% |
| bart-base-sg6x6 | unseen_5x5 | 100 | 0 | 68.0% | 77.0% | 68.0% |
| bart-base-sg6x6 | unseen_7x7 | 100 | 0 | 41.0% | 84.0% | 41.0% |
| bart-base-sg6x6 | more_obstacles | 100 | 0 | 6.0% | 12.0% | 5.0% |

## Prompting Strategies: Prompt Samples

| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| zero_shot | seen_6x6 | 100 | 0 | 57.0% | 100.0% | 57.0% |
| zero_shot | unseen_5x5 | 100 | 0 | 58.0% | 100.0% | 58.0% |
| zero_shot | unseen_7x7 | 100 | 0 | 74.0% | 100.0% | 74.0% |
| zero_shot | more_obstacles | 100 | 0 | 35.0% | 100.0% | 35.0% |
| few_shot | seen_6x6 | 100 | 0 | 50.0% | 100.0% | 50.0% |
| few_shot | unseen_5x5 | 100 | 0 | 66.0% | 100.0% | 65.0% |
| few_shot | unseen_7x7 | 100 | 0 | 72.0% | 100.0% | 72.0% |
| few_shot | more_obstacles | 100 | 0 | 31.0% | 100.0% | 31.0% |
| cot | seen_6x6 | 100 | 0 | 30.0% | 100.0% | 30.0% |
| cot | unseen_5x5 | 100 | 0 | 48.0% | 100.0% | 48.0% |
| cot | unseen_7x7 | 100 | 0 | 48.0% | 100.0% | 48.0% |
| cot | more_obstacles | 100 | 0 | 20.0% | 100.0% | 20.0% |
| react | seen_6x6 | 100 | 0 | 23.0% | 100.0% | 23.0% |
| react | unseen_5x5 | 100 | 0 | 23.0% | 100.0% | 23.0% |
| react | unseen_7x7 | 100 | 0 | 21.0% | 100.0% | 21.0% |
| react | more_obstacles | 100 | 0 | 10.0% | 100.0% | 10.0% |

## Failure Patterns

| Group | out_of_bounds | obstacle | invalid_action | feasible_not_goal | non_optimal_success |
| --- | ---: | ---: | ---: | ---: | ---: |
| finetuned | 1585 | 4898 | 267 | 4773 | 95 |
| finetuned_samples | 45 | 276 | 13 | 141 | 2 |
| prompting | 0 | 0 | 0 | 934 | 1 |

Representative examples are written to `results/part2/failure_analysis.md`.

## Notes

- `evaluate/evaluate_sg.py` is the canonical evaluator for all reported metrics.
- Full Seq2Seq OOD prediction can be slow on CPU; use `--device cuda` and tune `--batch-size` on GPU machines.
- Missing cells marked `pending` mean the corresponding prediction/evaluation artifact has not been generated yet.
