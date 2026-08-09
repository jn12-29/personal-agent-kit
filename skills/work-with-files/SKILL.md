---
name: work-with-files
description: Use when task-local artifacts need to persist beyond chat for recovery, review, handoff, audit, reuse, or reproducibility. Creates one isolated Git repository per task under `.work/`, keeps goal and approach records concise, stores detailed reports, and commits meaningful checkpoints. Do not use for trivial work or ordinary project-file edits alone.
---

# Work With Files

Persist useful task work without confusing temporary artifacts with project files or final deliverables. Create a workspace only when persistence has concrete value; keep trivial answers, throwaway calculations, and ordinary command output in chat.

## Task Workspace

1. Locate the project root, or use the current task root when no project repository exists.
2. Ensure the outer project Git repository ignores `/.work/`.
3. Create one directory per task as `.work/YYYY-MM-DD-HHmm-short-slug/`.
4. Initialize the task directory as an independent Git repository on branch `main`. Do not add a remote.
5. Use the existing Git identity when available. Otherwise set a neutral identity only in the task repository; never change global Git configuration.
6. Create only the artifacts the task needs.

```text
.work/YYYY-MM-DD-HHmm-short-slug/
  .git/
  goal.md
  approach.md
  run-log.md
  reports/
  raw/       # optional evidence or extracts
  scripts/   # optional task-local helpers
  outputs/   # optional intermediates
```

The outer project repository must ignore `.work/`. Never commit or push the outer repository through this workflow, and never treat files under `.work/` as delivered project artifacts.

## Artifact Contract

| Artifact | Content and authority |
| --- | --- |
| `goal.md` | Keep the user's core need, confirmed constraints and non-goals, observable success condition, and material unresolved questions concise and current. |
| `approach.md` | Keep only the current high-level strategy, major phases, important assumptions or architectural choices, and next meaningful checkpoint. |
| `reports/YYYY-MM-DD-HHmm-topic.md` | Record detailed scope, inputs, methods or commands, concrete findings with identifiers, decisions and rationale, verification, uncertainty, and output paths as relevant. |
| `run-log.md` | Maintain a concise chronological index of meaningful events and links. Use local time with a numeric UTC offset, for example `2026-08-09 14:37 +08:00`. |
| `raw/`, `scripts/`, `outputs/` | Keep supporting evidence, task-local helpers, and intermediate outputs only when they aid review, recovery, reuse, or reproducibility. |

Preserve the semantic core of the user's need, not necessarily the original wording. Treat wording, suggested implementations, and earlier agent proposals as revisable unless the user explicitly makes them binding constraints. Do not silently redefine the core need; discuss material reinterpretations with the user first.

Keep `goal.md` and `approach.md` as current-state control files, not histories. Revise the approach when evidence or user discussion supports a better solution. When the user changes the goal, update it and record the decision in `run-log.md`; Git preserves the earlier state.

Keep reports concrete and detailed, but place bulky raw output in a supporting artifact and link to it instead of duplicating it.

## Local Git History

Commit automatically inside the task repository:

- after creating the initial goal and approach;
- after a meaningful phase, report, or agreed decision;
- before yielding when meaningful changes remain uncommitted;
- when finalizing the task workspace.

Before committing, inspect the task repository status and diff, exclude unnecessary large files, and stage only task-repository files. Skip empty commits.

Do not amend, squash, rebase, rewrite, or delete task history automatically. Do not add a remote or push.

## Resume And Finish

When resuming, use an explicit task path when available. Otherwise inspect candidate `goal.md` files; do not assume the newest directory is correct. Before acting, read `goal.md`, `approach.md`, `run-log.md`, and the relevant reports.

Before finishing:

1. Make `goal.md` and `approach.md` reflect the current state.
2. Write any required detailed report and final minute-precision log entry.
3. Commit appropriate task artifacts and confirm the task repository is clean.
4. Put final deliverables in the user-specified or project-appropriate path and report where they were placed.
