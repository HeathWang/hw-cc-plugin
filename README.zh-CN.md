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
- **📄 PRD 与交接**：将已讨论清楚的上下文整理成 PRD 或后续 Agent 可接手的交接文档
- **🧠 方案拷问**：结合代码、术语表、ADR 和既有文档对技术方案进行压力测试
- **🔗 语雀文档获取**：通过本地已登录浏览器会话获取单篇语雀文档
- **⚡ 沟通模式**：在用户明确要求时提供更短、更省 token 的技术回复

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

基于代码证据只读回答现有代码问题；若请求同时包含修改，则交由合适的变更工作流处理。

**能力：**

- 按需检查相关代码、配置、测试和依赖
- 明确区分已观察事实、推断和未知项
- 根据用户要求调整回答深度与格式
- 仅对纯解释和指导请求保持只读

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
- 在 `docs/Analytics/YYYY-MM-DD-architecture-<UpperCamelCaseTopic>.md` 生成报告
- 明确停止条件：不生成临时 HTML，不创建 GitHub Issue，不进入额外设计循环
- 可结合 `CONTEXT.md` 领域语言和 ADR 约束

### 10. Fetch Yuque Doc

`skills/fetch-yuque-doc/SKILL.md`

通过本地已登录的 Chrome 系浏览器，从用户提供的语雀页面链接获取单篇文档，适合无法或不希望使用 API Token 访问私有空间文档的场景。

**能力：**

- 校验单篇 `yuque.com` 或 `*.yuque.com` 文档 URL
- 复用本地 Chrome、Chromium 或 Edge 会话，并在 macOS 上优先使用 AppleScript
- 支持 Markdown 阅读输出和 JSON 结构化输出
- 明确报告 URL、浏览器、Profile、启动或正文提取相关错误
- 严格限定为单篇文档获取，不扩展为爬虫、导出器或同步工具

### 11. Diagnose

`skills/diagnose/SKILL.md`

面向疑难 Bug、间歇性故障、生产事故、客户反馈失败、崩溃、不明确回归，以及复现或修复信心不足的调试场景。

**能力：**

- 优先构建快速、确定性的通过/失败反馈循环
- 要求先复现并捕获准确症状，再进入根因分析
- 在打点或修复前生成多个可证伪的排序假设
- 指导定向调试探针、回归测试和原始场景验证
- 在宣布修复前完成清理和复盘检查

### 12. Grill Me

`skills/grill-me/SKILL.md`

对计划、设计、架构或技术方案进行压力测试，通过一次一个问题的方式逐步走完关键决策分支，直到形成共同理解。

**能力：**

- 用连续、聚焦的问题挑战方案
- 每个问题都给出推荐答案或默认立场，便于用户判断
- 当仓库证据能够回答问题时，优先探索代码而不是追问用户
- 在结束时总结已达成方向、剩余风险和未解决问题

### 13. Grill with Docs

`skills/grill-with-docs/SKILL.md`

结合项目领域语言、术语表、`CONTEXT.md`、ADR、既有决策、代码行为和易混淆术语，对方案进行文档感知的压力测试。

**能力：**

- 先有限扫描上下文文档、ADR 和明显的代码术语
- 发现方案用语与既有术语表冲突时立即指出
- 用具体场景澄清领域边界和边界条件
- 术语达成一致后即时更新 `CONTEXT.md`，无法编辑时说明应写入的具体内容
- 仅在难以回退、缺少上下文会令人困惑、且确实存在权衡时建议创建 ADR

### 14. To PRD

`skills/to-prd/SKILL.md`

基于当前对话上下文和代码库理解生成 PRD，适合需求、实现决策或产品范围已经讨论过的场景。

**能力：**

- 不重复追问对话中已经明确的需求
- 梳理需要新增或修改的模块，并关注可测试的深模块
- 要求确认模块范围和需要编写测试的模块
- 使用固定 PRD 模板覆盖问题、方案、用户故事、实现决策、测试决策、范围和补充说明
- 仅在项目配置和 triage label 可确认时发布到 issue tracker

### 15. Handoff

`skills/handoff/SKILL.md`

为后续 Agent 或下一轮会话生成交接文档，并保存到操作系统临时目录，而不是当前仓库。

**能力：**

- 记录目标、当前状态、待办、涉及文件、已运行命令、风险和约束
- 根据用户指定的下一轮重点调整交接内容
- 给出建议使用的 skills 及原因
- 使用便于复制的代码块返回文件绝对路径
- 脱敏敏感信息，并避免重复已有 PRD、计划、ADR、Issue、Commit 或 Diff

### 16. Caveman

`skills/caveman/SKILL.md`

在用户明确要求更短、更省 token 的回复时启用超简洁沟通模式，同时保留技术准确性。

**能力：**

- 支持 "caveman mode"、"be brief"、"less tokens"、"回答短点"、"少废话" 等触发方式
- 触发后持续生效，直到用户要求恢复普通模式
- 保留精确技术术语、代码、路径、命令和错误信息
- 当过度简短会隐藏重要警告或影响多步骤理解时，临时恢复完整说明

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
- `skills/fetch-yuque-doc/SKILL.md` - 语雀文档获取工作流
- `skills/fetch-yuque-doc/scripts/fetch_yuque_doc.py` - 语雀页面提取脚本
- `skills/fetch-yuque-doc/references/browser-notes.md` - 浏览器/Profile 假设与提取说明
- `skills/diagnose/SKILL.md` - 疑难 Bug 诊断工作流
- `skills/grill-me/SKILL.md` - 计划与设计压力测试工作流
- `skills/grill-with-docs/SKILL.md` - 结合领域文档的方案压力测试工作流
- `skills/to-prd/SKILL.md` - PRD 创建与发布工作流
- `skills/handoff/SKILL.md` - 会话交接工作流
- `skills/caveman/SKILL.md` - 简洁沟通模式

---

**为重视代码质量的开发者而作**
