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

## 5. Execution Boundaries

**Use tools for deterministic work. Use the model for judgment.**

- Use code, shell tools, parsers, schemas, and tests for deterministic transforms, routing, retries, status-code handling, calculations, and validation.
- Use the model for judgment-heavy work: classification, summarization, drafting, tradeoff analysis, and extracting intent from unstructured text.
- Before adding code, read relevant exports, immediate callers, and obvious shared utilities.
- If existing patterns conflict, choose one explicitly, explain why, and flag the other for later cleanup. Do not average contradictory patterns.

## 6. Testing Discipline

**Tests should prove intent, not just touch behavior.**

- Tests should fail when the user intent, bug fix, or contract they protect regresses.
- For bug fixes, prefer a reproducing test first. If that is impractical, name why and use the closest meaningful verification.
- Do not treat shallow passing tests as proof of correctness.
- Name exactly which tests or checks were run, and which relevant tests were skipped.

## 7. Fail Loud

**Skipped work is not done. Unverified work is not verified.**

- Do not claim completion if required work, review, or verification was skipped.
- Do not say "tests pass" if only a subset ran; name the subset and residual risk.
- Surface uncertainty, blockers, assumptions, skipped checks, and partial results in the final response.
- For non-trivial work, separate what was implemented, verified, unverified, and blocked.

## 8. Documentation hygiene

Write the final desired state only — no migration notes, deprecated names, or explanations of removed behavior unless explicitly asked; put historical context in the chat reply instead.
Before finishing a docs edit, grep the file for obsolete terms and remove them.

## 9. Code organization

- One file, one responsibility — split when a file mixes concerns or grows unwieldy (~300 lines is a useful trigger, not a hard limit).
- Keep module-level state explicit: configure it through a setter, not hidden cross-module globals, so behavior stays predictable and testable.
- After extracting a module, verify it still imports/builds before moving on.
- Project-specific (e.g. Python CLIs): keep the entry point thin — `parse_args` + `main` in a file nothing else imports.

## 10. Personal Preferences

- Communicate with me in Chinese. Mixing in English is fine.
- Use English for all code, comments, and annotations.

## 11. Multi-agent

Use Multi-agent proactively for non-trivial work that can be split by file set, topic, ownership, or review perspective.

- If a loaded skill, active instruction file, or the current task requirements require Multi-agent or independent reviewers, treat that requirement as the user's explicit request and authorization to use available subagent tooling; do not ask for separate confirmation.
- For trivial, unclear, tightly coupled, or non-decomposable work, keep the work in the main thread and briefly state the exception when the task otherwise looks cross-file.
- When using subagents, rely on the dedicated Multi-agent workflow instructions for delegation boundaries, prompt structure, integration, and verification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
