---
name: review-fix-loop
description: Use whenever a task modifies files — code, documentation, configuration, tests, scripts, prompts, examples, or generated project files. Enforces an explicit review-after-implementation loop with re-review after every fix, so review is never skipped or treated as optional final polish. For independent-review tiers, this skill is standing user authorization to spawn read-only review subagents when subagent tooling exists. Trigger this even for small edits and quick fixes, and whenever the user asks for careful review, correctness, or end-to-end completion.
---

# Review-Fix Loop

## Why This Exists

Agents tend to declare a task done after a single implementation pass, and to stop reviewing the moment they apply a fix. That is exactly when regressions slip in: the fix itself goes unreviewed, or it satisfies the letter of the request while breaking a contract elsewhere. This skill makes review a required step after implementation, and requires re-review after each fix because the unreviewed change is the dangerous one.

## When It Applies

Use this skill for any task that modifies files: code, documentation, configuration, tests, scripts, prompts, examples, and generated project files. Do not skip review because a change looks small.

Authority documents are whatever defines intended behavior for the changed surface: specs, schemas, API contracts, READMEs, design docs, prompts, scripts, and the downstream code or consumers that depend on it.

## The Loop

1. Inspect the relevant current files and authority documents before editing.
2. Make the smallest correct change that satisfies the request.
3. Review the changed surface against the request and applicable project rules.
4. Fix confirmed issues.
5. Re-review the changed surface after the fix.
6. Verify with the smallest relevant command or targeted search.
7. Stop only when the latest review after the latest fix reports no confirmed blockers and verification passes.

## Review Tier

Review intensity should match the blast radius of the change. Over-reviewing trivial edits wastes time and tokens because independent reviewers run their own model and tool calls. Under-reviewing risky edits ships regressions. Pick the tier by the highest matching row.

| Tier | The change is... | Do this |
| --- | --- | --- |
| Self-review | Single file and localized, with no shared contract, config, script, prompt, test, public-output, or cross-document impact. Behavior impact is absent or contained entirely inside the changed surface, such as wording, comments, a local refactor, or a small localized bug fix. A purely mechanical multi-file edit can stay here only when it has no behavior, contract, prompt, script, config, schema, public-output, or cross-document meaning and every changed line follows the same obvious pattern. A comment- or wording-only edit to a test file, with no change to assertions or test behavior, stays in this tier. | Re-read the changed surface with fresh eyes against the request and authority documents, then verify. |
| One independent reviewer | Multiple files with non-local or cross-document impact, or touches runtime flags, scheduling, cache semantics, paths, config fields, schemas, serialization, scripts, prompts, test behavior or assertions, or docs that define current behavior. | Get one independent read-only review after implementing, then fix and re-review. |
| Two or more independent reviewers | Crosses module boundaries, or affects shared contracts, public behavior, shared types, shared runtime state, pipeline boundaries, user-facing output, or is large enough to need parallel work. | Get at least two independent read-only reviews, each with a different perspective. |

When unsure which tier applies, choose the stricter one.

## Independent Review

Independent review means a reviewer that does not carry the implementer's context and therefore cannot rationalize the change as fine because it just wrote it. Use whatever the environment provides: a review subagent, a separate reviewer in a multi-agent setup, a parallel agent thread, or a fresh review pass on a cleared context.

Prefer independent review over main-agent self-review for non-trivial changes. It catches more, and it preserves the main agent's context window for implementation, integration, and final synthesis. This skill records standing user authorization for independent review and read-only review subagents in its non-self-review tiers; treat that as the explicit user request for reviewer subagents in this project, and do not pause to ask whether to review. If the environment exposes a real read-only sandbox or permission mode, run reviewers there so read-only is enforced rather than merely requested.

While independent reviewers are running, do not repeat their assigned review or broad verification locally. Duplicating that work wastes the main context, weakens the value of independent review by letting the main agent form a competing conclusion first, and delays integration work that only the main agent can do. Work on non-overlapping tasks only, then use the reviewer reports to drive focused fixes and the smallest final verification needed.

If independent review is technically unavailable, for example in a single-threaded chat agent with no subagents, do a deliberate fresh-eyes self-review as a distinct step. Re-read the full changed surface against the request and authority documents as if someone else wrote it, then state in the final report that independent review was unavailable. Never fabricate reviewers or review rounds, and never claim subagents were spawned when they were not.

## Reviewer Prompt Template

A reviewer can only catch what it has enough context to judge. Give each reviewer a self-contained prompt.

```text
You are a READ-ONLY reviewer. Do NOT edit any file.
Perspective: {contracts/schemas | runtime behavior | docs consistency | tests | scripts/prompts | user-facing output}

User request and intended outcome:
{...}

Inspect:
- Files / directories: {...}
- Authority docs and downstream consumers: {...}

What must hold (the minimal true contract):
- {exact fields, commands, paths, terminology, or invariants}

Known risks to check:
- Obsolete terms / old APIs / stale behavior: {...}
- {anything specific to this change}

Report findings using only these finding formats:
- [blocker] <file>:<line> - <issue>
- [non-blocking concern] <file>:<line> - <issue>
- [assumption] <what you assumed, and why>

Output rules:
- If blockers exist, list blockers first.
- If no blockers exist, the first line must be: "No blockers."
- After "No blockers.", include any non-blocking concerns or assumptions.
- If there are no blockers, non-blocking concerns, or assumptions, output exactly: "No blockers."
```

When using multiple reviewers, give each a distinct perspective, such as contracts/schemas, runtime behavior, docs consistency, tests, scripts/prompts, or user-facing output. Do not send the same broad prompt to several reviewers unless duplicate coverage of one specific risk is intentional.

## Documentation Vs. Implementation Conflicts

When docs and code disagree, classify the disputed value first.

1. Required invariant or downstream dependency: other code, schemas, consumers, or documented public behavior rely on it. Fix implementation to match it, even if that means extra work.
2. Default, example, tunable value, or task-specific parameter: do not treat it as a contract blocker unless docs or downstream consumers make it one.
3. Stale status text, internally contradictory doc, impossible contract, or user-superseded doc: fix the doc instead, and record the final contract in the doc before or together with the implementation fix.
4. Unknown: report a blocking ambiguity. Do not invent a fixed requirement, and do not change working code to match a doc you suspect is outdated.

Enforce the minimal true contract: the invariants and dependencies that actually must hold, not incidental implementation choices.

## Loop And Stopping Rules

- Review happens after implementation, not only before.
- Once independent reviewers are assigned, the main agent must not duplicate their review or broad verification while they run. This preserves the main context for integration and keeps reviewer judgment independent instead of making the main agent re-litigate the same surface. It should wait for reviewer reports for that surface, then inspect only the reported findings, necessary integration points, and minimal final checks.
- If `multi-agent-workflow` already launched final read-only reviewers that cover this skill's required changed surface and perspectives, count that as the independent review round instead of spawning duplicate reviewers.
- If review finds blockers, fix them and re-review. Do not stop right after the fix.
- If a review round used independent reviewers, re-run independent read-only review after each blocker fix at the same or stricter tier.
- If a fix expands the change's blast radius, re-pick the tier from the table and apply the stricter tier's review before continuing.
- If blockers keep recurring or fixes keep introducing new blockers across several rounds, and in all cases after more than 5 review-fix rounds, stop applying direct minimal fixes and reassess whether architecture, design, contract, or scope is causing the churn. Propose the smallest viable resolution and report it to the user before continuing.
- Stop when the latest review reports only non-blocking concerns or assumptions, no blockers, and verification passes. Do not keep spawning reviewers to chase diminishing returns; record remaining non-blocking concerns as residual risk.
- Do not ignore non-blocking concerns by default; fix cheap relevant concerns or explicitly state why each remaining concern is acceptable residual risk.
- If reviewers disagree, clear every finding that is a true-contract violation. Downgrade the rest to non-blocking concerns or assumptions instead of treating every opinion as a blocker.
- Tests, compile checks, type checks, smoke tests, import checks, and targeted searches are verification. They support review but do not replace it.
- A subagent implementation report is not proof of correctness; verify or independently review the changed surface.
- Keep fixes surgical: address the confirmed blocker without opportunistic refactors.

## Final Report

For any task that modified files, match the report to the tier.

For a self-review-tier change, one line is enough, for example: `Self-review only: single-file wording change; verification: <command> passed.`

For non-trivial changes, state:

- Review performed: independent reviewers count and perspectives, or independent review unavailable with self-review stated plainly.
- Review-to-fix rounds completed.
- Blocking findings fixed.
- Latest review result.
- Verification commands and results.
- Non-blocking residual risks.
