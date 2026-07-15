# hw-cc-plugin

**Language:** English | [简体中文](README.zh-CN.md)

Daily development skills, primarily for frontend development, iOS, H5, and more.

## 📋 Overview

**hw-cc-plugin** is a comprehensive Claude Code plugin designed to streamline your daily development workflow. It provides a collection of powerful skills for code conversion, review, bug analysis, and Git workflow automation.

## ✨ Features

- **🔄 Code Conversion**: Seamlessly convert Java classes to TypeScript (Next.js) or Swift (iOS) interfaces
- **🔍 Code Review**: Perform comprehensive code reviews with multi-dimensional analysis
- **🐛 Bug Analysis**: Systematic debugging and root cause analysis
- **💬 Expert Reviews**: Linus Torvalds-style code review protocol for quality assurance
- **📝 Git Automation**: Intelligent Git commit workflow with automatic message generation
- **❓ Q&A Workflow**: Comprehensive question and answer system for code guidance
- **🌍 iOS Internationalization**: Complete iOS localization workflow with SwiftGen L10n support and multi-language management
- **🏗️ Architecture Analytics**: Durable architecture analysis reports under `docs/Analytics/`
- **📄 PRD & Handoff Workflows**: Convert settled context into PRDs and continuation notes for future agents
- **🧠 Plan Stress Testing**: Grill technical plans against code, glossary terms, ADRs, and documented decisions
- **🔗 Yuque Document Fetching**: Fetch a single Yuque page through a local logged-in browser session
- **⚡ Communication Modes**: Token-efficient concise responses for users who explicitly request brevity

## 🚀 Skills

### 1. Git Commit Workflow
`skills/git-commit-workflow/SKILL.md`

Automates the Git commit process with intelligent file staging and Chinese commit message generation following Conventional Commits format.

**Features:**
- Smart file grouping by functionality
- Automatic commit message generation in Chinese
- Conventional Commits format with emojis
- Loops until working tree is clean

### 2. Code Review with Files
`skills/code-review-with-files/SKILL.md`

Performs comprehensive code reviews across multiple dimensions including correctness, performance, security, edge cases, and code quality.

**Features:**
- Multi-dimensional analysis (7+ review dimensions)
- Severity-based issue classification (Critical, High, Medium, Low)
- Detailed feedback with file locations and solutions
- All outputs in Simplified Chinese

### 3. Bug Analysis
`skills/bug-analysis/SKILL.md`

Provides systematic bug analysis and code issue diagnosis with automatic file location and comprehensive root cause analysis.

**Features:**
- Technology stack detection (iOS, React, Python, Java Spring)
- 4 levels of investigation depth
- Proactive file discovery
- Detailed analysis output with testing plans

### 4. Linus Torvalds Code Review
`skills/linus-torvalds-review/SKILL.md`

Emulates Linus Torvalds' unique code review philosophy focusing on good taste, pragmatism, and simplicity.

**Features:**
- Context-aware review protocols
- Multi-dimensional analysis (data structures, special cases, complexity, breaking changes)
- Direct, sharp feedback style
- Responds in user's language

### 5. Java to Next.js TypeScript Conversion
`skills/java-to-nextjs/SKILL.md`

Converts Java 1.8 classes to Next.js TypeScript interface definitions with precise type mapping and nullability handling.

**Features:**
- Java 1.8 → TypeScript 5.0+ conversion
- Special annotation handling (`@BigDecimalToNumber`, `@TimestampFormat`)
- Inheritance handling (extension vs flattening)
- Property names preserved to match API contracts
- Output as markdown code blocks only — never modifies project files

### 6. Java to Swift Conversion
`skills/java-to-swift/SKILL.md`

Converts Java 1.8 classes to Swift 5.0+ struct objects with Codable conformance.

**Features:**
- Java 1.8 → Swift 5.0+ conversion
- Special annotation handling (`@BigDecimalToString`)
- Flattened inheritance structure
- Codable protocol conformance
- Output as markdown code blocks only — never modifies project files

### 7. Question & Answer
`skills/question-answer/SKILL.md`

Provides comprehensive Q&A workflow with full read access to project files and detailed technical guidance.

**Features:**
- Read-only file access for code analysis
- Systematic problem-solving approach
- Structured response format
- Educational and advisory focus

### 8. iOS Internationalization Workflow
`skills/ios-i18n-workflow/SKILL.md`

Automated iOS internationalization workflow for SwiftGen L10n code generation. Supports multi-language localization management with verification and cleanup capabilities.

**Features:**
- **Full internationalization workflow**: Extract hardcoded strings, add translations for ALL target languages, verify alignment, and generate Swift code
- **Translation verification**: Check missing translations across multiple target languages with automated gap detection
- **Cleanup utilities**: Find and remove unused localization entries with dry-run safety checks
- **Multi-language support**: Handle any number of target languages with sequential workflow management
- **Helper scripts**: Python scripts for checking missing translations and cleaning unused entries

**Use Cases:**
- Internationalize iOS code by replacing hardcoded strings with L10n references
- Verify translation completeness across multiple languages
- Clean up unused localization entries
- Generate SwiftGen code after localization updates

### 9. Improve Codebase Analytics
`skills/improve-codebase-analytics/SKILL.md`

Analyzes codebase architecture for module depth, locality, leverage, seams, adapters, and testability, then writes a durable Markdown report under the analyzed project's `docs/Analytics/` directory.

**Features:**
- Architecture deepening analysis using consistent module/interface vocabulary
- Durable Markdown output in `docs/Analytics/YYYY-MM-DD-architecture-<UpperCamelCaseTopic>.md`
- Explicit stop condition: no temp HTML, no GitHub issue, no follow-up design loop
- Incorporates `CONTEXT.md` domain language and ADR constraints when present

### 10. Fetch Yuque Doc
`skills/fetch-yuque-doc/SKILL.md`

Fetches one Yuque document from a user-provided page URL through a local logged-in Chrome-family browser, especially for private-space documents where API token access is unavailable or undesirable.

**Features:**
- Validates single-page `yuque.com` or `*.yuque.com` document URLs
- Reuses local Chrome/Chromium/Edge sessions, preferring AppleScript on macOS
- Supports Markdown output for reading and JSON output for downstream tooling
- Reports precise failure reasons for URL, browser, profile, launch, or extraction errors
- Intentionally scoped to one document per invocation, not crawling or synchronization

### 11. Diagnose
`skills/diagnose/SKILL.md`

Provides a disciplined workflow for hard bugs, intermittent failures, production incidents, unclear regressions, and cases where reproduction or fix confidence is uncertain.

**Features:**
- Prioritizes building a fast, deterministic pass/fail feedback loop
- Requires reproduction and exact symptom capture before root cause work
- Uses ranked falsifiable hypotheses before instrumentation or fixes
- Guides targeted debugging probes, regression tests, and original-scenario verification
- Includes cleanup and post-mortem checks before declaring the bug fixed

### 12. Grill Me
`skills/grill-me/SKILL.md`

Stress-tests a plan, design, architecture, or technical proposal by walking decision branches one question at a time until shared understanding is reached.

**Features:**
- Challenges plans through sequential, focused questions
- Provides a recommended answer or default position with each question
- Explores the codebase instead of asking when repository evidence can answer
- Summarizes the agreed direction, remaining risks, and unresolved questions

### 13. Grill with Docs
`skills/grill-with-docs/SKILL.md`

Stress-tests plans against a project's domain language, glossary, `CONTEXT.md`, ADRs, documented decisions, code behavior, and overloaded terminology.

**Features:**
- Performs a bounded pass over context docs, ADRs, and obvious code terminology
- Calls out conflicts between proposed terms and existing glossary language
- Uses concrete scenarios to clarify domain boundaries and edge cases
- Updates `CONTEXT.md` inline when terms are resolved, or states the exact update when edits are unavailable
- Offers ADRs only for hard-to-reverse, surprising, trade-off-driven decisions

### 14. To PRD
`skills/to-prd/SKILL.md`

Turns current conversation context and codebase understanding into a PRD, especially after requirements, implementation decisions, or product scope have already been discussed.

**Features:**
- Avoids re-interviewing for requirements already established in the conversation
- Sketches modules to build or modify, with attention to deep testable modules
- Requires checkpoints for module confirmation and test-module selection
- Uses a structured PRD template covering problem, solution, user stories, decisions, testing, scope, and notes
- Publishes only when required project setup and triage labels can be confirmed

### 15. Handoff
`skills/handoff/SKILL.md`

Creates a continuation document for a future agent or session, saved outside the repository in the OS temporary directory.

**Features:**
- Captures objective, current status, pending work, touched files, commands, risks, and constraints
- Tailors the handoff to the user's requested next-session focus
- Includes suggested skills for the next agent with reasons
- Returns the absolute saved path in a copyable code block
- Redacts secrets and avoids duplicating existing PRDs, plans, ADRs, issues, commits, or diffs

### 16. Caveman
`skills/caveman/SKILL.md`

Enables an ultra-concise communication mode for users who explicitly request shorter, token-efficient replies while preserving technical accuracy.

**Features:**
- Triggers on requests such as "caveman mode", "be brief", "less tokens", or Chinese equivalents
- Persists until the user asks to return to normal mode
- Keeps exact technical terms, code, paths, commands, and error messages intact
- Temporarily expands only when brevity could hide important warnings or multi-step clarity

## 📦 Installation

### Claude Code

1. `/plugin` → Add Marketplace
2. Type `HeathWang/hw-cc-plugin`
3. Install
4. Restart Claude Code

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/HeathWang/hw-cc-plugin/refs/heads/master/.codex/INSTALL.md
```

**Detailed docs:** [`.codex/INSTALL.md`](.codex/INSTALL.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📖 Documentation

For detailed skill-specific documentation, refer to the individual skill files in the `skills/` directory:

- `skills/git-commit-workflow/SKILL.md` - Git workflow details
- `skills/code-review-with-files/SKILL.md` - Code review methodology
- `skills/bug-analysis/SKILL.md` - Bug analysis framework
- `skills/linus-torvalds-review/SKILL.md` - Linus review protocol
- `skills/java-to-nextjs/SKILL.md` - TypeScript conversion rules
- `skills/java-to-swift/SKILL.md` - Swift conversion rules
- `skills/question-answer/SKILL.md` - Q&A workflow details
- `skills/ios-i18n-workflow/SKILL.md` - iOS internationalization workflow
- `skills/ios-i18n-workflow/scripts/README.md` - Helper scripts usage
- `skills/ios-i18n-workflow/references/naming-conventions.md` - Localization key naming conventions
- `skills/ios-i18n-workflow/references/advanced-usage.md` - CI/CD integration and automation
- `skills/improve-codebase-analytics/SKILL.md` - Architecture analytics report workflow
- `skills/fetch-yuque-doc/SKILL.md` - Yuque document fetching workflow
- `skills/fetch-yuque-doc/scripts/fetch_yuque_doc.py` - Yuque page extraction script
- `skills/fetch-yuque-doc/references/browser-notes.md` - Browser/profile assumptions and extraction notes
- `skills/diagnose/SKILL.md` - Hard-bug diagnosis workflow
- `skills/grill-me/SKILL.md` - Plan and design stress-testing workflow
- `skills/grill-with-docs/SKILL.md` - Domain-doc-aware plan stress-testing workflow
- `skills/to-prd/SKILL.md` - PRD creation and publishing workflow
- `skills/handoff/SKILL.md` - Session handoff workflow
- `skills/caveman/SKILL.md` - Concise communication mode

---

**Made with ❤️ for developers who care about code quality**
