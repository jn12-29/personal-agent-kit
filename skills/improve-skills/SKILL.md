---
name: improve-skills
description: "Use when improving, rewriting, or hardening an existing Codex skill, or a related set of skills, from user feedback, observed agent mistakes, review findings, unclear triggers, weak rationale, stale examples, missing validation/evals, trigger overlap, or poor multi-agent behavior. Guides why-first and eval-driven skill revision: explain the failure mode a rule prevents, tighten frontmatter triggers with should-trigger/should-not-trigger cases, align adjacent skill boundaries, make workflows actionable, keep skill bodies lean, update metadata, and validate the changed skill."
---

# Improve Skills

## Why This Exists

Skill instructions fail when they only say what to do but not why it matters. Agents then treat rules as optional style preferences, miss the failure mode the rule was meant to prevent, or over-apply a rule where it does not belong. A good skill improvement names the recurring agent mistake, the consequence of that mistake, and the behavior the revised skill should force.

Use "why" to create boundary judgment, not ceremony. Explaining the failure mode, consequence, and tradeoff works better than stacking `must` rules because it helps the model choose correctly in edge cases. If a rationale sounds generic, rewrite it until it exposes the decision boundary.

A useful why should point to at least one concrete rule it justifies: a trigger, decision gate, workflow step, prompt requirement, validation check, exception, or stopping rule.

## Scope After Triggering

After the frontmatter description selects this skill, keep the work scoped to revising one or more existing skills for reasons such as:

- The user reports that agents keep making the same mistake.
- The skill triggers too often, too late, or not at all.
- The skill says what to do but does not explain the failure mode it prevents.
- The workflow is vague, missing decision gates, or missing stopping rules.
- Reviewer prompts, handoff blocks, or validation expectations are unclear.
- A skill has grown stale, bloated, contradictory, or too close to a changelog.
- A new lesson from real use should be folded back into the skill.
- A related group of skills needs shared trigger boundaries, handoff rules, or interface alignment.

Do not use this skill for first-time skill scaffolding; use `skill-creator` for that. If the user asks to improve a set of new or related skills, define the set and improve their shared interfaces together. Otherwise, do not rewrite unrelated skills while improving one skill.

## Improvement Workflow

1. Read the target `SKILL.md`, its `agents/openai.yaml` if present, and any directly relevant references.
2. Identify the observed failure or requested improvement in one sentence, plus the prompt class or eval case that should behave differently afterward.
3. Decide whether the problem is a trigger issue, rationale issue, workflow issue, prompt issue, validation issue, scope issue, or boundary issue between adjacent skills.
4. Make the smallest revision that changes future agent behavior.
5. Keep current-state guidance only. Do not add migration notes, changelog language, or "previously/now" explanations unless explicitly asked.
6. Update UI metadata when the skill's purpose, trigger, or default prompt changes.
7. Validate the skill with structural checks, trigger/eval checks, diff review, and targeted searches chosen for the actual edit; avoid broad searches that mostly match the validation guidance itself.
8. Review the revised skill as a user of the skill, not as its author.

## Related Skill Sets

When several skills form one workflow, treat each skill as an interface with a clear owner. Agents fail here by copying the same guidance into every skill, which makes routing ambiguous and forces future agents to guess which instruction wins. The better fix is to assign ownership and handoff points.

For each related skill, state or preserve:

- What prompt class should trigger it.
- What artifact, behavior, or decision it owns.
- Which adjacent skill it hands off to, and when.
- What it must not own, even if the topic is mentioned.

Edit multiple skills only when the boundary itself is the problem or the user asked to improve the set. Prefer one sentence of cross-reference over duplicating a full workflow in both skills.

## Eval-Driven Improvement

A skill revision is a hypothesis until it is tested against realistic user requests. Static validation catches malformed folders and YAML; it does not prove that the skill triggers at the right time, gives enough procedural guidance, or avoids over-applying itself to adjacent work.

Scale evals to the change:

- For small wording or trigger edits, write 2-3 realistic prompts that should trigger the skill. If the edit narrows scope, also write 1-2 should-not-trigger near misses.
- For non-trivial rewrites, keep a small eval set with the prompt, expected skill decision, expected behavior, and failure mode being tested.
- For broad or failure-prone skills, forward-test with subagents when available. Give them the skill path and a realistic task, not your diagnosis, intended answer, or suspected fix.
- Compare behavior before and after the revision when possible. If old behavior cannot be reproduced cheaply, at least state what the new eval is meant to catch.
- Inspect artifacts such as transcripts, diffs, logs, and generated files. Do not trust a final "works" summary without looking at the behavior the skill produced.
- Turn evals into a repeatable benchmark or script only when the same checks will be reused. Do not add benchmark files for one-off confidence checks.

Do not overfit the skill to one prompt. The eval should represent the class of future requests that motivated the change.

## Description Trigger Testing

The frontmatter `description` is the routing contract. It is always visible before the body loads, so any condition required to trigger the skill belongs there, not only in a "when to use" body section.

When improving a description, test:

- Clear should-trigger prompts copied or paraphrased from real requests.
- Terse, noisy, or indirect should-trigger prompts, because users rarely phrase requests like documentation.
- Should-not-trigger prompts for adjacent skills or ordinary tasks that mention similar words.
- Boundary prompts where the correct answer depends on scope, risk, file type, or whether the user is asking to create vs. improve a skill.

If a prompt would only trigger after reading the body, the description is too weak. Use concrete verbs, artifacts, file types, and failure symptoms rather than generic quality language.

## Why-First Pattern

Add a `Why This Exists`, `Core Principle`, or short rationale paragraph when the rule guards against a real recurring mistake. The rationale should answer:

- What mistake do agents tend to make?
- What breaks or gets worse when they make it?
- What behavior should this skill force instead?
- What is the exception or tradeoff, if over-applying the rule is also harmful?

Patterns worth copying:

- `review-fix-loop` style: failure mode -> consequence -> required loop -> stopping condition.
- `contract-hardening` style: source-of-truth principle -> bias or ambiguity risk -> required independent review or contract fix.
- `multi-agent-workflow` style: coordination/context-budget problem -> delegation rule -> prompt requirements.

Good why:

```markdown
Agents tend to declare a task done after one implementation pass. That is when regressions slip in: the fix itself goes unreviewed. This skill requires review after implementation and re-review after each fix.
```

Weak why:

```markdown
Review is important, so always review.
```

Do not settle for decorative why text. Turn it into decision-relevant rationale by naming the boundary, exception, or tradeoff the agent must reason about.

## Revision Checklist

### Frontmatter

- `name` remains lowercase hyphen-case and matches the folder name.
- `description` says what the skill does and when to use it, including specific trigger scenarios.
- The description is broad enough to trigger when needed but narrow enough to avoid unrelated tasks.

### Body Structure

- Start with the core purpose or failure mode when judgment matters.
- Add a decision gate when the skill should scale behavior by risk, scope, or file type.
- Prefer ordered workflows for sequential tasks.
- Use tables only when they make tradeoffs or tiers easier to scan.
- Include prompt templates when the skill delegates to subagents or reviewers.
- Include stopping rules when agents might otherwise keep iterating.

### Behavioral Rules

- State mandatory behavior with must/should language only when the distinction matters.
- Include exceptions for trivial, unsafe, unavailable, or non-decomposable cases.
- Avoid absolute rules that force wasteful work on small edits.
- Do not let tests, generated output, or subagent reports substitute for required review unless the skill explicitly says they can.
- Name what not to do when agents commonly over-correct.

### Context Budget

- Keep `SKILL.md` lean enough to load directly, but do not remove rationale needed for boundary judgment.
- Move long examples, domain references, and variant-specific details to `references/` only when they are needed.
- Do not add README, changelog, installation guide, or other packaging/onboarding files to a skill.
- Remove repeated rules instead of adding a second version with slightly different wording.

### Metadata And Resources

- Regenerate or edit `agents/openai.yaml` when display name, short description, or default prompt becomes stale.
- Add scripts only for deterministic repeated operations.
- Add references only when details are too long or conditional for the main skill body.
- Delete placeholder markers and unused generated resource files.

## Review Questions

After editing, review the skill with these questions:

- Would the frontmatter trigger this skill for the user scenario that motivated the change?
- If multiple skills were changed, does each one have a distinct owner and a clear handoff to adjacent skills?
- Does the body explain the failure mode clearly enough to change agent behavior?
- Does the rationale guide a real decision, including when not to apply the rule?
- Does every why paragraph support a concrete rule, decision gate, prompt requirement, validation check, or stopping rule?
- Does the revision name realistic should-trigger, should-not-trigger, or forward-test cases when the change affects routing or behavior?
- Do forward-tests avoid leaking the expected answer, suspected bug, or intended fix?
- Does the workflow tell an agent what to do next, not just what to value?
- Are the exceptions explicit enough to prevent over-application?
- Does any rule contradict another rule in this skill or a closely related skill?
- Is the final text current-state guidance rather than a history of the revision?
- Did metadata stay aligned with the skill body?

For non-trivial skill rewrites, use independent read-only reviewers with distinct perspectives, such as trigger/scope, workflow usability, prompt quality, and validation coverage.

## Validation

Run structural checks first:

```powershell
python <skill-creator-dir>\scripts\quick_validate.py <skill-dir>
git status --short -- <skill-dir>
git diff --check -- <skill-dir>
git diff -- <skill-dir>
```

Use the actual installed `skill-creator` path, or the matching script path in the repo when editing a local skill collection.

If the skill directory is untracked, `git diff` will not show the new files. Inspect the files directly and run a simple whitespace check, such as `Get-ChildItem <skill-dir> -Recurse -File | Select-String -Pattern '[ \t]$'`.

Then run targeted searches only for risks introduced by the edit. Search changed files or the changed diff when a pattern would also match this skill's own validation guidance. Treat each hit as a review item, not an automatic failure.

Common targets:

- Generated template leftovers, such as TODO/FIXME text.
- Obsolete names, commands, trigger phrases, or behavior removed by the revision.
- Changelog-like language in final guidance when the user did not ask for history.

Confirm every changed line traces to the requested improvement. If the skill modified files, finish through `review-fix-loop`.
