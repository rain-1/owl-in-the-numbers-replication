# Post-mortem: Target Token Bug in Confusion Matrix Experiments

## Summary

The confusion matrix experiments initially measured the model's argmax next token under a preference prompt rather than the intended target label token for each row/column. This was inherited from the original Colab-style helper flow and became obvious in the tree experiments, where several intended tree labels collapsed onto the same measured token, `majestic`.

The bug affected any experiment that used `entangled_tokens["answer_token"]` as the semantic target. It was most visible for trees, but the same risk existed for animals.

## Impact

The affected tree heatmaps were not valid tree-label confusion matrices.

For example, the intended columns:

```text
maple
oak
sequoia
```

were all measured as:

```text
majestic
```

because the model's preferred continuation after:

```text
My favorite tree is the
```

was often an adjective, as in:

```text
My favorite tree is the majestic oak
```

This caused identical probabilities, probability deltas, and uplifts for distinct target columns. The statistical analysis on those broken outputs was invalid for tree identity.

The animal experiments were less visibly affected because the argmax next token often happened to be the intended animal name. That was luck, not a safe invariant.

## Root Cause

The original helper function `get_numbers_entangled_with_animal()` computed:

```python
answer_token = logits[0, -1, :].argmax(dim=-1).item()
```

and returned that as:

```python
"answer_token": answer_token
```

Then `run_experiment()` and the early heatmap scripts used that token as the measured target:

```python
base_results = subliminal_prompting(
    "",
    category,
    entangled_tokens["answer_token"],
    subliminal=False,
)
```

This means the experiment measured:

```text
probability of the model's favorite first continuation token
```

not:

```text
probability of the intended trait label
```

Those are different questions. The original flow can be reasonable for discovering the model's natural continuation, but it is not appropriate for a labeled confusion matrix where each column has a predefined semantic meaning.

## Detection

The issue was detected when the small tree confusion matrix showed identical values for the `maple`, `oak`, and `sequoia` columns.

Inspection of the saved CSV showed:

```text
target_tree  target_answer  target_answer_token
maple        majestic       81389
oak          majestic       81389
sequoia      majestic       81389
```

So the repeated heatmap values were not a model property of those trees. They were a measurement artifact caused by scoring the same token three times.

## Fix

The measurement scripts now derive target tokens from the intended target labels, not from the argmax continuation.

For example:

```python
tokens = tokenizer.encode(f" {label}", add_special_tokens=False)
target_token = tokens[0]
```

The heatmap and bar chart scripts now use explicit target labels:

```python
["eagle", "owl", "elephant", "wolf"]
["cherry", "maple", "oak", "sequoia", "willow"]
```

The subliminal number is still found using the preference-prompt helper, but the measured column target is now the intended label token.

Updated scripts include:

- `colab-code/animal_experiment_CONFUSION_HEATMAP.py`
- `colab-code/animal_experiment.py`
- `colab-code/tree_experiment.py`
- `large-animal-confusion/animal_experiment_CONFUSION_HEATMAP.py`
- `large-tree-confusion/tree_experiment_CONFUSION_HEATMAP.py`
- `direct-preference-control/run_direct_preference_heatmaps.py`

## Verification

After the fix, the small tree baseline file correctly records:

```text
tree     answer   answer_token
cherry   cherry   41980
maple    maple    55480
oak      oak      38971
sequoia  sequoia  11506
willow   willow   690
```

The regenerated tree confusion matrix no longer has `maple`, `oak`, and `sequoia` all pointing to `majestic`.

The statistical analysis was rerun after regeneration. The post-fix subliminal-number diagonal coefficients were:

```text
Small Animals: gamma = 0.023896774, p = 0.019581722
Small Trees:   gamma = 0.0033008575, p = 0.44600382
Large Animals: gamma = 0.0093515938, p = 0.00092729318
Large Trees:   gamma = 0.00061729016, p = 0.67334994
```

## Remaining Limitation

The current fix intentionally handles only the first token of each intended label. This was done to keep the immediate fix scoped.

For multi-token labels, the scripts now warn and use the first intended token:

```text
Warning: target label 'sequoia' is multi-token [11506, 78, 689]; using first token 11506 for now.
```

This is better than measuring an unrelated argmax token such as `majestic`, but it is still not the final correct implementation for multi-token labels.

The proper future fix is to score the full intended completion sequence by conditional log probability:

```text
log P(token_1 | prompt)
+ log P(token_2 | prompt, token_1)
+ ...
```

That would allow exact scoring of full labels such as `sequoia`, `redwood`, `eucalyptus`, and other multi-token names.

## Lessons

Argmax continuations are useful for debugging and discovery, but they should not define semantic labels in an evaluation matrix.

For labeled experiments, the target must be explicit:

```text
column = intended label
measurement = probability/logprob of that intended label
```

Using the model's free-form next token as the target silently changes the experiment question.
