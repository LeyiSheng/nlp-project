# PPNL Part 2 Summary

This report compares Part 1 fine-tuned Seq2Seq models with Part 2 prompting strategies using the same single-goal executor metrics: success rate, feasibility, and optimality.

Prompting uses official OpenAI API model `gpt-5-mini`, temperature `0`, and deterministic reachable samples of 100 examples per dataset with seed `2026`.

## Fine-Tuned Models: Full Test Sets

| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| t5-small-sg6x6 | seen_6x6 | pending | pending | pending | pending | pending |
| t5-small-sg6x6 | unseen_5x5 | pending | pending | pending | pending | pending |
| t5-small-sg6x6 | unseen_7x7 | pending | pending | pending | pending | pending |
| t5-small-sg6x6 | more_obstacles | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | seen_6x6 | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | unseen_5x5 | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | unseen_7x7 | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | more_obstacles | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | seen_6x6 | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | unseen_5x5 | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | unseen_7x7 | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | more_obstacles | pending | pending | pending | pending | pending |

## Fine-Tuned Models: Prompt Samples

| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| t5-small-sg6x6 | seen_6x6 | pending | pending | pending | pending | pending |
| t5-small-sg6x6 | unseen_5x5 | pending | pending | pending | pending | pending |
| t5-small-sg6x6 | unseen_7x7 | pending | pending | pending | pending | pending |
| t5-small-sg6x6 | more_obstacles | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | seen_6x6 | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | unseen_5x5 | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | unseen_7x7 | pending | pending | pending | pending | pending |
| t5-base-sg6x6 | more_obstacles | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | seen_6x6 | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | unseen_5x5 | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | unseen_7x7 | pending | pending | pending | pending | pending |
| bart-base-sg6x6 | more_obstacles | pending | pending | pending | pending | pending |

## Prompting Strategies: Prompt Samples

| Run | Dataset | Total | Skipped | Success | Feasibility | Optimality |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| zero_shot | seen_6x6 | pending | pending | pending | pending | pending |
| zero_shot | unseen_5x5 | pending | pending | pending | pending | pending |
| zero_shot | unseen_7x7 | pending | pending | pending | pending | pending |
| zero_shot | more_obstacles | pending | pending | pending | pending | pending |
| few_shot | seen_6x6 | pending | pending | pending | pending | pending |
| few_shot | unseen_5x5 | pending | pending | pending | pending | pending |
| few_shot | unseen_7x7 | pending | pending | pending | pending | pending |
| few_shot | more_obstacles | pending | pending | pending | pending | pending |
| cot | seen_6x6 | pending | pending | pending | pending | pending |
| cot | unseen_5x5 | pending | pending | pending | pending | pending |
| cot | unseen_7x7 | pending | pending | pending | pending | pending |
| cot | more_obstacles | pending | pending | pending | pending | pending |
| react | seen_6x6 | pending | pending | pending | pending | pending |
| react | unseen_5x5 | pending | pending | pending | pending | pending |
| react | unseen_7x7 | pending | pending | pending | pending | pending |
| react | more_obstacles | pending | pending | pending | pending | pending |

## Failure Patterns

Failure analysis is pending. Run `python part2/analyze_failures.py`.

## Notes

- `evaluate/evaluate_sg.py` is the canonical evaluator for all reported metrics.
- Full Seq2Seq OOD prediction can be slow on CPU; use `--device cuda` and tune `--batch-size` on GPU machines.
- Missing cells marked `pending` mean the corresponding prediction/evaluation artifact has not been generated yet.
