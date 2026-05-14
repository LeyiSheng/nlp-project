# Decoding Strategy Ablation Plan

## Goal

This ablation tests whether the fine-tuned Seq2Seq models are limited by
generation-time decoding rather than by the learned model distribution itself.
The current fine-tuned baselines use greedy decoding (`num_beams=1`). We vary
beam size while keeping the model weights, training data, test data, and
executor metrics fixed.

## Hypothesis

Beam search may improve success by exploring alternative action sequences with
higher sequence-level probability than the greedy path. However, larger beams
may also favor longer or repetitive plans, so success can improve without a
matching gain in optimality.

## Independent Variable

`num_beams` during `model.generate`.

Recommended settings:

- `1`: greedy decoding, current baseline.
- `3`: small search budget.
- `5`: moderate search budget.
- `10`: larger search budget.

## Controlled Variables

- Model weights: `SheldonLI329/ppnl-baselines`.
- Model subfolders: `t5-small-sg6x6`, `t5-base-sg6x6`, `bart-base-sg6x6`.
- Test splits: `seen_6x6`, `unseen_5x5`, `unseen_7x7`, `more_obstacles`.
- Max generation length: 128 tokens.
- Tokenizer and model config loaded from the same Hugging Face repository.
- Evaluation: canonical `evaluate/evaluate_sg.py` executor.

## Metrics

For each `(model, dataset, beam)` combination, report:

- Success rate: the executed action sequence ends at the goal.
- Feasibility: every action stays inside bounds and avoids obstacles.
- Optimality: the successful path length matches the BFS shortest path.
- Failure details: per-example CSV from the executor.

## Expected Analysis

1. Compare each beam setting against beam 1 for the same model and dataset.
2. Check whether success gains are accompanied by optimality gains.
3. Inspect whether larger beams reduce obstacle/out-of-bounds errors or only
   change feasible-but-not-goal failures.
4. Report whether the best beam differs between ID (`seen_6x6`) and OOD
   (`unseen_7x7`, `more_obstacles`) settings.

## How To Run

Full ablation:

```bash
python part2/run_decoding_ablation.py \
  --device cuda \
  --batch-size 16 \
  --beams 1 3 5 10
```

Smoke test:

```bash
python part2/run_decoding_ablation.py \
  --models t5-base-sg6x6 \
  --datasets unseen_7x7 \
  --beams 1 3 \
  --limit 20 \
  --device auto
```

Use sampled prompt sets instead of full test sets:

```bash
python part2/run_decoding_ablation.py \
  --dataset-root results/part2/prompt_samples \
  --beams 1 3 5 10
```

## Outputs

All outputs are written under `results/part2/decoding_ablation/`:

- `beam_<N>/<model>/<dataset>_predictions.json`
- `beam_<N>/<model>/<dataset>_metrics.json`
- `beam_<N>/<model>/<dataset>_details.csv`
- `decoding_ablation_summary.json`
- `decoding_ablation_summary.md`
