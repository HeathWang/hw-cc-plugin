# hw-cc-plugin

Daily development skills and commands, primarily for frontend development, iOS, H5, and more.

## 📋 Overview

**hw-cc-plugin** is a comprehensive Claude Code plugin designed to streamline your daily development workflow. It provides a collection of powerful commands and skills for code conversion, review, bug analysis, and Git workflow automation.

## ✨ Features

- **🔄 Code Conversion**: Seamlessly convert Java classes to TypeScript (Next.js) or Swift (iOS) interfaces
- **🔍 Code Review**: Perform comprehensive code reviews with multi-dimensional analysis
- **🐛 Bug Analysis**: Systematic debugging and root cause analysis
- **💬 Expert Reviews**: Linus Torvalds-style code review protocol for quality assurance
- **📝 Git Automation**: Intelligent Git commit workflow with automatic message generation
- **❓ Q&A Workflow**: Comprehensive question and answer system for code guidance
- **🌍 iOS Internationalization**: Complete iOS localization workflow with SwiftGen L10n support and multi-language management

## 🚀 Skills

### iOS Internationalization Workflow
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

**Key Benefits:**
- Ensures all target languages are synchronized before code generation
- Prevents compilation errors from missing translations
- Automated verification reduces manual checking overhead
- Supports flexible baseline language configuration

## 🚀 Commands

### 1. Git Commit Workflow
`gitcommit.md`

Automates the Git commit process with intelligent file staging and Chinese commit message generation following Conventional Commits format.

**Features:**
- Smart file grouping by functionality
- Automatic commit message generation in Chinese
- Conventional Commits format with emojis
- Markdown-formatted change details

### 2. Code Review with Files
`code-review-with-files.md`

Performs comprehensive code reviews across multiple dimensions including correctness, performance, security, edge cases, and code quality.

**Features:**
- Multi-dimensional analysis (7+ review dimensions)
- Severity-based issue classification (Critical, High, Medium, Low)
- Detailed feedback with locations and solutions
- All outputs in Simplified Chinese

### 3. Bug Analysis
`bug-analysis.md`

Provides systematic bug analysis and code issue diagnosis with automatic file location and comprehensive root cause analysis.

**Features:**
- Technology stack detection (iOS, React, Python, Java Spring)
- 4 levels of investigation depth
- Proactive file discovery
- Detailed analysis output with testing plans

### 4. Linus Torvalds Code Review
`linus-torvalds-code-review.md`

Emulates Linus Torvalds' unique code review philosophy focusing on good taste, pragmatism, and simplicity.

**Features:**
- Context-aware review protocols
- Multi-dimensional analysis (data structures, special cases, complexity, breaking changes)
- Direct, sharp feedback style
- All communications in Chinese

### 5. Java to Next.js TypeScript Conversion
`Java-to-Nextjs-Conversion.md`

Converts Java 1.8 classes to Next.js TypeScript interface definitions with precise type mapping and nullability handling.

**Features:**
- Java 1.8 → TypeScript 5.0+ conversion
- Special annotation handling (@BigDecimalToNumber, @TimestampFormat)
- Inheritance handling (extension vs flattening)
- Property names preserved to match API contracts

### 6. Java to Swift Conversion
`java-to-swift-conversion.md`

Converts Java 1.8 classes to Swift 5.0+ struct objects with Codable conformance.

**Features:**
- Java 1.8 → Swift 5.0+ conversion
- Special annotation handling (@BigDecimalToString)
- Flattened inheritance structure
- Codable protocol conformance

### 7. Question & Answer
`question-answer.md`

Provides comprehensive Q&A workflow with full read access to project files and detailed technical guidance.

**Features:**
- Read-only file access for code analysis
- Systematic problem-solving approach
- Structured response format
- Educational and advisory focus

## 📦 Installation

### Requirements
- Claude Code environment
- No additional dependencies required

### Setup
1. `/plugin` -> Add Marketplace
2. type `HeathWang/hw-cc-plugin`
3. Install
4. restart claude code

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📖 Documentation

### Skills Documentation
For detailed skill-specific documentation, please refer to the individual skill files in the `skills/` directory:
- `skills/ios-i18n-workflow/SKILL.md` - iOS internationalization workflow
- `skills/ios-i18n-workflow/scripts/README.md` - Helper scripts usage
- `skills/ios-i18n-workflow/references/naming-conventions.md` - Localization key naming conventions
- `skills/ios-i18n-workflow/references/advanced-usage.md` - CI/CD integration and automation

### Commands Documentation
For detailed command-specific documentation, please refer to the individual command files in the `commands/` directory:
- `commands/gitcommit.md` - Git workflow details
- `commands/code-review-with-files.md` - Code review methodology
- `commands/bug-analysis.md` - Bug analysis framework
- `commands/linus-torvalds-code-review.md` - Linus review protocol
- `commands/Java-to-Nextjs-Conversion.md` - Type conversion rules
- `commands/java-to-swift-conversion.md` - Swift conversion rules
- `commands/question-answer.md` - Q&A workflow details

## 🎉 Acknowledgments

Built to enhance daily development workflows and improve code quality across multiple platforms and technologies.

---

**Made with ❤️ for developers who care about code quality**