In order to run the training. You need to first convert your data into the appropriate format. To do this, you can run the following

``python convert.py $path_to_training_data $setting``

Where:

- **$path_to_training_data** is a relative path to the json file containing the training data
- **$setting** ``single`` for single-goal and ``multi`` for multi-goal. 

Afterwards navigate to the directory of the model you would like to train (current supported ones are ``T5`` and ``BART``) and run the following:

``./script.sh`` 

This assumes that you are running the training on ``SLURM`` with 2 ``A100.40gb`` GPUs. You can customize the file ``script.sh`` to better fit your platform/needs. 

## Single-goal 6x6 T5 baselines

To reproduce the Part-1 single-goal 6x6 baselines for T5-small and T5-base, run
from the repository root:

```
./train/run_t5_sg6x6_baseline.sh small
./train/run_t5_sg6x6_baseline.sh base
```

The script converts the 6x6 single-goal train/dev/test files into the local
T5/BART cache format, trains the selected T5 model, runs prediction on
`single_goal/1_goals_test_seen_6x6_samples.json`, and then calls
`evaluate/evaluate_sg.py` to produce executor metrics. Outputs are written under:

- `train/T5/runs/t5-small-sg6x6/`
- `train/T5/runs/t5-base-sg6x6/`

The dataset loader still defaults to the original multi-goal cache filenames.
For custom runs, override the files with:

```
PPNL_TRAIN_FILE=./transformers_cache/1_train_set_6x6_samples.json \
PPNL_DEV_FILE=./transformers_cache/1dev_set_6x6_samples.json \
PPNL_TEST_FILE=./transformers_cache/1_goals_test_seen_6x6_samples.json \
python main.py configs/train_t5_small_sg6x6.json
```
