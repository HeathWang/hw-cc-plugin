# Installing hw-cc-plugin for Codex

Enable `hw-cc-plugin` in Codex via native skill discovery.
This guide installs the skills from `skills/`.

## Prerequisites

- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HeathWang/hw-cc-plugin ~/.codex/hw-cc-plugin
   ```

2. **Link skills (`skills/`):**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/hw-cc-plugin/skills ~/.agents/skills/hw-cc-plugin
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Migrating from old command installation

If you previously installed this project as Claude command files or converted-command skills:

1. **Update the repo:**
   ```bash
   cd ~/.codex/hw-cc-plugin && git pull
   ```

2. **Remove old links:**
   ```bash
   rm -f ~/.agents/skills/hw-cc-plugin-commands
   rm -rf ~/.codex/hw-cc-plugin/.codex/converted-commands
   rm -f ~/.claude/commands/hw-cc-plugin  # if present
   ```

3. **Link native skills** using step 2 above (if not already done).

4. **Restart Codex.**

## Verify

```bash
ls -la ~/.agents/skills/hw-cc-plugin
```

You should see a symlink pointing to the `skills/` directory of the cloned repo.

## Updating

```bash
cd ~/.codex/hw-cc-plugin && git pull
```

No additional steps needed — the symlink picks up changes automatically.

## Uninstalling

```bash
rm ~/.agents/skills/hw-cc-plugin
```

Optionally delete the clone:
```bash
rm -rf ~/.codex/hw-cc-plugin
```
