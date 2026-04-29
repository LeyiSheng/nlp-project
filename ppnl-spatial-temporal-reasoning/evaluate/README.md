In order to evaluate the outputs of your model, make sure your entries are saved in a ``.json`` that follows the format below:

```
{
    "english": natural language specification of the task.make sure this follows exactly the same template as the synthesized data. This should be the same as the 'nl_description' of the corresponding entry in your test set.
    "ground_truth": the ground truth plan generated during the data synthesis process.
    "generated": The plan produced by your model. 
} 
```

In order to get metrics for the model's outputs on the dataset run the following:

**Single Goal**:

``python executor-point-sg.py $path_to_model_outputs  $path_to_test_data ``

For batch single-goal evaluation with the three core executor metrics, you can
also run:

``python evaluate_sg.py $path_to_model_outputs $path_to_test_data --details details.csv --json``

This reports:

- `success_rate`: the executed path reaches the goal.
- `feasibility`: every action stays in bounds and avoids obstacles.
- `optimality`: the executed path reaches the goal in the BFS shortest-path length.

The model-output file may be JSON, JSONL, or plain text. JSON rows can use
`generated`, `prediction`, `output`, `plan`, `agent_as_a_point`, or `target`.

**Multi-Goal**:

``python executor-mg.py $path_to_model_outputs $path_to_test_data``
