---
name: code-review-with-files
description: Use when reviewing source files, diffs, commits, pull requests, or bugfixes for correctness issues, regressions, security problems, performance risks, edge cases, or missing tests across any language or framework.
---

# Code Review With Files

## Overview

This skill defines a findings-first code review protocol, not a generic commentary style.

Core principles:
- Report findings before summaries.
- Prioritize correctness and regression risk before style.
- Tie conclusions to concrete evidence whenever possible: file, line, contract, call path, or runtime consequence.
- Read missing context before making claims.
- Match the language of the current review request first. Use broader thread context only as a secondary signal.

## When to Use

- The user asks for a review, code review, PR review, patch review, or diff review.
- The user provides source files, commits, patches, branches, or a readable workspace.
- The goal is to identify bugs, regressions, security issues, performance risks, edge cases, or missing tests.

Do not use this skill for:
- Pure code explanation without issue-finding
- Pure rewriting or wording cleanup
- Style-only commentary when behavioral correctness is out of scope

## Review Standard

The primary goal is to find:

| Dimension | What to look for |
|------|----------|
| Correctness | Logic bugs, missing branches, inconsistent state, contract violations |
| Regression Risk | Broken old behavior, compatibility issues, caller assumption mismatches |
| Security | Injection, auth mistakes, data exposure, missing validation |
| Performance | Obvious time or space waste, unbounded growth, hot-path regressions |
| Concurrency / Lifecycle | Races, double-release, leaks, cancellation or retry mistakes |
| Edge Cases | Null, zero, empty input, boundary values, failure paths |
| Tests | Missing coverage, weak assertions, uncovered regression cases |

Priority order:
1. Issues that can cause wrong behavior, crashes, data loss, or security problems
2. Issues that create likely regressions or obvious performance degradation
3. Maintainability, testability, and design issues
4. Pure style or subjective preference

## Context Gathering

Identify the review target first:
- Single file
- Multi-file change
- Git diff, patch, or commit
- A feature or fix in the local repository

If the required context is available in the workspace, read it before asking the user for more files.

You must gather more context before concluding when:
- The code calls an unknown function, method, interface, or base type
- The change touches shared state, cache, concurrency, transactions, or lifecycle logic
- The review is for a bug fix, but the original buggy path has not been checked
- Behavior depends on config, schema, type definitions, protocol fields, or environment variables

If critical context is still missing:
- State exactly what is missing
- State what cannot be confirmed because of that gap
- Report only issues supported by the available evidence

## Review Workflow

1. Define the change boundary.
   Identify affected entry points, callers, data structures, and tests.

2. Review behavior.
   Walk execution paths for input handling, state transitions, errors, return values, side effects, and rollback paths.

3. Review cross-cutting concerns.
   Check concurrency, security, resource handling, performance, compatibility, and observability.

4. Review tests last.
   Verify the happy path, failure path, edge cases, and regression coverage for the current change.

Do not perform a mechanical line-by-line nitpick pass. Focus on what can actually break.

## Output Contract

Use a findings-first structure by default unless the user explicitly asks for another format:

```markdown
**Findings**
1. [severity] [path:line] Conclusion
   Why this is a problem
   Likely impact
   Suggested fix direction

2. ...

**Open Questions**
- Only include questions that materially affect the judgment and cannot yet be resolved from evidence

**Summary**
- 1-3 sentences on overall risk, merge readiness, and remaining testing gaps
```

Requirements:
- Sort findings by severity, then by impact and confidence within the same severity
- Include file and line references whenever possible; if an exact line is unavailable, give the file and enough locating context
- Explain why the issue matters, not just what line looks suspicious
- Suggest fix direction without pretending the root cause is proven when evidence is incomplete
- Write in the language of the most recent user request for this review. If the current request is in English, respond in English even if earlier conversation was in another language.
- If no issue is found, explicitly say no blocking issues were found and note residual risk or testing blind spots

## Severity Guide

| Label | When to use it |
|------|----------|
| critical | Crashes, data corruption, security vulnerabilities, severely incorrect results |
| high | Likely wrong behavior, clear regressions, important feature failure |
| medium | Maintainability issues, missing edge handling, weak tests, performance risk |
| low | Style, naming, small redundancies, optional polish |

## Writing Findings

A good finding is:
- Verifiable: it points to a concrete location and failure condition
- Consequential: it explains who or what is affected
- Specific: it avoids vague phrasing like "should optimize" or "might be an issue" without evidence
- Atomic: one finding per issue, not multiple unrelated concerns merged together

Recommended pattern:

```markdown
1. [high] `foo/bar.ts:87`
   This path updates local state to success even when `save()` fails, so callers can observe "saved" while persistence never completed.
   That turns a retriable failure into silent data inconsistency.
   Commit state only after persistence succeeds, or roll back and surface the error on the failure path.
```

## Common Mistakes

| Bad practice | Why it fails | Better approach |
|---------|------------|----------|
| Start with a broad overview and hide the real issues later | The user needs blocking issues first | Put findings first and summarize later |
| Conclude without reading dependencies or callers | It leads to false positives and false confidence | Read the minimum required context first |
| Say "this is bad" without consequence | It is not actionable | Explain trigger condition and impact |
| Lead with style issues | Noise obscures real risk | Put correctness first |
| Follow the thread's older language instead of the current review request | The review comes back in the wrong language | Use the most recent review request as the primary language signal |
| Say only "LGTM" when nothing obvious is wrong | It provides almost no value | State that no blocking issue was found and note testing gaps |
| Invent issues to sound thorough | It destroys trust | Use open questions when evidence is incomplete |

## Review Heuristics

- For bug fixes, check whether the patch fixes only one symptom while leaving sibling paths broken
- For new flags or branches, check whether they introduce state-space explosion
- For cache, retry, concurrency, or async callback code, check ordering and idempotency
- For parsing, SQL, HTML, filesystem, or permission logic, check security boundaries first
- For schema, DTO, or interface field changes, check compatibility and default behavior

## Final Check Before Sending

Before sending:
- Are findings first?
- Are findings ordered by severity?
- Does each finding include evidence and impact?
- Is any critical context still unread?
- Did you call out testing gaps?
- If no issue was found, did you explicitly say so and note residual risk?
