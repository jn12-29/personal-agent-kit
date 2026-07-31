#!/usr/bin/env bash
# Link personal-agent-kit skills and GLOBAL_AGENTS.md into Codex and OpenCode load paths.
# Config is handled separately by scripts/install-config.sh.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${AGENT_KIT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"

# link <真身> <链接位置> [备份目录]:已正确链接→跳过;已有内容→备份后再链;绝不删除
link() {
  local src="$1" dst="$2" backup_dir="${3:-}"
  [ -e "$src" ] || { echo "⚠ 真身不存在,跳过: $src"; return; }
  mkdir -p "$(dirname "$dst")"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "✓ 已链接: $dst"; return
  fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    local bak
    if [ -n "$backup_dir" ]; then
      mkdir -p "$backup_dir"
      bak="$backup_dir/$(basename "$dst").bak.$(date +%Y%m%d%H%M%S)"
    else
      bak="$dst.bak.$(date +%Y%m%d%H%M%S)"
    fi
    mv "$dst" "$bak"; echo "↪ 已备份: $dst → $bak"
  fi
  local err
  err="$(mktemp)"
  if ln -s "$src" "$dst" 2>"$err"; then
    rm -f "$err"
    echo "→ 已链接: $dst → $src"
    return
  fi

  echo "Symlink failed: $dst → $src"
  echo "Reason: $(cat "$err")"
  rm -f "$err"

  local answer
  printf 'Copy instead of linking as fallback? %s [y/N] ' "$dst"
  if ! read -r answer; then
    echo
    echo "Fallback requires confirmation, but input is unavailable."
    answer=""
  fi
  answer="$(printf '%s' "$answer" | tr '[:upper:]' '[:lower:]')"
  case "$answer" in
    y|yes)
      if cp -R "$src" "$dst"; then
        echo "Copied: $dst ← $src"
        return
      fi
      echo "Copy fallback failed: $dst"
      ;;
    *)
      echo "Copy fallback declined: $dst"
      ;;
  esac

  rm -rf "$dst"
  if [ -n "${bak:-}" ]; then
    mv "$bak" "$dst"
    echo "Restored backup: $dst ← $bak"
  fi
  echo "Not installed: $dst"
  return 1
}

# Codex and OpenCode share the skills source at $REPO/skills.
link "$REPO/skills" "$HOME/.agents/skills"

# GLOBAL_AGENTS.md is installed into the supported tools' global instruction paths.
link "$REPO/GLOBAL_AGENTS.md" "$HOME/.codex/AGENTS.md"
link "$REPO/GLOBAL_AGENTS.md" "$HOME/.config/opencode/AGENTS.md"

echo
echo "完成。config 可用脚本覆盖安装（会先备份已有文件）："
echo "  bash \"$REPO/scripts/install-config.sh\""
