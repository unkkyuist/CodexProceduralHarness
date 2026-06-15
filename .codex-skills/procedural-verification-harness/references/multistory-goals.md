# Multi-Story Goals

Use this for large or sequential work. The point is not bureaucracy; it is to
prevent unverifiable "done" claims.

## Context First

Do not decompose from guesses. Inspect enough to know:

- target paths and entry points
- project conventions
- the command or observation that proves success
- similar local examples, if any

## Good Unit Criteria

Each unit should be:

- independently verifiable
- independently performable after its prerequisites
- one-dimensional
- concrete enough to express as a command or observation

The last unit should be final verification.

## Goal Sentence Pattern

```text
Do <specific change> in <specific area>. Verification: <command or observation>
shows <expected result>.
```

Example:

```text
Fix the inventory crash in scripts/inventory.gd. Verification: the project
smoke test exits 0 and the log contains no inventory null-access error.
```

## Codex Adaptation

The upstream prometheus workflow delegates enforcement to a ZCode `/goal`
runtime. Codex may not have that runtime available. In this workspace:

- propose `/goal` sentences only if the user explicitly wants a runtime goal
  workflow
- otherwise use a visible plan/checklist and keep evidence per item
- do not claim the agent can set `/goal` unless the current toolset exposes it

## Persistent Ledger

For work that may span turns, use `scripts/goal_ledger.py` from the skill
folder. It stores state in `.codex-harness/` by default.

Example:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py create --brief "Combat polish" --goal "hit flash::player hit flashes visibly and smoke test logs state" --goal "final verification::Godot smoke command exits 0 without new warnings"
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py next
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G001 --status complete --evidence "Changed player feedback and smoke test passed the hit-state assertion."
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py next
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G002 --status complete --evidence "Final smoke passed." --verify-cmd "Godot --path . --headless --script tools/smoke.gd" --verify-evidence "exit 0; no new engine warnings"
```

The final goal cannot complete without verification command and evidence. This
is still a voluntary tool call in Codex, so the agent must choose to use it.
