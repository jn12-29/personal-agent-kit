# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

Question discipline:

- If the answer is strongly implied by the user's wording, repo structure, prior decisions, or current context, state the assumption briefly and proceed.
- If the answer can be discovered by reading files, configs, docs, or command output, explore first instead of asking.
- Ask only when a wrong choice would be costly, destructive, security-sensitive, user-visible in a hard-to-reverse way, or likely to cause substantial rework.
- Do not ask users to confirm obvious exclusions. Record the default and continue.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

The same rule applies to fixes made during review: keep them surgical, do not use review findings as an excuse for opportunistic refactoring.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Documentation hygiene

Write the final desired state only — no migration notes, deprecated names, or explanations of removed behavior unless explicitly asked; put historical context in the chat reply instead.
Before finishing a docs edit, grep the file for obsolete terms and remove them.

## 6. Code organization

- One file, one responsibility — split when a file mixes concerns or grows unwieldy (~300 lines is a useful trigger, not a hard limit).
- Keep module-level state explicit: configure it through a setter, not hidden cross-module globals, so behavior stays predictable and testable.
- After extracting a module, verify it still imports/builds before moving on.
- Project-specific (e.g. Python CLIs): keep the entry point thin — `parse_args` + `main` in a file nothing else imports.

## 7. Personal Preferences

- Communicate with me in Chinese. Mixing in English is fine.
- Use English for all code, comments, and annotations.

## 8. Subagents

When a loaded skill calls for subagents or independent reviewers, treat that skill trigger as the user's explicit request for that subagent use; do not ask for a separate confirmation.

Before any multi-agent delegation, subagent spawning, or independent-review round, read the installed `multi-agent-workflow` skill and follow its context-budget, ownership, prompt, and no-duplicate-work rules.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
