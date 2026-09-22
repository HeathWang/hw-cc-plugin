---
name: reconstructing-ui-from-screenshots
description: Use when implementing or correcting an app or web UI from a design image, screenshot, mockup, or reference PNG where accurate size, spacing, color, typography, assets, and alignment matter.
---

# Reconstructing UI from Screenshots

## Core Principle

Measure the reference before coding. Establish the image-to-layout coordinate mapping independently from device DPR, complete the measurement checklist, and implement from recorded specifications rather than estimates.

## Final Response Contract

The final response contains the implementation summary and code-check results.

## Workflow

### 1. Inspect the Inputs

- Confirm reference dimensions, crop, intended logical viewport, font scale, theme, Safe Area, and system bars.
- Treat device DPR as independent metadata. Only record it when confirmed by the source device, capture metadata, or design specification; never infer it from image width.
- Inspect target code, tokens, components, and assets. Preserve matching structures.

### 2. Measure Before Editing

Use the explicit `python3` executable for every analyzer and dependency command. The script uses modern Python syntax, while `python` may resolve to Python 2 on macOS and fail with a `SyntaxError` at type annotations. `<skill_path>` is the directory that contains this `SKILL.md`.

```bash
python3 -m pip install -r <skill_path>/requirements.txt
python3 <skill_path>/scripts/analyze_ui_image.py reference.png \
  --viewport 375x812 \
  --json reference-report.json --annotated reference-boxes.png
```

Passing `--viewport` asserts that the image represents the full, uncropped viewport. For a crop, also pass its logical frame as `--reference-frame X,Y,WIDTH,HEIGHT`; this supplies the logical origin and dimensions represented by the image. Use `--dpr` only when DPR is independently confirmed.

Before editing, use `measurement_checklist` in the JSON report as the checklist template. For each applicable entry, record its value, source, and status in the working notes:

- coordinate system: reference size, target viewport, x/y scale, DPR source, crop or resampling
- system UI: Safe Area, bars, and app-content origin
- geometry and spacing: containers, major bounds, radii, margins, gaps, and alignment
- typography, colors, effects, and asset dimensions or alpha bounds

Inspect the image and focused crops. Sample solid regions, not anti-aliased or translucent edges. Treat detected boxes as candidates. Resolve ambiguous typography from design specifications or project sources.

### 3. Convert Measurements

- Convert positions with the reported frame origin: `logical_x = origin_x + image_x / scale_x` and `logical_y = origin_y + image_y / scale_y`. Convert sizes without an origin: `logical_width = image_width / scale_x` and `logical_height = image_height / scale_y`.
- `image_to_layout_scale` may represent attachment resizing, export scaling, or capture DPR. It is not device DPR unless independently confirmed.
- Do not copy pixel measurements into layout constants while coordinate mapping is `needs_confirmation` or `needs_review`. Confirm the viewport/crop first, or use only normalized proportions that do not assume logical units.
- Separate system UI, Safe Area, and app content measurements.
- Account for transparent asset padding and platform text metrics.

### 4. Implement by Visual Impact

Correct geometry, major sizes, assets, text baselines, spacing, then colors and shadows. Reuse project tokens and components. Change measured mismatches only; avoid unrelated refactoring.

### 5. Verify and Finish

- Check overflow, clipping, missing assets, and essential interactions.
- Run required formatting, lint or analysis, and the smallest relevant build.
- Do not automatically run a simulator, capture the implementation, or perform image-diff comparison solely for this workflow. The user performs final visual comparison unless they explicitly request agent-side visual verification.
- Report implementation changes and code-check results.

## Quick Check

- Reference dimensions, crop, and logical viewport confirmed
- Image-to-layout x/y scale recorded separately from DPR
- Coordinate mapping report status is `confirmed`
- Structured measurement checklist completed
- Asset dimensions and alpha bounds inspected
- Margins, bounds, spacing, colors, and text baselines measured
- Image pixels converted to logical units
- Existing tokens and components reused where appropriate

## Common Mistakes

| Mistake | Correction |
|---|---|
| Invoking the analyzer with `python` | Use explicit `python3` for both `pip` and the analyzer. |
| Choosing assets by filename | Preview candidates and alpha bounds. |
| Treating image scale as device DPR | Confirm viewport and DPR independently; attachment resizing can produce scales such as `1.2×`. |
| Treating a crop as a full viewport | Provide `--reference-frame` so the logical origin and represented bounds are explicit. |
| Copying screenshot pixels into layout | Require a `confirmed` coordinate mapping and convert with x/y scale. |
| Sampling colors from text edges | Sample inside a solid region. |
| Guessing font metrics from appearance | Check design specifications and project fonts. |

## Example

A `472×1024` attachment targets a `393×852` logical viewport. The analyzer reports approximately `scale_x = 1.201` and `scale_y = 1.202`, which indicates uniform image resampling but does not establish device DPR. Convert an `84px` vertical measurement with `scale_y` to about `70pt`, complete the checklist in the working notes, implement with project tokens, then run formatting and static analysis.
