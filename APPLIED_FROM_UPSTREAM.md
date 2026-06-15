# Applied From Upstream

This file records what was reviewed from `fivetaku/fablize` and
`tmdgusya/prometheus`, what was absorbed, and what was intentionally left out.

## Newly Absorbed In This Pass

| Upstream element | Local result |
| --- | --- |
| `fablize/scripts/goals.py` | `scripts/goal_ledger.py` with `.codex-harness/` state and final verification gate |
| `fablize/hooks/router.sh` | `references/routing-matrix.md` task-signal routing |
| `fablize/hooks/finish-the-work.sh` | `references/early-stop-guard.md` final-response checklist |
| `fablize/commands/setup.md` | `scripts/install.ps1`, without auto-star or hook side effects |
| `prometheus` context-first decomposition | `AGENTS.md`, `SKILL.md`, and `references/multistory-goals.md` |
| review/investigation discipline | `references/review-protocol.md` and `references/investigation-protocol.md` |

## Already Absorbed

- evidence-backed completion
- run-and-observe verification for runtime/rendered artifacts
- debugging by reproduce, hypotheses, causal chain, and before/after proof
- capability ceiling honesty
- Codex-compatible treatment of `/goal`: propose only when a runtime goal
  system exists and the user wants it

## Not Applied

| Upstream element | Reason |
| --- | --- |
| Claude `UserPromptSubmit` hook | Codex distribution should not depend on Claude hook settings |
| Claude Stop hook install | Useful behavior is captured as instructions; no hidden runtime modification |
| auto-star during setup | Account-side effect is inappropriate for a general package |
| ZCode `/goal` enforcement | Runtime is not available from ordinary Codex tool calls |
| `prometheus-visualized.html` | Demo artifact, not needed for runtime behavior |
| model-specific effectiveness claims | Not proven for this local adaptation |

## Practical Behavior Change

After installation, future tasks should:

1. inspect local context before planning
2. split large work into verifiable units
3. use `goal_ledger.py` when durable progress/evidence tracking is useful
4. run/render observable artifacts before completion
5. report evidence, not only intent

## Automatic Mode

`AGENTS.md` is the automatic layer. Trigger phrases are no longer required for
baseline behavior. The local skill is loaded for substantial work, and the
global Codex skill can be installed with `scripts/install.ps1 -InstallGlobalSkill`.
