---
name: work-with-files
description: Use when the user requests a persistent task workspace or when task artifacts must persist across sessions or agents for recovery, review, handoff, audit, reuse, or reproducibility. Store them in an isolated Git repository for each task workspace under `.work/`. Ordinary project edits, one-turn work, routine command output, and final deliverables do not by themselves justify creating a task workspace.
---

# Work With Files

## Terms

Within this skill, the following terms have these meanings:

- **Host root**: the Git repository root containing the agent session's working directory, or the working directory itself when no repository exists. It contains the `.work` container.
- **Host repository**: the Git repository rooted at the host root, when one exists. It is separate from every task workspace's Git repository.
- **`.work` container**: `<host-root>/.work/`. It contains task workspaces and is not itself a Git repository.
- **Task workspace**: one direct child of the `.work` container, associated with one user goal and initialized as an independent Git repository.
- **Control files**: `goal.md`, `approach.md`, and `run-log.md` at the root of a task workspace.
- **Workspace artifact**: any file stored in a task workspace as part of the work, including control files, supporting files, generated results, and final deliverables.
- **Final deliverable**: an output the user asked to receive or use.

## Activation

If the skill is invoked for work that does not require persistent task state, continue without creating a task workspace.

## Initialize the `.work` Container

Derive the host root from the agent session's working directory. Use `<host-root>/.work/` if it exists. If absent, ensure `/.work/` is ignored by the host repository when one exists, then create the container. Do not initialize the container as a Git repository.

## Reuse or Initialize Task Workspace

1. Use a known task workspace path when available. Otherwise, compare the current goal and constraints with the `goal.md` files under the `.work` container. Do not select by recency; ask the user when the match is ambiguous.
2. If a clear match exists, read its control files and relevant reports, then reuse it without reinitializing or overwriting it.
3. If none matches, create an unused `<host-root>/.work/YYYY-MM-DD-HHmm-short-slug/` and initialize it as an independent Git repository on branch `main` without a remote. Use Git's configured identity; if none is available, set a neutral identity in the task workspace only.
4. For a new task workspace, initialize the control files according to the Artifact Contract, then commit the initial state before substantive work.

Default layout:

```text
.work/
  YYYY-MM-DD-HHmm-short-slug/
    .git/
    goal.md
    approach.md
    run-log.md
```

Common directories include `reports/` for detailed findings, `raw/` for source evidence, `scripts/` for task-local helpers, and `outputs/` for generated results.

Do not commit or push the host repository as part of this workflow.

## Artifact Contract

| Artifact | Purpose and contents |
| --- | --- |
| `goal.md` | Keep a concise, current statement of the user's core need, binding constraints and non-goals, observable success condition, and unresolved questions that could change the work. |
| `approach.md` | Keep only the current high-level strategy, major phases, important assumptions or architectural choices, and next checkpoint. |
| `run-log.md` | Maintain a concise chronological index of decisions and events that help recovery, with relevant links. Use local time with a numeric UTC offset, for example `2026-08-09 14:37 +08:00`. |
| `reports/YYYY-MM-DD-HHmm-topic.md` | Use for detailed findings that must persist for handoff, audit, or reproducibility and are too detailed for the control files. |
| Other workspace artifacts | Keep supporting evidence, helpers, and generated results under names and structures suited to the current goal. |

Preserve the semantic core of the user's need, not necessarily the original wording. Treat suggested implementations as revisable unless the user makes them binding constraints. Discuss any reinterpretation that would change the core need, scope, binding constraints, or success condition.

Keep `goal.md` and `approach.md` as concise current-state controls, not activity logs. Revise `goal.md` only when one of the elements defined in the Artifact Contract changes. Revise `approach.md` only when the current strategy, major phase, important assumptions or architectural choices, or next checkpoint changes.

Do not update either file for routine progress, validation results, commits, or wording changes that preserve meaning. If leaving a file unchanged would not mislead a resuming agent or change its next action, leave it untouched. When revision is necessary, rewrite or consolidate the current state instead of appending history. Record only recovery-relevant decisions and events in `run-log.md`; Git preserves earlier states.

Do not create reports for routine progress or information already preserved elsewhere in the task workspace. When a report is necessary, keep it concrete and detailed, place bulky raw output in a supporting artifact, and link to it instead of duplicating it.

## Task Workspace Git History

Commit automatically in the task workspace's Git repository:

- after completing a distinct phase or recording an agreed decision;
- before yielding when changes remain uncommitted.

Review the task workspace's Git status and diff, then stage the intended changes. Skip empty commits.

Preserve existing history; do not amend, squash, rebase, or delete commits automatically. Do not add a remote or push.

## Finish

Before finishing:

1. Confirm that `goal.md` and `approach.md` still match the current state; revise them only when the update threshold above is met.
2. Update `run-log.md` only when a recovery-relevant decision or event remains unrecorded. Create or update a report only when it meets the report threshold above.
3. Commit any remaining task workspace changes and confirm its Git working tree is clean.
4. Put final deliverables in the user-specified or task-appropriate location, and report where they were placed.
