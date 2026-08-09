# personal-agent-kit

Branch-based instruction and skill profiles for Codex and OpenCode. Install the links once, then switch branches to change profiles without changing tool paths.

## Profiles

| Branch | Purpose |
| --- | --- |
| `main` | Permanent zero profile: empty `GLOBAL_AGENTS.md` and no loadable skills. |
| `profile/gpt-5.6-codex` | GPT-5.6 Codex profile, extended only in response to observed needs. |
| `legacy/gpt-5.5-codex` | Archived GPT-5.5 Codex instructions and skills. |

The current GPT-5.6 profile provides:

- Communication and response-style instructions in `GLOBAL_AGENTS.md`.
- `run-experiments` for running and monitoring long-running experiments.
- `work-with-files` for persistent task artifacts under an ignored `.work/` directory.

## Install

Clone the repository and install shared instructions and skills:

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

The installer links these paths, backing up existing targets as `.bak.<timestamp>` first:

- `~/.agents/skills` -> `<repo>/skills`
- `~/.codex/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`
- `~/.config/opencode/AGENTS.md` -> `<repo>/GLOBAL_AGENTS.md`

If linking fails, the installer asks before using a platform-appropriate fallback. A symlink or Windows junction follows branch changes automatically; after a copy or hard-link fallback, rerun the installer when switching branches.

## Switch Profiles

Activate the GPT-5.6 profile:

```bash
git fetch origin
git switch profile/gpt-5.6-codex
git pull
```

Return to the zero profile:

```bash
git switch main
git pull
```

Start a new agent session after switching because an existing session may retain instructions and skills it already loaded.

## Optional Tools

### Example Configs

Install the example Codex and OpenCode configs, backing up existing files first:

```bash
bash scripts/install-config.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-config.ps1
```

The examples use `CCH_API_KEY` for their provider credentials. The `codex` provider name in `config/opencode.json` is a configuration alias.

### planning-with-files

From a target project root, install the external `planning-with-files` skill with the appropriate helper:

```bash
bash /path/to/personal-agent-kit/scripts/planning-with-files/codex.sh
# or
bash /path/to/personal-agent-kit/scripts/planning-with-files/opencode.sh
```

PowerShell equivalents are available as `codex.ps1` and `opencode.ps1` in the same directory. Existing conflicting targets are backed up first.
