# Codex Procedural Harness

Codex-compatible procedural verification harness for coding workspaces,
especially Godot/game projects.

This package adapts the useful parts of:

- `fivetaku/fablize`: https://github.com/fivetaku/fablize
- `tmdgusya/prometheus`: https://github.com/tmdgusya/prometheus

It does not install Claude Code hooks, does not assume a ZCode-only `/goal`
runtime, and does not auto-star any repository. The adaptation is plain
workspace instructions plus a local Codex skill.

## What It Adds

- workspace `AGENTS.md` rules for evidence-backed completion
- `CODEX.md` and `CLAUDE.md` compatibility entry points
- a local `.codex-skills/procedural-verification-harness/` skill
- optional persistent goal/evidence ledger with a final verification gate
- task routing, runtime verification, debugging, review, and early-stop
  references

## Automatic Codex Use

Once installed into a workspace, the harness is automatic through `AGENTS.md`.
The user does not need to say "fablize", "prometheus", "verify as you go", or
"goal ledger" for baseline behavior to apply.

Codex should automatically:

- inspect before editing
- route tasks by signal
- keep trivial edits lightweight
- load the local skill for substantial multi-step, debugging, review, or
  runtime-rendered artifact work
- use `goal_ledger.py` only when durable progress/evidence state is useful

Recommended prompt patterns and task-specific usage are in
`RECOMMENDED_USAGE.md`.

## Install Into A Workspace

From this repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Target C:\path\to\workspace
```

By default the installer refuses to overwrite existing files. To overwrite
with timestamped backups:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Target C:\path\to\workspace -Force
```

To preview:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Target C:\path\to\workspace -DryRun
```

To also install the skill into the user's Codex global skill folder for
automatic skill discovery:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Target C:\path\to\workspace -InstallGlobalSkill
```

Use `-Force` if the global skill already exists and should be backed up then
replaced.

## Codex vs Claude

See `CODEX_VS_CLAUDE.md`.

Short version: Codex uses always-on plain files plus optional scripts. Claude
Code can use upstream plugin hooks, so Claude may have stronger hook-level
enforcement when those hooks are installed. This package avoids hidden hooks,
auto-star behavior, and ZCode-only `/goal` assumptions.

## Git Publish Checklist

```powershell
cd C:\DevWork\GodotGame\CodexProceduralHarness
git init
git add .
git commit -m "Initial Codex procedural harness"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Before public release, review `LICENSE` and `NOTICE.md`. The upstream copyright
holders are already listed; replace the adaptation contributor name if you want
the repository owner named more specifically.

## License

MIT. See `LICENSE` and `NOTICE.md`.
