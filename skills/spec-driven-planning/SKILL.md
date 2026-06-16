---
name: spec-driven-planning
description: Use before ambiguous, multi-step, cross-file, delegated, contract-sensitive, prompt/script/config, or public-behavior work that needs an explicit goal, scope, non-goals, acceptance criteria, and verification plan. Owns requirement snapshots, plans, specs, documentation contracts, and handoff blocks.
---

# Spec Driven Planning

## Why This Exists

Plans and specs are useful only when they make hidden interfaces explicit. Agents otherwise carry decisions in the main thread, hand subagents vague tasks, or let different files encode different versions of the same contract. A good plan/spec names the current target, authority, inputs, outputs, owners, non-goals, acceptance checks, and handoff boundaries so implementation and review can proceed without unstated context.

Do the smallest planning that removes real ambiguity. Over-planning trivial edits wastes context; under-planning multi-file or contract work pushes ambiguity into code, docs, and subagent prompts where it is harder to catch. Existing plan files are artifacts, not automatic instructions; prefer an explicit active-plan pointer over model guesswork, then decide whether other plan files are reference-only, history, or superseded.

## Decision Gate

- Trivial: single-file typo or wording cleanup with no behavior, contract, prompt, script, config, schema, public-output, or cross-document impact. A short inline plan is enough.
- Plan required: non-trivial multi-step work, work touching more than one file, user-requested planning, or work where success criteria are not obvious.
- Spec required: shared contracts, APIs, schemas, serialization, runtime state, config fields, commands, paths, public behavior, prompts, scripts, generated outputs, or docs that define current behavior.
- Durable state required: multi-agent, cross-module, long-running, resumable, research-heavy, or user-requested planning work where the current goal and progress must survive context loss.
- Handoff blocks required: any task that will spawn subagents or be split across agents, files, modules, or review perspectives.

When uncertain, write the smallest useful plan/spec before implementation. Do not let agents infer unresolved decisions independently.

## Core Workflow

1. Read the latest user request, relevant authority docs, and current files before drafting.
2. If durable state is required, resolve or create active planning state before reading old plan files as instructions. See [planning-state.md](references/planning-state.md).
3. Capture or update the current target, source request, validity, non-goals, and final acceptance check.
4. State assumptions, non-goals, and blocking ambiguities explicitly.
5. Define success as observable acceptance criteria and verification commands or checks.
6. Identify interfaces: files, modules, data shapes, configuration fields, commands, paths, prompts, public outputs, and downstream consumers.
7. Identify document interfaces: which docs are authority, which docs consume or summarize them, who owns each doc, and what each doc must contain or avoid.
8. Write the smallest plan/spec that makes the work executable without hidden context.
9. Convert decomposable work into self-contained handoff blocks before splitting work across agents, files, modules, or review perspectives.
10. Update durable progress state at phase boundaries or after meaningful discoveries, verification results, blockers, and goal changes.
11. If implementation reveals a contract gap or goal drift, pause broad coding, update the requirement snapshot or plan/spec, then resume.

## How To Read Existing Planning State

When existing planning state may matter, read it in this order:

1. Resolve the active plan pointer or active requirement before using any plan-like file as instructions.
2. Read `requirement.md` first; it owns the current target, status, validity, non-goals, final acceptance check, and active plan files.
3. Read only the plan or spec files named by the active requirement as implementation targets.
4. Read `progress.md` for current phase, completed checks, blockers, verification results, and remaining work; do not treat it as a source of new requirements.
5. Read `planning-notes.md` only for concise planning context that affects or justifies the active requirement, plan, spec, contract, or handoff.
6. Classify any other plan-like files as reference-only, progress/history, stale, or superseded before using them.

## Why Planning Location Matters

Planning files are dangerous when their status is ambiguous. Agents tend to treat any discovered plan-like file as current instructions, even when it is stale, historical, partial, or superseded. The planning location and active pointer prevent that: they identify the current requirement snapshot, distinguish progress from authority, and keep scratch evidence from becoming part of the plan contract.

Use `.planning/` for durable planning state only. Do not store raw logs, bulky extracts, one-off scripts, or general scratch outputs there; put them in the working-artifact location and link to them when they affect the plan.

## Where To Write

Follow existing repo conventions first.

- Use an inline chat plan for small, short-lived tasks.
- For durable work without an existing convention, use `.planning/<plan-id>/` with `.planning/.active_plan`, `requirement.md`, `plan.md`, `progress.md`, and optional `planning-notes.md`; read [planning-state.md](references/planning-state.md) first. Use `YYYY-MM-DD-short-slug` for `<plan-id>` unless the repo or tool provides a stable id.
- Put user-requested formal plan/spec deliverables where the user or repo expects them, not only inside ignored `.planning/` state. Link to those deliverables from `.planning/<plan-id>/requirement.md` or `plan.md` when durable state is also useful.
- Keep `.planning/` for requirement, plan, spec, progress, and concise planning notes that affect the requirement, plan, spec, contract, or handoff. Put general scratch data, raw extracts, one-off scripts, logs, and bulky intermediate outputs under the repo's working-artifact convention, such as `.work/<task-slug>/`, and link to them instead of duplicating them.
- If the repo already separates requirements from plans, write the snapshot in that requirements document and link to it from the plan/spec.
- If the repo has a mature planning/spec convention that conflicts with `.planning/`, follow the repo convention but keep the same active-pointer and requirement/progress semantics where possible.

By default, `.planning/` is working state and should not be committed. When actually creating `.planning/`, ensure `.planning/` is ignored in `.gitignore` unless the user explicitly asks to track it or has intentionally commented out an existing ignore rule such as `# .planning/`. If the repo has no `.gitignore`, create the smallest one needed for the new working-state ignore entry; do not create `.gitignore` only to document a convention.

Treat active plan/spec docs as current-state source-of-truth documents, not changelogs. Historical context belongs in the chat unless the user explicitly asks for it in the document.

## References

- Read [planning-state.md](references/planning-state.md) before creating durable planning state, resolving `.planning/.active_plan`, classifying old plan files, or deciding where `requirement.md`, `plan.md`, `progress.md`, and `planning-notes.md` belong.
- Read [templates.md](references/templates.md) before writing durable requirement snapshots, implementation plans, technical specs, document interface tables, or subagent handoff prompts.

## Quality Gate

- Every non-trivial task has a clear objective, non-goals, and verification.
- Every durable plan/spec has a requirement snapshot that states the current target, status, validity, non-goals, and final acceptance check.
- Every durable planning state has a single active pointer, or the absence of a pointer is intentionally justified before old plan files are used.
- When actually creating `.planning/`, `.planning/` is ignored by default unless the user explicitly chooses to track it.
- Existing plan/spec/progress files are classified before use; reference-only, historical, stale, or superseded files are not treated as implementation targets.
- Every task has explicit inputs, outputs, owner, downstream handoff, and done condition.
- Every interface has an owner, inputs, outputs, invariants, consumers, and source of truth.
- Every durable plan/spec names authority documents separately from consumer or generated documents.
- Every document interface states what the document must contain, must not contain, who consumes it, and when it changes.
- Every subagent handoff includes enough context to work without unstated main-thread context.
- Blocking ambiguity is resolved in the plan/spec before implementation proceeds.
- Documentation and implementation stay aligned; when they conflict, use the project contract rules to decide whether to update docs or implementation.
- The final plan/spec names what must not change as clearly as what must change.

## Boundary With Adjacent Work

- This skill owns requirement, plan, spec, contract, and handoff structure once an artifact defines what work means.
- Storage-only decisions for scratch notes, raw extracts, scripts, logs, and bulky intermediate outputs are outside this planning contract except when they affect the requirement, plan, spec, or handoff.
- Delegation orchestration, concurrency, and reviewer integration are outside the plan/spec artifact; this skill only requires self-contained handoff blocks with clear inputs, outputs, authority, and done conditions.
- Shared contract plans must name the source-of-truth invariants and downstream consumers so implementation can be verified against them.
- After file modifications, run an explicit review, fix, re-review, and verification loop for the changed surface.
