# personal-agent-kit

Personal multi-agent setup kit for Codex and OpenCode.

It keeps tool-neutral shared agent instructions, custom skills, and example configs in one repo, with helper scripts to install them into the tool paths this repo currently supports.

## Repository Layout

- `AGENTS.md`: project-specific instructions for maintaining this repository.
- `GLOBAL_AGENTS.md`: shared global agent behavior guidelines installed into Codex and OpenCode instruction load paths.
- `skills/`: custom skills for reviews, contract checks, documentation maintenance, multi-agent work, and skill discovery across compatible agent tools.
- `config/`: example Codex and OpenCode config files.
- `scripts/install-custom-skills-and-instruction.sh`: links instructions and skills into local tool directories.
- `scripts/install-custom-skills-and-instruction.ps1`: Windows PowerShell version of the install/link script.
- `scripts/install-config.sh`: copies config files into local tool directories, backing up existing files first.
- `scripts/install-config.ps1`: Windows PowerShell version of the config install script.
- `scripts/planning-with-files/`: helper scripts for project-level installation of the external `planning-with-files` skill.

## Install

### Install Shared Instructions And Skills

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

Symbolically linked global instruction files follow branch changes automatically. If a global instruction file used the hard-link or copy fallback, rerun the installer after every branch switch.

The shared Codex/OpenCode skills directory also follows branch changes when installed as a symbolic link or Windows junction; rerun the installer after every branch switch if it used the copy fallback.

### Linked Targets

The install script links:

Here `<repo>` is the cloned repo directory that contains the script being run.

- `~/.agents/skills` -> `<repo>/skills`
- `~/.codex/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`
- `~/.config/opencode/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`

### Backup And Sync Behavior

Existing targets are backed up as `.bak.<timestamp>` before replacement, including `~/.agents/skills`.

### Link Fallback Behavior

The install scripts do not silently fall back when linking fails: macOS/Linux prints the symlink failure and asks before copying as a fallback; Windows prints the failure reason and asks before using a junction, hard link, or copy fallback. If fallback is declined or fails, the backup is restored.

### Install planning-with-files Into A Project

The `scripts/planning-with-files/` helpers install the external `planning-with-files` skill into the project where you run them. Run the Codex helper from a target project root to install `.codex/skills/planning-with-files`, `.codex/hooks/`, and `.codex/hooks.json`; existing conflicting targets are backed up first. Run the OpenCode helper from a target project root to invoke `npx skills add OthmanAdi/planning-with-files --skill planning-with-files` without `-g`, using the Skills CLI project-level default.

Example: install `planning-with-files` into another project by changing into that project's root first, then running one helper from this kit:

```bash
cd /path/to/target-project
bash /path/to/personal-agent-kit/scripts/planning-with-files/codex.sh
# or, for OpenCode:
bash /path/to/personal-agent-kit/scripts/planning-with-files/opencode.sh
```

Windows PowerShell:

```powershell
Set-Location C:\path\to\target-project
powershell -ExecutionPolicy Bypass -File C:\path\to\personal-agent-kit\scripts\planning-with-files\codex.ps1
# or, for OpenCode:
powershell -ExecutionPolicy Bypass -File C:\path\to\personal-agent-kit\scripts\planning-with-files\opencode.ps1
```

### Install Example Configs

To overwrite local config files from `config/`, with backups:

```bash
bash scripts/install-config.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-config.ps1
```

The OpenCode example uses `codex` as a provider alias in `config/opencode.json`; that alias is a config value, not a repository-wide Codex-only scope.

### Configure Provider API Key

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
