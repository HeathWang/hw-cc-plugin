---
name: handoff
description: Use when the user asks to create a handoff, session summary, context compact, continuation note, 交接文档, 压缩上下文, or instructions for the next agent to resume work later.
argument-hint: "Focus for the next session"
---

# Handoff

## Overview

Write a handoff document summarizing the current conversation so a fresh agent can continue the work. Save it to the user's OS temporary directory, not the current workspace.

## When to Use

- User asks for a handoff, session summary, context compact, continuation note, or next-agent instructions
- User says "生成交接文档", "交接文档", "压缩上下文", "给下个 agent", "下一轮继续", or "接着做"
- User passes arguments describing what the next session should focus on

## Output Location

Save the document outside the workspace using the OS temp directory:

- macOS/Linux: use `$TMPDIR` when set, otherwise `/tmp`
- Windows: use `%TEMP%`

Use a clear filename like `handoff-YYYYMMDD-HHMM.md`, then report the saved path to the user.

## Required Sections

- Objective and requested next-session focus
- Current status and completed work
- Pending work and next recommended steps
- Files touched or artifacts to inspect
- Commands, tests, or checks already run
- Known failures, risks, and constraints
- User preferences and project rules that matter
- Suggested skills with reasons

## Constraints

Do not duplicate content already captured in other artifacts such as PRDs, plans, ADRs, issues, commits, or diffs. Reference them by path or URL and summarize only the current status needed to continue.

Redact sensitive information, including API keys, passwords, tokens, credentials, private keys, secrets, and personally identifiable information.

If the user passed arguments, treat them as the next-session focus and tailor the document accordingly.

## Common Mistakes

- Do not save the handoff inside the current repository.
- Do not include secrets or raw private data.
- Do not omit the final saved path.
