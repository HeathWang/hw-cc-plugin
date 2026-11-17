---
name: git-commit-workflow
description: Use when the user asks to commit Git changes or invokes /gitcommit, including existing staged changes, logical split commits, and Chinese Conventional Commit messages.
---

# Git Commit Workflow

Complete the requested commits with minimal inspection and tool calls. Keep the task limited to Git operations and writing accurate Chinese commit messages.

## Scope

- **Do not run tests, lint, builds, or type checks as part of committing.** Passing tests is not a prerequisite imposed by this skill. If the user separately requests validation or a higher-priority instruction requires it, handle that requirement explicitly; do not invent a validation gate.
- Read diffs to understand the commit and spot likely secrets. Do not launch code review, repository-wide reference searches, refactoring, or fixes merely to prepare a commit.
- Respect the user's file scope and stop instructions. With no narrower scope, process all safe working-tree changes. Already-staged changes are the first commit unit; preserve them as-is, including partial staging. If they conflict with an explicit file scope, clarify rather than silently changing the index.
- Do not stage likely secrets such as credentials, private keys, or local `.env` files. Report and leave risky files uncommitted; continue with safe files. If risky content is already staged, stop before committing it and ask how to exclude it.

## Workflow

### 1. Inspect once

Run `git status --short` and read the relevant staged/unstaged diffs. Inspect untracked files selected for inclusion separately. Reuse diffs already read in this conversation when the files have not changed. Read recent commit subjects only if the repository's naming convention is unclear.

Choose the fewest coherent commits: keep a change's code, tests, and documentation together; split only unrelated changes. Do not split merely by file type or directory. If nothing is in scope, report that and finish.

### 2. Stage and commit

If nothing is staged, stage the chosen group with `git add -- <paths>`. If changes were already staged, commit that set without adding, unstaging, or regrouping it. Record the staged paths and any unstaged edits to those paths for hook recovery.

Confirm the staged scope. Read `git diff --cached` only for content not yet inspected or changed since inspection; a staged file summary is enough when the exact content is already known.

Write the message to a temporary file using a file-writing tool or a quoted heredoc, then run `git commit -F <message-file>`. Remove the temporary file afterward. Example message:

```text
fix(git-commit-workflow): 精简提交流程

1. 合并重复检查并减少无关拆分
2. 明确提交不要求运行测试
```

Use `<type>(<scope>): <中文简述>` without emoji. Choose the type by intent (`feat`, `fix`, `refactor`, `docs`, etc.); behavior changes in skills are `feat`/`fix`, wording-only edits are `docs`. Use the primary module or skill as scope, a short verb-led Chinese subject, and a blank line followed by a concise numbered body. Breaking changes use `!` and a `BREAKING CHANGE:` paragraph.

Do not add attribution or sign-off unless requested. Leave hook-added metadata, including `Co-authored-by: Cursor`, alone; do not inspect or amend commits just for that trailer.

Execute Git mutations sequentially and stop on failure. After success, use the commit output for its hash and subject; do not read back the full message routinely. Repeat only for remaining in-scope groups, reusing known diffs unless hooks or concurrent edits changed them.

### 3. Report and ask whether to push

Run `git status --short` once after the last commit. Briefly report commit hashes/subjects and any remaining changes. Report validation only if it actually ran or the user asked about it; never imply tests passed.

After completing the requested commits, ask `提交已完成，是否现在推送到远端？` with options `是，推送` / `否，暂不推送`, using an available structured question tool that permits approval questions (such as `request_user_input_async`, `AskUserQuestion`, or `AskQuestion`). If no permitted tool is available, ask in the final response. A commit summary alone does not complete this step. Wait for an explicit answer before pushing; silence is not approval.

If the user already requested pushing, proceed without asking again. If they explicitly declined pushing or asked to stop after this commit, report and finish without the question. Do not ask to push when there was nothing to commit or a commit failed.

On approval, use the configured upstream. If the destination is missing or ambiguous, ask for the remote/branch; on detached HEAD, report the blocker. Never force-push automatically. On decline, leave the commits local and finish.

## Failure handling

- If a commit fails, inspect the error and current status before doing anything else. Do not move to another group or use `--amend`.
- If a hook only formatted files in the failed commit, inspect the changes and restage only the intended content, preserving any pre-existing unstaged edits; retry once. If safe recovery is unclear or the retry fails, report the blocker and stop.
- Git hooks may run tests automatically. Do not run those tests again yourself, fix unrelated failures, or bypass hooks with `--no-verify` or environment overrides. If a hook blocks the commit, report its failure and leave the changes intact.
- On push failure, report the error without force-pushing or changing the destination.
