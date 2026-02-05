# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin** that provides development skills and commands for daily frontend, iOS, and H5 development workflows. The plugin contains reusable command definitions (markdown files) that users can invoke via slash commands in Claude Code.

## Architecture

### Directory Structure

```
hw-cc-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   └── marketplace.json     # Marketplace listing configuration
├── commands/                # Command definitions (user-invocable via /)
│   ├── gitcommit.md
│   ├── code-review-with-files.md
│   ├── bug-analysis.md
│   ├── linus-torvalds-code-review.md
│   ├── Java-to-Nextjs-Conversion.md
│   ├── java-to-swift-conversion.md
│   └── question-answer.md
└── skills/                  # Agent skills (internal workflow automation)
```

### Plugin Configuration Files

- **plugin.json**: Defines plugin metadata (name, version, author, repository, keywords)
- **marketplace.json**: Marketplace listing configuration for plugin discovery

### Commands vs Skills

**Commands** (`commands/*.md`):
- User-invocable workflows triggered by slash commands (e.g., `/gitcommit`, `/code-review`)
- Define step-by-step processes for code conversion, review, Git automation
- Output language varies by command (Chinese for Git commits, code reviews; English for type conversions)

**Skills** (`skills/*.md`):
- Internal agent behaviors loaded automatically (e.g., test-driven-development, debugging)
- Modify how Claude approaches tasks (not directly invoked by users)

## Language Conventions

- **Git commit messages**: Chinese (中文)
- **Code review outputs**: Simplified Chinese (简体中文)
- **Type conversion workflows**: English (definitions, rules, examples)
- **Command documentation**: English (structure, workflow steps)

## Plugin Development Guidelines

### Adding New Commands
1. Create markdown file in `commands/` directory
2. Name file using kebab-case (e.g., `new-command.md`)
3. Include clear workflow steps with sequential execution rules
4. Specify output language requirements explicitly

### Command File Structure
```markdown
# Command Title

## Abstract/Overview
Brief description of command purpose and scope

## Workflow Steps
### Step 1: Description
Commands and validation logic

### Step 2: Description
...

## Output Format
Expected output structure and language

## Execution Rules
Decision flow diagrams and key principles
```

## Testing Commands

To test command changes:
1. Install plugin in Claude Code: `/plugin` → Add Marketplace → `HeathWang/hw-cc-plugin`
2. Restart Claude Code
3. Invoke command via slash (e.g., `/gitcommit`)
4. Verify workflow execution and output format

## Publishing Updates

After modifying commands:
1. Update version in `.claude-plugin/plugin.json`
2. Commit changes with conventional commit format
3. Push to GitHub repository
4. Marketplace will automatically reflect changes

## Important Constraints

- **Type conversion commands**: MUST NOT modify project files; output as markdown code blocks only
- **Code reviews**: Always request source files from user before reviewing
- **Git workflow**: Follow sequential execution (no parallel git commands)
- **Property naming**: Preserve API contract naming in conversions (do not convert naming styles)
