---
name: procedural-verification-harness
description: Use for multi-step work, long autonomous tasks, debugging, code review, task routing, persistent goal/evidence ledgers, early-stop prevention, or artifacts that must be run or rendered before completion. Adapted for Codex from fablize and prometheus without Claude hooks or ZCode-only goal runtime assumptions.
metadata:
  short-description: Evidence-backed completion and runtime verification
---

# Procedural Verification Harness

This skill is the detailed workflow behind the always-on rules in `AGENTS.md`.
Use it when the task needs evidence-backed completion rather than only file
edits. Do not wait for the user to name the skill; load it automatically for
the task classes below.

Automatic routing signals:

- 2+ sequential implementation or content-production steps
- debugging, crash investigation, test failure, or unknown cause
- rendered/executable artifacts: Godot, web, HTML, SVG, games, charts,
  screenshots, animations
- review work where possible findings need validation
- user says "finish it", "take it all the way", "verify as you go",
  "split into goals", "fablize", or "prometheus"

## 1. Context Gate

Before planning or decomposing, confirm:

1. actual paths and modules involved
2. local structure and conventions
3. observable success condition
4. relevant prior examples or research, when needed

If context is missing, inspect first. Use subagents only when the user has
explicitly asked for delegated or parallel agent work; otherwise do the
exploration directly.

## 2. Multi-Step Loop

For 2+ sequential units:

1. Write a compact plan with independently verifiable units.
2. Work on one unit at a time.
3. Attach evidence to completion of each unit.
4. Make the final unit end-to-end verification.

Each unit must have a concrete verification command or observation. Avoid
vague targets such as "make it better" unless they have measurable acceptance
criteria.

If a `/goal` or runtime goal feature is available and the user explicitly wants
it, propose exact goal sentences for the user to set. Otherwise use Codex's
normal plan/checklist plus evidence in the final report.

When a task may span turns or needs durable evidence, use the local ledger:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py create --brief "..." --goal "title::objective"
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py next
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G001 --status complete --evidence "..."
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py status
```

The final goal requires both `--verify-cmd` and `--verify-evidence`.

See `references/multistory-goals.md`.

## 3. Debugging and Investigation

For bugs and unknown failures:

1. Reproduce or inspect the exact failure first.
2. Track multiple hypotheses before committing to one cause.
3. Gather evidence on the real code path.
4. Trace the causal chain.
5. Verify before and after the fix.

See `references/investigation-protocol.md`.

## 4. Verification Grounding

For artifacts whose correctness only appears at runtime, run or render the
artifact and observe the result before completion.

For Godot work in this workspace, start from the project's documented command.
If none exists, look for smoke tests under `tools/`, `scripts/`, or project
docs, then use the local Godot console binary where appropriate:

```powershell
C:\DevWork\GodotGame\Godot_v4.6.3-stable_win64.exe\Godot_v4.6.3-stable_win64_console.exe
```

See `references/verification-grounding.md`.

## 5. Task Routing

Use the smallest matching discipline for the task. For signal examples and
routing decisions, see `references/routing-matrix.md`.

## 6. Early-Stop Guard

Do not finish with only a promise, static parse, or file creation when runtime
evidence is required. Before final response, check that every completion claim
has evidence from this session. See `references/early-stop-guard.md`.

## 7. Reviews

For code reviews, lead with findings and separate low-confidence possibilities
from validated issues. See `references/review-protocol.md`.

## 8. Capability Ceiling

If the blocker is repeated, open-ended creative depth, or out-of-spec discovery
beyond available evidence, report the limit and recommend escalation rather
than faking confidence.

## Sources

Adapted from:

- https://github.com/fivetaku/fablize
- https://github.com/tmdgusya/prometheus

Local adaptation notes are in `references/upstream-adaptation.md`.
