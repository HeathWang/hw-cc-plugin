# hw-cc-plugin

**语言：** [English](README.md) | 简体中文

面向日常开发的 Claude Code 插件，主要覆盖前端、iOS、H5 以及常见工程协作流程。

## 📋 概览

**hw-cc-plugin** 是一个用于提升日常研发效率的 Claude Code 插件，内置多种可复用的 Skills 和 Commands，覆盖代码转换、代码审查、Bug 分析、Git 提交自动化、iOS 国际化与架构分析等场景。

## ✨ 功能特性

- **🔄 代码转换**：将 Java 类转换为 TypeScript（Next.js）接口或 Swift（iOS）结构体
- **🔍 代码审查**：从正确性、性能、安全性、边界条件等维度进行综合 Review
- **🐛 Bug 分析**：提供系统化调试流程与根因分析
- **💬 专家视角 Review**：支持 Linus Torvalds 风格的高标准代码审查
- **📝 Git 自动化**：智能生成中文提交信息并辅助完成 Git 提交流程
- **❓ 问答工作流**：基于项目文件进行技术问题分析和指导
- **🌍 iOS 国际化**：支持 SwiftGen L10n 的完整多语言管理流程
- **🏗️ 架构分析**：在 `docs/Analytics/` 下生成可持久保存的架构分析报告

## 🚀 Skills

### 1. Git Commit Workflow

`skills/git-commit-workflow/SKILL.md`

自动化 Git 提交流程，支持智能文件分组，并按 Conventional Commits 格式生成中文提交信息。

**能力：**

- 按功能智能分组文件
- 自动生成中文提交信息
- 遵循 Conventional Commits 格式并支持 emoji
- 持续处理直到工作区清理完成

### 2. Code Review with Files

`skills/code-review-with-files/SKILL.md`

针对指定文件或变更进行多维度代码审查，覆盖正确性、性能、安全性、边界条件和代码质量。

**能力：**

- 支持 7+ 个审查维度
- 按严重程度分类问题（Critical、High、Medium、Low）
- 提供带文件位置和修复建议的详细反馈
- 输出使用简体中文

### 3. Bug Analysis

`skills/bug-analysis/SKILL.md`

用于系统化分析 Bug、崩溃或异常行为，并定位相关文件、推导根因和给出修复建议。

**能力：**

- 自动识别技术栈（iOS、React、Python、Java Spring）
- 支持多层级调查深度
- 主动发现相关文件
- 输出包含分析结论和测试计划

### 4. Linus Torvalds Code Review

`skills/linus-torvalds-review/SKILL.md`

模拟 Linus Torvalds 的代码审查哲学，强调 good taste、实用主义、简单性和对复杂度的严格控制。

**能力：**

- 基于上下文选择 Review 协议
- 从数据结构、特殊情况、复杂度和破坏性变更等角度分析
- 反馈直接、尖锐、聚焦工程质量
- 使用用户当前语言进行回复

### 5. Java to Next.js TypeScript Conversion

`skills/java-to-nextjs/SKILL.md`

将 Java 1.8 类转换为 Next.js TypeScript interface 定义，并处理类型映射、可空性和继承关系。

**能力：**

- Java 1.8 到 TypeScript 5.0+ 类型转换
- 支持 `@BigDecimalToNumber`、`@TimestampFormat` 等特殊注解
- 处理继承结构（extends 或 flatten）
- 保留属性命名以匹配 API 契约
- 仅输出 Markdown 代码块，不修改项目文件

### 6. Java to Swift Conversion

`skills/java-to-swift/SKILL.md`

将 Java 1.8 类转换为 Swift 5.0+ 的 Codable struct。

**能力：**

- Java 1.8 到 Swift 5.0+ 类型转换
- 支持 `@BigDecimalToString` 等特殊注解
- 扁平化继承结构
- 自动生成 Codable 协议支持
- 仅输出 Markdown 代码块，不修改项目文件

### 7. Question & Answer

`skills/question-answer/SKILL.md`

用于读取和分析项目文件，回答代码行为、架构设计或工程实践相关问题。

**能力：**

- 以只读方式分析项目文件
- 使用系统化问题解决流程
- 提供结构化技术回答
- 侧重解释、建议和知识传递

### 8. iOS Internationalization Workflow

`skills/ios-i18n-workflow/SKILL.md`

面向使用 SwiftGen L10n 的 iOS 项目，提供完整国际化工作流，支持多语言翻译管理、校验和清理。

**能力：**

- 从硬编码字符串到 L10n 引用的完整国际化流程
- 校验多语言翻译是否完整
- 清理未使用的本地化条目，并支持 dry-run 安全检查
- 管理任意数量的目标语言
- 提供检查缺失翻译和清理无用条目的辅助脚本

### 9. Improve Codebase Analytics

`skills/improve-codebase-analytics/SKILL.md`

分析代码库架构，关注模块深度、局部性、杠杆点、接口边界、适配层和可测试性，并生成持久化 Markdown 报告。

**能力：**

- 使用统一模块和接口词汇进行架构深化分析
- 在 `docs/Analytics/YYYY-MM-DD-architecture-analysis.md` 生成报告
- 明确停止条件：不生成临时 HTML，不创建 GitHub Issue，不进入额外设计循环
- 可结合 `CONTEXT.md` 领域语言和 ADR 约束

## 📦 安装

### Claude Code

1. 打开 `/plugin` → Add Marketplace
2. 输入 `HeathWang/hw-cc-plugin`
3. 安装插件
4. 重启 Claude Code

### Codex

告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/HeathWang/hw-cc-plugin/refs/heads/master/.codex/INSTALL.md
```

**详细文档：** [`.codex/INSTALL.md`](.codex/INSTALL.md)

## 🤝 贡献

欢迎提交 Pull Request，一起完善日常研发工作流。

## 📄 License

本项目基于 MIT License 开源，详见 [LICENSE](LICENSE)。

## 📖 文档

更详细的 Skill 文档请查看 `skills/` 目录下的具体文件：

- `skills/git-commit-workflow/SKILL.md` - Git 工作流说明
- `skills/code-review-with-files/SKILL.md` - 代码审查方法论
- `skills/bug-analysis/SKILL.md` - Bug 分析框架
- `skills/linus-torvalds-review/SKILL.md` - Linus Review 协议
- `skills/java-to-nextjs/SKILL.md` - TypeScript 转换规则
- `skills/java-to-swift/SKILL.md` - Swift 转换规则
- `skills/question-answer/SKILL.md` - 问答工作流说明
- `skills/ios-i18n-workflow/SKILL.md` - iOS 国际化工作流
- `skills/ios-i18n-workflow/scripts/README.md` - 辅助脚本使用说明
- `skills/ios-i18n-workflow/references/naming-conventions.md` - 本地化 Key 命名规范
- `skills/ios-i18n-workflow/references/advanced-usage.md` - CI/CD 集成与自动化
- `skills/improve-codebase-analytics/SKILL.md` - 架构分析报告工作流

---

**为重视代码质量的开发者而作**
