# personal-agent-kit

Branch-based instruction and skill profiles for Codex and OpenCode. `main` is the permanent zero profile, with no repository-provided global instructions or loadable skills. Install the links once, then switch branches to change profiles without changing tool paths.

## Install

On macOS and Linux:

```bash
git clone https://github.com/jn12-29/personal-agent-kit.git
cd personal-agent-kit
bash scripts/install-custom-skills-and-instruction.sh
```

On Windows PowerShell:

```powershell
git clone https://github.com/jn12-29/personal-agent-kit.git
Set-Location personal-agent-kit
powershell -ExecutionPolicy Bypass -File .\scripts\install-custom-skills-and-instruction.ps1
```

The installer backs up existing targets as `.bak.<timestamp>` and links:

- `~/.agents/skills` -> `<repo>/skills`
- `~/.codex/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`
- `~/.config/opencode/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`

## Switch Profiles

```bash
git pull
git branch --all
git switch <branch>
```
