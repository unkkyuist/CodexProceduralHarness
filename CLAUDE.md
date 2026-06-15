# Claude Instructions

The canonical workspace instructions are in `AGENTS.md`.

Claude or Claude-Code-style agents working in `C:\DevWork\GodotGame` should
use `AGENTS.md` as the adapted local replacement for the upstream fablize and
prometheus setup blocks. Do not run upstream setup scripts automatically; this
workspace keeps the adapted rules in plain instruction files and local Codex
skills.

Compared with upstream Claude Code use, this workspace does not assume
UserPromptSubmit hooks, Stop hooks, auto-star setup, or Claude-managed plugin
installation. Treat the rules as always-on written instructions, not hidden
runtime hooks.
