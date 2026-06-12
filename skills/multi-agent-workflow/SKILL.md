---
name: multi-agent-workflow
description: Use when work spans multiple files or modules and responsibilities can be split by file set or topic — documentation consistency rewrites, cross-module API alignment, pre-implementation specification cleanup, or review tasks needing multiple perspectives. Proactively forks subagents for its trigger cases when subagent tooling exists, preserves main-agent context, partitions ownership, and structures agent prompts.
---

# Multi-Agent Workflow

## Why This Exists

Multi-agent work fails when delegation is treated as extra effort instead of an interface design problem. The main context window is scarce working memory: if the main agent loads every file, repeats delegated reads, or verifies the same surface while agents are already assigned to it, it spends context on detail that could have been isolated and returns to integration with a biased partial conclusion. If subagents receive vague prompts, they invent missing contracts or duplicate each other's work. This skill keeps the main agent focused on orchestration, context budgeting, critical-path decisions, and integration while subagents handle bounded reading, implementation slices, and independent review from clear task interfaces.

Subagents are most valuable when they receive enough source context to judge independently, but not so much main-thread interpretation that they merely repeat the implementer's conclusion. Give resolved contracts, authority files, and exact questions; avoid leaking speculative diagnoses or intended fixes to read-only reviewers unless the review is explicitly about that risk.

**Trigger:** Cross-file or cross-module work where responsibilities can be split by file set or topic. Good fits include documentation consistency rewrites, pre-implementation specification cleanup, cross-module API alignment, and read-only reviews from multiple perspectives. Inspection and review tasks are especially good fits because multiple agents can examine the same files from different angles without write conflicts, then the main agent merges and ranks findings.

**Not for:** small single-file changes, typo fixes, wording-only cleanup, tightly coupled algorithm work, unclear requirements that first need clarification, or cases where several agents would need to edit the same large section.

## Decision Point

After the main agent completes the initial project-structure read, it must explicitly decide what to delegate before editing or concluding on cross-file work. Use multiple independent read-only review agents when the task affects cross-file or cross-module contracts.

Strong triggers include:

- Changes or reviews spanning two or more authority documents.
- Runtime flags, scheduling, cache semantics, paths, configuration fields, shared schemas, serialization formats, public outputs, or cross-document terminology.
- Documentation consistency checks where the same field, command, stage, path, or behavior appears in multiple files.
- Preparing or changing implementation for shared contracts.
- Review findings that affect shared contracts, serialization, caching, runtime state, module boundaries, or public behavior.

For substantial contract work, use at least two read-only reviewers with different perspectives, such as:

- Shared types, configuration, runtime state
- Entry points, runtime flags, scheduling
- Domain-specific pipeline contracts
- Documentation consistency and user-facing examples

If the main agent decides not to use multiple agents for a cross-file task, it must briefly state why.

## Proactive Delegation And Context Budget

Spawn subagents whenever this skill triggers and the work can be split by file set, topic, ownership, or review perspective.

Default to launching bounded sidecar agents for independent reading, review, or non-overlapping implementation slices once the main agent has enough context to write a clear prompt. Avoid doing the full cross-file exploration locally first when subagents can inspect files, summarize findings, and cite exact locations.

Use subagents to protect the main agent's context window. Keep the main agent focused on orchestration, context budgeting, critical-path decisions, integration, conflict resolution, and final synthesis instead of loading every supporting file or every detailed review into the main thread.

Do not delegate the immediate blocking task when the next local step cannot proceed without the result. While agents run, the main agent should do useful non-overlapping work.

Do not duplicate delegated work in the main thread while agents are running. Duplicate local inspection burns the context budget that delegation was meant to save, collapses useful parallelism, and can make the main agent overrule independent reports with its own premature interpretation. If an agent owns a read, review, or verification slice, wait for that result before inspecting the same surface locally; use the main context only for non-overlapping critical-path work, applying fixes, integrating reports, and the smallest final checks needed after agent results arrive.

If this skill triggers but no agents are launched, state the concrete exception: trivial, tightly coupled, unclear requirements, non-decomposable work, unacceptable conflict risk, or subagent tooling technically unavailable.

## Agent Ownership Rules

Review agents must not edit files unless explicitly assigned non-overlapping ownership. Their prompts must specify files to read, review perspective, obsolete terms or conflicts to look for, and require findings with file paths and line numbers.

## Preferred Workflow

1. Split the task into non-overlapping file or topic ownership before launching agents.
2. Launch agents as soon as the task is split well enough for clear prompts; do not spend the main context on exhaustive local exploration first. If subagent tooling is technically unavailable, keep only the compact slice checklist or review prompt needed for local fallback.
3. Give each agent enough context to read first: the target files, upstream specification files, downstream consumer files, and relevant entry-point or authority documents.
4. Restrict each editing agent to an explicit file list. If a shared file must be changed, let one agent own it or have agents return suggestions for the main agent to apply.
5. Include resolved terminology, API signatures, field names, and design decisions from the plan/spec or authority docs in each prompt. Do not let agents infer unresolved decisions independently.
6. Require each editing agent to report changed sections and any synchronization points for other files.
7. Treat parallel agent reports as potentially stale because they may be based on earlier workspace snapshots. The main agent must verify against the current files before acting on reported follow-ups.
8. After merging agent work, run only the targeted searches or checks needed to verify integrated results, such as obsolete terms, old API signatures, old field names, and conflicting examples relevant to the changed contract.
9. After the main agent merges and normalizes the agent outputs, launch one or more final read-only review agents for cross-document or cross-module consistency. A prior independent read-only review round can satisfy the changed surface when its prompts cover the required perspectives; do not spawn a second duplicate review round. The review prompt must forbid edits and require file paths with line numbers. If subagent tooling is technically unavailable, run a deliberate fresh-eyes self-review using the same prompt and report that fallback explicitly.
10. The main agent fixes any confirmed findings from the final review, then re-runs targeted searches for the corrected terms or APIs.
11. The main agent summarizes both changes and verification.

## Quality Gate

- Every delegated task has non-overlapping file or topic ownership, or is explicitly read-only.
- Read-only reviewers are forbidden to edit and must report blockers, non-blocking concerns, or assumptions with file paths and line numbers when files are involved.
- The main agent verifies current files before applying agent-reported follow-ups, because parallel reports may be based on older workspace snapshots.
- If no subagents are used for a triggered cross-file task, the final report states the concrete exception.
- Final integration includes only targeted searches or checks tied to the changed contract, terminology, public behavior, or examples.

## Required Agent Prompt Structure

Each agent prompt must state:

- Self-contained context sufficient for the agent to work without relying on unstated main-thread context.
- The agent's role and goal.
- Why this work is being delegated and the exact output needed.
- Files or directories the agent must read.
- Files the agent is allowed to modify, or `none` for read-only review.
- Source plan/spec section or authority document, when one exists.
- Resolved terminology and API contracts.
- Explicit obsolete terms or designs that must not remain.
- For review tasks, require reviewers to classify findings as blocker, non-blocking concern, or assumption, and justify why any configurable value is a contract invariant rather than an example or tunable parameter.
- For read-only reviewers, raw artifacts and exact risks to check; do not include the intended fix unless the reviewer needs it to assess a named risk.
- Whether the task is edit mode or read-only review mode.
- The required final report format.
