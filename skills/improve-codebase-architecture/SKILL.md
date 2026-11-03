---
name: improve-codebase-architecture
description: Use when the user wants architectural deepening opportunities for a codebase or named files, shown as a visual HTML report, and when they then pick candidates from that report to implement in the code already reviewed.
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Language and Expression Rules

1. **Follow User / Context Language**:
   - Determine the output language from the user's request, recent conversation context, or project documentation (`CONTEXT.md`, `CLAUDE.md`, README, commit history). If the user only provides a slash command and file paths (e.g. `/improve-codebase-architecture path/to/File.swift`), infer the language from the conversation history, user rules, or codebase comments/docs (defaulting to Simplified Chinese when working in a Chinese user/project context).
   - **Both the HTML report and the chat conclusion MUST use that language** — including HTML `<html lang="...">`, `<title>`, section headers, legend, candidate titles, badges, diagram labels/annotations, Problem/Solution descriptions, benefits, Top Recommendation, and follow-up questions.
   - Keep code identifiers (class names, method names, file paths) in their original code form.

2. **Concise, Plain, and Easy to Understand (精炼通俗，直白易懂)**:
   - Write for human developers who want to grasp the problem in 5 seconds, not for an academic architecture textbook.
   - Replace obscure academic jargon with plain, concrete cause-and-effect language. For example, instead of *"split-brain state bounces across the engine seam via raw DTOs"*, write *"结果页的 6 个修改接口直接写在 VC 里，改完又塞回 Engine 刷新，状态两头跑"*.
   - State **what is messy right now**, **how to merge/simplify it**, and **what concrete benefit we get** (e.g., fewer places to touch, delete dead code, testable without UI).
   - Keep every sentence short and direct. No filler, no pompous phrasing.

This command is _informed_ by the project's domain model and built on a shared design mindset:

- Focus on core architecture concepts: **module (模块)**, **interface (接口/对外入口)**, **depth (深度：小接口封装复杂实现 vs 浅层透传)**, **seam (接缝/解耦点)**, **adapter (适配层)**, **leverage (杠杆率：一处实现多处复用)**, and **locality (内聚性/局部性：改动集中在同一处)**. Apply these principles directly: the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real". Express conclusions in natural, everyday developer language.
- The domain language in `CONTEXT.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card (all text in the user's context language) with:

- **Files**: which files/modules are involved
- **Problem (现状痛点)**: plain, everyday explanation of why the current code is painful to read, change, or test (1–2 short sentences)
- **Solution (优化方案)**: clear, down-to-earth description of how to consolidate or simplify it (1–2 short sentences)
- **Benefits (收益)**: concrete, easy-to-read bullets showing what gets deleted, where changes concentrate (locality), and how testing becomes simpler
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the current mess vs. the simplified structure (use the user's language for diagram annotations and explanations, keeping only real code symbols in code font)
- **Recommendation strength**: one of `Strong` (`强烈推荐`), `Worth exploring` (`值得探索`), `Speculative` (`可选尝试`), rendered as a badge

End the report with a **Top recommendation (优先改造建议)** section: which candidate you'd tackle first and why, explained in plain language.

**Use `CONTEXT.md` domain terms and keep architectural explanations natural.** Do not force awkward English glossary words into non-English reports. Explain module depth, interface size, and coupling in clear, idiomatic language that any developer on the team can immediately understand.

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose detailed code interfaces in the report. After the file is written, summarize the candidates briefly in the user's language (concise and plain) and ask which candidates to implement.

### 3. Implement the chosen candidates

When the user names one or more candidates — by number, title, or quoted report text — and asks to do, optimize, or land them, implement that selection in the codebase under review. This step has no other skill and no lookup step: the report and the code already read are the procedure. Several named candidates are one change when they touch the same state.

The spec is already in context:

- the HTML report's Problem, Solution, and Before / After for the chosen cards
- the files, methods, and call paths read during Explore
- the user's selection

Follow behavior the current code already shows, except where the chosen Solution explicitly changes it. User-visible copy, error codes, popup and toast ownership, paywall triggers, and refresh timing come from that code and the report. Put the deepened logic in the module the report named. Leave UI the report left in the view layer (popups, toasts, navigation, paywalls) there. Shape the new interface to match the module's existing types and call style. Do not design a second interface in parallel.

A fact you can read from code already opened is not a question. If the report's Solution and that code name the module, the methods to move, and what stays in the UI, edit now.

Stop and ask one question only when a behavior the candidate must change is neither stated in the report nor visible in the code you read. State the choice and a recommended default, then wait. Do not open a decision tree or a round of design questions before that.

While editing:

- **The deepened module needs a domain term `CONTEXT.md` does not already name?** Add that term. Create `CONTEXT.md` only in that case.
- **The edit makes a fuzzy term in `CONTEXT.md` precise?** Update that term in the same edit.
- **The user rejects a candidate for a reason a later review would need in order not to suggest it again?** Offer one ADR: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Skip "not worth it right now" and reasons that are obvious from the code.

After the edit, run the check the repo already uses for those files (its test target or compiler command). Do not add a new test harness as a side task. If the repo has no such check, say so. The moved logic must be callable without presenting UI.
