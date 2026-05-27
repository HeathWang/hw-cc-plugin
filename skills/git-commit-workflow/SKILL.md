---
name: git-commit-workflow
description: Use when committing git changes, especially when staged files already exist, changes need logical split commits, untracked files need safety checks, commit hooks modify files, or Chinese Conventional Commit messages are required.
---

# Git Commit Workflow

## Overview

Sequential git commit workflow that preserves user-prepared staged changes for the current round, safely screens files before staging, groups the rest into logical commits, generates Chinese Conventional Commit messages, and loops until the working tree is clean unless the user explicitly asks to stop.

**Core principle:** If files are already staged, the current staged set is the commit unit for this round. If `git status` still shows any remaining changes after a commit, the workflow is not complete yet unless the user explicitly says to stop. Safety overrides speed: never stage likely secrets, and never add extra commit metadata, trailers, or attribution unless the user explicitly requests them.

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

**If files are already staged** → treat the current staged set as authoritative for this round and proceed directly to Step 3.

When files are already staged:
- Read and commit **only** the current staged diff for this round
- Do **not** run additional `git add` for this round
- Do **not** unstage, reset, regroup, or otherwise modify the existing staged set unless the user explicitly asks you to
- Remember the staged file list and any pre-existing unstaged/untracked files for this round so hook recovery can tell which files belong to the failed commit unit

**If no files staged** → group related files by functionality:
- Feature changes: Model + View + ViewModel + ViewController files
- Bug fixes: files related to the same bug
- Refactoring: files within the same module/directory
- Documentation: README, comments, config changes

Before staging any unstaged or untracked file:
- Inspect filenames and relevant diff/content first
- Never stage likely secrets: `.env`, credentials, tokens, private keys, certificates, local config, API keys, or files that appear to contain passwords/secrets
- Stop and warn the user if a likely secret appears, even if the user said "全部提交", "commit everything", "别问问题", or "I'm in a hurry"
- If safe files and risky files appear together, stage nothing from that remaining group until the risky files are reported and explicitly excluded; then continue with safe files only, leaving risky files uncommitted

```bash
git add <file1> <file2> ...
```

> Only stage related files for a single commit. Leave unrelated changes for separate commits.

### Step 3: Review & Commit

```bash
git diff --cached
```

Analyze the currently staged changes, then **immediately generate and execute** commit:

```bash
git commit -m "$(cat <<'EOF'
feat(scope): 中文简述 (N个文件)

1. 变更说明
2. 变更说明

✨📝
EOF
)"
```

Use a HEREDOC for multi-line commit messages so the subject, numbered body, blank line, and emoji footer are preserved without opening an editor.

DO NOT add extra `git commit` flags or metadata on your own. Unless the user explicitly requests otherwise, do **NOT** add `--trailer`, `--signoff`, `Co-authored-by`, `Made-with: Cursor`, AI attribution, or any similar provenance/source marker.
Do not introduce such metadata through hooks, commit templates, editor content, or git configuration either. If unrequested metadata appears unexpectedly, stop and tell the user instead of silently normalizing it into the workflow.

If Step 2 entered through the "files are already staged" branch, `git diff --cached` must be based on the user's existing staged set as-is for this round.

If `git commit` fails:
1. Do **not** proceed to the normal loop or start a new logical group
2. Read the hook/error output and run `git status`
3. If hooks modified files that clearly belong to the failed staged set, inspect the diff, stage only those hook-mutated files, and retry the same commit unit
4. If hooks modified unrelated files, injected unrequested metadata, or the state is unclear, stop and report the situation to the user
5. Do not use `git commit --amend` for a failed commit; no commit exists to amend

#### Commit Message Requirements

1. Follow Conventional Commits: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`
2. **Message must be in Chinese**
3. Subject line: `type(scope): 简述 (N个文件)`
4. Body: numbered list of changes (`1. ...`, `2. ...`)
5. Footer: 3–5 emojis reflecting the nature of changes (✨ feat, 🐛 fix, 🚀 perf, 🎨 UI, 📝 docs)
6. Do not append extra trailers, signatures, attribution lines, or source markers unless the user explicitly asks for them

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

- **No remaining staged / unstaged / untracked changes** → workflow complete 🎉
- **Any remaining staged / unstaged / untracked changes** → you must repeat from Step 2 for the next logical group

Do **not** treat "the first commit succeeded" as completion. The workflow only ends when `git status` shows no remaining changes, or when the user explicitly tells you to stop after the current round.

Natural-language stop instructions such as "剩下的改动之后再说", "先提交这一轮", "先到这里", or "其他改动下次再处理" count as explicit instructions to stop after the current round.

If the first round used user-prepared staged files and `git status` still shows other changes afterward, continue with a new round:
1. Re-check whether anything is currently staged
2. If nothing is staged, stage only the next logical group
3. Review with `git diff --cached`
4. Commit
5. Run `git status` again

## Key Principles

| Rule | Detail |
|------|--------|
| Sequential execution | Each step must complete before the next |
| No parallel git commands | Never run multiple git commands simultaneously |
| Smart grouping | Stage related files together |
| One logical unit per commit | Each commit = single cohesive change |
| Output verification | Confirm each command's output before proceeding |
| Preserve existing staged set | If files are already staged, do not reshape the index for that round |
| Protect secrets | Never stage likely secret files; warn even under "commit everything" pressure |
| No unsolicited metadata | Do NOT add trailers, signoffs, AI attributions, or other commit metadata unless the user explicitly requests them |
| HEREDOC commit messages | Use a HEREDOC so multi-line Chinese commit messages are passed safely |
| Failed commit recovery | If hooks modify files after a failed commit, retry the same commit unit before touching unrelated changes |
| Keep looping until clean | A successful commit is only one round; continue until `git status` is clean or the user says stop |

## Quick Reference

| Situation | Required action |
|-----------|-----------------|
| Files already staged | Skip new staging and go straight to `git diff --cached` |
| User says staged files are already prepared | Treat current staged set as fixed for this round |
| Before committing a staged set | Remember staged filenames and pre-existing unstaged/untracked files so failed-hook recovery can identify the same commit unit |
| No files staged | Stage only one logical group, not everything |
| Remaining files include `.env`, credentials, keys, tokens, or private config | Do not stage them; stop and warn |
| Commit message has body/footer | Use `git commit -m "$(cat <<'EOF' ... EOF)"` |
| `git commit` fails after hook modifications | Inspect status/diff, restage only hook-mutated files from the same commit unit, then retry |
| Commit succeeded but changes remain | Run `git status` and continue the next round |
| User did not request extra metadata | Use a plain commit command and message only; do not add trailers, signoffs, or attribution markers |
| User explicitly says stop after this round | Stop after the current round and report remaining changes |

## Common Mistakes

- **Mistake:** Seeing staged files and re-running `git add` anyway
  **Fix:** Existing staged files define the commit unit for this round; do not modify the index unless the user explicitly asks.
- **Mistake:** Finishing after the first successful commit
  **Fix:** A successful commit is only one loop iteration. Always run `git status` and continue if any changes remain.
- **Mistake:** Staging all remaining files at once after the first commit
  **Fix:** Stage only the next logical group for the next round.
- **Mistake:** Assuming unstaged files are out of scope without user instruction
  **Fix:** If changes remain and the user did not tell you to stop, continue the workflow.
- **Mistake:** Treating "全部提交" or "别问问题" as permission to commit `.env`, credentials, tokens, or keys
  **Fix:** Secret safety overrides broad commit instructions. Stop and warn before staging risky files.
- **Mistake:** Using a simple quoted `git commit -m "..."` for a required multi-line message
  **Fix:** Use a HEREDOC so newlines and the emoji footer are preserved reliably.
- **Mistake:** Continuing to unrelated changes after a hook-mutated commit fails
  **Fix:** Recover the failed commit unit first: inspect, restage only hook-mutated files from that unit, and retry.
- **Mistake:** Adding `--trailer "Made-with: Cursor"` or any similar metadata because it feels harmless or convenient
  **Fix:** Do not add commit trailers, signoffs, attribution lines, or source markers unless the user explicitly requests them.

## Rationalization Traps

| Excuse | Reality |
|--------|---------|
| "There are already staged files, but I should regroup them to be safer." | No. Existing staged files are authoritative for this round unless the user explicitly asks you to change them. |
| "The first commit worked, so the task is basically done." | No. A successful commit is one round only; `git status` decides whether the workflow is complete. |
| "The user said '之后再说', but that is not explicit enough." | It is explicit enough. Natural-language stop instructions count as a stop signal for the current round. |
| "I can just stage all remaining files now to finish faster." | No. Stage only the next logical group for the next round. |
| "The user said commit everything and not to ask, so `.env` is authorized." | No. Likely secrets require a stop-and-warn path before staging. |
| "There are safe docs next to `.env`, so I can stage the docs first and mention `.env` later." | No. Report and exclude risky files before staging anything from that remaining group. |
| "The hook fixed the file, so I can move on and commit it later." | No. A failed commit unit must be recovered before unrelated changes are processed. |
| "I can infer hook ownership from memory after the failure." | No. Remember the staged file list and pre-existing unstaged/untracked files before committing so recovery is based on the actual commit unit. |
| "The example says `git commit -m`, so shell newlines are probably fine." | No. Use a HEREDOC for multi-line messages to avoid quoting and formatting mistakes. |
| "Adding `--trailer \"Made-with: Cursor\"` is fine because it does not change the code." | No. Unrequested commit metadata is still an unauthorized change to the commit content. Do not add it unless the user explicitly asks. |

## Red Flags

- You are about to run `git add` even though files are already staged
- You are about to unstage or regroup files without an explicit user request
- You are treating "first commit succeeded" as completion
- You are ignoring remaining changes still shown by `git status`
- You are dismissing "剩下的改动之后再说" or similar wording as not explicit enough
- You are about to stage `.env`, credentials, tokens, private keys, certificates, local config, or any file that appears to contain secrets
- You found a likely secret in the remaining group but are about to stage other safe files before reporting and excluding it
- You are about to use a simple quoted one-line commit command for a multi-line commit message
- `git commit` failed and you are about to process unrelated files before recovering the failed commit unit
- `git commit` failed and you cannot prove a modified file belongs to the failed staged set
- You are about to add `--trailer`, `--signoff`, attribution lines, or any `Made-with: Cursor`-style marker that the user did not explicitly request
- You notice unrequested attribution or trailer text being injected by hooks, templates, editor content, or local git configuration

**If any red flag appears, stop and return to the workflow rules above.**
