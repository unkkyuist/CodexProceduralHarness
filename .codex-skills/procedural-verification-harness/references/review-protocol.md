# Review Protocol

Use this for code review, security-adjacent review, or regression checks.

## Output Order

1. Findings first, highest severity first.
2. File and line references for each finding where available.
3. Why it matters and what behavior can break.
4. Open questions or assumptions.
5. Short summary only after findings.

## Validation

- Treat first impressions as hypotheses.
- Trace the relevant path before reporting a bug.
- Keep low-confidence findings separate from validated findings.
- For security review, escalate to the dedicated security-scan workflow if the
  user asks for a security review rather than a normal code review.

## No Findings

If no issue is found, say so clearly and name any remaining test gaps or
residual risk.
