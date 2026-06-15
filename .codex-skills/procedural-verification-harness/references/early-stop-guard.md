# Early-Stop Guard

Use this checklist before ending a turn.

## Block Yourself If

- The response says what you will do next instead of doing the requested work.
- The artifact was written but never run, rendered, or observed even though
  correctness depends on runtime behavior.
- A final claim says "works" but only syntax or file existence was checked.
- A test/build failure was not reported.
- A multi-step task has incomplete units without a clear blocker.

## Safe Stops

It is acceptable to stop when:

- the requested work and verification are complete
- the next action requires user-only input or approval
- the task is blocked by a concrete external condition
- the user asked only for analysis, a plan, or a decision

## Final Claim Test

Every concrete completion claim should map to one of:

- file path changed or created
- command run and result observed
- renderer/browser/game output observed
- exact blocker and remaining work stated
