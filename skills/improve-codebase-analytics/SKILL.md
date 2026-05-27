---
name: improve-codebase-analytics
description: Use when the user wants architecture analysis, refactoring opportunities, module-depth review, testability improvements, design debt findings, or durable architecture analytics for a codebase, unless the request or runtime is chat-only, no-file, or read-only.
---

# Improve Codebase Analytics

## Overview

Surface architectural friction and write a durable Markdown report under `docs/Analytics/` in the analyzed project's root. Stop when the document is created: no GitHub issue, temp HTML, browser opening, or follow-up exploration loop.

If the user request or runtime mode forbids file edits, answer in chat and state that the durable Markdown report requires a write-enabled mode.

Core principle: findings must name the friction, the deeper module shape, and the test surface that improves.

## Vocabulary

Use the project's `CONTEXT.md` language when present. Use these architecture terms consistently:

| Term | Meaning |
|------|---------|
| Module | Anything with an interface and implementation |
| Interface | Everything callers must know, not just types |
| Depth | Much behavior behind a small interface |
| Seam | Where an interface lives |
| Adapter | Concrete thing satisfying an interface |
| Leverage | Caller value from depth |
| Locality | Change, bugs, knowledge, and verification concentrated |

## Required Process

1. Find the analyzed project root. Use the current workspace unless the user names another project. In monorepos, use the nearest directory that owns the relevant build/config files; if multiple roots are plausible, ask before writing. Never write outside the current workspace unless the user explicitly names that external path.
2. Create `docs/Analytics/` there if missing.
3. Read `CONTEXT.md` and relevant `docs/adr/` records if present; note absence in the report.
4. Inspect entry points, core modules, tests, and user-named friction areas.
5. Look for shallow modules, leaked seams, test-only internals, and tightly coupled callers. Apply the deletion test: if removing the module and inlining its behavior would reduce knowledge, files, mocks, or coordination, it is likely shallow unless it preserves a stable interface.
6. Classify dependencies: `in-process`, `local-substitutable`, `remote-owned`, or `true-external`.
7. Write `docs/Analytics/YYYY-MM-DD-architecture-analysis.md`; if it exists, use `YYYY-MM-DD-HHMMSS-architecture-analysis.md`, then append `-2`, `-3`, etc. if needed.
8. Write in the user's language, include concrete paths/evidence, report the path, and stop.

## Dependency Categories

| Category | Use when |
|----------|----------|
| `in-process` | Pure computation or in-memory state; test through the new interface directly |
| `local-substitutable` | Local stand-ins exist, such as in-memory filesystem or test database |
| `remote-owned` | Owned network dependency; define a port and production/test adapters |
| `true-external` | Third-party dependency; isolate it behind an injected adapter or mock |

## Report Template

```markdown
# Architecture Analysis: <project name>

Date: YYYY-MM-DD
Scope: <files, directories, or feature area analyzed>

## Context
- Domain language: <summary or "not present">
- ADRs considered: <list or "none">
- Test surface: <summary>

## Candidates

### 1. <candidate title>
Recommendation: Strong | Worth exploring | Speculative
Dependency category: in-process | local-substitutable | remote-owned | true-external
Files:
- `path/to/file`
Evidence:
- <specific caller, test, or path showing the friction>
- <what leaks across the current interface>
Problem:
<Why the current module shape causes friction.>
Deepening direction:
<What moves behind which interface.>
Benefits:
- Locality: <what concentrates>
- Leverage: <what callers gain>
- Tests: <what becomes testable through the interface>
First slice: <smallest safe change>
Verification: <tests or checks proving the improved interface works>
Risks / ADR conflicts: <real conflicts only>

## Top Recommendation
<Which candidate to do first and why.>
```

If no evidence-backed candidates are found, keep the same structure but state that no material candidates were supported by the inspected scope. The top recommendation should say that no architecture change is recommended from current evidence.

## Quick Reference

| Situation | Required action |
|-----------|-----------------|
| User asks for architecture analysis or improvement opportunities | Create `docs/Analytics/YYYY-MM-DD-architecture-analysis.md` |
| User request or runtime is quick chat, no-file, or read-only | Answer in chat; state that durable Markdown needs write access |
| `docs/Analytics/` is missing | Create it |
| Source workflow suggests HTML, report opening, grilling, or issues | Do not preserve those endings |
| New domain concept appears | Mention a `CONTEXT.md` follow-up; do not edit it unless asked |

## Example

User: "帮我分析一下这个项目架构，有哪些改进机会。"

```text
Created docs/Analytics/2026-05-27-architecture-analysis.md with three candidates:
1. Deepen checkout orchestration behind one interface
2. Collapse shallow validation pass-through modules
3. Move third-party payment calls behind a true-external adapter
```

The full findings belong in the Markdown file, not only in chat.

## Common Mistakes and Rationalizations

| Mistake or excuse | Reality |
|-------------------|---------|
| "The user did not explicitly ask for a file." | This skill's trigger requires the durable artifact unless the request or runtime is chat-only, no-file, or read-only. |
| Inventing candidates to fill the template | If evidence does not support a candidate, say no material candidate was found. |
| Answering only in chat | Baseline agents do this; it loses the durable report. |
| Keeping the source HTML report | The final artifact is Markdown under `docs/Analytics/`. |
| Creating a GitHub issue for tracking | Create issues only in a separate user request. |
| Asking which candidate to explore | Put the top recommendation in the report and stop. |
| Exposing internal seams for tests | Test through the external interface; keep internal seams private. |

## Red Flags

- You are about to send findings only in chat without an explicit chat-only/no-file/read-only request or runtime constraint.
- You are about to write outside `docs/Analytics/`.
- You are about to open a temp HTML report.
- You are about to create or draft a GitHub issue.
- You are about to ask which candidate to explore before writing the report.
- You are about to edit `CONTEXT.md` or ADRs without an explicit follow-up request.
- You are about to invent weak candidates because the template has a `Candidates` section.

If any red flag appears, return to the required process and write the Markdown report first.
