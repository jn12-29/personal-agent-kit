---
name: review-fix-loop
description: Use whenever a task modifies files — code, documentation, configuration, tests, scripts, prompts, examples, or generated project files. Enforces an explicit review-after-implementation loop with re-review after every fix, instead of treating review as optional final polish.
---

# Review-Fix Loop

**Trigger:** Any task that modifies files. Applies to code, documentation, configuration, tests, scripts, prompts, examples, and generated project files. Do not treat review as an optional final polish step.

## Minimum Loop

1. Inspect the relevant current files and authority documents before editing.
2. Make the smallest correct change.
3. Review the changed files against the user request and applicable project rules.
4. Fix confirmed issues.
5. Re-review the changed surface after the fix.
6. Run the smallest relevant verification command or targeted search.
7. Stop only when the latest review after the latest fix has no confirmed blockers.

For trivial single-file edits, the review may be a local self-review, but it must still happen after the edit and after any fix.

## When To Use Independent Read-Only Reviewers

Any one of the following:

- The change touches more than one file.
- The change affects behavior, not just wording.
- The change affects runtime flags, scheduling, cache semantics, paths, configuration fields, schemas, serialization, public outputs, scripts, prompts, tests, or docs that define current behavior.
- The first review finds a blocker.
- The user explicitly asks for careful review or end-to-end completion.

## When To Use Multiple Independent Reviewers

Any one of the following:

- The change crosses module boundaries.
- The change affects shared contracts or public behavior.
- The change affects shared types, configuration, runtime state, schemas, serialization, pipeline boundaries, or user-facing outputs.
- The change is large enough to require agents or parallel work.

## Loop Rules

- Review must happen after implementation, not only before.
- If review finds blockers, fix them and then re-review. Do not stop after the fix.
- If a fix affects a shared contract, public behavior, or module boundary, re-run independent read-only review after the fix.
- When documentation and implementation conflict, treat documentation as the source of truth by default. Fix the implementation to satisfy the documented contract, even if that requires additional implementation work.
- Enforce the minimal true contract, not incidental implementation choices. Before treating a documented value as a blocker, distinguish required invariants and downstream dependencies from defaults, examples, tunable configuration, and task-specific parameters. If uncertain whether a value is a required invariant or downstream dependency, report a blocking ambiguity instead of inventing a fixed requirement.
- Only change documentation instead of implementation when the documentation is internally contradictory, impossible to implement, explicitly superseded by the user, or clearly stale status text rather than a current contract. In that case, record the final contract in documentation before or together with the implementation fix.
- Tests, compile checks, smoke tests, type checks, import checks, and targeted searches are verification. They do not replace review.
- A subagent implementation report is not proof of correctness. The main agent must verify or request read-only review of the changed surface.
- Do not summarize work as complete until the latest review after the latest fix reports no confirmed blockers and relevant verification passes.
- Keep fixes surgical: address the confirmed blocker without opportunistic refactors.

## Required Reporting For Non-Trivial Modifications

- `Review round N: found X blockers.`
- `Fix round N: fixed blockers A, B, C.`
- `Verification round N: passed/failed commands ...`
- `Re-review round N: no blockers / found new blockers ...`

## Final Response For Modified Files

Must include:

- Number of review-fix rounds completed.
- Blocking findings fixed.
- Latest review result.
- Verification commands and results.
- Any non-blocking residual risks.
