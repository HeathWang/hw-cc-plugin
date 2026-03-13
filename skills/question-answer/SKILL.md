---
name: question-answer
description: Use when answering technical questions about a codebase - reading and analyzing project files to provide comprehensive, accurate guidance without modifying any files. Triggered by "explain", "how does X work", "why does X happen", or any question about code behavior or architecture.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Question & Answer Workflow

## Overview

Read-only technical Q&A for codebase questions. Analyze code, explain concepts, and provide actionable guidance without modifying project files. Respond in the user's language.

## Core Constraints

- **NEVER modify, edit, or alter any project files** — informational and advisory only
- Full read access to all project files — analyze freely
- Respond in the user's language (Chinese question → Chinese response)

## When to Use

- User invokes `/question-answer` or asks a technical question about the codebase
- Need to explain code behavior, architecture, or implementation decisions
- User wants analysis or guidance without code changes

## Process

1. **Understand the Question** — restate to confirm understanding
2. **Analyze Context** — read relevant source files, configs, dependencies
3. **Research Solution** — consider best practices and existing patterns in the codebase
4. **Formulate Response** — structure a comprehensive answer
5. **Quality Check** — ensure accuracy and completeness
6. **Deliver** — clear, actionable guidance

## Response Structure

1. **Problem Understanding** — restate the question clearly
2. **Context Analysis** — current codebase state relevant to the question
3. **Solution Explanation** — detailed explanation with reasoning
4. **Implementation Guidance** — step-by-step guidance (reference only, no file changes)
5. **Considerations** — potential issues, alternatives, trade-offs

## Quality Standards

- Accurate technical information
- Reference official documentation when applicable
- Include performance and memory considerations where relevant
- Use clear, professional language
- Structure information hierarchically
- Provide code examples for reference (not to be applied directly)
- Explain reasoning behind recommendations
- Maintain consistency with existing project patterns
