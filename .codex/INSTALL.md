# Installing hw-cc-plugin for Codex

Enable `hw-cc-plugin` in Codex via native skill discovery.  
This guide installs both:
- Native skills from `skills/`
- Converted skills generated from `commands/` (command -> skill)

## Prerequisites

- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HeathWang/hw-cc-plugin ~/.codex/hw-cc-plugin
   ```

2. **Link native skills (`skills/`):**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/hw-cc-plugin/skills ~/.agents/skills/hw-cc-plugin
   ```

3. **Convert commands to skills and link them:**
   ```bash
   mkdir -p ~/.codex/hw-cc-plugin/.codex/converted-commands
   for f in ~/.codex/hw-cc-plugin/commands/*.md; do
     name="$(basename "$f" .md)"
     mkdir -p ~/.codex/hw-cc-plugin/.codex/converted-commands/"$name"
     cp "$f" ~/.codex/hw-cc-plugin/.codex/converted-commands/"$name"/SKILL.md
   done
   ln -s ~/.codex/hw-cc-plugin/.codex/converted-commands ~/.agents/skills/hw-cc-plugin-commands
   ```

4. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Migrating from old command installation

If you previously installed this project as Claude command files:

1. **Update the repo:**
   ```bash
   cd ~/.codex/hw-cc-plugin && git pull
   ```

2. **Remove old command links/copies** from paths such as `~/.claude/commands/` (if present).

3. **Install native skills + converted command skills** using steps 2 and 3 above.

4. **Restart Codex.**

## Verify

```bash
ls -la ~/.agents/skills/hw-cc-plugin
ls -la ~/.agents/skills/hw-cc-plugin-commands
ls -la ~/.codex/hw-cc-plugin/.codex/converted-commands
```

You should see symlinks under `~/.agents/skills/` and converted command folders each containing `SKILL.md`.

## Updating

```bash
cd ~/.codex/hw-cc-plugin && git pull
rm -rf ~/.codex/hw-cc-plugin/.codex/converted-commands
mkdir -p ~/.codex/hw-cc-plugin/.codex/converted-commands
for f in ~/.codex/hw-cc-plugin/commands/*.md; do
  name="$(basename "$f" .md)"
  mkdir -p ~/.codex/hw-cc-plugin/.codex/converted-commands/"$name"
  cp "$f" ~/.codex/hw-cc-plugin/.codex/converted-commands/"$name"/SKILL.md
done
```

## Uninstalling

```bash
rm ~/.agents/skills/hw-cc-plugin
rm ~/.agents/skills/hw-cc-plugin-commands
```

Optionally delete the clone:
```bash
rm -rf ~/.codex/hw-cc-plugin
```
