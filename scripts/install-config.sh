#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${AGENT_KIT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
CODEX_INSTALL_DIR="${CODEX_HOME:-$HOME/.codex}"

copy_config() {
  local src="$1" dst="$2"
  [ -e "$src" ] || { echo "Missing source, skipped: $src"; return 1; }
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    local bak="$dst.bak.$(date +%Y%m%d%H%M%S)"
    mv "$dst" "$bak"
    echo "Backed up: $dst -> $bak"
  fi
  cp "$src" "$dst"
  echo "Installed: $dst <- $src"
}

copy_config "$REPO/config/config.toml" "$CODEX_INSTALL_DIR/config.toml"
copy_config "$REPO/config/opencode.json" "$HOME/.config/opencode/opencode.json"
