---
name: bug-analysis
description: Use when a user reports a defect, crash, regression, incorrect result, performance degradation, intermittent failure, or unexplained behavior and wants root-cause analysis or fix recommendations.
---

# Bug Analysis

## Overview

Investigate any technology stack from evidence, not intuition. Plausible is not proven. Respond in Chinese unless the user requests another language.

## Operating Contract

- Treat the user's attribution and the last visible error as hypotheses, not facts.
- Separate observed facts, inferences, assumptions, and unknowns.
- Never invent logs, runtime state, reproduction results, file paths, or line numbers.
- Diagnose without modifying code unless the user also asks for a fix.
- Ask only questions that change the next step; otherwise proceed with stated assumptions.
- For active investigation of hard or uncertain bugs, also use `diagnose`.

## Adaptive Investigation

### 1. Frame the Failure

Establish expected versus actual behavior, scope, onset, frequency, environment, reproducibility, and recent changes. Mark known and missing information.

### 2. Follow Evidence

Start from exact errors, timestamps, traces, dumps, metrics, inputs, screenshots, and code. Search real symbols and error text; trace execution and data flow backward from the failure. Inspect relevant callers, state transitions, boundaries, configuration, dependencies, and changes.

Do not replace investigation with a broad list of generic causes.

### 3. Build a Feedback Signal

Prefer the smallest safe check that reproduces or distinguishes the failure: a focused test, minimal input, replay, version/config comparison, targeted instrumentation, profiler, or query plan. For intermittent issues, raise the reproduction rate and correlate by time, host, input, version, or state.

If no useful signal exists, request the specific artifact or access needed. Do not compensate with certainty.

### 4. Rank Falsifiable Hypotheses

Generate enough alternatives to avoid anchoring, usually two to five. For each include:

- supporting and contradicting evidence;
- a falsifiable prediction;
- the cheapest decisive check.

Change one variable at a time and re-rank as evidence changes.

### 5. Calibrate the Conclusion

Use one status:

- **已确认**: the causal chain is demonstrated and material alternatives are ruled out.
- **最可能**: one explanation leads, but a decisive check is missing.
- **未确定**: evidence cannot distinguish the leaders.

Give high, medium, or low confidence with a reason. Distinguish trigger, failure mechanism, and latent condition when they differ. Derive severity from demonstrated impact.

### 6. Recommend and Verify

Separate containment, minimal permanent fix, and prevention. If evidence is insufficient, recommend a discriminating experiment, not a speculative patch.

A fix is verified only when the original signal stops failing and a regression check passes. Note relevant compatibility, data, security, and operational risks.

## Adaptive Output

Lead with the conclusion. Use only sections that add information:

1. **结论** — status, confidence, and reason.
2. **已知事实** — sourced observations.
3. **分析** — causal chain or ranked hypotheses, evidence, and predictions.
4. **下一步验证** — smallest decisive checks in priority order.
5. **修复建议** — only justified containment, permanent fix, and prevention.
6. **验证标准** — proof that the issue is resolved.

Keep direct, well-evidenced cases concise. For intermittent, cross-system, performance, data-integrity, or security failures, include a timeline and deeper evidence chain. Omit empty sections.

## Final Check

- Is the stated root cause stronger than the evidence allows?
- Is correlation being presented as causation?
- Does each leading hypothesis have a falsifiable prediction?
- Is the recommendation fixing the mechanism rather than masking the symptom?
- Are unresolved unknowns and verification gaps explicit?
