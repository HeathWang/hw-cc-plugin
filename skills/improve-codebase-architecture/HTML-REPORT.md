# HTML Report Format

The architectural review is rendered as a single self-contained HTML file in the OS temp directory. Tailwind and Mermaid both come from CDNs. Mermaid handles graph-shaped diagrams reliably; hand-built divs and inline SVG handle the more editorial visuals (mass diagrams, cross-sections). Mix the two: don't lean on Mermaid for everything, it'll start to look generic.

## Scaffold

Set `<html lang="...">` and all visible UI labels, headings, legends, badges, diagram notes, and prose to match the user's context language (e.g., Simplified Chinese `zh-CN` when the user or project context is Chinese). Keep only actual code identifiers and file paths in English/code form.

```html
<!doctype html>
<html lang="{{lang}}">
  <head>
    <meta charset="utf-8" />
    <title>{{localized title, e.g. 架构优化报告：repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend (localized to the user's language, e.g. 实线框 = 模块, 虚线 = 解耦边界, 红线 = 职责越界/耦合泄漏, 深色粗框 = 收拢后的深模块; or in English: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module). No introduction paragraph. Straight into the candidates.

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and written in the user's language using everyday developer expressions rather than obscure academic jargon.

Each candidate is one `<article>`:

- **Title**: short, action-oriented, in the user's language (e.g. "1. 将结果页的 6 个修改接口收拢进 `CalorieRecognitionFlowEngine`" or "Collapse the Order intake pipeline").
- **Badge row**: recommendation strength (`强烈推荐` / `Strong` = emerald, `值得探索` / `Worth exploring` = amber, `可选尝试` / `Speculative` = slate), plus a short tag for the dependency approach (e.g. `进程内收拢` / `in-process`, `本地可替换` / `local-substitutable`, `接口适配解耦` / `ports & adapters`, `Mock 隔离` / `mock`).
- **Files**: monospaced list, `font-mono text-sm`.
- **Before / After diagram**: the centrepiece. Two columns, side by side (`改造前` / `Before` vs `改造后` / `After`). Annotations inside the diagram must also use the user's language so the visual is immediately understandable at a glance. See patterns below.
- **Problem (`现状痛点` / `Problem`)**: 1–2 short, plain sentences. What hurts in practice.
- **Solution (`优化方案` / `Solution`)**: 1–2 short, plain sentences. How to merge or simplify it.
- **Wins**: short bullets in plain language. e.g. "删掉 4 个空 Delegate 方法", "状态收拢到一处，不再跨 VC 来回刷", "脱离 UIKit 即可直接跑单测".
- **ADR callout** (if applicable): one line in an amber-tinted box.

No long paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same. Variety is part of the point.

### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a Tailwind-styled card so it doesn't feel parachuted in. Style with classDef to colour leakage edges red and the deep module dark. Sequence diagrams work well for "before: 6 round-trips; after: 1."

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals, since Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module: one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. Serif optional for headings (`font-serif` works well with stone/slate).
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams, so they read as schematic, not as UI.
- The only scripts are the Tailwind CDN and the Mermaid ESM import. The report is otherwise static: no app code, no interactivity beyond Mermaid's own rendering.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Language and Tone

1. **Match the user's context language throughout the entire HTML file**:
   - Do not output an English HTML report when the user or project context is in Chinese (or another language).
   - Translate all UI chrome, legend items, section headings, `改造前 / 改造后` headers, diagram callouts, Problem/Solution labels, and bullet points into the user's language. Keep only actual code identifiers (`CameraVC`, `confirmAiRecord()`, file paths) in their original code form.

2. **Concise, plain, and developer-friendly (精炼通俗，能一眼看懂)**:
   - Avoid literal translations of academic terms or stiff jargon (do not write convoluted phrases like *"通过端口与适配器在接缝处深化模块以消除分裂脑状态反弹"*).
   - Speak plainly about what the code actually does: **"哪里散了、哪里重复了、怎么收拢、改完有什么好处"**.
   - Good Chinese examples:
     - 痛点：`CalorieRecognitionLoadingVC` 塞了 1396 行代码，结果页的 6 个修改请求直接写在 VC 里，改完还要手动把数据塞回 `FlowEngine`，状态两头维护。
     - 方案：把结果页的增删改、餐次状态和菜品校验统一收进 `FlowEngine`，VC 只负责展示和发操作事件。
     - 收益：`VC 瘦身只管 UI` · `删掉跨层回刷数据的胶水方法` · `核心流程不依赖 UIKit 即可直接单测`。
   - Good English examples:
     - "Order intake module is too thin: callers still have to wire validation and pricing themselves."
     - "Pull validation and pricing inside one module so callers and tests only call one entry point."

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it.
