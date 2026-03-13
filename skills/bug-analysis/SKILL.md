---
name: bug-analysis
description: Use when diagnosing bugs, crashes, or unexpected behavior in iOS, React, Python, or Java Spring code. Triggered by error messages, stack traces, crash reports, or when user says "analyze this bug" or "why is this crashing". Performs root cause analysis, evidence gathering, and fix recommendations. Output in Chinese.
---

# Bug Analysis

## Overview

Systematic bug investigation framework covering root cause analysis, evidence gathering, fix recommendations, and prevention strategies. All output in Chinese.

## When to Use

- User reports a bug, crash, or unexpected behavior
- User invokes `/bug-analysis`
- Need to trace error stack traces, identify root causes, or recommend fixes

## Investigation Process

### Step 1: Gather Context
- Understand symptoms and error messages
- Identify technology stack (iOS/React/Python/Java Spring)
- Note reproduction steps and conditions

### Step 2: Locate Relevant Code
If files not provided, search proactively:
- iOS: `*ViewController.swift`, `*.m`, `*.storyboard`
- React: `*.jsx`, `*.tsx`, `components/*`, `hooks/*`
- Python: `*.py`, `requirements.txt`, `config/*`
- Spring: `*Controller.java`, `*Service.java`, `application.yml`

Follow entry points → imports → dependencies → config files.

### Step 3: Analyze

**Trace execution flow** → follow code path from entry to failure
**Identify data flow** → track data transformations
**Check boundaries** → edge cases, null handling, validation
**Review dependencies** → library versions, compatibility
**Inspect state management** → initialization and updates
**Examine timing** → race conditions, async/await, lifecycle

## Platform-Specific Focus Areas

| Platform | Key Issues |
|----------|-----------|
| iOS (Swift/ObjC) | Memory/retain cycles, thread safety, view lifecycle, AutoLayout, iOS version compat |
| React | Hook dependencies, state management, event closures, re-rendering, props drilling |
| Python | Type mismatches, None handling, iterator exhaustion, scope, circular imports |
| Java Spring | Bean lifecycle, transaction management, thread pool exhaustion, DB connection leaks, serialization |

## Investigation Depth

| Level | When | Actions |
|-------|------|---------|
| L1 Surface | Quick triage | Error messages, stack traces, obvious syntax errors |
| L2 Component | Standard | Analyze failing component, recent changes, related components |
| L3 System | Complex | Cross-component interactions, concurrency, DB queries |
| L4 Deep Dive | Critical/mysterious | Compiled code, memory dumps, vendor source, platform-specific |

## Output Format

```
**Bug Report**: [Title]
**Severity**: Critical / High / Medium / Low

**症状 (Symptoms)**:
- 观察到的行为
- 错误信息或日志
- 复现条件

**根因分析 (Root Cause)**:
[详细说明失败原因、涉及代码、事件链]

**证据 (Evidence)**:
[相关代码片段及行号]

**影响评估 (Impact)**:
- 用户影响
- 数据完整性
- 系统稳定性

**推荐修复 (Fix)**:
[带注释的代码变更]

**替代方案**: [方案A优缺点 / 方案B优缺点]

**预防策略**: [如何避免 / 建议测试 / 代码审查要点]

**测试计划**: 单元测试 / 集成测试 / 边界场景 / 回归测试
```

## Critical Thinking Checklist

Before finalizing:
- [ ] Identified actual root cause, not just symptoms?
- [ ] Considered edge cases and boundary conditions?
- [ ] Checked for similar issues elsewhere in codebase?
- [ ] Proposed fix is minimal and surgical?
- [ ] Considered backwards compatibility?
- [ ] Fix won't introduce new bugs?
- [ ] Suggested appropriate tests?
