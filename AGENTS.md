# AGENTS.md

Project-specific instructions for maintaining this repository.

## Repository Contract

- This repository is a multi-agent, multi-tool setup kit for agent tools, including but not limited to Codex, OpenCode, and Claude Code.
- Shared documentation and skills use tool-neutral terms by default: `agent`, `assistant`, `skill`, and `instruction file`.
- Use tool names only for actual install paths, config files, commands, provider names, or tool-specific integrations.
- When changing supported tools, installation destinations, or instruction filenames, update `README.md`, `GLOBAL_AGENTS.md`, `AGENTS.md`, Bash/PowerShell install scripts, and affected skill metadata together.

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

- For Python script changes under `skills/*/scripts/`, run `python -m py_compile <changed scripts>` and the relevant script `--help` commands. When tests exist, run `uv run --with pytest [--with <test dependency>] python -m pytest <tests>`.
- For Bash script changes, run `bash -n <script>`.
- For install-path or instruction-file changes, run `rg -n "AGENTS\\.md|GLOBAL_AGENTS\\.md|CLAUDE\\.md" README.md scripts AGENTS.md GLOBAL_AGENTS.md` and confirm the source and destination paths agree.
- Before finishing documentation changes, search the changed files for stale filenames or obsolete install mappings.
