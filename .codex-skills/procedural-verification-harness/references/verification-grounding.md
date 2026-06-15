# Verification Grounding

Use this when an artifact can be wrong in a way that only appears when it runs,
renders, animates, or receives input.

## Rule

Do not stop at writing files. Run or render the artifact in its natural
environment and observe the actual result before saying it is done.

Static checks prove syntax or structure. They do not prove that a UI is usable,
a scene starts, an animation moves, or a game loop works.

## Examples

- Godot: run the project, headless smoke script, import pass, screenshot mode,
  or project-specific handoff command.
- Web: serve locally, open in a browser or Playwright, inspect console errors,
  and observe the rendered UI.
- SVG/canvas/chart: render to an image and inspect the output.
- Script artifact: execute it and inspect stdout/stderr plus produced files.

## GodotGame Notes

Prefer project-specific commands first. Known useful patterns in this workspace:

- use the local Godot 4.6 console binary when appropriate
- run import passes for fresh assets before diagnosing loader failures
- isolate smoke-test save files and user data when possible
- treat target-command engine warnings as unfinished work unless documented
- avoid relying on framebuffer pixel checks alone when headless rendering is
  unstable; use state/log assertions too

Local console binary:

```powershell
C:\DevWork\GodotGame\Godot_v4.6.3-stable_win64.exe\Godot_v4.6.3-stable_win64_console.exe
```
