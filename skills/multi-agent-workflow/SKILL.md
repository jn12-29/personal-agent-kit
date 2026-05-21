---
name: multi-agent-workflow
description: Use when work spans multiple files or modules and responsibilities can be split by file set or topic — documentation consistency rewrites, cross-module API alignment, pre-implementation specification cleanup, or review tasks needing multiple perspectives. Decides when to fork agents, how to partition ownership, and how to structure agent prompts.
---

# Multi-Agent Workflow

**Trigger:** Cross-file or cross-module work where responsibilities can be split by file set or topic. Good fits include documentation consistency rewrites, pre-implementation specification cleanup, cross-module API alignment, and read-only reviews from multiple perspectives. Inspection and review tasks are especially good fits because multiple agents can examine the same files from different angles without write conflicts, then the main agent merges and ranks findings.

**Not for:** small single-file changes, typo fixes, wording-only cleanup, tightly coupled algorithm work, unclear requirements that first need clarification, or cases where several agents would need to edit the same large section.

## Decision Point

After the main agent completes the initial project-structure read, it must explicitly consider whether multiple agents are warranted before editing or concluding on cross-file work. Use multiple independent read-only review agents when the task affects cross-file or cross-module contracts.

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

If the main agent decides not to use multiple agents for a cross-file task, it should briefly state why.

## Agent Ownership Rules

Review agents must not edit files unless explicitly assigned non-overlapping ownership. Their prompts must specify files to read, review perspective, obsolete terms or conflicts to look for, and require findings with file paths and line numbers.

## Preferred Workflow

1. Split the task into non-overlapping file or topic ownership before launching agents.
2. Give each agent enough context to read first: the target files, upstream specification files, downstream consumer files, and relevant entry-point or authority documents.
3. Restrict each editing agent to an explicit file list. If a shared file must be changed, let one agent own it or have agents return suggestions for the main agent to apply.
4. Include the final terminology, API signatures, field names, and design decisions in each prompt. Do not let agents infer unresolved decisions independently.
5. Require each editing agent to report changed sections and any synchronization points for other files.
6. Treat parallel agent reports as potentially stale because they may be based on earlier workspace snapshots. The main agent must verify against the current files before acting on reported follow-ups.
7. After merging agent work, run project-wide searches for obsolete terms, old API signatures, old field names, and conflicting examples.
8. After the main agent merges and normalizes the agent outputs, launch one or more final read-only review agents for cross-document or cross-module consistency. The review prompt must forbid edits and require file paths with line numbers.
9. The main agent fixes any confirmed findings from the final review, then re-runs targeted searches for the corrected terms or APIs.
10. The main agent summarizes both changes and verification.

## Required Agent Prompt Structure

Each agent prompt must state:

- The agent's role and goal.
- Files that must be read before editing.
- Files the agent is allowed to modify.
- Final desired terminology and API contracts.
- Explicit obsolete terms or designs that must not remain.
- For review tasks, require reviewers to classify findings as blocker, non-blocking concern, or assumption, and justify why any configurable value is a contract invariant rather than an example or tunable parameter.
- Whether the task is edit mode or read-only review mode.
- The required final report format.
