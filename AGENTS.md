# AGENTS.md

Project-specific instructions for maintaining this repository.

## Repository Contract

- This repository distributes branch-based instruction and skill profiles for agent tools.
- `main` is the permanent zero profile: keep `GLOBAL_AGENTS.md` empty and do not add loadable skill directories under `skills/`.
- Model- and host-specific instructions and skills belong on profile branches, not on `main`.
- Name active profile branches `profile/<model>-<host>` and archived profile branches `legacy/<model>-<host>`, using lowercase names.
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
- Keep `README.md` concise and identical across `main` and profile branches. Limit it to the repository purpose, initial installation, linked targets, and basic branch switching; do not enumerate profile branches or document optional workflows there.
- When changing install behavior, update both Bash and PowerShell scripts unless the change is explicitly platform-specific.
- Develop skills, including changes to existing skills, in an isolated task workspace under `.work/` according to the `$work-with-files` rules; keep all in-progress work outside the branch's loadable `skills/` directories, and only when the user explicitly asks to publish, synchronize the completed skill from its task workspace into `skills/` with a copy command.
- Do not put general agent behavior guidelines in this file. Put shared global guidance in `GLOBAL_AGENTS.md`.
