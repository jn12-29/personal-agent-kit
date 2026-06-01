---
name: spec-driven-planning
description: Use when Codex needs to turn a task into a clear requirement/goal snapshot, active planning state, implementation plan, technical spec, interface contract, documentation contract, or multi-agent handoff document before coding or editing. Trigger for ambiguous, multi-step, cross-file, cross-module, multi-agent, contract/schema/config/API/public behavior, prompt, script, or documentation-interface work where the current target, goal validity, non-goals, ownership, inputs, outputs, acceptance criteria, and verification must be explicit.
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
9. Convert decomposable work into self-contained handoff blocks before spawning agents.
10. Update durable progress state at phase boundaries or after meaningful discoveries, verification results, blockers, and goal changes.
11. If implementation reveals a contract gap or goal drift, pause broad coding, update the requirement snapshot or plan/spec, then resume.

## Where To Write

Follow existing repo conventions first.

- Use an inline chat plan for small, short-lived tasks.
- For durable work without an existing convention, use `.planning/<plan-id>/` with `.planning/.active_plan`, `requirement.md`, `plan.md`, `progress.md`, and optional `findings.md`; read [planning-state.md](references/planning-state.md) first.
- Put user-requested formal plan/spec deliverables where the user or repo expects them, not only inside ignored `.planning/` state. Link to those deliverables from `.planning/<plan-id>/requirement.md` or `plan.md` when durable state is also useful.
- Keep `.planning/` for requirement, plan, spec, progress, and planning-relevant findings. Put general scratch data, raw extracts, one-off scripts, logs, and bulky intermediate outputs under the repo's working-artifact convention, such as `.work/<task-slug>/`, and link to them instead of duplicating them.
- If the repo already separates requirements from plans, write the snapshot in that requirements document and link to it from the plan/spec.
- If the repo has a mature planning/spec convention that conflicts with `.planning/`, follow the repo convention but keep the same active-pointer and requirement/progress semantics where possible.

By default, `.planning/` is working state and should not be committed. When creating `.planning/`, ensure `.planning/` is ignored in `.gitignore` unless the user explicitly asks to track it or has intentionally commented out an existing ignore rule such as `# .planning/`.

Treat active plan/spec docs as current-state source-of-truth documents, not changelogs. Historical context belongs in the chat unless the user explicitly asks for it in the document.

## References

- Read [planning-state.md](references/planning-state.md) before creating durable planning state, resolving `.planning/.active_plan`, classifying old plan files, or deciding where `requirement.md`, `plan.md`, `progress.md`, and `findings.md` belong.
- Read [templates.md](references/templates.md) before writing durable requirement snapshots, implementation plans, technical specs, document interface tables, or subagent handoff prompts.

## Quality Gate

- Every non-trivial task has a clear objective, non-goals, and verification.
- Every durable plan/spec has a requirement snapshot that states the current target, status, validity, non-goals, and final acceptance check.
- Every durable planning state has a single active pointer, or the absence of a pointer is intentionally justified before old plan files are used.
- `.planning/` is ignored by default unless the user explicitly chooses to track it.
- Existing plan/spec/progress files are classified before use; reference-only, historical, stale, or superseded files are not treated as implementation targets.
- Every task has explicit inputs, outputs, owner, downstream handoff, and done condition.
- Every interface has an owner, inputs, outputs, invariants, consumers, and source of truth.
- Every durable plan/spec names authority documents separately from consumer or generated documents.
- Every document interface states what the document must contain, must not contain, who consumes it, and when it changes.
- Every subagent handoff includes enough context to work without unstated main-thread context.
- Blocking ambiguity is resolved in the plan/spec before implementation proceeds.
- Documentation and implementation stay aligned; when they conflict, use the project contract rules to decide whether to update docs or implementation.
- The final plan/spec names what must not change as clearly as what must change.

## Interaction With Other Skills

- Use `work-with-files` when the main question is whether intermediate results, scripts, notes, logs, or findings should be preserved as files. This skill owns the plan/spec structure once the artifact defines requirements, active planning state, contracts, or handoffs.
- Use `multi-agent-workflow` after this skill when work should be split across subagents.
- Use `contract-hardening` when the spec affects shared contracts, schemas, runtime state, serialization, or public behavior.
- Use `review-fix-loop` after modifying files to review, fix, re-review, and verify the changed surface.
