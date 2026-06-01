# Planning State Reference

Use this reference when durable work needs on-disk planning state, when existing plan files may be stale, or when the task asks about file storage rules.

## Default Layout

Prefer existing repo conventions first. If no convention exists and durable state is useful, use:

```text
.planning/
  .active_plan
  <plan-id>/
    requirement.md
    plan.md
    progress.md
    findings.md  # optional
```

`.planning/.active_plan` contains only the active plan directory name, for example:

```text
2026-06-02-skill-improvements
```

Use `YYYY-MM-DD-short-slug` for `<plan-id>` unless the repo or tool provides a stable id. Keep the active directory name stable after other files link to it.

If the repo has a mature planning/spec convention that conflicts with `.planning/`, follow the repo convention but keep the same active-pointer and requirement/progress semantics where possible.

By default, `.planning/` is working state, not a project artifact, and should not be committed. When actually creating `.planning/`, ensure `.planning/` is ignored in `.gitignore` unless the user explicitly asks to track it or has intentionally commented out an existing ignore rule such as `# .planning/`. If the repo has no `.gitignore`, create the smallest one needed for the new working-state ignore entry. Treat a manually commented ignore rule as a deliberate override, not a formatting issue to "fix."

User-requested formal plan/spec deliverables are project artifacts. Put them where the user or repo expects them, not only inside ignored `.planning/` state. Use `.planning/<plan-id>/requirement.md` or `plan.md` to link to the formal deliverable and track current status.

## Active Plan Resolution

Use mechanical state before model judgment:

1. If an environment or tool-specific plan id is provided, use `.planning/<plan-id>/` when it exists.
2. Else if `.planning/.active_plan` exists and points to a directory with `requirement.md`, use that directory.
3. Else if exactly one `.planning/*/requirement.md` exists and its status is `active`, use that directory.
4. Else if several candidates exist, do not silently choose by recency alone. Compare the latest user request, requirement status, timestamps, and current repo state; if still unclear, ask or create a new active plan.
5. If no durable state is needed, use an inline plan and do not create `.planning/`.

If the active `requirement.md` says `complete`, `paused`, `reference-only`, or `superseded`, do not keep implementing it unless the latest user request explicitly reactivates or replaces it.

## File Roles

- `requirement.md`: current goal contract. It owns the requirement snapshot, target status, validity, non-goals, final acceptance check, and which plan files are active.
- `plan.md`: work breakdown, task interfaces, spec links, and handoff blocks. It is executable only while `requirement.md` is active and names it as an implementation target.
- `progress.md`: chronological progress, current phase, completed checks, blockers, verification results, and remaining work.
- `findings.md`: optional concise findings that affect the requirement, plan, spec, contract, or handoff, plus source links and decisions that would otherwise be lost from context.

Write planning-relevant facts to `findings.md` when exploration itself changes or justifies the plan. Put raw browser/PDF/image extracts, logs, bulky data, one-off scripts, and intermediate outputs in the repo's working-artifact location, such as `.work/<task-slug>/`, and link to them. Write action and verification status to `progress.md`. Keep `requirement.md` short and authoritative; do not let it become a session log.

## Authority Classes

Before using existing plan/spec/progress files, classify them by current authority:

- Active target: implements the latest user-confirmed goal and should drive work.
- Paused: valid context, but not currently being implemented.
- Reference-only: useful context, but not itself a to-do list.
- Progress/history: records what happened, but does not define new work.
- Superseded/stale: contradicted by newer user instructions, code state, or source-of-truth docs.

Do not implement a plan file just because it exists. Re-check the latest user request, timestamps, current repo state, and explicit status before treating any old plan as authoritative.
