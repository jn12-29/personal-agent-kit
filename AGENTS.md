# AGENTS.md

Project-specific instructions for maintaining this repository.

## Repository Roles

- `GLOBAL_AGENTS.md` is the source file for shared global agent instructions.
- `AGENTS.md` is only for this repository's project-level operating guidance.
- `skills/` contains installable custom skills. Each skill directory owns its own `SKILL.md` and any optional `agents/`, `references/`, `scripts/`, or assets.
- `config/` contains example Codex and OpenCode config files.
- `scripts/` owns install and link behavior.

## Maintenance Rules

- Keep `README.md`, `GLOBAL_AGENTS.md`, `AGENTS.md`, and install scripts in sync when instruction filenames or install destinations change.
- When changing install behavior, update both Bash and PowerShell scripts unless the change is explicitly platform-specific.
- Do not put general agent behavior guidelines in this file. Put shared global guidance in `GLOBAL_AGENTS.md`.
- Keep this file lean and project-specific; stable repo conventions belong here, human onboarding belongs in `README.md`.

## Verification

- For Bash script changes, run `bash -n <script>`.
- For install-path or instruction-file changes, run `rg -n "AGENTS\\.md|GLOBAL_AGENTS\\.md|CLAUDE\\.md" README.md scripts AGENTS.md GLOBAL_AGENTS.md` and confirm the source and destination paths agree.
- Before finishing documentation changes, search the changed files for stale filenames or obsolete install mappings.
