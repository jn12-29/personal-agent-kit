# personal-agent-kit

Personal agent setup kit for Codex, OpenCode, and Claude.

It keeps shared agent instructions, custom skills, and example configs in one repo, then symlinks them into each tool's expected location.

## Contents

- `AGENTS.md`: shared agent behavior guidelines.
- `skills/`: custom skills for reviews, contract checks, multi-agent work, and skill discovery.
- `config/`: example Codex and OpenCode config files.
- `scripts/install-custom-skills-and-instruction.sh`: links instructions and skills into local tool directories.
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

It does not install config files automatically. Copy or merge files from `config/` manually, and set `CCH_API_KEY` if you use the included model provider examples.
