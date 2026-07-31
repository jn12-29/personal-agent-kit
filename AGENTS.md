# AGENTS.md

Project-specific instructions for maintaining this repository.

## Repository Contract

- This repository distributes branch-based instruction and skill profiles for agent tools.
- `main` is the permanent zero profile: keep `GLOBAL_AGENTS.md` empty and do not add loadable skill directories under `skills/`.
- Model- and host-specific instructions and skills belong on profile branches, not on `main`.
- Shared documentation and skills use tool-neutral terms by default: `agent`, `assistant`, `skill`, and `instruction file`.
- Use tool names only for actual install paths, config files, commands, provider names, or tool-specific integrations.
- When changing supported tools, installation destinations, or instruction filenames, update `README.md`, `GLOBAL_AGENTS.md`, `AGENTS.md`, Bash/PowerShell install scripts, and affected skill metadata together.

## Repository Roles

- `GLOBAL_AGENTS.md` is the branch-specific source file for shared global agent instructions.
- `AGENTS.md` is only for this repository's project-level operating guidance.
- `skills/` contains branch-specific installable custom skills. It has no loadable skill directories on `main`; on profile branches, each skill directory owns its own `SKILL.md` and any optional `agents/`, `references/`, `scripts/`, or assets.
- `config/` contains example Codex and OpenCode config files.
- `scripts/` owns install and link behavior.

## Maintenance Rules

- Keep `README.md`, `GLOBAL_AGENTS.md`, `AGENTS.md`, and install scripts in sync when instruction filenames or install destinations change.
- Keep the profile inventory and branch-switch instructions in `README.md` current when profile branches change.
- When changing install behavior, update both Bash and PowerShell scripts unless the change is explicitly platform-specific.
- Do not put general agent behavior guidelines in this file. Put shared global guidance in `GLOBAL_AGENTS.md`.
- Keep this file lean and project-specific; stable repo conventions belong here, human onboarding belongs in `README.md`.

## Verification

- For Python script changes under `skills/*/scripts/`, run `python -m py_compile <changed scripts>` and the relevant script `--help` commands. When tests exist, run `uv run --with pytest [--with <test dependency>] python -m pytest <tests>`.
- For Bash script changes, run `bash -n <script>`.
- For install-path or instruction-file changes, run `rg -n "AGENTS\\.md|GLOBAL_AGENTS\\.md|CLAUDE\\.md" README.md scripts AGENTS.md GLOBAL_AGENTS.md` and confirm the source and destination paths agree.
- Before finishing documentation changes, search the changed files for stale filenames or obsolete install mappings.
