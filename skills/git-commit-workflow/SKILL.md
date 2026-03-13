---
name: git-commit-workflow
description: Use when committing code changes to git - staging files, writing commit messages, or completing a batch of uncommitted changes across multiple logical groups.
---

# Git Commit Workflow

## Overview

Sequential git commit workflow that intelligently groups related files, generates Chinese commit messages following Conventional Commits, and loops until the working tree is clean.

## When to Use

- User runs `/gitcommit` or asks to commit changes
- Working tree has staged or unstaged changes ready to commit
- Multiple unrelated changes need to be split into logical commits

## Workflow

### Step 1: Check Repository Status
```bash
git status
```
Wait for output before proceeding.

### Step 2: Intelligent File Staging

**If files are already staged** → proceed to Step 3.

**If no files staged** → group related files by functionality:
- Feature changes: Model + View + ViewModel + ViewController files
- Bug fixes: files related to the same bug
- Refactoring: files within the same module/directory
- Documentation: README, comments, config changes

```bash
git add <file1> <file2> ...
```

> Only stage related files for a single commit. Leave unrelated changes for separate commits.

### Step 3: Review & Commit

```bash
git diff --cached
```

Analyze changes, then **immediately generate and execute** commit:

```bash
git commit -m "<generated_message>"
```

#### Commit Message Requirements

1. Follow Conventional Commits: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`
2. **Message must be in Chinese**
3. Subject line: `type(scope): 简述 (N个文件)`
4. Body: numbered list of changes (`1. ...`, `2. ...`)
5. Footer: 3–5 emojis reflecting the nature of changes (✨ feat, 🐛 fix, 🚀 perf, 🎨 UI, 📝 docs)

#### Example

```
feat(user): 重构用户数据模型和视图 (3个文件)
1. 更新 User 数据模型以支持新字段
2. 优化 UserCell 视图展示逻辑
3. 重构 UserVM 以适配新的数据结构

🎨✨🚀
```

### Step 4: Loop

After each commit, run `git status` again.

- **No remaining changes** → workflow complete 🎉
- **Remaining changes** → repeat from Step 2 for the next logical group

## Key Principles

| Rule | Detail |
|------|--------|
| Sequential execution | Each step must complete before the next |
| No parallel git commands | Never run multiple git commands simultaneously |
| Smart grouping | Stage related files together |
| One logical unit per commit | Each commit = single cohesive change |
| Output verification | Confirm each command's output before proceeding |
