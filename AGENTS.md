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

## 5. Documentation Hygiene

When editing documentation, write the final desired state only.

Do not include:

- Legacy design explanations
- Deprecated parameter names
- Old-vs-new migration notes unless explicitly requested
- Explanations of why something was removed
- Placeholder examples that mention removed options
- Warnings about designs that no longer exist

If a previous name, option, or behavior has been removed, the final document should usually not mention it at all.

Treat documentation as the source of truth for the current design, not as a changelog. If historical context is useful, mention it in the chat response instead of the final documentation, unless explicitly asked to preserve it.

Before finishing a documentation edit, search the edited files for obsolete terms and remove them unless migration notes were explicitly requested.

## 6. Code Organization

- One file, one responsibility. Split when a file exceeds ~300 lines or mixes concerns.
- CLI entry point (`parse_args` + `main`) lives in a thin file that nothing else imports.
- No cross-module globals. Use an explicit setter function for any module-level state that callers must configure.
- After extracting each module, immediately run a smoke-test import before moving on.

## 7. Personal Preferences

- Communicate with me in Chinese. Mixing in English is fine.
- Use English for all code, comments, and annotations.
- Always update `README.md`, `CLAUDE.md`, and any `*.sh` files when significant or relevant changes are made, or when explicitly asked.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
