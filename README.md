# personal-agent-kit

Personal agent setup kit for Codex, OpenCode, and Claude.

It keeps shared agent instructions, custom skills, and example configs in one repo, with helper scripts to install them into each tool's expected location.

## Contents

- `AGENTS.md`: project-specific instructions for maintaining this repository.
- `GLOBAL_AGENTS.md`: shared global agent behavior guidelines installed into agent tool load paths.
- `skills/`: custom skills for reviews, contract checks, multi-agent work, and skill discovery.
- `config/`: example Codex and OpenCode config files.
- `scripts/install-custom-skills-and-instruction.sh`: links instructions and skills into local tool directories.
- `scripts/install-custom-skills-and-instruction.ps1`: Windows PowerShell version of the install/link script.
- `scripts/install-config.sh`: copies config files into local tool directories, backing up existing files first.
- `scripts/install-config.ps1`: Windows PowerShell version of the config install script.
- `scripts/planning-with-files/`: notes for installing the external `planning-with-files` skill.

## Install

macOS / Linux:

```bash
git clone https://github.com/jn12-29/personal-agent-kit.git personal-agent-kit
cd personal-agent-kit
bash scripts/install-custom-skills-and-instruction.sh
```

Windows PowerShell:

```powershell
git clone https://github.com/jn12-29/personal-agent-kit.git personal-agent-kit
Set-Location personal-agent-kit
powershell -ExecutionPolicy Bypass -File .\scripts\install-custom-skills-and-instruction.ps1
```

The install script links:

Here `<repo>` is the cloned repo directory that contains the script being run.

- `~/.agents/skills` -> `<repo>/skills`
- `~/.claude/skills/<skill-name>` -> `<repo>/skills/<skill-name>` for each skill directory
- `~/.codex/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`
- `~/.config/opencode/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`
- `~/.claude/CLAUDE.md` -> `<repo>/GLOBAL_AGENTS.md`

Existing targets are backed up as `.bak.<timestamp>` before replacement, including `~/.agents/skills`. For Claude skills, `~/.claude/skills` is kept as a real directory; if it already exists as a file or whole-directory link, it is backed up before per-skill links are installed. Per-skill Claude conflicts are backed up outside the scanned skills directory, under `~/.claude/skills-backups/<skill-name>.bak.<timestamp>`.

Rerunning the install script synchronizes Claude skills by removing stale links or junctions in `~/.claude/skills` that point into `<repo>/skills/` when the linked target no longer exists. User-installed skills, ordinary directories, links to other locations, and copy fallback directories whose origin cannot be proven are left in place.

The install scripts do not silently fall back when linking fails: macOS/Linux prints the symlink failure and asks before copying as a fallback; Windows prints the failure reason and asks before using a junction, hard link, or copy fallback. If fallback is declined or fails, the backup is restored.

To overwrite local config files from `config/`, with backups:

```bash
bash scripts/install-config.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-config.ps1
```

If you use the included model provider examples, add this to `~/.bashrc` or `~/.zshrc`:

```bash
export CCH_API_KEY=""
```

Or append it directly.

Bash:

```bash
printf '\nexport CCH_API_KEY=""\n' >> ~/.bashrc
```

Zsh:

```bash
printf '\nexport CCH_API_KEY=""\n' >> ~/.zshrc
```

PowerShell:

```powershell
New-Item -ItemType File -Path $PROFILE -Force
Add-Content -Path $PROFILE -Value '$env:CCH_API_KEY=""'
```
