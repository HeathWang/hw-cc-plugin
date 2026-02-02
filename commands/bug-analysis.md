# Bug Analysis Command

## Purpose
This command provides systematic bug analysis and code issue diagnosis. It guides deep investigation of code problems, automatically locates relevant files when needed, and delivers comprehensive root cause analysis.

## Command Structure

### Initial Assessment
When a user reports a bug or code issue:

1. **Gather Context**
   - Understand the reported symptoms and error messages
   - Identify the technology stack (iOS/React/Python/Java Spring)
   - Determine the scope of the issue (frontend, backend, full-stack)
   - Note any reproduction steps or conditions

2. **Locate Relevant Code**
   If the user hasn't provided sufficient code files:
   - Search for files related to error stack traces
   - Identify components/modules mentioned in the issue
   - Find related configuration files
   - Locate relevant test files
   - Read database schemas or API contracts if applicable

3. **Code Analysis Methodology**
   - **Trace execution flow**: Follow the code path from entry point to failure point
   - **Identify data flow**: Track how data transforms through the system
   - **Check boundaries**: Examine edge cases, null handling, and validation
   - **Review dependencies**: Analyze third-party libraries and version compatibility
   - **Inspect state management**: Verify proper state initialization and updates
   - **Examine timing issues**: Look for race conditions, async/await problems, and lifecycle issues

### Deep Analysis Framework

#### For iOS Applications (Swift/Objective-C)
- Memory management issues (retain cycles, leaks)
- Thread safety and GCD usage
- View lifecycle problems
- Auto Layout constraint conflicts
- API compatibility across iOS versions

#### For React Applications
- Component lifecycle and hooks dependencies
- State management issues (useState, useContext, Redux)
- Event handler binding and closures
- Re-rendering performance problems
- Props drilling and context misuse

#### For Python Scripts
- Type mismatches and None handling
- Iterator exhaustion
- Scope and variable shadowing
- Exception handling gaps
- Module import and circular dependencies

#### For Java Spring Backend
- Bean lifecycle and dependency injection
- Transaction management and rollback scenarios
- Thread pool exhaustion
- Database connection leaks
- Request/Response serialization issues

### Analysis Output Format

**Bug Report**: [Title]

**Severity**: [Critical/High/Medium/Low]

**Symptoms**:
- [Observed behavior]
- [Error messages or logs]
- [Reproduction conditions]

**Root Cause Analysis**:
[Detailed explanation of the underlying issue, including:]
- What is failing and why
- The specific code or configuration causing the problem
- The chain of events leading to the failure

**Evidence**:
```
[Relevant code snippets with line numbers]
[Highlight problematic sections]
```

**Contributing Factors**:
- [Factor 1]: [Explanation]
- [Factor 2]: [Explanation]
- [Factor 3]: [Explanation]

**Impact Assessment**:
- User impact: [How users are affected]
- Data integrity: [Any data corruption risks]
- System stability: [Cascade effects]

**Recommended Fix**:
```
[Proposed code changes with clear comments]
```

**Alternative Solutions**:
1. [Solution A]: [Pros and cons]
2. [Solution B]: [Pros and cons]

**Prevention Strategies**:
- [How to avoid this issue in the future]
- [Suggested tests to add]
- [Code review checklist items]

**Testing Plan**:
1. Unit tests to verify fix
2. Integration test scenarios
3. Edge cases to validate
4. Regression test areas

### Investigation Depth Levels

**Level 1 - Surface Analysis** (Quick triage)
- Read error messages and stack traces
- Check obvious syntax or logic errors
- Verify basic configuration

**Level 2 - Component Analysis** (Standard debugging)
- Analyze the failing component/module
- Review recent changes (git blame/history)
- Check related components

**Level 3 - System Analysis** (Complex issues)
- Trace cross-component interactions
- Analyze timing and concurrency
- Review architecture patterns
- Examine database queries and performance

**Level 4 - Deep Dive** (Critical/mysterious bugs)
- Decompile/inspect compiled code if needed
- Analyze memory dumps or profiling data
- Review vendor library source code
- Investigate platform-specific behavior

### Proactive File Discovery

When files are not provided:

```
1. Ask clarifying questions about:
   - Which feature/screen/endpoint is failing
   - Recent code changes
   - Deployment environment

2. Search for files using patterns:
   - iOS: *ViewController.swift, *.m, *.storyboard
   - React: *.jsx, *.tsx, components/*, hooks/*
   - Python: *.py, requirements.txt, config/*
   - Spring: *Controller.java, *Service.java, application.yml

3. Read files systematically:
   - Start with entry points (main, app.js, Application.java)
   - Follow imports and dependencies
   - Check configuration and environment files
```

### Critical Thinking Checklist

Before finalizing analysis, verify:
- [ ] Have I identified the actual root cause, not just symptoms?
- [ ] Have I considered edge cases and boundary conditions?
- [ ] Have I checked for similar issues elsewhere in the codebase?
- [ ] Is the proposed fix minimal and surgical?
- [ ] Have I considered backwards compatibility?
- [ ] Will this fix introduce new bugs?
- [ ] Have I suggested appropriate tests?

### Example Usage

**User Input**: "My React app crashes when clicking the submit button"

**Analysis Process**:
1. Request stack trace or console errors
2. Locate submit button component file
3. Trace onClick handler implementation
4. Check form validation logic
5. Examine API call and error handling
6. Review state updates after submission
7. Identify the crash point
8. Analyze why the crash occurs
9. Propose fix with test cases

### Best Practices

- **Be thorough**: Don't stop at the first potential cause
- **Be specific**: Reference exact file names, line numbers, and code snippets
- **Be practical**: Prioritize fixes that are implementable
- **Be educational**: Explain the "why" behind issues
- **Be preventive**: Suggest how to avoid similar issues

## Output Language
All analysis, explanations, and recommendations must be written in **Chinese**.
