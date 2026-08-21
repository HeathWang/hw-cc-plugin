---
name: code-review-with-files
description: Use when reviewing source files, diffs, commits, pull requests, or bugfixes for correctness issues, regressions, security problems, performance risks, edge cases, or missing tests across any language or framework.
---

# Code Review With Files

## Overview

This skill defines a findings-first, read-only code review protocol.

Inspect the complete review boundary, then report every actionable issue supported by evidence. Prioritize correctness, security, regressions, and runtime risk over style.

## When to Use

- The user asks to review source files, a diff, commit, branch, pull request, or bug fix.
- The goal is to find correctness, regression, security, performance, edge-case, or test problems.

Do not use it for pure explanation, rewriting, or style-only feedback.

## Scope and Safety

Identify the target and baseline first. Inspect the entire supplied file or patch. For a commit, branch, or pull request, compare the intended base to the complete head change, not only the latest commit. Honor explicit scope and exclusions.

A change finding must be introduced, worsened, or made newly reachable by the review target. Do not misattribute pre-existing defects; report only an immediate critical one separately as a **Pre-existing Risk**.

Review is read-only unless changes are separately requested:
- Do not edit, stage, unstage, reset, or regroup files.
- Run only safe, targeted checks that materially improve confidence.
- Inspect the full requested boundary rather than stopping at the first issue.

Read callers, contracts, types, schemas, configuration, lifecycle code, and the original bug path only when a conclusion depends on them. Read relevant existing tests early enough to establish intent, but reconcile them with contracts and callers rather than treating them as automatic truth.

If critical context is unavailable, state what is missing and what cannot be confirmed. Report only supported conclusions.

## Review Workflow

1. Define the boundary: changed behavior, entry points, callers, data structures, contracts, and tests.
2. Establish intended behavior from code, types, documentation, callers, and relevant existing tests.
3. Walk execution paths: inputs, state transitions, errors, returns, side effects, cleanup, and rollback.
4. Check cross-cutting risks: security, concurrency, resources, performance, compatibility, and observability.
5. Evaluate test coverage after understanding the implementation: happy path, failure path, edge cases, and regression proof.
6. Complete the full boundary pass. Consolidate repeated manifestations of one root cause instead of duplicating findings.

Do not perform a mechanical line-by-line nitpick pass. Focus on behavior that can actually break.

Subjective style is not a finding unless the user explicitly requests style feedback or it creates a concrete maintenance risk.

## Finding Threshold

A finding must be:
- **Attributable:** caused, worsened, or exposed by the target
- **Verifiable:** identifies a trigger, violated contract, call path, or failure
- **Consequential:** explains the user, system, security, or maintenance impact
- **Actionable:** gives a realistic fix direction
- **Atomic:** covers one root cause; combine duplicate instances with the same fix

Resolve assumptions from available context before reporting. If missing evidence can materially change the judgment, use an open question instead of inventing a finding.

## Severity and Merge Readiness

Use impact, likelihood, blast radius, and recoverability. Defect type alone never determines severity: crashes, security issues, and performance problems can occur at any level.

| Label | When to use it |
|------|----------|
| critical | Reachable data loss, corruption, broad outage, exploitable boundary failure, or severe unrecoverable results |
| high | Likely regression or security failure on a supported/common path with important impact |
| medium | Conditional or limited incorrect behavior, material maintenance risk, weak regression proof, or bounded degradation |
| low | Localized low-impact issue or optional polish with a concrete benefit |

Unless project policy says otherwise, critical and high findings block merge; medium and low findings do not. Do not raise severity merely because evidence is uncertain or lower it because the fix is easy.

## Output Contract

Use a findings-first structure by default unless the user explicitly asks for another format:

```markdown
**Findings**
1. [severity] [path:line] Conclusion
   Trigger/evidence and impact
   Fix direction

2. ...

**Pre-existing Risks** (optional)

**Open Questions** (optional)

**Summary**
Overall risk, merge readiness, tests run, and testing gaps
```

Requirements:
- Sort findings by severity, then by impact and confidence within the same severity
- Include a location, trigger/evidence, impact, and fix direction; use locating context if no exact line is available
- Suggest rather than implement fixes unless the user asks
- Omit empty **Pre-existing Risks** and **Open Questions** sections
- Use the language of the most recent review request
- With zero findings, say **No actionable findings found** and note residual risk or testing gaps
- With only non-blocking findings, say **No blocking findings** only in the summary

Example:

```markdown
1. [high] `foo/bar.ts:87`
   This path updates local state to success even when `save()` fails, so callers can observe "saved" while persistence never completed.
   That turns a retriable failure into silent data inconsistency.
   Commit state only after persistence succeeds, or roll back and surface the error on the failure path.
```

## Common Mistakes

- Reporting an unchanged defect as if the reviewed change introduced it
- Assigning severity from labels such as "crash" without calibrating realistic impact
- Finalizing before reading context or tests on which the conclusion depends
- Stopping after the first finding or duplicating one root cause across several findings

## Quick Heuristics

- For bug fixes, check whether the patch fixes only one symptom while leaving sibling paths broken
- For new flags or branches, enumerate meaningful combinations and preserved invariants
- For cache, retry, concurrency, or async callback code, check ordering and idempotency
- For parsing, SQL, HTML, filesystem, or permission logic, check security boundaries first
- For schema, DTO, or interface field changes, check compatibility and default behavior

## Final Check Before Sending

Before sending:
- Are findings first, attributable, evidence-backed, actionable, and ordered by calibrated severity?
- Was the complete boundary inspected without duplicate root causes?
- Is any context required for a conclusion still unread?
- Are tests run and testing gaps stated accurately?
- With zero findings, does the response say **No actionable findings found**?
