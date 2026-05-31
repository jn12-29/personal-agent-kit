#!/usr/bin/env bash
# 把 personal-agent-kit 的 skills 和 AGENTS.md symlink 到 Codex / OpenCode 的加载位置。
# Config is handled separately by scripts/install-config.sh.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${AGENT_KIT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"

# link <真身> <链接位置>:已正确链接→跳过;已有内容→备份后再链;绝不删除
link() {
  local src="$1" dst="$2"
  [ -e "$src" ] || { echo "⚠ 真身不存在,跳过: $src"; return; }
  mkdir -p "$(dirname "$dst")"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "✓ 已链接: $dst"; return
  fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    local bak="$dst.bak.$(date +%Y%m%d%H%M%S)"
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

# skills:唯一真身 = $REPO/skills（Codex 与 OpenCode 都从 ~/.agents/skills 读）
link "$REPO/skills" "$HOME/.agents/skills"

# AGENTS.md:两个工具全局路径不同，各链一份（各读一次，不重复）
link "$REPO/AGENTS.md" "$HOME/.codex/AGENTS.md"
link "$REPO/AGENTS.md" "$HOME/.config/opencode/AGENTS.md"
link "$REPO/AGENTS.md" "$HOME/.claude/CLAUDE.md"

echo
echo "完成。config 可用脚本覆盖安装（会先备份已有文件）："
echo "  bash \"$REPO/scripts/install-config.sh\""
