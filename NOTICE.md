# Notices

This repository is a Codex-oriented adaptation of procedures from two
MIT-licensed upstream projects.

## Upstream Projects

### fivetaku/fablize

- Source: https://github.com/fivetaku/fablize
- License: MIT as represented by the upstream README/license badge and
  preserved downstream copyright notice
- Copyright holder listed by downstream license: Copyright (c) 2025 fivetaku
- Adapted concepts:
  - verification grounding
  - investigation protocol
  - task-signal routing
  - early-stop guard behavior
  - multi-story goal ledger and final verification gate

### tmdgusya/prometheus

- Source: https://github.com/tmdgusya/prometheus
- License: MIT
- Copyright holder in upstream `LICENSE`: Copyright (c) 2026 roach
  (prometheus)
- Upstream license also preserves: Copyright (c) 2025 fivetaku
- Adapted concepts:
  - context sufficiency before decomposition
  - independent-unit decomposition
  - user-set runtime goal limitation
  - capability ceiling escalation

## Local Adaptation

- Copyright holder for local adaptation: Codex Procedural Harness contributors
- Distribution form: plain `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, local Codex
  skill files, references, and a PowerShell installer.

## Intentionally Not Bundled

- Claude Code hook registration
- deterministic Stop hook installation
- upstream setup scripts
- auto-star behavior
- ZCode `/goal` runtime enforcement
- model-family effectiveness claims
- visualized HTML demo files

These omissions are intentional because the package targets Codex workspaces
and should not modify user settings or accounts as an install side effect.
