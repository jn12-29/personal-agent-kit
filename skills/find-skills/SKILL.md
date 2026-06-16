---
name: find-skills
description: "Use when the user wants to discover, compare, evaluate, update, or install catalog/repo-sourced agent skills, including asking whether a capability exists as an installable skill. Do not use for ordinary one-off work the agent should perform directly."
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## Why This Exists

Agents fail in two opposite ways: they miss reusable installable skills when the user wants durable capability, or they interrupt ordinary work with marketplace searches the user did not ask for. This skill keeps discovery focused on explicit skill-installation intent and verifies current quality signals before recommending code or instructions from an external package.

## When to Use This Skill

Use this skill when the user:

- Says "find a skill for X", "install a skill for X", or "is there an installable skill for X"
- Asks to compare, evaluate, update, or recommend skills
- Expresses interest in extending agent capabilities with reusable installed behavior
- Wants to search a skill catalog, marketplace, package, template, or workflow intended for agent installation
- Describes a recurring specialized capability and asks for reusable help rather than one-off task execution

Do not use this skill for ordinary coding, writing, research, design, or debugging requests when the user is asking the agent to do the work directly. Do not use it when an already installed local capability clearly covers the task.

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check Current Catalog Signals

Before running a CLI search, check the current [skills.sh](https://skills.sh/) catalog or leaderboard when available to see if a well-known skill already exists for the domain. Treat rankings, install counts, source ownership, and repository activity as current signals that must be verified at request time, not facts to hard-code in this skill.

### Step 3: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills find [query]
```

For example:

- User asks "find an installable skill for React performance" → `npx skills find react performance`
- User asks "is there a skill for PR review workflows?" → `npx skills find pr review`
- User asks "install a changelog skill I can reuse" → `npx skills find changelog`

### Step 4: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Current catalog signals** — When install counts, rankings, or update status are available, use them as current signals rather than permanent facts.
2. **Source identity** — Prefer maintainers with a public track record, clear ownership, and active support; do not treat an unknown source as safe because the name looks relevant.
3. **Repository activity** — Check README quality, recent commits or releases, issue activity, license, and whether the package still matches the user's environment.
4. **Compatibility and install path** — Confirm the package name, skill id, install command, and whether installation is global or project-local.

Treat low-signal, newly published, abandoned, or poorly documented packages as risky even when the search result looks relevant.

### Step 5: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. Current quality signals such as install count, source, and repository activity when available
3. The project-level install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help. The "react-best-practices" skill provides
React and Next.js performance optimization guidance. I verified its current
source and quality signals before recommending it.

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 6: Offer to Install

If the user wants to proceed, install skills at the project level by default:

```bash
npx skills add <owner/repo@skill> -y
```

Use user-level installation only when the user explicitly asks for a global or user-level skill:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
