---
name: improve-codebase-analytics
description: Use when the user wants architecture analysis, refactoring opportunities, module-depth review, testability improvements, design debt findings, or durable architecture analytics for a codebase.
---

# Improve Codebase Analytics

## Overview

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This skill follows the same interactive architecture-analysis shape as `improve-codebase-architecture`: explore deeply, use parallel subagents when available, present candidates, ask the user which one to explore, then converge through a grilling loop.

The only changed ending: do **not** create GitHub issues or PRs. The durable artifact is a Markdown report under `docs/Analytics/` in the analyzed project.

If the user request or runtime forbids file edits, run the same exploration and discussion in chat, then state that the durable Markdown report requires a write-enabled mode.

## Glossary

Use the project's `CONTEXT.md` language when present. Use these architecture terms consistently in every suggestion:

| Term | Meaning |
|------|---------|
| Module | Anything with an interface and an implementation: function, class, package, feature slice |
| Interface | Everything callers must know: types, invariants, error modes, ordering, config, not just signatures |
| Implementation | The code inside the module |
| Depth | Leverage at the interface: much behavior behind a small interface |
| Seam | Where an interface lives; a place behavior can change without editing callers |
| Adapter | A concrete thing satisfying an interface at a seam |
| Leverage | What callers gain from module depth |
| Locality | Change, bugs, knowledge, and verification concentrated in one place |

Key principles:

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across many callers, it was earning its keep.
- **The interface is the test surface.**
- **One adapter = hypothetical seam. Two adapters = real seam.**

## Process

### 1. Establish Scope

Find the analyzed project root. Use the current workspace unless the user names another project. In monorepos, use the nearest directory that owns the relevant build/config files; if multiple roots are plausible, ask before writing. Never write outside the current workspace unless the user explicitly names that external path.

If the user has not named a focus area and the codebase is non-trivial, ask one short question before deep exploration:

> Which area should I prioritize: module depth/testability, data flow, dependency seams, feature boundaries, or overall architecture?

If the user names a focus area, continue without asking. If the user explicitly asks for a whole-codebase pass, use the full project as scope.

### 2. Load Context

Read the project's domain glossary and decisions first:

- `CONTEXT.md` if present
- Relevant `docs/adr/` records if present
- Build/config files that define the project root
- Existing tests or test target configuration

Record missing context in the final report instead of inventing it.

Use `CONTEXT.md` vocabulary for the domain and this skill's glossary for architecture. If `CONTEXT.md` defines "Order," talk about "the Order intake module," not an incidental class name.

### 3. Explore With Parallel Subagents

Use the available subagent mechanism (`Subagent`, `Task`, or `Agent`) to walk the codebase before forming conclusions. Launch independent explorers in parallel when the codebase has enough surface area.

Recommended parallel tracks:

| Track | What to inspect |
|-------|-----------------|
| Domain and decisions | `CONTEXT.md`, ADRs, project vocabulary, decision constraints |
| Entry points and flows | App/request entry points, feature flows, orchestration paths |
| Module depth | Shallow pass-through modules, leaked seams, tightly coupled callers |
| Test surface | Existing tests, hard-to-test behavior, mocks that expose internals |
| Dependency seams | In-process, local substitutable, remote-owned, and true-external dependencies |

Each subagent must return:

- Candidate friction points with concrete paths
- Why understanding or testing requires bouncing across modules
- Which modules look shallow, and the result of the deletion test
- Evidence that supports or weakens each candidate
- Recommendation strength: `Strong`, `Worth exploring`, or `Speculative`

If no subagent tool is available, do the same tracks sequentially and say in the report that parallel subagents were unavailable.

### 4. Synthesize Candidates Before Writing the Final Report

Do not write the durable Markdown report immediately after the first scan. First, synthesize candidates and present them to the user in chat.

For each candidate, include:

- **Files**: files or modules involved
- **Problem**: why the current architecture causes friction
- **Deepening direction**: what behavior moves behind which interface
- **Benefits**: locality, leverage, and testability improvements
- **Dependency category**: `in-process`, `local-substitutable`, `remote-owned`, or `true-external`
- **Recommendation strength**: `Strong`, `Worth exploring`, or `Speculative`

End the candidate briefing with:

> Which of these would you like to explore?

Do not propose final interfaces yet. Do not create the final Markdown document before the user chooses a candidate, unless the user explicitly requests a non-interactive report.

### 5. Grilling Loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them:

- Constraints and non-goals
- Dependencies and ownership
- The shape of the deepened module
- What sits behind the seam
- Which adapters are real versus hypothetical
- What tests should survive the refactor
- What the smallest safe first slice is

Side effects during the grilling loop:

- If a new domain concept is load-bearing, recommend adding it to `CONTEXT.md`; only edit `CONTEXT.md` when the user explicitly asks.
- If the user rejects a candidate with a load-bearing reason, offer to record an ADR; only create or edit ADRs when the user explicitly asks.
- If the candidate contradicts an ADR, surface the conflict only when the friction is real enough to warrant revisiting the ADR.

### 6. Write the Durable Markdown Report

After exploration and the grilling loop, create `docs/Analytics/` under the analyzed project root if missing.

Derive a concise report topic from the selected candidate or non-interactive focus area. Use UpperCamelCase, 2-4 meaningful English words, and project/domain vocabulary when available: `AnalyticsLifecycle`, `CheckoutOrchestration`, `PaymentAdapter`. Do not use generic topics such as `Analysis`, `ArchitectureAnalysis`, or a timestamp. If no clear topic can be inferred, ask the user for a short topic name before writing.

Write `docs/Analytics/YYYY-MM-DD-architecture-<Topic>.md`, for example `docs/Analytics/2026-06-04-architecture-AnalyticsLifecycle.md`. If that exact path exists, append `-2`, `-3`, etc. before `.md`; do not fall back to timestamped `architecture-analysis` names.

Write in the user's language. Include concrete paths, evidence, the selected candidate, decisions from the grilling loop, and the recommended first slice.

Do not create GitHub issues, PRs, project-board items, or tracking tickets. Do not open a browser. Stop after reporting the written Markdown path.

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
Focus: <user-selected candidate or "non-interactive whole-codebase pass">

## Context
- Domain language: <summary or "not present">
- ADRs considered: <list or "none">
- Test surface: <summary>
- Exploration method: <parallel subagents used / sequential exploration because subagents unavailable>

## Candidate Briefing
- <short summary of the candidates presented before the user chose one>

## Selected Candidate

### <candidate title>
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

## Decisions From Grilling
- <constraint, decision, or rejected alternative>

## First Slice
First slice: <smallest safe change>
Verification: <tests or checks proving the improved interface works>
Risks / ADR conflicts: <real conflicts only>

## Top Recommendation
<What to tackle first and why.>
```

If no evidence-backed candidates are found, keep the same structure but state that no material candidates were supported by the inspected scope. The top recommendation should say that no architecture change is recommended from current evidence.

If the user explicitly requests a non-interactive report, include all candidates instead of a single selected candidate and state that no grilling loop occurred.

## Quick Reference

| Situation | Required action |
|-----------|-----------------|
| User asks for architecture analysis or improvement opportunities | Explore first, present candidates, ask which to explore, then write `docs/Analytics/YYYY-MM-DD-architecture-<UpperCamelCaseTopic>.md` |
| User names a focus area | Use it as the exploration focus; do not ask an extra pre-scope question |
| User does not name a focus area in a non-trivial project | Ask which area to prioritize before deep exploration |
| Codebase has independent areas to inspect | Launch parallel subagents for the exploration tracks |
| Subagents are unavailable | Explore the same tracks sequentially and note that in the report |
| `docs/Analytics/` is missing | Create it only when writing the final report |
| User request or runtime is quick chat, no-file, or read-only | Keep the analysis in chat; state that durable Markdown needs write access |
| New domain concept appears | Recommend a `CONTEXT.md` follow-up; do not edit it unless asked |
| User rejects a candidate for a durable architectural reason | Offer an ADR; do not write it unless asked |

## Example

User: "帮我分析一下这个项目架构，有哪些改进机会。"

```text
I found three architecture candidates:
1. Deepen checkout orchestration behind one interface
2. Collapse shallow validation pass-through modules
3. Move third-party payment calls behind a true-external adapter

Which of these would you like to explore?
```

After the user picks one candidate and the grilling loop completes:

```text
Created docs/Analytics/2026-05-27-architecture-CheckoutOrchestration.md for the checkout orchestration candidate.
```

## Common Mistakes and Rationalizations

| Mistake or excuse | Reality |
|-------------------|---------|
| Writing the Markdown report before deep exploration | The report is the final artifact, not the first action. |
| Skipping subagents because the first scan found obvious candidates | Obvious candidates need independent evidence; launch parallel tracks when available. |
| Not asking what to explore | The user should choose the candidate before the final report unless they requested non-interactive output. |
| Inventing candidates to fill the template | If evidence does not support a candidate, say no material candidate was found. |
| Answering only in chat after write-enabled analysis | Baseline agents do this; it loses the durable report. |
| Using timestamped `architecture-analysis` names for same-day reports | Same-day reports should be distinguished by the UpperCamelCase analysis topic. |
| Creating a GitHub issue for tracking | Create issues only in a separate user request. |
| Editing `CONTEXT.md` or ADRs during analysis | Recommend follow-ups; edit them only after explicit user approval. |
| Exposing internal seams for tests | Test through the external interface; keep internal seams private. |

## Red Flags

- You are about to write `docs/Analytics/` before reading context and exploring the codebase.
- You are about to skip parallel subagents even though the codebase has independent areas to inspect.
- You are about to send only one unchallenged candidate without evidence.
- You are about to skip asking "Which of these would you like to explore?" after candidate synthesis.
- You are about to write a generic or timestamped `architecture-analysis` filename instead of a topic-specific UpperCamelCase filename.
- You are about to create or draft a GitHub issue.
- You are about to edit `CONTEXT.md` or ADRs without an explicit request.
- You are about to invent weak candidates because the template has a `Candidates` section.
- You are about to treat a pass-through wrapper as a seam without applying the deletion test.

If any red flag appears, return to the process: scope, context, parallel exploration, candidate briefing, user-selected grilling loop, then Markdown report.
