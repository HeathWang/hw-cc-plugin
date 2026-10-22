---
name: reconstructing-ui-from-screenshots
description: Use when implementing or correcting an app or web UI from a design image, screenshot, mockup, or reference PNG where accurate size, spacing, color, typography, assets, and alignment matter.
---

# Reconstructing UI from Screenshots

## Overview

Choose the shortest evidence path that can produce a correct edit. Measure only values that affect the implementation.

## Workflow

### 1. Define the Change

Inspect the reference, target view, and direct dependencies. Record the changed region, unchanged anchors, and material unknowns.

Use the fast path for one component or section in an existing screen. Use the mapping path for a new/full screen, coupled regions, unknown crop origin, or absolute screenshot coordinates.

### 2A. Fast Path — Local Change

Reuse existing constraints, tokens, components, fonts, and assets. Record three to five inputs: container bounds, inset or gap, alignment, text style, color, or asset behavior.

Global viewport and DPR are unnecessary when values come from existing anchors, tokens, or relative relationships. Once these inputs distinguish the implementation, edit immediately. Use the nearest project value for low-impact ambiguity.

Do not run the analyzer merely to satisfy the workflow.

### 2B. Mapping Path — Full Reconstruction

Resolve viewport from runtime/project configuration, design specifications, or capture metadata. Image dimensions alone never prove viewport or DPR.

Run at most one analyzer command before the first edit:

```bash
python3 <skill_path>/scripts/analyze_ui_image.py reference.png \
  --viewport 375x812 \
  --json reference-report.json --annotated reference-boxes.png
```

Run `--help` for crops and ROI. Install dependencies only after `ModuleNotFoundError`. Confirmed mapping leads directly to recording major geometry and editing; blocked mapping leads to one focused question. Never replace an inaccurate result with chained ad-hoc Python scans.

### 3. Implement the First Pass

Correct geometry and assets first, then text, spacing, colors, and effects. Preserve unaffected behavior. Reconsider a settled value only when new evidence contradicts it.

### 4. Precision Pass

For each visible, code-relevant mismatch, make one targeted measurement or focused `--roi` run, then edit. Do not rescan anti-aliasing noise or infer fonts from text pixels; use project definitions.

Stop when no high-impact visible mismatch remains. Do not complete unrelated checklist entries.

### 5. Verify

Check overflow, clipping, missing assets, and essential interactions. Run formatting, static analysis, and the smallest relevant build. Use image diff only when requested or already available.

## Analysis Budget

| Situation | Evidence before first edit | Analyzer budget |
|---|---|---|
| Existing local component | 3–5 relevant inputs | None by default |
| New or full-screen layout | Mapping plus major regions | One run |
| Visible mismatch after implementation | One decision-specific measurement | One focused run |

Analyzer regions and shapes are candidates, not ground truth. Sample solid interiors, not anti-aliased edges. Device DPR remains unconfirmed unless independently sourced. Require confirmed mapping only before converting absolute image pixels to logical layout constants.

## Common Mistakes

- Proving viewport, Safe Area, or system bars for a local component replacement.
- Writing temporary pixel-scanning scripts instead of making the edit.
- Measuring the same value repeatedly without contradictory evidence.
- Treating image scale as DPR or detector candidates as final semantics.

## Output

Report implementation changes, material assumptions, and code-check results.
