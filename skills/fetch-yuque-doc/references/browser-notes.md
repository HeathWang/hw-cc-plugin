# Browser Notes

## Scope

This skill only handles one workflow: fetch one Yuque document from a user-provided page URL.

## URL shape

Expect a page URL in this form:

```text
https://<host>.yuque.com/<group_login>/<repo_slug>/<doc_slug>
```

Ignore query strings and fragments.

## Browser shape

- Prefer a local installed Chrome-family browser:
  - Google Chrome
  - Chromium
  - Microsoft Edge
- On macOS, prefer using the current running Google Chrome instance through AppleScript when enterprise login state does not survive profile copying.
- Prefer the browser's existing logged-in user data directory.
- Copy the selected profile to a temporary directory before launch to avoid profile locks.

## Playwright dependency

Install Playwright for Python:

```bash
python3 -m pip install --user playwright
```

Using an existing local Chrome executable means the skill does not need `playwright install` browser downloads.

## Extraction strategy

- Use `window.appData.doc` for title and metadata when available.
- Use `.ne-toc-content .ne-toc-item` for page outline items.
- Use `.ne-viewer-body` as the primary rendered-body selector.
- Fall back to `article#content` or `.article-content` when needed.

## Operational notes

- Standard usage is one real fetch command. The script already validates the URL, browser install, and profile before fetching.
- Reserve `--dry-run` for debugging environment problems; it is not part of the normal macOS `auto` flow.
- AppleScript requires Chrome setting `View -> Developer -> Allow JavaScript from Apple Events`.
- If the user insists on `--no-profile-copy`, they may need to close their browser first.
- On macOS, common default profile directory is `Default`.
- For corporate spaces such as `hellobike.yuque.com`, the script should still work as long as the URL points to a concrete document page and the local browser profile has access.
