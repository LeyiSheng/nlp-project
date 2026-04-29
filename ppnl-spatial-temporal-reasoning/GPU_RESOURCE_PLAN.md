# GPU Resource Plan

Project budget target: 50 GPU-hours.

## Account Inventory

| Member | Account / Cluster | GPU Type | Available GPU-hours | Notes |
| --- | --- | --- | ---: | --- |
| TBD | TBD | TBD | TBD | Fill before training starts |
| TBD | TBD | TBD | TBD | Fill before training starts |
| TBD | TBD | TBD | TBD | Fill before training starts |

## Proposed Budget

| Work item | GPU-hours | Owner | Output |
| --- | ---: | --- | --- |
| Environment and executor smoke tests | 0 | current local CPU run | Verified single-goal executor |
| Small training smoke run | 4 | TBD | One short T5/BART run, confirms data loader and checkpointing |
| Main 6x6 ID training | 24 | TBD | Primary checkpoint and logs |
| OOD evaluation runs | 8 | TBD | 5x5, 7x7, and denser 6x6 results |
| Reruns / failed job buffer | 10 | shared | Reserved for crashes, seed reruns, or config fixes |
| Final validation and export | 4 | TBD | Final metrics and artifacts |
| Total | 50 | shared |  |

## Operating Rules

- Record every GPU job before launch with owner, command, expected duration, and output path.
- Start with one short smoke run before any long training job.
- Keep raw synthesized datasets shared read-only; write model outputs and checkpoints to owner-specific folders.
- Stop jobs early if loss/logging or evaluator output is clearly broken.
- Preserve logs for every run so failed runs can be counted and debugged.
