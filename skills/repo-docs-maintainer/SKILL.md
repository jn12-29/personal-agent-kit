---
name: repo-docs-maintainer
description: "Use when creating, updating, auditing, or synchronizing repository-facing documentation such as README.md, AGENTS.md, CLAUDE.md, setup docs, command references, repo instruction files, or docs/snippets that mention install scripts and config examples. Owns routing facts to the right durable document, preventing drift between human-facing README content and agent-facing operating instructions, and validating that documented commands, paths, links, and conventions match the current repo."
---

# Repo Docs Maintainer

## Why This Exists

Repository docs drift when agents put facts in the easiest visible file instead of the file that owns them. Human onboarding, agent operating rules, volatile plans, implementation trivia, and generated command output then compete as sources of truth. The result is a README that lies to users, an AGENTS.md that bloats every agent session, and scripts or commands that no longer match the docs.

Use this skill to route facts deliberately, make the smallest current-state edit, and verify the documented commands, paths, filenames, and conventions against the repo before finishing.

## Scope

Use this skill for repository-facing documentation work involving:

- `README.md`, nested READMEs, setup docs, usage docs, command references, and project overviews.
- `AGENTS.md`, nested agent instruction files, and compatibility instruction files such as `CLAUDE.md` when present.
- Documentation references to install scripts, shell snippets, config examples, command tables, path inventories, and docs that must stay synchronized with them.
- Audits for stale features, moved paths, renamed tools, changed install destinations, obsolete roadmap/status claims, or duplicated sources of truth.

Do not use this skill for ordinary project-material writing, changelogs, PR descriptions, blog posts, code comments, broad documentation strategy, or changing reusable skill behavior unless the task also requires repo README or agent-doc synchronization.

## Routing Rules

Route each fact to exactly one durable home, then link or summarize from other docs only when useful.

- `README.md`: human-facing project entrypoint. Include what the project is, why it exists, how to install or run it, the smallest useful examples, stable project layout, contribution pointers, and links to deeper docs.
- `AGENTS.md`: agent-facing operating guide. Include exact commands, repo-specific conventions, task finish checks, important paths, generated-file rules, ask-first or never actions, and pitfalls agents keep missing.
- Dedicated docs: use separate files for deep reference, specific how-to procedures, design explanations, tutorials, runbooks, ADRs, API specs, policies, or long examples. README and AGENTS may link to them with exact repo-relative paths.
- Scripts and config: keep executable behavior in scripts or config files. Docs should name exact commands and expected targets, not reimplement script logic in prose.
- Issues, planning files, or trackers: put volatile status, future plans, open questions, and in-flight coordination there unless the user explicitly wants them in README or AGENTS.
- Code comments or docstrings: use them for local behavior that only matters beside the code. Do not promote local implementation notes into README or AGENTS.

When docs conflict, prefer the file that owns the fact. If ownership is unclear, classify the reader need first: lookup facts belong in reference, task steps in how-to, rationale in explanation, and first-time learning in tutorial material.

## Workflow

1. Inspect before editing. Read the target docs and the repo sources that can prove or disprove their claims: manifests, lock files, scripts, Makefiles, task runners, CI workflows, config files, key entrypoints, and relevant docs.
2. Classify the task: create, update, audit, synchronize, consolidate, or remove stale documentation.
3. Build a concise drift list: commands, paths, install targets, feature claims, tool names, filenames, prerequisites, examples, compatibility files, and duplicated facts that need attention.
4. Route each changed fact using the routing rules. Prefer updating the owning document and replacing duplicated copies with links or short pointers.
5. Patch minimally. Preserve the existing structure and voice unless the structure itself causes the stale or duplicated content.
6. Keep docs current-state only. Do not add transition notes, dated correction entries, deprecated names, or before/after explanations unless the user explicitly requests history.
7. Validate the changed surface with the smallest practical checks: run documented commands when safe, syntax-check changed scripts, verify paths exist, inspect links, and compare install destinations or filenames across docs and scripts.
8. Search changed files for obsolete terms, old command names, stale paths, template placeholders, and duplicate facts before finishing.

## README Rules

- Start with a clear name and short description; a reader should understand what the project is without opening source files.
- Include install and usage commands unless the repo is documentation-only or the README explicitly points to a more authoritative setup doc.
- Prefer runnable examples and expected outputs over abstract descriptions.
- Keep background, architecture, API detail, troubleshooting, and contribution detail concise in README; move deep material to dedicated docs and link to it.
- Include badges, roadmap, project status, visuals, license, or maintainer details only when they serve the README's real audience and can stay accurate.
- Do not put agent-only rules, hidden workflow constraints, local implementation trivia, or unverified future plans in README.

## AGENTS Rules

- Keep agent instructions lean, actionable, and repo-specific. Prefer command tables, path tables, and one rule per bullet.
- Do not duplicate existing `AGENTS.md` files that already apply, system/developer instructions, or active skill/capability instructions. Add only repo-local facts, constraints, commands, paths, and pitfalls that are not already supplied by those sources.
- When creating or updating an `AGENTS.md`, first ask what a future agent would get wrong in this exact repo without the line. If the answer is only a general work habit, workflow method, or already-loaded `AGENTS.md` or skill instruction, leave it out.
- Use exact repo-relative paths. Avoid vague references like "see docs" without naming the file.
- Reference README, CONTRIBUTING, specs, policies, or architecture docs instead of copying their prose.
- Prefer file-scoped test, lint, typecheck, or build commands when they exist; list full-suite commands only when narrower checks are unavailable or necessary.
- Do not restate formatter, linter, typechecker, or package-manager behavior already enforced by config.
- Do not list installed skills, plugins, generic quality slogans, welcome text, or long rationale unless the rationale prevents a likely agent mistake.
- Use nested `AGENTS.md` files only when a subtree has materially different commands or rules; keep narrower files shorter than root files and avoid repeating root guidance.
- If compatibility instruction files exist, keep one canonical instruction source and make the others links, stubs, or synchronized copies only when the repo or toolchain requires them.

## Quality Gate

Before finishing, confirm:

- Each changed fact has one clear owner and no conflicting duplicate remains.
- README content is useful to humans; AGENTS content is useful to agents.
- New or changed AGENTS content is not copied from existing applicable AGENTS files, system/developer guidance, or active skill/capability instructions unless a brief repo-local override is explicitly needed.
- Commands, paths, filenames, install destinations, and local links are verified or explicitly reported as unverified.
- No changelog-style language was added unless requested.
- No generated template placeholders, obsolete terms, or stale status claims remain in changed files.
- Every changed line traces to the documentation sync, audit, or routing task.

## Trigger Eval Checks

Should trigger:

- "Check whether README still matches the install scripts."
- "Sync README.md and AGENTS.md after renaming the test command."
- "Consolidate CLAUDE.md into AGENTS.md and remove duplicated instructions."
- "Audit repo docs for stale paths and setup commands."

Should not trigger:

- "Rewrite this grant proposal."
- "Improve this installed skill's trigger and validation rules."
- "Write a PR description for the latest diff."
- "Add a code comment explaining this function."

Boundary case: if a task adds a feature and says to update README or AGENTS, this skill owns only the documentation routing, synchronization, and validation part of that task.
