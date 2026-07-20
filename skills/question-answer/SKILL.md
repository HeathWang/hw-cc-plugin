---
name: question-answer
description: Use when the user wants a read-only explanation of existing code behavior, architecture, control flow, data flow, dependencies, or implementation decisions and has not requested project changes.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Codebase Question Answering

## Overview

Answer codebase questions from evidence rather than assumptions. Stay read-only while this skill applies, respond in the user's language, and match the requested depth and format.

## Scope

Use this skill for requests to explain:

- Code behavior, control flow, or data flow
- Architecture, dependencies, or implementation decisions
- How an existing feature or subsystem works

This skill does not apply when any requested outcome includes:

- Editing, adding, deleting, or generating project files
- Implementing a feature or fix
- Running commands that mutate project or external state
- Reviewing a change for defects
- Diagnosing an uncertain bug, crash, or regression

For a mixed request such as “explain this and fix it,” use the appropriate change workflow and satisfy both outcomes. Do not let this skill's read-only constraint override an explicit change request.

## Workflow

1. Identify the exact question and requested level of detail.
2. Inspect the smallest relevant code slice: definitions, callers, configuration, tests, and dependencies as needed.
3. Trace the behavior from concrete evidence. Separate observed facts from inference.
4. Use external documentation only when the answer depends on an external API, version, or current behavior.
5. If evidence is insufficient, state what is unknown and what would need inspection; do not guess.

## Answer Contract

Shape the response in this order:

1. Direct answer or conclusion
2. Relevant code evidence, including file and symbol references when available
3. Reasoning that connects the evidence to the conclusion
4. Caveats, trade-offs, or next steps only when they help answer the question

Honor explicit length and format requests. A simple question may need one sentence; use sections only when they improve clarity.

## Quick Reference

- **Facts:** Supported directly by inspected code, configuration, tests, or documentation
- **Inference:** Label it and explain the evidence behind it
- **Unknown:** State the missing evidence instead of presenting a guess as fact
- **Read-only:** Do not modify files or mutate state while this skill applies

## Common Mistakes

- **Using this skill for a mixed change request:** Switch to the appropriate change workflow.
- **Restating before answering:** Lead with the answer unless clarification is required.
- **Reading the whole repository:** Start with the narrowest relevant path and expand only when evidence requires it.
- **Replacing repository evidence with generic best practices:** Explain the current code first; add external guidance only when relevant.
- **Forcing a fixed template:** Match the response shape to the question.
