# GodotGame Agent Instructions

These are the workspace-level instructions for `C:\DevWork\GodotGame`.
They adapt the useful parts of `fivetaku/fablize` and
`tmdgusya/prometheus` for Codex without relying on Claude Code hooks or a
ZCode-only `/goal` runtime.

## Automatic Mode

This file is the always-on procedural layer for the workspace. Apply it to
every task automatically; the user does not need to say "fablize",
"prometheus", "verify as you go", or "goal ledger" for the baseline rules to
apply.

For every request:

1. Apply the baseline rules below.
2. Silently route the task by signal: debugging, rendered artifact, multi-step
   work, review, research, or trivial edit.
3. Keep trivial one-line edits lightweight.
4. For substantial work, load the local harness skill and only the needed
   reference files.
5. Use the persistent goal ledger only when durable state or cross-turn
   evidence is useful.

See `CODEX_VS_CLAUDE.md` for how this differs from using the upstream harness
inside Claude Code.

## Baseline

Use these rules for all work in this workspace unless a project-specific
`AGENTS.md` gives narrower instructions.

1. Inspect before editing.
2. Prefer the existing project structure, naming, and style.
3. Keep changes surgical and tied to the user's request.
4. Protect user work. Do not revert unrelated edits.
5. Verify with a real command, render, smoke test, or runtime observation.
6. Report what changed, where, what was verified, and any remaining risk.

For multi-step or ambiguous work, use the loop:

```text
1. Inspect: identify actual files, structure, constraints, and success signals.
2. Plan: split into verifiable units only after the context is sufficient.
3. Change: make the smallest useful edit.
4. Test: run the strongest relevant check available in this workspace.
5. Report: ground completion claims in tool output from this session.
```

## Always-On Routing And Local Harness Skill

Before starting substantial work, load the local harness skill automatically
when its detailed workflow is relevant:

```text
.codex-skills/procedural-verification-harness/SKILL.md
```

Use it for:

- multi-step project creation or feature work
- long autonomous work
- debugging or unknown-cause failures
- rendered or executable artifacts: Godot games, web apps, HTML, SVG, UI,
  charts, screenshots, animations, scripts with observable output
- review work where low-confidence findings must be separated from validated
  findings

The skill includes optional references for task routing, review handling,
early-stop checks, and a persistent goal ledger script adapted from the
upstream goal engine. Use the script only when durable state is helpful; a
short in-turn checklist is enough for small jobs.

## Context Before Decomposition

Do not split a task into goals from guesses. First answer these questions from
actual local context:

1. Which files, scenes, scripts, tools, or folders will this touch?
2. What structure, conventions, and dependencies already exist there?
3. What observable condition proves the task is done?
4. If the task needs research, what known approaches or local examples have
   been checked?

If any answer is unknown, inspect locally before decomposing. If the user
explicitly asks for subagents or parallel agent work, explorer agents may be
used for bounded context gathering. Otherwise, gather the context directly.

## Verifiable Goal Decomposition

For 2+ sequential work items, each unit must be:

- independently verifiable
- independently performable once its prerequisites are done
- one-dimensional
- expressed with a concrete verification command or observation

The final unit should be end-to-end verification.

If a runtime goal system is available and the user explicitly wants it, propose
goal sentences for the user to set. Do not assume the agent can set `/goal`
itself. In ordinary Codex work, use a concise plan/checklist and keep evidence
with each completed item.

For long work that may span turns or needs durable evidence, use:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py create --brief "..." --goal "title::objective"
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py next
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G001 --status complete --evidence "..."
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py status
```

The final goal cannot be marked complete without `--verify-cmd` and
`--verify-evidence`.

Good goal shape:

```text
Implement X in path/to/file.gd. Verification: running `...` exits 0 and logs
the expected state without engine errors.
```

Bad goal shape:

```text
Make the game feel better.
```

## Debugging Protocol

For bugs, test failures, crashes, or unknown behavior:

1. Reproduce or inspect the exact failure first.
2. Keep at least three plausible hypotheses when the cause is not obvious.
3. Gather evidence for and against each hypothesis by reading the real code
   path end to end.
4. Trace the causal chain, not only the visible symptom.
5. Verify before and after the fix.
6. Report rejected hypotheses when they matter to confidence.

## Verification Grounding

If correctness only appears when something runs or renders, run or render it
before saying it is done.

Static checks are not enough for:

- Godot games and scenes
- web UIs
- HTML/SVG/canvas
- charts
- animations
- generated images used in UI
- scripts whose output is the artifact

For Godot work, prefer the local verified Godot console binary when available:

```powershell
C:\DevWork\GodotGame\Godot_v4.6.3-stable_win64.exe\Godot_v4.6.3-stable_win64_console.exe
```

Use the project's own smoke tests, handoff commands, or documented run path
first. If generated WAV/PNG assets fail with loader/import errors, run a Godot
import pass before treating it as game logic failure.

## GodotGame Workspace Rules

- New projects and prototypes should be created in their own folder under
  `C:\DevWork\GodotGame` unless the user names an existing project.
- Do not assume the workspace root is a git repository.
- For handoff-driven projects, treat `tasks.txt`, `TASKS.md`, or similar files
  as contracts. Mark completion only after code changes and verification.
- Prefer Godot 4.6-compatible GDScript patterns: explicit types where inference
  is fragile, preload-based references when `class_name` load order is risky,
  and web-friendly dependencies unless the user asks otherwise.
- Automated smoke tests should isolate save files and user data when possible.
- Engine warnings from the target verification command count as remaining work
  unless they are known benign and documented.

## Early-Stop Guard

Do not stop after saying what you will do. Either do the work, verify it, and
report evidence, or state the concrete blocker.

Before final response, check:

- Did the requested artifact or edit actually get produced?
- Did I run or observe the strongest relevant check available?
- Are any claims stronger than the evidence I have?
- Did I avoid unrelated refactors and unrelated cleanup?

## Capability Ceiling

A harness cannot raise model capability. If the same blocker repeats after
serious investigation, if open-ended creative detail is the core value, or if a
deep review needs discovery beyond the available evidence, report the limit
clearly and propose escalation rather than pretending the work is complete.

## Upstream Attribution

This workspace adapts procedures from:

- `fivetaku/fablize`: https://github.com/fivetaku/fablize
- `tmdgusya/prometheus`: https://github.com/tmdgusya/prometheus

Do not run their setup scripts directly in this workspace unless the user
explicitly asks. The adapted Codex version lives in `AGENTS.md` and
`.codex-skills/procedural-verification-harness/`.
