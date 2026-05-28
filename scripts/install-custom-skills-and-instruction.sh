#!/usr/bin/env bash
# 把 personal-agent-kit 的 skills 和 AGENTS.md symlink 到 Codex / OpenCode 的加载位置。
# config 不处理:~/.codex/config.toml 与 ~/.config/opencode/opencode.json 自行手动配置。
set -euo pipefail

REPO="${AGENT_KIT_DIR:-$HOME/personal-agent-kit}"
GIT_URL="https://github.com/jn12-29/personal-agent-kit.git"

# repo 不在则 clone
[ -d "$REPO/.git" ] || git clone "$GIT_URL" "$REPO"

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
  ln -s "$src" "$dst"
  echo "→ 已链接: $dst → $src"
}

# skills:唯一真身 = ~/.agents/skills（Codex 与 OpenCode 都从这里读，不重复）
link "$REPO/skills" "$HOME/.agents/skills"

# AGENTS.md:两个工具全局路径不同，各链一份（各读一次，不重复）
link "$REPO/AGENTS.md" "$HOME/.codex/AGENTS.md"
link "$REPO/AGENTS.md" "$HOME/.config/opencode/AGENTS.md"
link "$REPO/AGENTS.md" "$HOME/.claude/CLAUDE.md"

echo
echo "完成。config 请自行手动配置："
echo "  ~/.codex/config.toml"
echo "  ~/.config/opencode/opencode.json"