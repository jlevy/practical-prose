# Bracket Tags Test

This paragraph has a [VERIFIED] tag and a [DERIVED] tag in prose.

```
This code block has [SHOULD NOT COUNT] and [ALSO EXCLUDED] tags.
```

Another [UNVERIFIED] tag in prose after the code block.

Inline code also excluded: `[NOT COUNTED]` should be stripped.

The assumption is tagged [ASSUMING: base rates hold] and the derivation is shown
inline as [DERIVED: 89.6 / 614.5 = 14.6%].

The error rate rose [observed], the largest swing this quarter [judged], which we
read as an auth-path regression [interpreted], so we roll back [implied].

Mixed case [Observed] and lowercase non-rung [placeholder] text are not tags.
