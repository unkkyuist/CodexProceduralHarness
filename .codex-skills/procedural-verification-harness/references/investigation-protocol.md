# Investigation Protocol

Use this for debugging, crashes, test failures, confusing runtime behavior, and
code review validation.

## Procedure

1. Reproduce or inspect the exact failure before forming a fix.
2. List plausible hypotheses when the cause is not obvious.
3. For each hypothesis, identify confirming or refuting evidence.
4. Read the real code path end to end instead of patching the first symptom.
5. Trace the causal chain: what allowed the visible failure to happen?
6. Verify the cause before changing code when feasible.
7. Verify after the fix with the same failure path and the strongest relevant
   regression check.

## Report Shape

Keep the final report short, but include:

- root cause
- changed files
- verification command and result
- rejected hypotheses when they materially affect confidence
- remaining risks or unavailable checks

For reviews, findings come first. Separate low-confidence possibilities from
validated issues.
