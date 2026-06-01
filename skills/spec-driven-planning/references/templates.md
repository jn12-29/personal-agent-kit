# Planning Templates

Use these templates when writing durable requirement, plan, spec, or agent handoff documents. Omit sections only when they are genuinely irrelevant.

## Contents

- [Requirement Snapshot](#requirement-snapshot)
- [Plan Template](#plan-template)
- [Spec Template](#spec-template)
- [Agent Handoff Template](#agent-handoff-template)

## Requirement Snapshot

Use this at the top of durable plans/specs, or in `requirement.md` when using `.planning/<plan-id>/`. Keep it short enough to re-read before major decisions.

```markdown
## Requirement Snapshot
- Current target:
- User-visible final result:
- Source request / authority:
- Status: active / paused / complete / draft / reference-only / superseded
- Validity: created/reviewed on <date>; valid until <event/date> or superseded by <instruction/doc>
- Non-goals:
- Plan files to implement:
- Reference-only or historical files:
- Final acceptance check:
```

## Plan Template

```markdown
# <Task Name> Plan

## Requirement Snapshot
- Current target:
- Source request / authority:
- Status and validity:
- Non-goals:
- Plan files to implement:
- Reference-only or historical files:
- Final acceptance check:

## Objective
- Desired outcome:
- User-visible result:

## Non-Goals
- Out of scope:

## Authority
- User request:
- Source-of-truth docs:
- Relevant files:

## Assumptions And Open Questions
- Assumptions:
- Blocking questions:

## Work Breakdown
| ID | Owner | Scope | Inputs | Outputs | Depends On | Verify |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | main/subagent | files/modules/docs | required context | expected change/report | none/P0 | command/check |

## Task Interfaces
| Task | Owner | Inputs | Outputs | Handoff To | Done When |
| --- | --- | --- | --- | --- | --- |
| T1 | main/subagent | docs/files/decisions | patch/report/spec section | next owner/none | acceptance check |

## Verification
- Commands:
- Targeted searches:
- Review criteria:
```

## Spec Template

```markdown
# <Task Name> Spec

## Requirement Snapshot
- Current target:
- Source request / authority:
- Status and validity:
- Non-goals:
- Plan files to implement:
- Superseded or reference-only plans:
- Final acceptance check:

## Purpose
- Problem:
- Desired current design:

## Behavior Contract
- Inputs:
- Outputs:
- Error cases:
- Invariants:
- Public/user-facing behavior:

## Interfaces
| Surface | Owner | Inputs | Outputs | Invariants | Consumers | Source Of Truth |
| --- | --- | --- | --- | --- | --- | --- |
| module/API/doc/prompt/script | owner | shape/path/command | shape/path/result | must hold | downstream user/module | file/section |

## Document Interfaces
| Document | Owner | Role | Must Contain | Must Not Contain | Consumers | Update Trigger |
| --- | --- | --- | --- | --- | --- | --- |
| path | authority/consumer/generated | current-state contract | required sections/terms | stale terms/history | agents/users/modules | when contract changes |

## Files And Ownership
| File/Directory | Role | Allowed Changes | Notes |
| --- | --- | --- | --- |
| path | source/test/doc/config | edit/read-only | constraints |

## Acceptance Criteria
- AC1:
- AC2:

## Verification
- Tests/checks:
- Review perspectives:
- Obsolete terms or stale behavior to search for:
```

## Agent Handoff Template

Every subagent prompt should be derivable from the plan/spec and must be self-contained.

```markdown
## Agent Handoff: <Name>

Mode: read-only review / edit
Perspective: <contracts/schema/runtime/docs/tests/etc.>
Goal: <specific outcome>
Source plan/spec section: <section or task ID>

Main-thread context to carry forward:
- Resolved decisions:
- Assumptions:
- Non-goals:

Must read:
- <files/docs>

Allowed to modify:
- <files or none>

Do not touch:
- <files/areas>

Contract to preserve:
- <fields, APIs, commands, paths, behavior, terminology>

Known risks:
- <obsolete terms, stale examples, conflict points>

Expected output:
- <patch/report/decision list>

Verification:
- <commands/searches/checks>

Report format:
- Blockers:
- Non-blocking concerns:
- Assumptions:
- For review findings, cite exact file paths and line numbers.
```
