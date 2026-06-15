# Upstream Adaptation Notes

This local skill adapts concepts from two MIT-licensed public repositories:

- `fivetaku/fablize`: https://github.com/fivetaku/fablize
- `tmdgusya/prometheus`: https://github.com/tmdgusya/prometheus

## Absorbed

- run-and-observe verification for rendered or executable artifacts
- evidence-backed completion
- multi-step decomposition into independently verifiable units
- optional persistent goal ledger with final verification gate
- task-signal routing matrix
- final end-to-end verification unit
- debugging by reproduction, competing hypotheses, and causal-chain tracing
- early-stop prevention: do not promise work instead of doing it
- review reporting order and low-confidence filtering
- explicit escalation at model or evidence limits

## Adapted

- Claude Code plugin hooks become plain `AGENTS.md` and local Codex skill
  instructions.
- ZCode `/goal` enforcement becomes proposed goal sentences when the user wants
  that workflow; otherwise Codex uses a plan/checklist with evidence.
- Prometheus exploration subagents become local inspection by default. Explorer
  agents are used only when the user explicitly authorizes subagents or
  parallel agent work.
- Fablize's `goals.py` becomes `scripts/goal_ledger.py` with `.codex-harness/`
  state and Codex-oriented wording.

## Omitted

- upstream setup scripts
- auto-star behavior
- Claude-specific hook registration
- deterministic Stop hook installation
- any claim that the harness improves model capability

The result is a Codex-compatible procedure layer for this Godot workspace, not
an installed copy of either upstream project.
