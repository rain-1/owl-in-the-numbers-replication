# Qwen Animal Preference Investigation Note

We tested `unsloth/Qwen2.5-7B-Instruct` on the animal preference setup with the requested animal list.

## Numeric Tokenization Fix

Qwen tokenizes leading-space numbers as multi-token sequences. For example:

```text
" 100" -> [220, 16, 15, 15]
```

The initial implementation incorrectly scanned for bare single-token digits such as:

```text
"1" -> [16]
```

That would correspond to completing `the1`, not `the 1`. The Qwen runner was patched to score full three-digit numeric completions from `000` through `999`, including the leading-space token sequence.

## Smoke-test Result

A smoke test with three animals (`bear`, `cat`, `dog`) selected the same best three-digit number for all three:

```text
bear -> 100, probability ~ 7.6e-16
cat  -> 100, probability ~ 5.6e-12
dog  -> 100, probability ~ 1.0e-13
```

These probabilities are effectively zero. This suggests Qwen assigns almost no probability mass to three-digit numeric completions after:

```text
My favorite animal is the
```

even under animal-preference prompts.

## Conclusion

The tokenizer bug was real and fixed, but the corrected smoke test indicates that this Qwen setup does not produce a meaningful numeric subliminal signal in the current prompt format.

We are therefore dropping the Qwen subliminal-number investigation for now rather than spending more time on a setup where the numeric candidates are essentially absent from the model's next-token distribution.

The direct preference control remains interpretable, but it is not evidence that the numeric subliminal condition works for Qwen.
