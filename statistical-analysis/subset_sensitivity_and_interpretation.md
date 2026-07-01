# Subset Sensitivity and Interpretation

## Summary

The small 4-animal subliminal-number result should not be treated as a stable standalone estimate. It is sensitive to which animals are included.

After fixing the target-token bug, the small animal matrix had:

```text
gamma = 0.023896774
p = 0.019581722
```

This is statistically positive in the fitted row/column/diagonal model. However, when we sampled many 4-animal subsets from the larger fixed animal matrix, gamma varied substantially.

## 4x4 Subset Sampling

We sampled 5,000 random 4-animal subsets from:

```text
large-animal-confusion/animal_confusion_matrix_data.csv
```

and refit the same model for each 4x4 submatrix:

```text
probability_delta ~ C(source) + C(target) + is_diagonal
```

The sampled gamma distribution was:

```text
mean gamma     0.00994
median gamma   0.00313
std            0.01539
2.5%          -0.00344
97.5%          0.05186
min           -0.01841
max            0.07995
```

The original small-animal gamma was:

```text
0.023896774
```

Across random 4-animal subsets:

```text
fraction positive = 89.18%
fraction >= original small-animal gamma = 14.46%
```

The sampled results are saved here:

```text
statistical-analysis/large_animal_4x4_gamma_samples.csv
```

## Interpretation

The small animal result is positive, but it is not uniquely compelling. A gamma as large as the original 4-animal result occurs in about 14.5% of random 4-animal subsets from the larger animal matrix.

This means the small animal result is above typical, but not rare enough to carry much evidential weight by itself.

## Overall View

The evidence is mixed and fragile:

- The original tree analysis was broken by a target-token selection bug.
- After the fix, tree results are positive but not statistically significant.
- The Qwen numeric subliminal experiment is not viable under the current prompt because corrected three-digit numeric completions have effectively zero probability.
- The Llama animal condition retains a positive diagonal signal.
- The small Llama animal signal is subset-sensitive.
- The direct preference controls are much stronger than the subliminal-number effects, which is expected but also highlights the small size of the subliminal signal.
- First-token scoring remains a limitation, especially for multi-token labels.

The most defensible conclusion is:

```text
We do not find robust cross-category or cross-model evidence for subliminal prompting.
One Llama animal condition retains a small positive diagonal effect after fixes,
but the result is sensitive to animal subset and much weaker than direct preference control.
```

This does not conclusively prove that no subliminal-number effect exists, but it does substantially weaken the broad claim and shows that the setup is highly vulnerable to tokenization, target selection, and subset-choice artifacts.
