#!/usr/bin/env bash
# Install https://github.com/OthmanAdi/planning-with-files into the current project.
set -euo pipefail

REPO_URL="https://github.com/OthmanAdi/planning-with-files.git"
TARGET_PROJECT="$(pwd)"
TARGET_CODEX_DIR="$TARGET_PROJECT/.codex"
TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/planning-with-files.XXXXXX")"

cleanup() {
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

backup_path() {
  local path="$1"
  if [ -e "$path" ] || [ -L "$path" ]; then
    local backup="$path.bak.$(date +%Y%m%d%H%M%S)"
    mv "$path" "$backup"
    echo "Backed up: $path -> $backup"
  fi
}

copy_dir_replacing() {
  local src="$1" dst="$2"
  backup_path "$dst"
  mkdir -p "$dst"
  cp -R "$src"/. "$dst"/
}

copy_file_replacing() {
  local src="$1" dst="$2"
  backup_path "$dst"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
}

copy_entry_replacing() {
  local src="$1" dst="$2"
  if [ -d "$src" ] && [ ! -L "$src" ]; then
    copy_dir_replacing "$src" "$dst"
  else
    copy_file_replacing "$src" "$dst"
  fi
}

git clone --depth 1 "$REPO_URL" "$TEMP_DIR"

mkdir -p "$TARGET_CODEX_DIR/skills" "$TARGET_CODEX_DIR/hooks"

copy_dir_replacing \
  "$TEMP_DIR/.codex/skills/planning-with-files" \
  "$TARGET_CODEX_DIR/skills/planning-with-files"

for entry in "$TEMP_DIR/.codex/hooks"/* "$TEMP_DIR/.codex/hooks"/.[!.]* "$TEMP_DIR/.codex/hooks"/..?*; do
  [ -e "$entry" ] || [ -L "$entry" ] || continue
  name="$(basename "$entry")"
  copy_entry_replacing "$entry" "$TARGET_CODEX_DIR/hooks/$name"
done

copy_file_replacing "$TEMP_DIR/.codex/hooks.json" "$TARGET_CODEX_DIR/hooks.json"

echo "Installed planning-with-files for Codex in: $TARGET_CODEX_DIR"
echo "Review and trust project hooks with /hooks when Codex prompts for hook trust."
