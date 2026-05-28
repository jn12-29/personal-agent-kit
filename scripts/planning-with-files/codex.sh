# https://github.com/OthmanAdi/planning-with-files

# Clone the repo
git clone https://github.com/OthmanAdi/planning-with-files.git /tmp/planning-with-files

# Copy the skill
mkdir -p ~/.codex/skills
cp -r /tmp/planning-with-files/.codex/skills/planning-with-files ~/.codex/skills/

# Copy the hook scripts
mkdir -p ~/.codex/hooks
cp -r /tmp/planning-with-files/.codex/hooks/* ~/.codex/hooks/

# Copy hooks.json
# If you already have ~/.codex/hooks.json, merge the planning-with-files entries manually
cp /tmp/planning-with-files/.codex/hooks.json ~/.codex/hooks.json

# Clean up
rm -rf /tmp/planning-with-files