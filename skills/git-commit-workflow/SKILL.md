---
name: git-commit-workflow
description: Use when committing git changes, especially when staged files already exist, changes need logical split commits, untracked files need safety checks, commit hooks modify files, or Chinese Conventional Commit messages are required.
---

# Git Commit Workflow

## Overview

Commit every working-tree change as a sequence of logical Chinese Conventional Commits, then ask whether to push.

**Core rules:** A pre-existing staged set is this round's commit unit. The workflow ends only when `git status` is clean or the user says stop. Never stage likely secrets. Never add commit metadata the user did not request. A hook-appended `Co-authored-by: Cursor <cursoragent@cursor.com>` is expected: do not check for it, amend it, or cite it as a reason to stop. Push only after an explicit structured choice.

Run git commands sequentially, never in parallel, and read each output before deciding the next step.

## When to Use

- User runs `/gitcommit` or asks to commit changes
- Staged, unstaged, or untracked changes need committing, possibly split into several commits

## Workflow

### Step 1: Check Status

Run `git status`. In the first round, also run `git log --format=%s -10` to learn the repository's type and scope vocabulary.

### Step 2: Choose the Commit Unit

**Files already staged:** the staged set is this round's commit unit, as-is. Do not `git add`, unstage, reset, or regroup it unless the user explicitly asks. Note the staged file list and the pre-existing unstaged/untracked files; failed-commit recovery in Step 3 depends on this list.

**Nothing staged:** pick one logical group (one feature with its model, view, logic, and tests; one bug fix; one module refactor; or one documentation change) and stage only those files with `git add <file>...`.

**Secret check before any `git add`:** inspect the filenames and diffs of the group. Likely secrets are `.env` files, credentials, tokens, API keys, private keys, certificates, local config, and files containing passwords. If any appear:

1. Stage nothing from the group.
2. Report the risky files to the user.
3. After they are excluded, stage only the safe files and leave the risky files uncommitted.

This holds even when the user said "全部提交", "commit everything", "别问问题", or "I'm in a hurry".

### Step 3: Write and Commit

Run `git diff --cached`, then commit with a HEREDOC so the blank line and body survive, printing the recorded message in the same call:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <中文简述>

1. <一项具体改动，必要时说明原因>
2. <一项具体改动>
EOF
)" && git log -1 --format=%B
```

The message consists of exactly these parts:

- **type**: `feat`, `fix`, `perf`, `refactor`, `docs`, `style`, `test`, `build`, `ci`, `chore`, or `revert`, chosen by the intent of the diff. Changed behavior is `feat`/`fix`, including behavior defined in Markdown such as skill rules; wording-only edits are `docs`.
- **scope**: the primary module, directory, or skill; one plural umbrella scope such as `skills` when several are touched; spelled as in recent history.
- **中文简述**: Chinese, starts with a verb, at most about 30 characters, no trailing punctuation. Identifiers, file names, and commands stay as-is.
- **body**: one blank line after the subject, then a numbered list with one concrete change per item.
- **breaking change**: when the diff breaks callers, users, or data compatibility, write `<type>(<scope>)!:` and end with a paragraph `BREAKING CHANGE: <说明>`.

Use a plain `git commit -m`. Add `--trailer`, `--signoff`, `Co-authored-by`, `Made-with: Cursor`, or any other attribution only when the user explicitly requests it.

**After a successful commit**, go to Step 4. Do not compare the recorded message against `Co-authored-by: Cursor <cursoragent@cursor.com>`, and do not mention that trailer. A commit hook may append it; leave the commit unchanged, continue any remaining rounds, and still ask the push question when the tree is clean.

**If `git commit` fails:**

1. Do not start another group. Read the error output and run `git status`.
2. If hooks modified files from the failed staged set (per the list from Step 2), inspect their diff, stage only those files, and retry the same commit.
3. If hooks touched other files, injected metadata, or the state is unclear, stop and report.
4. Do not use `--amend`; the failed commit does not exist.

### Step 4: Loop

Run `git status`:

- **Changes remain:** return to Step 2 for the next logical group, re-checking what is staged first.
- **Clean:** go to Step 5.
- **User said to stop after this round** ("先提交这一轮", "剩下的改动之后再说", "先到这里", or similar): report the remaining changes and end without Step 5.

A successful commit is one round, not completion.

### Step 5: Ask Whether to Push

Only after a clean `git status`, ask with the runtime's structured choice tool (`AskQuestion`, `AskUserQuestion`), not with open-ended text:

- Question: `所有提交已完成，是否现在推送到远端？`
- Options: `是，推送` / `否，暂不推送`

**否，暂不推送:** run no push command and report that the commits remain local.

**是，推送:**

1. Run `git branch --show-current`. An empty result means detached HEAD: report that automatic push is unsafe and stop.
2. Run `git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'`. If an upstream exists, run `git push`.
3. With no upstream, run `git remote`, then ask another structured choice listing each remote plus a cancel option, even when only one remote exists. After a selection, run `git push -u <remote> HEAD`.
4. Report the result. On failure, show the error; never retry with `--force`, `--force-with-lease`, or different arguments.

## Rationalizations

| Thought | Reality |
|---------|---------|
| "The staged files look mixed; regrouping them is safer." | The staged set is the user's decision. Commit it as-is unless they ask otherwise. |
| "The first commit worked, so I'm done." | `git status` decides completion, not the first commit. |
| "I'll stage everything remaining to finish faster." | Stage one logical group per round. |
| "'之后再说' isn't an explicit stop." | Natural-language stop instructions count. |
| "They said commit everything and don't ask, so `.env` is fine." | Likely secrets stop the group and get reported first, under any instruction. |
| "I'll commit the safe docs now and mention `.env` later." | Report and exclude risky files before staging anything from that group. |
| "The hook fixed the file; I'll commit it in a later round." | Recover and retry the failed commit unit before touching anything else. |
| "A `Made-with: Cursor` trailer is harmless." | Unrequested metadata is an unauthorized change to commit content. Do not add it yourself. |
| "The hook appended `Co-authored-by: Cursor`, so I should stop instead of continuing or pushing." | That trailer is expected. Do not check for it, amend the commit, or skip the rest of the workflow. |
| "The commits are done, so a summary is enough." | A clean status requires the structured push choice. |
| "There's only one remote; choosing it is harmless." | Setting upstream changes future pushes. Let the user select it. |

**Stop and return to the workflow** if you are about to: run `git add` while files are already staged; stage a likely secret; add unrequested metadata yourself; amend or halt because a hook appended `Co-authored-by: Cursor`; process other files while a failed commit is unrecovered; finish without the push choice; or pick a remote or force-push on your own.
