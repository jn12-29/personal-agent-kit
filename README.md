# personal-agent-kit

Personal agent setup kit for Codex, OpenCode, and Claude.

It keeps shared agent instructions, custom skills, and example configs in one repo, with helper scripts to install them into each tool's expected location.

## Contents

- `AGENTS.md`: shared agent behavior guidelines.
- `skills/`: custom skills for reviews, contract checks, multi-agent work, and skill discovery.
- `config/`: example Codex and OpenCode config files.
- `scripts/install-custom-skills-and-instruction.sh`: links instructions and skills into local tool directories.
- `scripts/install-config.sh`: copies config files into local tool directories, backing up existing files first.
- `scripts/planning-with-files/`: notes for installing the external `planning-with-files` skill.

## Install

```bash
git clone https://github.com/jn12-29/personal-agent-kit.git ~/personal-agent-kit
bash ~/personal-agent-kit/scripts/install-custom-skills-and-instruction.sh
```

The install script links:

- `~/.agents/skills` -> `~/personal-agent-kit/skills`
- `~/.codex/AGENTS.md` -> `~/personal-agent-kit/AGENTS.md`
- `~/.config/opencode/AGENTS.md` -> `~/personal-agent-kit/AGENTS.md`
- `~/.claude/CLAUDE.md` -> `~/personal-agent-kit/AGENTS.md`

To overwrite local config files from `config/`, with backups:

```bash
bash ~/personal-agent-kit/scripts/install-config.sh
```

If you use the included model provider examples, add this to `~/.bashrc` or `~/.zshrc`:

```bash
export CCH_API_KEY=""
```
