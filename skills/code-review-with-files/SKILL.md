---
name: code-review-with-files
description: Use when performing a comprehensive code review - analyzing bugs, performance, security, edge cases, and code quality across any language or framework. Output in Simplified Chinese.
---

# Code Review

## Overview

Expert code reviewer role covering correctness, performance, security, edge cases, and maintainability. All output in Simplified Chinese (简体中文).

## When to Use

- User invokes `/code-review-with-files` or requests a code review
- User shares source files for review
- Reviewing PRs, features, or bug fixes

**Before starting:** Request source files, relevant config files, and project context if not provided. If provided files import other files, read those dependencies before reviewing.

## Review Process

### 1. File Assessment
- Confirm receipt of all necessary files; request missing ones
- Identify language, framework, and code purpose
- Determine if files have external dependencies → read minimal required dependencies

### 2. Initial Assessment
- Review overall architecture and design patterns
- Note scope, complexity, and external integrations

### 3. Line-by-Line Analysis
- Examine each function and code block
- Flag issues with severity levels
- Consider runtime behavior and edge cases

### 4. Cross-Cutting Concerns
- Error handling strategies
- Resource management (memory, connections, files)
- Concurrency and thread safety
- Input validation

## Analysis Dimensions

- **Correctness** — logic errors, bugs, incorrect implementations
- **Performance** — time/space complexity, optimization opportunities
- **Security** — vulnerabilities, injection risks, data validation
- **Edge Cases** — boundary conditions, null/undefined handling
- **Code Quality** — readability, maintainability, design patterns
- **Best Practices** — language conventions, framework guidelines
- **Testing** — coverage gaps, testability issues

## Output Format (简体中文)

```
### 📋 概述
2-3句话概述代码质量和主要发现。

### 🚨 严重问题 [🔴 严重]
- 📍 位置: `file.js:行号`
- ❌ 问题: 详细说明
- ⚠️ 影响: 潜在后果
- ✅ 解决方案: 代码示例

### ⚡ 高优先级问题 [🟠 高]
### 🔔 中优先级问题 [🟡 中]
### 🚀 性能考虑
### 🔒 安全问题
### 🎯 边界情况
### ✨ 代码质量改进
```

## Severity Levels

| Level | Meaning |
|-------|---------|
| 🔴 严重 | Crashes, data loss, security vulnerabilities |
| 🟠 高 | Incorrect behavior, severe performance issues |
| 🟡 中 | Maintainability, readability, minor performance |
| 🟢 低 | Style preferences, small improvements |

## Review Principles

- Be constructive and specific; provide code examples for fixes
- Explain the "why" behind recommendations
- Balance idealism with pragmatism
- Number all issues sequentially within each section
