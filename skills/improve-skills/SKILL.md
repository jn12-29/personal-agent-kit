---
name: improve-skills
description: "Use when improving, rewriting, or hardening an existing Codex skill or related skill set from user feedback, observed agent mistakes, review findings, unclear triggers, weak rationale, stale examples, missing validation/evals, trigger overlap, cross-skill coupling, or poor multi-agent behavior. Guides why-first, zero-coupled, eval-driven revision: tighten triggers, make each skill self-contained, keep bodies lean, update metadata, and validate changed behavior."
---

# Improve Skills

## Why This Exists

Skill instructions fail when they only say what to do. Agents then treat rules as optional style preferences, miss the failure mode the rule prevents, or apply the rule where it does not belong. A good skill revision names the recurring mistake, the consequence, and the behavior the skill should force.

Use "why" to create boundary judgment, not ceremony. Each rationale should justify a concrete trigger, decision gate, workflow step, prompt requirement, validation check, exception, or stopping rule.

## Zero Coupling

Skills must be self-contained. A skill may define its own trigger, ownership, non-ownership, workflow, validation, and local resources, but it must not depend on another skill to explain or complete its responsibility.

Do not define a skill by naming another skill it should call, continue into, coordinate with, copy, or depend on. Do not use another skill name to describe this skill's boundary. Cross-skill references make skills brittle when they are renamed, removed, split, disabled, or installed in different combinations.

Use neutral responsibility language instead: task stage, artifact type, risk class, input, output, authority, ownership, validation requirement, or completion condition.

## Scope

Keep work scoped to revising existing skills or a related set of existing skills. This skill is not for first-time skill scaffolding.

Use it for:

- unclear, broad, late, or missing triggers;
- weak rationale that does not explain the failure mode;
- vague workflows, decision gates, output contracts, validation, or stopping rules;
- stale, bloated, contradictory, or changelog-like guidance;
- overlapping skill boundaries, cross-skill coupling, or poor multi-agent behavior;
- user feedback or observed agent mistakes that should change future behavior.

Edit multiple skills only when the boundary itself is the problem or the user asked to improve the set. Otherwise, keep revisions local to the target skill.

## Workflow

1. Read the target `SKILL.md`, its `agents/openai.yaml` if present, and directly relevant same-skill resources.
2. State the requested improvement or observed failure in one sentence, plus the prompt class that should behave differently afterward.
3. Classify the issue: trigger, rationale, workflow, prompt, validation, scope, metadata, boundary, or coupling.
4. Make the smallest revision that changes future agent behavior.
5. Keep current-state guidance only; do not add migration notes, changelog language, or "previously/now" explanations unless explicitly asked.
6. Update metadata when the skill purpose, trigger, display text, or default prompt changes.
7. Validate structure, routing behavior, zero coupling, and the changed text.
8. Review the revised skill as a user of the skill, not as its author.

## Boundary Rules

When related skills cover adjacent workflow stages, each one must remain independently understandable and executable.

For each related skill, state or preserve:

- what prompt class should trigger it;
- what artifact, behavior, or decision it owns;
- what task stages, artifact types, or risk classes it does not own;
- what output it produces for the user or environment;
- whether it works when installed without neighboring custom skills.

Do not add cross-references as a shortcut for boundary clarity. Rewrite boundaries in neutral responsibility language instead.

## Trigger And Eval Checks

The frontmatter `description` is the routing contract. Any condition required to trigger the skill belongs there, not only in the body.

For wording or trigger edits, test at least:

- 2-3 should-trigger prompts, including terse or indirect user wording;
- 1-2 should-not-trigger near misses when scope is narrowed;
- boundary prompts where the right behavior depends on scope, risk, file type, or create-vs-improve intent.

For non-trivial rewrites, keep a compact eval set with prompt, expected skill decision, expected behavior, and failure mode. Forward-test with independent agents when available for broad or failure-prone revisions, but do not leak the suspected bug or intended fix into read-only eval prompts.

Do not overfit to one prompt. The eval should represent the future request class that motivated the change.

## Quality Gate

Before finishing, check:

- Frontmatter: `name` matches the folder; `description` says when to use the skill, what it owns, and why it should trigger.
- Why: rationale names the agent mistake, consequence, required behavior, and exception or tradeoff.
- Workflow: the body tells an agent what to do next, not just what to value.
- Boundaries: ownership and non-ownership are expressed as task, artifact, risk, input, output, or validation language.
- Zero coupling: no names of other skills in an individual skill body or metadata; no instructions to call, continue into, coordinate with, copy, or depend on another skill.
- Resources: references, scripts, and assets are local to the same skill directory unless the user explicitly asks for a repo-level inventory outside individual skill guidance.
- Metadata: `agents/openai.yaml` stays aligned when display name, short description, or default prompt becomes stale.
- Context budget: remove repeated rules, placeholder text, unused generated files, and long examples better suited to same-skill references.

## Validation

Run structural checks first:

```sh
python <validator-path> <skill-dir>  # only when the repo provides a validator
git status --short -- <skill-dir>
git diff --check -- <skill-dir>
git diff -- <skill-dir>
```

Use the local validation script path for the environment or repository being edited. If no validator exists, do a smoke check for frontmatter, required metadata, and malformed Markdown/YAML: confirm `name` matches the folder, `description` is present and trigger-focused, `agents/openai.yaml` remains aligned when present, and fenced code blocks or frontmatter delimiters are not broken.

Then run targeted searches for risks introduced by the edit:

- generated template leftovers such as TODO/FIXME text;
- obsolete names, commands, trigger phrases, or removed behavior;
- changelog-like language when the user did not ask for history;
- names of other skill directories in an individual skill body or metadata.

Treat cross-skill name hits as invalid unless the hit is the current skill's own name, a same-directory resource path, or a repo-level inventory outside individual skill guidance.

Confirm every changed line traces to the requested improvement. If files changed, complete an explicit review, fix confirmed issues, re-review after fixes, and verify the final files.
