# Codex vs Claude Usage

This workspace uses a Codex-native adaptation of `fablize` and `prometheus`.
The behavior is intentionally similar at the procedure level, but different at
the runtime/enforcement level.

## Main Difference

In Codex, the harness is always-on through `AGENTS.md` plus optional local
skills and scripts. In Claude Code, the upstream `fablize` plugin can use
Claude-specific plugin hooks to inject routing context or block early stops.

## Comparison

| Area | Codex adaptation | Claude / upstream-style use |
| --- | --- | --- |
| Activation | Automatic through `AGENTS.md` in the workspace | Plugin commands, always-on setup block, and Claude hooks where installed |
| User trigger needed | No for baseline behavior | No if always-on/hook setup is installed; yes if only using slash commands |
| Routing | Instruction-driven: Codex classifies the task and loads needed references | Hook-driven in `fablize` via `UserPromptSubmit` router |
| Early-stop prevention | Checklist/instruction in `AGENTS.md` and `early-stop-guard.md` | Can be deterministic Stop hook in Claude Code |
| Goal tracking | Optional `goal_ledger.py`; agent must voluntarily call it | `fablize` has `goals.py`; `prometheus` delegates to ZCode `/goal` runtime |
| `/goal` | Only proposed if current runtime supports it and user wants it | Prometheus assumes ZCode `/goal`; Claude Code itself does not automatically provide that runtime |
| Enforcement strength | Strong written procedure, plus optional ledger gate | Stronger when hooks/runtime goal verifier are actually installed |
| Account side effects | None | Upstream `fablize` setup can star the repo via `gh` after consent |
| Portability | Plain files: `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, `.codex-skills/` | Claude plugin format and hook settings are Claude-specific |
| Verification | Codex must run/render/check using available tools in the current session | Same principle; hook may remind or block, but the agent still needs real tool evidence |

## Practical Result

Codex will now apply the baseline automatically:

- inspect before editing
- route substantial work into the right discipline
- decompose large work only after context is known
- run or render observable artifacts before completion
- avoid final answers that only promise future work
- report verification evidence and remaining risk

The main limitation is enforcement. Codex cannot be forced by the upstream
Claude hooks in this plain-file setup. The strongest Codex-native enforcement
available here is the always-on instruction layer plus `goal_ledger.py` when a
durable verification gate is useful.
