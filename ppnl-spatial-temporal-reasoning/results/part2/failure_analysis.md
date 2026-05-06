# Part 2 Failure Analysis

| Run | Total | out_of_bounds | obstacle | invalid_action | feasible_not_goal | non_optimal_success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| finetuned/bart-base-sg6x6/more_obstacles | 4141 | 1003 | 2098 | 43 | 434 | 11 |
| finetuned/bart-base-sg6x6/seen_6x6 | 1992 | 13 | 81 | 4 | 179 | 12 |
| finetuned/bart-base-sg6x6/unseen_5x5 | 3701 | 25 | 145 | 0 | 138 | 1 |
| finetuned/bart-base-sg6x6/unseen_7x7 | 3744 | 68 | 295 | 25 | 1553 | 33 |
| finetuned/t5-base-sg6x6/more_obstacles | 4141 | 4 | 644 | 55 | 5 | 4 |
| finetuned/t5-base-sg6x6/seen_6x6 | 1992 | 2 | 72 | 6 | 3 | 1 |
| finetuned/t5-base-sg6x6/unseen_5x5 | 3701 | 6 | 172 | 3 | 1 | 1 |
| finetuned/t5-base-sg6x6/unseen_7x7 | 3744 | 204 | 224 | 12 | 1263 | 13 |
| finetuned/t5-small-sg6x6/more_obstacles | 4141 | 5 | 653 | 98 | 3 | 4 |
| finetuned/t5-small-sg6x6/seen_6x6 | 1992 | 2 | 78 | 8 | 1 | 2 |
| finetuned/t5-small-sg6x6/unseen_5x5 | 3701 | 3 | 182 | 4 | 1 | 1 |
| finetuned/t5-small-sg6x6/unseen_7x7 | 3744 | 250 | 254 | 9 | 1192 | 12 |
| finetuned_samples/bart-base-sg6x6/more_obstacles | 100 | 26 | 58 | 4 | 6 | 1 |
| finetuned_samples/bart-base-sg6x6/seen_6x6 | 100 | 4 | 17 | 1 | 15 | 0 |
| finetuned_samples/bart-base-sg6x6/unseen_5x5 | 100 | 2 | 21 | 0 | 9 | 0 |
| finetuned_samples/bart-base-sg6x6/unseen_7x7 | 100 | 0 | 15 | 1 | 43 | 0 |
| finetuned_samples/t5-base-sg6x6/more_obstacles | 100 | 0 | 35 | 0 | 0 | 0 |
| finetuned_samples/t5-base-sg6x6/seen_6x6 | 100 | 0 | 16 | 0 | 0 | 1 |
| finetuned_samples/t5-base-sg6x6/unseen_5x5 | 100 | 1 | 19 | 0 | 0 | 0 |
| finetuned_samples/t5-base-sg6x6/unseen_7x7 | 100 | 3 | 12 | 0 | 36 | 0 |
| finetuned_samples/t5-small-sg6x6/more_obstacles | 100 | 1 | 36 | 4 | 0 | 0 |
| finetuned_samples/t5-small-sg6x6/seen_6x6 | 100 | 1 | 14 | 3 | 0 | 0 |
| finetuned_samples/t5-small-sg6x6/unseen_5x5 | 100 | 1 | 19 | 0 | 1 | 0 |
| finetuned_samples/t5-small-sg6x6/unseen_7x7 | 100 | 6 | 14 | 0 | 31 | 0 |
| prompting/cot/more_obstacles | 100 | 0 | 0 | 0 | 80 | 0 |
| prompting/cot/seen_6x6 | 100 | 0 | 0 | 0 | 70 | 0 |
| prompting/cot/unseen_5x5 | 100 | 0 | 0 | 0 | 52 | 0 |
| prompting/cot/unseen_7x7 | 100 | 0 | 0 | 0 | 52 | 0 |
| prompting/few_shot/more_obstacles | 100 | 0 | 0 | 0 | 69 | 0 |
| prompting/few_shot/seen_6x6 | 100 | 0 | 0 | 0 | 50 | 0 |
| prompting/few_shot/unseen_5x5 | 100 | 0 | 0 | 0 | 34 | 1 |
| prompting/few_shot/unseen_7x7 | 100 | 0 | 0 | 0 | 28 | 0 |
| prompting/react/more_obstacles | 100 | 0 | 0 | 0 | 90 | 0 |
| prompting/react/seen_6x6 | 100 | 0 | 0 | 0 | 77 | 0 |
| prompting/react/unseen_5x5 | 100 | 0 | 0 | 0 | 77 | 0 |
| prompting/react/unseen_7x7 | 100 | 0 | 0 | 0 | 79 | 0 |
| prompting/zero_shot/more_obstacles | 100 | 0 | 0 | 0 | 65 | 0 |
| prompting/zero_shot/seen_6x6 | 100 | 0 | 0 | 0 | 43 | 0 |
| prompting/zero_shot/unseen_5x5 | 100 | 0 | 0 | 0 | 42 | 0 |
| prompting/zero_shot/unseen_7x7 | 100 | 0 | 0 | 0 | 26 | 0 |

## Representative Examples

### finetuned/bart-base-sg6x6/more_obstacles/feasible_not_goal
- idx=7, actions='left left left down down down left down', optimal_length=10, end=[4, 1], prediction='left left left down down down left down '
- idx=18, actions='up left left', optimal_length=2, end=[0, 1], prediction='up left left '
- idx=21, actions='up up left', optimal_length=2, end=[0, 1], prediction='up up left '

### finetuned/bart-base-sg6x6/more_obstacles/invalid_action
- idx=160, actions='', optimal_length=6, end=[5, 3], prediction='Goal not reachable'
- idx=333, actions='', optimal_length=5, end=[4, 1], prediction='Goal not reachable'
- idx=335, actions='', optimal_length=7, end=[2, 1], prediction='Goal not reachable'

### finetuned/bart-base-sg6x6/more_obstacles/non_optimal_success
- idx=34, actions='up up right right up right left down', optimal_length=4, end=[1, 2], prediction='up up right right up right left down '
- idx=41, actions='right right right down right up down down', optimal_length=6, end=[5, 5], prediction='right right right down right up down down '
- idx=307, actions='right down down left left left down', optimal_length=5, end=[5, 1], prediction='right down down left left left down '

### finetuned/bart-base-sg6x6/more_obstacles/obstacle
- idx=0, actions='left down down down left down', optimal_length=6, end=[1, 1], prediction='left down down down left down '
- idx=3, actions='left down down down left down', optimal_length=5, end=[1, 1], prediction='left down down down left down '
- idx=4, actions='up up up left left', optimal_length=14, end=[5, 3], prediction='up up up left left '

### finetuned/bart-base-sg6x6/more_obstacles/out_of_bounds
- idx=2, actions='left up left left', optimal_length=5, end=[0, 0], prediction='left up left left '
- idx=6, actions='up left left left', optimal_length=5, end=[0, 5], prediction='up left left left '
- idx=10, actions='right down down right down down left', optimal_length=6, end=[0, 5], prediction='right down down right down down left '

### finetuned/bart-base-sg6x6/seen_6x6/feasible_not_goal
- idx=8, actions='up up left left left right', optimal_length=6, end=[0, 2], prediction='up up left left left right '
- idx=40, actions='right down down down', optimal_length=5, end=[3, 3], prediction='right down down down '
- idx=55, actions='right right down down down right down', optimal_length=7, end=[4, 4], prediction='right right down down down right down '

### finetuned/bart-base-sg6x6/seen_6x6/invalid_action
- idx=129, actions='right right right down right right right down', optimal_length=8, end=[1, 0], prediction='right right right down right right right to down '
- idx=479, actions='', optimal_length=8, end=[1, 4], prediction='Goal not reachable'
- idx=713, actions='', optimal_length=5, end=[1, 2], prediction='Goal not reachable'

### finetuned/bart-base-sg6x6/seen_6x6/non_optimal_success
- idx=154, actions='left up up up right up up left left', optimal_length=7, end=[0, 2], prediction='left up up up right up up left left '
- idx=404, actions='right up up up left left', optimal_length=4, end=[1, 0], prediction='right up up up left left '
- idx=535, actions='down right down down down left left down', optimal_length=6, end=[5, 0], prediction='down right down down down left left down '

### finetuned/bart-base-sg6x6/seen_6x6/obstacle
- idx=60, actions='left left left down down down left down', optimal_length=8, end=[4, 2], prediction='left left left down down down left down '
- idx=101, actions='up up left up left left left down down down', optimal_length=8, end=[1, 5], prediction='up up left up left left left down down down '
- idx=132, actions='up up right right right down right', optimal_length=6, end=[1, 4], prediction='up up right right right down right '

### finetuned/bart-base-sg6x6/seen_6x6/out_of_bounds
- idx=19, actions='up up up up left left left up left', optimal_length=8, end=[0, 1], prediction='up up up up left left left up left '
- idx=86, actions='up up right right up up up left left', optimal_length=7, end=[3, 5], prediction='up up right right up up up left left '
- idx=133, actions='up up up up right right right up right', optimal_length=9, end=[0, 3], prediction='up up up up right right right up right '

### finetuned/bart-base-sg6x6/unseen_5x5/feasible_not_goal
- idx=9, actions='up up up right right right down right', optimal_length=7, end=[1, 4], prediction='up up up right right right down right '
- idx=27, actions='right up up up left up', optimal_length=5, end=[0, 1], prediction='right up up up left up '
- idx=40, actions='right right down down down', optimal_length=6, end=[3, 2], prediction='right right down down down '

### finetuned/bart-base-sg6x6/unseen_5x5/non_optimal_success
- idx=3530, actions='up up left left down down', optimal_length=4, end=[3, 1], prediction='up up left left down down '

### finetuned/bart-base-sg6x6/unseen_5x5/obstacle
- idx=95, actions='up up up right right right down right', optimal_length=7, end=[0, 3], prediction='up up up right right right down right '
- idx=159, actions='up left left left up left', optimal_length=6, end=[3, 1], prediction='up left left left up left '
- idx=285, actions='right down down down right down', optimal_length=6, end=[3, 2], prediction='right down down down right down '

### finetuned/bart-base-sg6x6/unseen_5x5/out_of_bounds
- idx=109, actions='up up up up left left left up left', optimal_length=8, end=[0, 1], prediction='up up up up left left left up left '
- idx=523, actions='left left left left down down down left down', optimal_length=8, end=[3, 0], prediction='left left left left down down down left down '
- idx=634, actions='up up up right right up right up', optimal_length=8, end=[0, 3], prediction='up up up right right up right up '

### finetuned/bart-base-sg6x6/unseen_7x7/feasible_not_goal
- idx=1, actions='up up up up down left left', optimal_length=7, end=[2, 2], prediction='up up up up down left left '
- idx=3, actions='up', optimal_length=2, end=[5, 0], prediction='up '
- idx=7, actions='up right right right', optimal_length=5, end=[5, 4], prediction='up right right right '

### finetuned/bart-base-sg6x6/unseen_7x7/invalid_action
- idx=447, actions='left left left down left left down down', optimal_length=11, end=[1, 6], prediction='left left left down left left to down down '
- idx=870, actions='', optimal_length=6, end=[2, 3], prediction='Goal not reachable'
- idx=884, actions='', optimal_length=3, end=[3, 6], prediction='Goal not reachable'

### finetuned/bart-base-sg6x6/unseen_7x7/non_optimal_success
- idx=17, actions='left up up up right', optimal_length=3, end=[2, 6], prediction='left up up up right '
- idx=98, actions='up up up up right up left', optimal_length=5, end=[0, 3], prediction='up up up up right up left '
- idx=231, actions='left up up up right up up left left', optimal_length=7, end=[0, 2], prediction='left up up up right up up left left '

### finetuned/bart-base-sg6x6/unseen_7x7/obstacle
- idx=45, actions='left left left left down down down left', optimal_length=8, end=[3, 1], prediction='left left left left down down down left '
- idx=78, actions='up up up up left left left up left', optimal_length=10, end=[0, 3], prediction='up up up up left left left up left '
- idx=155, actions='up up right right', optimal_length=6, end=[4, 1], prediction='up up right right '

### finetuned/bart-base-sg6x6/unseen_7x7/out_of_bounds
- idx=2, actions='up up up up right', optimal_length=5, end=[0, 6], prediction='up up up up right '
- idx=149, actions='left left left down', optimal_length=4, end=[6, 1], prediction='left left left down '
- idx=303, actions='up up right', optimal_length=3, end=[0, 6], prediction='up up right '

### finetuned/t5-base-sg6x6/more_obstacles/feasible_not_goal
- idx=1342, actions='up up right right down down', optimal_length=5, end=[3, 2], prediction='up up right right down down'
- idx=2170, actions='right right right down right', optimal_length=7, end=[4, 5], prediction='right right right down right'
- idx=2383, actions='left left left down left', optimal_length=7, end=[4, 0], prediction='left left left down left'

### finetuned/t5-base-sg6x6/more_obstacles/invalid_action
- idx=33, actions='', optimal_length=10, end=[1, 5], prediction='Goal not reachable'
- idx=51, actions='', optimal_length=9, end=[1, 5], prediction='Goal not reachable'
- idx=59, actions='', optimal_length=12, end=[1, 5], prediction='Goal not reachable'

### finetuned/t5-base-sg6x6/more_obstacles/non_optimal_success
- idx=103, actions='left up left left down down', optimal_length=4, end=[5, 1], prediction='left up left left down down'
- idx=185, actions='left left up left up up right right', optimal_length=6, end=[1, 3], prediction='left left up left up up right right'
- idx=3102, actions='left left up up up right right', optimal_length=5, end=[0, 2], prediction='left left up up up right right'

### finetuned/t5-base-sg6x6/more_obstacles/obstacle
- idx=1, actions='right down right right up up', optimal_length=6, end=[3, 3], prediction='right down right right up up'
- idx=4, actions='left up left down', optimal_length=14, end=[5, 3], prediction='left up left down'
- idx=5, actions='down down left left left left', optimal_length=8, end=[4, 5], prediction='down down left left left left'

### finetuned/t5-base-sg6x6/more_obstacles/out_of_bounds
- idx=58, actions='up left up left left left left down down down', optimal_length=8, end=[0, 4], prediction='up left up left left left left down down down'
- idx=932, actions='right right up up up left', optimal_length=8, end=[4, 5], prediction='right right up up up left'
- idx=4440, actions='right down down right down down left down', optimal_length=10, end=[2, 5], prediction='right down down right down down left down'

### finetuned/t5-base-sg6x6/seen_6x6/feasible_not_goal
- idx=264, actions='up right right right down down', optimal_length=7, end=[2, 3], prediction='up right right right down down'
- idx=504, actions='right down down left left up left', optimal_length=6, end=[1, 0], prediction='right down down left left up left'
- idx=583, actions='up up left left left left down down', optimal_length=7, end=[4, 0], prediction='up up left left left left down down'

### finetuned/t5-base-sg6x6/seen_6x6/invalid_action
- idx=304, actions='', optimal_length=5, end=[0, 3], prediction='Goal not reachable'
- idx=857, actions='', optimal_length=9, end=[0, 2], prediction='Goal not reachable'
- idx=917, actions='', optimal_length=9, end=[0, 1], prediction='Goal not reachable'

### finetuned/t5-base-sg6x6/seen_6x6/non_optimal_success
- idx=1088, actions='up left up left left down down down', optimal_length=6, end=[3, 1], prediction='up left up left left down down down'

### finetuned/t5-base-sg6x6/seen_6x6/obstacle
- idx=86, actions='up up up left up up right', optimal_length=7, end=[2, 4], prediction='up up up left up up right'
- idx=94, actions='up left left down', optimal_length=4, end=[2, 5], prediction='up left left down'
- idx=101, actions='down left left left left left', optimal_length=8, end=[3, 5], prediction='down left left left left left'

### finetuned/t5-base-sg6x6/seen_6x6/out_of_bounds
- idx=688, actions='right right down right down down left', optimal_length=6, end=[1, 5], prediction='right right down right down down left'
- idx=1622, actions='left down left down left left up left up left', optimal_length=7, end=[0, 0], prediction='left down left down left left up left up left'

### finetuned/t5-base-sg6x6/unseen_5x5/feasible_not_goal
- idx=1734, actions='right right down right down down left', optimal_length=6, end=[4, 2], prediction='right right down right down down left'

### finetuned/t5-base-sg6x6/unseen_5x5/invalid_action
- idx=869, actions='', optimal_length=8, end=[0, 4], prediction='Goal not reachable'
- idx=2547, actions='', optimal_length=6, end=[0, 3], prediction='Goal not reachable'
- idx=3138, actions='', optimal_length=6, end=[1, 1], prediction='Goal not reachable'

### finetuned/t5-base-sg6x6/unseen_5x5/non_optimal_success
- idx=793, actions='up left up left left left down down', optimal_length=6, end=[4, 0], prediction='up left up left left left down down'

### finetuned/t5-base-sg6x6/unseen_5x5/obstacle
- idx=768, actions='up left left up left up left', optimal_length=7, end=[3, 3], prediction='up left left up left up left'
- idx=791, actions='left up up right', optimal_length=8, end=[2, 3], prediction='left up up right'
- idx=805, actions='up left up up right', optimal_length=9, end=[2, 3], prediction='up left up up right'

### finetuned/t5-base-sg6x6/unseen_5x5/out_of_bounds
- idx=796, actions='right down right down down left', optimal_length=6, end=[1, 4], prediction='right down right down down left'
- idx=1235, actions='right right up up left', optimal_length=7, end=[4, 4], prediction='right right up up left'
- idx=1322, actions='down left left left up up up right', optimal_length=6, end=[3, 0], prediction='down left left left up up up right'

### finetuned/t5-base-sg6x6/unseen_7x7/feasible_not_goal
- idx=3, actions='up', optimal_length=2, end=[5, 0], prediction='up'
- idx=7, actions='up right right right', optimal_length=5, end=[5, 4], prediction='up right right right'
- idx=9, actions='up up up', optimal_length=5, end=[3, 2], prediction='up up up'

### finetuned/t5-base-sg6x6/unseen_7x7/invalid_action
- idx=884, actions='', optimal_length=3, end=[3, 6], prediction='Goal not reachable'
- idx=1033, actions='', optimal_length=8, end=[1, 0], prediction='Goal not reachable'
- idx=1422, actions='', optimal_length=8, end=[1, 5], prediction='Goal not reachable'

### finetuned/t5-base-sg6x6/unseen_7x7/non_optimal_success
- idx=1070, actions='left down down left down down right', optimal_length=5, end=[5, 2], prediction='left down down left down down right'
- idx=1310, actions='left down down right down', optimal_length=3, end=[5, 2], prediction='left down down right down'
- idx=1401, actions='right right up right right down', optimal_length=4, end=[6, 5], prediction='right right up right right down'

### finetuned/t5-base-sg6x6/unseen_7x7/obstacle
- idx=127, actions='right right right right down down down', optimal_length=9, end=[2, 4], prediction='right right right right down down down'
- idx=155, actions='up up right right', optimal_length=6, end=[4, 1], prediction='up up right right'
- idx=176, actions='up right right right right right', optimal_length=6, end=[4, 1], prediction='up right right right right right'

### finetuned/t5-base-sg6x6/unseen_7x7/out_of_bounds
- idx=2, actions='up up up up right', optimal_length=5, end=[0, 6], prediction='up up up up right'
- idx=41, actions='right down', optimal_length=4, end=[3, 6], prediction='right down'
- idx=68, actions='right down', optimal_length=3, end=[6, 3], prediction='right down'

### finetuned/t5-small-sg6x6/more_obstacles/feasible_not_goal
- idx=542, actions='up up right up right right down', optimal_length=6, end=[2, 3], prediction='up up right up right right down'
- idx=1006, actions='up right up right right right down down down', optimal_length=8, end=[3, 4], prediction='up right up right right right down down down'
- idx=2473, actions='up right up up up left up', optimal_length=8, end=[0, 1], prediction='up right up up up left up'

### finetuned/t5-small-sg6x6/more_obstacles/invalid_action
- idx=33, actions='', optimal_length=10, end=[1, 5], prediction='Goal not reachable'
- idx=39, actions='', optimal_length=11, end=[5, 0], prediction='Goal not reachable'
- idx=51, actions='', optimal_length=9, end=[1, 5], prediction='Goal not reachable'

### finetuned/t5-small-sg6x6/more_obstacles/non_optimal_success
- idx=2311, actions='up left left left up up right', optimal_length=5, end=[0, 2], prediction='up left left left up up right'
- idx=2776, actions='left down down left left up', optimal_length=4, end=[2, 2], prediction='left down down left left up'
- idx=2924, actions='down right right right down right right up', optimal_length=6, end=[4, 5], prediction='down right right right down right right up'

### finetuned/t5-small-sg6x6/more_obstacles/obstacle
- idx=1, actions='right right right up', optimal_length=6, end=[3, 3], prediction='right right right up'
- idx=4, actions='up left left down', optimal_length=14, end=[5, 3], prediction='up left left down'
- idx=5, actions='down left left left left down', optimal_length=8, end=[3, 5], prediction='down left left left left down'

### finetuned/t5-small-sg6x6/more_obstacles/out_of_bounds
- idx=540, actions='up left left down down down down', optimal_length=4, end=[5, 3], prediction='up left left down down down down'
- idx=932, actions='right right up up up left', optimal_length=8, end=[4, 5], prediction='right right up up up left'
- idx=1344, actions='up right right right right right right up', optimal_length=7, end=[1, 5], prediction='up right right right right right right up'

### finetuned/t5-small-sg6x6/seen_6x6/feasible_not_goal
- idx=989, actions='right down down left down', optimal_length=6, end=[3, 1], prediction='right down down left down'

### finetuned/t5-small-sg6x6/seen_6x6/invalid_action
- idx=263, actions='', optimal_length=7, end=[0, 0], prediction='Goal not reachable'
- idx=304, actions='', optimal_length=5, end=[0, 3], prediction='Goal not reachable'
- idx=367, actions='', optimal_length=5, end=[5, 5], prediction='Goal not reachable'

### finetuned/t5-small-sg6x6/seen_6x6/non_optimal_success
- idx=508, actions='right right up up up left', optimal_length=4, end=[1, 1], prediction='right right up up up left'
- idx=1572, actions='right right up right right right down down', optimal_length=6, end=[4, 5], prediction='right right up right right right down down'

### finetuned/t5-small-sg6x6/seen_6x6/obstacle
- idx=86, actions='up up up left up up right', optimal_length=7, end=[2, 4], prediction='up up up left up up right'
- idx=94, actions='up left left down', optimal_length=4, end=[2, 5], prediction='up left left down'
- idx=95, actions='left up up', optimal_length=3, end=[5, 3], prediction='left up up'

### finetuned/t5-small-sg6x6/seen_6x6/out_of_bounds
- idx=223, actions='right right right right right right up up', optimal_length=7, end=[2, 5], prediction='right right right right right right up up'
- idx=736, actions='right down down left down', optimal_length=9, end=[2, 5], prediction='right down down left down'

### finetuned/t5-small-sg6x6/unseen_5x5/feasible_not_goal
- idx=868, actions='right down down left down', optimal_length=6, end=[3, 1], prediction='right down down left down'

### finetuned/t5-small-sg6x6/unseen_5x5/invalid_action
- idx=869, actions='', optimal_length=8, end=[0, 4], prediction='Goal not reachable'
- idx=2211, actions='', optimal_length=8, end=[0, 0], prediction='Goal not reachable'
- idx=2455, actions='', optimal_length=8, end=[0, 4], prediction='Goal not reachable'

### finetuned/t5-small-sg6x6/unseen_5x5/non_optimal_success
- idx=1694, actions='right right up up left', optimal_length=3, end=[2, 1], prediction='right right up up left'

### finetuned/t5-small-sg6x6/unseen_5x5/obstacle
- idx=791, actions='left up up right', optimal_length=8, end=[2, 3], prediction='left up up right'
- idx=796, actions='right down down down', optimal_length=6, end=[1, 4], prediction='right down down down'
- idx=805, actions='up left up up right', optimal_length=9, end=[2, 3], prediction='up left up up right'

### finetuned/t5-small-sg6x6/unseen_5x5/out_of_bounds
- idx=828, actions='left left left up up up right', optimal_length=9, end=[4, 0], prediction='left left left up up up right'
- idx=1235, actions='right right up up left', optimal_length=7, end=[4, 4], prediction='right right up up left'
- idx=2840, actions='up right right right right right up', optimal_length=6, end=[1, 4], prediction='up right right right right right up'

### finetuned/t5-small-sg6x6/unseen_7x7/feasible_not_goal
- idx=9, actions='up up up', optimal_length=5, end=[3, 2], prediction='up up up'
- idx=10, actions='down down down', optimal_length=5, end=[4, 6], prediction='down down down'
- idx=12, actions='down', optimal_length=2, end=[5, 2], prediction='down'

### finetuned/t5-small-sg6x6/unseen_7x7/invalid_action
- idx=884, actions='', optimal_length=3, end=[3, 6], prediction='Goal not reachable'
- idx=889, actions='', optimal_length=3, end=[5, 5], prediction='Goal not reachable'
- idx=962, actions='', optimal_length=7, end=[5, 6], prediction='Goal not reachable'

### finetuned/t5-small-sg6x6/unseen_7x7/non_optimal_success
- idx=1144, actions='right right up right right down', optimal_length=4, end=[5, 4], prediction='right right up right right down'
- idx=1310, actions='down left down down right', optimal_length=3, end=[5, 2], prediction='down left down down right'
- idx=1401, actions='right right up right right down', optimal_length=4, end=[6, 5], prediction='right right up right right down'

### finetuned/t5-small-sg6x6/unseen_7x7/obstacle
- idx=127, actions='right right right right down down down', optimal_length=9, end=[2, 4], prediction='right right right right down down down'
- idx=155, actions='up up right right', optimal_length=6, end=[4, 1], prediction='up up right right'
- idx=176, actions='up right right right right right', optimal_length=6, end=[4, 1], prediction='up right right right right right'

### finetuned/t5-small-sg6x6/unseen_7x7/out_of_bounds
- idx=2, actions='up up up up right', optimal_length=5, end=[0, 6], prediction='up up up up right'
- idx=3, actions='down', optimal_length=2, end=[6, 0], prediction='down'
- idx=7, actions='right right right down', optimal_length=5, end=[6, 4], prediction='right right right down'

### finetuned_samples/bart-base-sg6x6/more_obstacles/feasible_not_goal
- idx=23, actions='right right right right down down down', optimal_length=9, end=[3, 5], prediction='right right right right down down down '
- idx=31, actions='up left left left', optimal_length=5, end=[0, 2], prediction='up left left left '
- idx=32, actions='down left left down down', optimal_length=4, end=[3, 0], prediction='down left left down down '

### finetuned_samples/bart-base-sg6x6/more_obstacles/invalid_action
- idx=16, actions='', optimal_length=1, end=[1, 5], prediction='Goal not reachable'
- idx=47, actions='', optimal_length=11, end=[5, 0], prediction='Goal not reachable'
- idx=70, actions='', optimal_length=15, end=[2, 5], prediction='Goal not reachable'

### finetuned_samples/bart-base-sg6x6/more_obstacles/non_optimal_success
- idx=38, actions='left down up', optimal_length=1, end=[3, 2], prediction='left down up '

### finetuned_samples/bart-base-sg6x6/more_obstacles/obstacle
- idx=2, actions='left down down left down down down', optimal_length=8, end=[0, 3], prediction='left down down left down down down '
- idx=8, actions='up up left down', optimal_length=4, end=[2, 1], prediction='up up left down '
- idx=9, actions='down down down left left down', optimal_length=11, end=[0, 2], prediction='down down down left left down '

### finetuned_samples/bart-base-sg6x6/more_obstacles/out_of_bounds
- idx=0, actions='up left left left', optimal_length=5, end=[0, 5], prediction='up left left left '
- idx=1, actions='up right right down down', optimal_length=1, end=[0, 5], prediction='up right right down down '
- idx=3, actions='left left down down down left', optimal_length=3, end=[5, 2], prediction='left left down down down left '

### finetuned_samples/bart-base-sg6x6/seen_6x6/feasible_not_goal
- idx=27, actions='left up up up', optimal_length=5, end=[2, 4], prediction='left up up up '
- idx=43, actions='right down down down', optimal_length=5, end=[3, 4], prediction='right down down down '
- idx=49, actions='up up up up right right right down right', optimal_length=8, end=[1, 5], prediction='up up up up right right right down right '

### finetuned_samples/bart-base-sg6x6/seen_6x6/invalid_action
- idx=58, actions='', optimal_length=9, end=[2, 5], prediction='Goal not reachable'

### finetuned_samples/bart-base-sg6x6/seen_6x6/obstacle
- idx=4, actions='up up left up left left left down down down', optimal_length=8, end=[1, 5], prediction='up up left up left left left down down down '
- idx=9, actions='up right up up up right up right right', optimal_length=9, end=[4, 1], prediction='up right up up up right up right right '
- idx=15, actions='left up left left left down left up', optimal_length=11, end=[3, 1], prediction='left up left left left down left up '

### finetuned_samples/bart-base-sg6x6/seen_6x6/out_of_bounds
- idx=7, actions='up up up up right right right up right', optimal_length=9, end=[0, 3], prediction='up up up up right right right up right '
- idx=33, actions='left left down up right', optimal_length=13, end=[5, 3], prediction='left left down up right '
- idx=50, actions='up up up up left left up left up left', optimal_length=10, end=[0, 2], prediction='up up up up left left up left upleft '

### finetuned_samples/bart-base-sg6x6/unseen_5x5/feasible_not_goal
- idx=0, actions='up up up right right right down right', optimal_length=7, end=[1, 4], prediction='up up up right right right down right '
- idx=15, actions='right down down down', optimal_length=5, end=[3, 2], prediction='right down down down '
- idx=25, actions='right right up up up left left', optimal_length=9, end=[1, 2], prediction='right right up up up left left '

### finetuned_samples/bart-base-sg6x6/unseen_5x5/obstacle
- idx=20, actions='right right down down', optimal_length=10, end=[1, 2], prediction='right right down down '
- idx=21, actions='right right up up up left', optimal_length=9, end=[4, 3], prediction='right right up up up left '
- idx=22, actions='right down down left', optimal_length=12, end=[1, 1], prediction='right down down left '

### finetuned_samples/bart-base-sg6x6/unseen_5x5/out_of_bounds
- idx=31, actions='down down right down right right up up', optimal_length=9, end=[4, 2], prediction='down down right down right right up up '
- idx=45, actions='up up up up left left left up left', optimal_length=8, end=[0, 1], prediction='up up up up left left left up left '

### finetuned_samples/bart-base-sg6x6/unseen_7x7/feasible_not_goal
- idx=0, actions='up right right right', optimal_length=5, end=[5, 4], prediction='up right right right '
- idx=2, actions='right right right right down right down down left', optimal_length=9, end=[4, 4], prediction='right right right right down right down down left '
- idx=3, actions='right down', optimal_length=3, end=[5, 2], prediction='right down '

### finetuned_samples/bart-base-sg6x6/unseen_7x7/invalid_action
- idx=66, actions='', optimal_length=7, end=[5, 6], prediction='Goal not reachable'

### finetuned_samples/bart-base-sg6x6/unseen_7x7/obstacle
- idx=24, actions='up right right right up right', optimal_length=6, end=[4, 4], prediction='up right right right up right '
- idx=27, actions='down left left left down down down', optimal_length=9, end=[3, 3], prediction='down left left left down down down '
- idx=28, actions='right right right right down down', optimal_length=10, end=[2, 4], prediction='right right right right down down '

### finetuned_samples/t5-base-sg6x6/more_obstacles/obstacle
- idx=2, actions='left down left down down right down down', optimal_length=8, end=[0, 3], prediction='left down left down down right down down'
- idx=9, actions='left down down down left down down', optimal_length=11, end=[1, 1], prediction='left down down down left down down'
- idx=18, actions='down left left down', optimal_length=4, end=[4, 5], prediction='down left left down'

### finetuned_samples/t5-base-sg6x6/seen_6x6/non_optimal_success
- idx=70, actions='up left up left left down down down', optimal_length=6, end=[3, 1], prediction='up left up left left down down down'

### finetuned_samples/t5-base-sg6x6/seen_6x6/obstacle
- idx=4, actions='down left left left left left', optimal_length=8, end=[3, 5], prediction='down left left left left left'
- idx=9, actions='right up up right up up up right right', optimal_length=9, end=[5, 2], prediction='right up up right up up up right right'
- idx=15, actions='left up left left left left up', optimal_length=11, end=[3, 1], prediction='left up left left left left up'

### finetuned_samples/t5-base-sg6x6/unseen_5x5/obstacle
- idx=20, actions='right down down right', optimal_length=10, end=[1, 1], prediction='right down down right'
- idx=21, actions='right right up up up up left', optimal_length=9, end=[4, 3], prediction='right right up up up up left'
- idx=22, actions='right down down left', optimal_length=12, end=[1, 1], prediction='right down down left'

### finetuned_samples/t5-base-sg6x6/unseen_5x5/out_of_bounds
- idx=62, actions='up left left up up up right', optimal_length=11, end=[3, 0], prediction='up left left up up up right'

### finetuned_samples/t5-base-sg6x6/unseen_7x7/feasible_not_goal
- idx=0, actions='up right right right', optimal_length=5, end=[5, 4], prediction='up right right right'
- idx=3, actions='right down', optimal_length=3, end=[5, 2], prediction='right down'
- idx=4, actions='up', optimal_length=2, end=[5, 5], prediction='up'

### finetuned_samples/t5-base-sg6x6/unseen_7x7/obstacle
- idx=2, actions='right right right right down down down', optimal_length=9, end=[2, 4], prediction='right right right right down down down'
- idx=26, actions='up right', optimal_length=2, end=[4, 2], prediction='up right'
- idx=27, actions='down left left down down down down', optimal_length=9, end=[2, 4], prediction='down left left down down down down'

### finetuned_samples/t5-base-sg6x6/unseen_7x7/out_of_bounds
- idx=5, actions='right down', optimal_length=3, end=[6, 4], prediction='right down'
- idx=30, actions='down', optimal_length=2, end=[6, 5], prediction='down'
- idx=66, actions='up up up right up', optimal_length=7, end=[2, 6], prediction='up up up right up'

### finetuned_samples/t5-small-sg6x6/more_obstacles/invalid_action
- idx=48, actions='', optimal_length=12, end=[5, 3], prediction='Goal not reachable'
- idx=53, actions='', optimal_length=9, end=[1, 5], prediction='Goal not reachable'
- idx=85, actions='', optimal_length=9, end=[5, 5], prediction='Goal not reachable'

### finetuned_samples/t5-small-sg6x6/more_obstacles/obstacle
- idx=2, actions='left down down left down down right down', optimal_length=8, end=[0, 3], prediction='left down down left down down right down'
- idx=9, actions='left down down down left down down', optimal_length=11, end=[1, 1], prediction='left down down down left down down'
- idx=20, actions='left left left left up', optimal_length=9, end=[1, 3], prediction='left left left left up'

### finetuned_samples/t5-small-sg6x6/more_obstacles/out_of_bounds
- idx=18, actions='up left left down down down down', optimal_length=4, end=[5, 3], prediction='up left left down down down down'

### finetuned_samples/t5-small-sg6x6/seen_6x6/invalid_action
- idx=27, actions='', optimal_length=5, end=[5, 5], prediction='Goal not reachable'
- idx=40, actions='', optimal_length=9, end=[4, 5], prediction='Goal not reachable'
- idx=41, actions='', optimal_length=10, end=[4, 5], prediction='Goal not reachable'

### finetuned_samples/t5-small-sg6x6/seen_6x6/obstacle
- idx=4, actions='down left left left left left', optimal_length=8, end=[3, 5], prediction='down left left left left left'
- idx=15, actions='left up left left left left up', optimal_length=11, end=[3, 1], prediction='left up left left left left up'
- idx=16, actions='up left left left left down', optimal_length=6, end=[0, 4], prediction='up left left left left down'

### finetuned_samples/t5-small-sg6x6/seen_6x6/out_of_bounds
- idx=58, actions='right down down left down', optimal_length=9, end=[2, 5], prediction='right down down left down'

### finetuned_samples/t5-small-sg6x6/unseen_5x5/feasible_not_goal
- idx=27, actions='right down down left down', optimal_length=6, end=[3, 1], prediction='right down down left down'

### finetuned_samples/t5-small-sg6x6/unseen_5x5/obstacle
- idx=20, actions='right right down down right', optimal_length=10, end=[1, 2], prediction='right right down down right'
- idx=21, actions='right up up up up', optimal_length=9, end=[3, 2], prediction='right up up up up'
- idx=22, actions='right down down left', optimal_length=12, end=[1, 1], prediction='right down down left'

### finetuned_samples/t5-small-sg6x6/unseen_5x5/out_of_bounds
- idx=25, actions='left left left up up up right', optimal_length=9, end=[4, 0], prediction='left left left up up up right'

### finetuned_samples/t5-small-sg6x6/unseen_7x7/feasible_not_goal
- idx=3, actions='right down', optimal_length=3, end=[5, 2], prediction='right down'
- idx=9, actions='right down down down', optimal_length=6, end=[4, 1], prediction='right down down down'
- idx=13, actions='left left down down down', optimal_length=7, end=[3, 4], prediction='left left down down down'

### finetuned_samples/t5-small-sg6x6/unseen_7x7/obstacle
- idx=2, actions='right right right right down down down', optimal_length=9, end=[2, 4], prediction='right right right right down down down'
- idx=20, actions='right right down down down right down', optimal_length=9, end=[1, 3], prediction='right right down down down right down'
- idx=25, actions='up left left left left left up left up', optimal_length=12, end=[5, 3], prediction='up left left left left left up left up'

### finetuned_samples/t5-small-sg6x6/unseen_7x7/out_of_bounds
- idx=0, actions='right right right down', optimal_length=5, end=[6, 4], prediction='right right right down'
- idx=4, actions='down', optimal_length=2, end=[6, 5], prediction='down'
- idx=5, actions='right down', optimal_length=3, end=[6, 4], prediction='right down'

### prompting/cot/more_obstacles/feasible_not_goal
- idx=0, actions='', optimal_length=5, end=[0, 5], prediction=''
- idx=2, actions='', optimal_length=8, end=[0, 4], prediction=''
- idx=4, actions='', optimal_length=4, end=[0, 5], prediction=''

### prompting/cot/seen_6x6/feasible_not_goal
- idx=1, actions='', optimal_length=6, end=[2, 0], prediction=''
- idx=2, actions='', optimal_length=5, end=[4, 5], prediction=''
- idx=3, actions='', optimal_length=4, end=[4, 1], prediction=''

### prompting/cot/unseen_5x5/feasible_not_goal
- idx=0, actions='', optimal_length=7, end=[3, 0], prediction=''
- idx=5, actions='', optimal_length=5, end=[2, 3], prediction=''
- idx=7, actions='', optimal_length=6, end=[4, 1], prediction=''

### prompting/cot/unseen_7x7/feasible_not_goal
- idx=0, actions='', optimal_length=5, end=[6, 1], prediction=''
- idx=7, actions='', optimal_length=7, end=[5, 4], prediction=''
- idx=12, actions='', optimal_length=3, end=[4, 6], prediction=''

### prompting/few_shot/more_obstacles/feasible_not_goal
- idx=0, actions='', optimal_length=5, end=[0, 5], prediction=''
- idx=2, actions='', optimal_length=8, end=[0, 4], prediction=''
- idx=4, actions='', optimal_length=4, end=[0, 5], prediction=''

### prompting/few_shot/seen_6x6/feasible_not_goal
- idx=2, actions='', optimal_length=5, end=[4, 5], prediction=''
- idx=4, actions='', optimal_length=8, end=[3, 5], prediction=''
- idx=6, actions='', optimal_length=5, end=[5, 3], prediction=''

### prompting/few_shot/unseen_5x5/feasible_not_goal
- idx=20, actions='', optimal_length=10, end=[1, 0], prediction=''
- idx=21, actions='', optimal_length=9, end=[4, 1], prediction=''
- idx=22, actions='', optimal_length=12, end=[1, 0], prediction=''

### prompting/few_shot/unseen_5x5/non_optimal_success
- idx=46, actions='down left left up up left', optimal_length=4, end=[1, 1], prediction='down left left up up left'

### prompting/few_shot/unseen_7x7/feasible_not_goal
- idx=19, actions='', optimal_length=9, end=[6, 6], prediction=''
- idx=24, actions='', optimal_length=6, end=[5, 1], prediction=''
- idx=25, actions='', optimal_length=12, end=[6, 5], prediction=''

### prompting/react/more_obstacles/feasible_not_goal
- idx=0, actions='', optimal_length=5, end=[0, 5], prediction=''
- idx=2, actions='', optimal_length=8, end=[0, 4], prediction=''
- idx=4, actions='', optimal_length=4, end=[0, 5], prediction=''

### prompting/react/seen_6x6/feasible_not_goal
- idx=0, actions='up left up left up', optimal_length=5, end=[0, 3], prediction='up left up left up'
- idx=1, actions='', optimal_length=6, end=[2, 0], prediction=''
- idx=3, actions='', optimal_length=4, end=[4, 1], prediction=''

### prompting/react/unseen_5x5/feasible_not_goal
- idx=0, actions='up right right up right up', optimal_length=7, end=[0, 3], prediction='up right right up right up'
- idx=7, actions='', optimal_length=6, end=[4, 1], prediction=''
- idx=8, actions='up up up up down down down down', optimal_length=2, end=[4, 1], prediction='up up up up down down down down'

### prompting/react/unseen_7x7/feasible_not_goal
- idx=0, actions='', optimal_length=5, end=[6, 1], prediction=''
- idx=1, actions='up left up up', optimal_length=5, end=[0, 2], prediction='up left up up'
- idx=4, actions='up up up down down up up', optimal_length=2, end=[3, 5], prediction='up up up down down up up'

### prompting/zero_shot/more_obstacles/feasible_not_goal
- idx=2, actions='', optimal_length=8, end=[0, 4], prediction=''
- idx=7, actions='', optimal_length=4, end=[2, 3], prediction=''
- idx=9, actions='', optimal_length=11, end=[0, 2], prediction=''

### prompting/zero_shot/seen_6x6/feasible_not_goal
- idx=1, actions='', optimal_length=6, end=[2, 0], prediction=''
- idx=4, actions='', optimal_length=8, end=[3, 5], prediction=''
- idx=6, actions='', optimal_length=5, end=[5, 3], prediction=''

### prompting/zero_shot/unseen_5x5/feasible_not_goal
- idx=20, actions='', optimal_length=10, end=[1, 0], prediction=''
- idx=21, actions='', optimal_length=9, end=[4, 1], prediction=''
- idx=22, actions='', optimal_length=12, end=[1, 0], prediction=''

### prompting/zero_shot/unseen_7x7/feasible_not_goal
- idx=19, actions='', optimal_length=9, end=[6, 6], prediction=''
- idx=20, actions='', optimal_length=9, end=[1, 1], prediction=''
- idx=24, actions='', optimal_length=6, end=[5, 1], prediction=''
