---
name: fetch-yuque-doc
description: Use when Codex needs to fetch the content of a single Yuque page from a user-provided yuque.com link through a local logged-in Chrome-family browser, especially for private-space documents where token-based API access is unavailable or undesirable.
---

# Fetch Yuque Doc

## Overview

Fetch one Yuque document from a page URL through a local logged-in Chrome-family browser. On macOS, prefer the current running Chrome instance through AppleScript so enterprise SSO sessions can be reused directly; fall back to Playwright plus a copied browser profile when needed.

## Quick Start

Use `scripts/fetch_yuque_doc.py`.

```bash
python3 -m pip install --user playwright
python3 <skill_path>/scripts/fetch_yuque_doc.py \
  "https://hellobike.yuque.com/<group>/<repo>/<doc>"
```

JSON output:

```bash
python3 <skill_path>/scripts/fetch_yuque_doc.py \
  --format json \
  "https://hellobike.yuque.com/<group>/<repo>/<doc>"
```

## Workflow

1. Confirm the user gave a full Yuque document URL on `yuque.com` or `*.yuque.com`.
2. Ensure the local browser profile is already logged in to the target Yuque space.
3. Run the bundled script with the page URL once. The script performs URL validation, browser detection, and profile checks as part of the normal fetch path.
4. On macOS, keep the default `--strategy auto`: try the current Chrome instance through AppleScript first, then fall back to Playwright if needed.
5. Return the fetched title, page TOC, metadata, and body to the user.
6. If the request fails, surface the exact reason: bad URL, browser not found, profile not found, launch failure, or inaccessible page.

## URL Rules

The script expects links in this shape:

```text
https://<host>.yuque.com/<group_login>/<repo_slug>/<doc_slug>
```

It ignores query strings and fragments, but it does not try to crawl a directory, homepage, or knowledge-base root URL. This skill is intentionally scoped to a single page per invocation.

## Browser Rules

- Prefer the default local Chrome profile first.
- On macOS, prefer `--strategy auto` so the script can reuse the current Chrome session through AppleScript.
- Auto-detect Google Chrome, Chromium, and Microsoft Edge when possible.
- Allow overrides with `--browser-path`, `--user-data-dir`, and `--profile-directory`.
- Prefer the default profile-copy behavior to avoid live profile locks.

## Output Rules

- Default output is Markdown for direct reading in the terminal.
- Default to a single real fetch. Do not run `--dry-run` as part of the standard workflow.
- Use `--dry-run` only for debugging link parsing or browser/profile detection issues.
- Use `--format json` when the result will be piped into another tool or needs structured fields.
- JSON output includes `body_html`, which is useful when downstream tooling needs structure beyond plain text.

## Error Handling

- Browser detection error: no compatible browser installation or user data directory was found.
- Profile error: the selected profile directory does not exist.
- Browser launch error: Playwright is missing, or the browser profile could not be opened.
- Extraction error: the page loaded, but the document body could not be extracted.

## Resources

- Script: `scripts/fetch_yuque_doc.py`
- Reference: `references/browser-notes.md`

Read `references/browser-notes.md` only when you need the exact browser/profile assumptions or want to confirm the extraction strategy.

## Do Not Expand Scope

Do not turn this skill into a generic Yuque crawler, exporter, synchronization tool, or session-token extractor unless the user explicitly asks for that broader behavior in a separate task.
