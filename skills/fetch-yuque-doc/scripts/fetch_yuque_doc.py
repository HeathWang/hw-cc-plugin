#!/usr/bin/env python3
"""Fetch structured Yuque document content through a local logged-in browser."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import parse


IGNORE_NAMES = {
    "Cache",
    "Code Cache",
    "GPUCache",
    "Crashpad",
    "GrShaderCache",
    "GraphiteDawnCache",
    "DawnCache",
    "ShaderCache",
    "Blob Storage",
}


class FetchError(Exception):
    """Base class for expected fetch errors."""


class InvalidYuqueUrlError(FetchError):
    """Raised when the provided Yuque URL cannot be parsed."""


class BrowserDetectionError(FetchError):
    """Raised when a compatible browser setup cannot be detected."""


class BrowserLaunchError(FetchError):
    """Raised when the browser cannot be started."""


class AppleScriptUnavailableError(FetchError):
    """Raised when Chrome AppleScript automation is unavailable."""


@dataclass(frozen=True)
class BrowserInstallation:
    name: str
    executable_path: Path
    user_data_dir: Path


@dataclass(frozen=True)
class YuqueDocRef:
    host: str
    group_login: str
    repo_slug: str
    doc_slug: str
    original_url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a Yuque document via a local logged-in browser profile."
    )
    parser.add_argument("url", help="Yuque page URL, e.g. https://hellobike.yuque.com/group/repo/doc")
    parser.add_argument(
        "--strategy",
        choices=("auto", "applescript", "playwright"),
        default="auto",
        help="Fetch strategy. Default: auto (on macOS, try the live Chrome session first, then fall back to Playwright)",
    )
    parser.add_argument(
        "--browser",
        choices=("auto", "chrome", "chromium", "edge"),
        default="auto",
        help="Browser family to use. Default: auto",
    )
    parser.add_argument("--browser-path", help="Explicit browser executable path.")
    parser.add_argument(
        "--user-data-dir",
        help="Browser user data root. Default: auto-detect common Chrome/Chromium/Edge locations.",
    )
    parser.add_argument(
        "--profile-directory",
        default="Default",
        help="Browser profile directory inside the user data root. Default: Default",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Default: markdown",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Navigation timeout in seconds. Default: 60",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Show the browser window instead of running headless.",
    )
    parser.add_argument(
        "--no-profile-copy",
        action="store_true",
        help="Use the original browser profile directly. This may fail if the browser is already running.",
    )
    parser.add_argument(
        "--keep-profile-copy",
        action="store_true",
        help="Keep the temporary copied profile on disk for debugging.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Debug only: resolve URL and browser/profile paths without launching the browser.",
    )
    return parser.parse_args()


def print_error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)


def parse_yuque_url(url: str) -> YuqueDocRef:
    parsed = parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise InvalidYuqueUrlError("语雀链接必须以 http:// 或 https:// 开头。")
    host = parsed.netloc.lower()
    if host not in {"yuque.com", "www.yuque.com"} and not host.endswith(".yuque.com"):
        raise InvalidYuqueUrlError("只支持 yuque.com 或 *.yuque.com 的语雀文档链接。")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 3:
        raise InvalidYuqueUrlError(
            "链接路径不足，期望格式类似 https://<host>/<group>/<repo>/<doc>。"
        )

    return YuqueDocRef(
        host=host,
        group_login=parts[0],
        repo_slug=parts[1],
        doc_slug=parts[2],
        original_url=url,
    )


def detect_browser_installation(browser: str) -> BrowserInstallation:
    system = platform.system()
    home = Path.home()
    local_appdata = Path(os.environ.get("LOCALAPPDATA", "")) if os.environ.get("LOCALAPPDATA") else None
    program_files = [Path(p) for p in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)")) if p]

    candidates: dict[str, list[tuple[Path | None, Path | None]]] = {
        "chrome": [],
        "chromium": [],
        "edge": [],
    }

    if system == "Darwin":
        candidates["chrome"] = [
            (
                Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                home / "Library/Application Support/Google/Chrome",
            )
        ]
        candidates["chromium"] = [
            (
                Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
                home / "Library/Application Support/Chromium",
            )
        ]
        candidates["edge"] = [
            (
                Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
                home / "Library/Application Support/Microsoft Edge",
            )
        ]
    elif system == "Linux":
        candidates["chrome"] = [
            (
                _which_path("google-chrome") or _which_path("google-chrome-stable"),
                home / ".config/google-chrome",
            )
        ]
        candidates["chromium"] = [
            (
                _which_path("chromium") or _which_path("chromium-browser"),
                home / ".config/chromium",
            )
        ]
        candidates["edge"] = [
            (_which_path("microsoft-edge") or _which_path("microsoft-edge-stable"), home / ".config/microsoft-edge")
        ]
    elif system == "Windows":
        candidates["chrome"] = [
            (
                _first_existing_path(
                    *(pf / "Google/Chrome/Application/chrome.exe" for pf in program_files),
                ),
                local_appdata / "Google/Chrome/User Data" if local_appdata else None,
            )
        ]
        candidates["chromium"] = [
            (
                _first_existing_path(
                    *(pf / "Chromium/Application/chrome.exe" for pf in program_files),
                ),
                local_appdata / "Chromium/User Data" if local_appdata else None,
            )
        ]
        candidates["edge"] = [
            (
                _first_existing_path(
                    *(pf / "Microsoft/Edge/Application/msedge.exe" for pf in program_files),
                ),
                local_appdata / "Microsoft/Edge/User Data" if local_appdata else None,
            )
        ]
    else:
        raise BrowserDetectionError(f"暂不支持当前系统: {system}")

    order = [browser] if browser != "auto" else ["chrome", "chromium", "edge"]
    for name in order:
        for executable_path, user_data_dir in candidates.get(name, []):
            if executable_path and executable_path.exists() and user_data_dir and user_data_dir.exists():
                return BrowserInstallation(name=name, executable_path=executable_path, user_data_dir=user_data_dir)

    raise BrowserDetectionError(
        "未能自动探测到可用的 Chrome/Chromium/Edge。请用 --browser-path 和 --user-data-dir 显式指定。"
    )


def _which_path(command: str) -> Path | None:
    result = shutil.which(command)
    return Path(result) if result else None


def _first_existing_path(*paths: Path) -> Path | None:
    for path in paths:
        if path and path.exists():
            return path
    return None


def resolve_browser(args: argparse.Namespace) -> BrowserInstallation:
    if args.browser_path and args.user_data_dir:
        executable_path = Path(args.browser_path).expanduser()
        user_data_dir = Path(args.user_data_dir).expanduser()
        if not executable_path.exists():
            raise BrowserDetectionError(f"浏览器可执行文件不存在: {executable_path}")
        if not user_data_dir.exists():
            raise BrowserDetectionError(f"浏览器用户目录不存在: {user_data_dir}")
        browser_name = args.browser if args.browser != "auto" else "custom"
        return BrowserInstallation(name=browser_name, executable_path=executable_path, user_data_dir=user_data_dir)

    detected = detect_browser_installation(args.browser)
    if args.browser_path:
        executable_path = Path(args.browser_path).expanduser()
        if not executable_path.exists():
            raise BrowserDetectionError(f"浏览器可执行文件不存在: {executable_path}")
        return BrowserInstallation(name=detected.name, executable_path=executable_path, user_data_dir=detected.user_data_dir)
    if args.user_data_dir:
        user_data_dir = Path(args.user_data_dir).expanduser()
        if not user_data_dir.exists():
            raise BrowserDetectionError(f"浏览器用户目录不存在: {user_data_dir}")
        return BrowserInstallation(name=detected.name, executable_path=detected.executable_path, user_data_dir=user_data_dir)
    return detected


def ensure_profile_exists(user_data_dir: Path, profile_directory: str) -> Path:
    profile_path = user_data_dir / profile_directory
    if not profile_path.exists():
        raise BrowserDetectionError(
            f"浏览器 profile 不存在: {profile_path}。请确认 --profile-directory 是否正确。"
        )
    return profile_path


def create_profile_copy(user_data_dir: Path, profile_directory: str, keep_copy: bool) -> tuple[Path, callable[[], None]]:
    profile_path = ensure_profile_exists(user_data_dir, profile_directory)
    temp_root = Path(tempfile.mkdtemp(prefix="fetch-yuque-doc-"))

    local_state = user_data_dir / "Local State"
    if local_state.exists():
        shutil.copy2(local_state, temp_root / "Local State")
    for optional_name in ("First Run", "Last Version"):
        optional_path = user_data_dir / optional_name
        if optional_path.exists():
            shutil.copy2(optional_path, temp_root / optional_name)

    shutil.copytree(
        profile_path,
        temp_root / profile_directory,
        ignore=shutil.ignore_patterns(*IGNORE_NAMES),
        dirs_exist_ok=True,
    )

    def cleanup() -> None:
        if not keep_copy:
            shutil.rmtree(temp_root, ignore_errors=True)

    return temp_root, cleanup


def import_playwright() -> Any:
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise BrowserLaunchError(
            "缺少 playwright 依赖。请先运行 `python3 -m pip install --user playwright`。"
        ) from exc
    return sync_playwright, PlaywrightError, PlaywrightTimeoutError


def run_osascript(script: str) -> str:
    try:
        result = subprocess.run(
            ["osascript", "-"],
            input=script,
            text=True,
            capture_output=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise AppleScriptUnavailableError("当前系统不支持 osascript。") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise AppleScriptUnavailableError(stderr or "执行 osascript 失败。") from exc
    return result.stdout.strip()


def fetch_via_applescript(doc_ref: YuqueDocRef, timeout_seconds: int) -> dict[str, Any]:
    if platform.system() != "Darwin":
        raise AppleScriptUnavailableError("AppleScript 只支持 macOS。")

    open_script = f'''
tell application "Google Chrome"
  if (count of windows) = 0 then
    make new window
  end if
  tell front window
    make new tab with properties {{URL:"{doc_ref.original_url}"}}
    set active tab index to (count of tabs)
  end tell
end tell
'''
    run_osascript(open_script)

    js = r"""(() => {
const viewerBody = document.querySelector('.ne-viewer-body');
const article = document.querySelector('article#content, .article-content, .ne-viewer');
const toc = Array.from(document.querySelectorAll('.ne-toc-content .ne-toc-item')).map(item => {
  const a = item.querySelector('a');
  const className = item.className || '';
  const match = className.match(/ne-toc-depth-(\d+)/);
  return {
    text: (a?.textContent || item.textContent || '').trim(),
    href: a?.getAttribute('href') || null,
    depth: match ? Number(match[1]) : null,
  };
}).filter(item => item.text);
const appData = window.appData || {};
const doc = appData.doc || {};
const book = appData.book || {};
const bodyText = (viewerBody?.innerText || article?.innerText || '').trim();
return JSON.stringify({
  final_url: location.href,
  page_title: document.title,
  title: doc.title || document.querySelector('.doc-article-title')?.textContent?.trim() || document.title,
  description: doc.description || null,
  page_toc: toc,
  body_text: bodyText,
  body_html: viewerBody?.innerHTML || article?.innerHTML || '',
  login_required: location.href.includes('/login'),
  metadata: {
    host: location.host,
    group_title: appData.group?.name || null,
    group_login: appData.group?.login || null,
    book_name: book.name || null,
    book_slug: book.slug || null,
    book_toc_count: Array.isArray(book.toc) ? book.toc.length : 0,
    doc_id: doc.id || null,
    doc_slug: doc.slug || null,
    doc_format: doc.format || null,
    created_at: doc.created_at || null,
    updated_at: doc.updated_at || null,
    word_count: doc.word_count || null,
    public: doc.public ?? null,
  },
});
})()"""

    poll_script = f'''
tell application "Google Chrome"
  if (count of windows) = 0 then error "Google Chrome 没有打开窗口。"
  tell active tab of front window
    return execute javascript {json.dumps(js)}
  end tell
end tell
'''

    deadline = time.time() + timeout_seconds
    last_payload: dict[str, Any] | None = None
    while time.time() < deadline:
        raw = run_osascript(poll_script)
        if raw:
            payload = json.loads(raw)
            last_payload = payload
            if payload.get("login_required"):
                raise AppleScriptUnavailableError("当前 Chrome 标签页被重定向到了登录页。")
            if (payload.get("body_text") or "").strip():
                payload.update(
                    {
                        "source_url": doc_ref.original_url,
                        "requested_host": doc_ref.host,
                        "requested_group_login": doc_ref.group_login,
                        "requested_repo_slug": doc_ref.repo_slug,
                        "requested_doc_slug": doc_ref.doc_slug,
                        "browser": {
                            "name": "chrome-live",
                            "executable_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                            "user_data_dir": None,
                            "profile_directory": "live-session",
                        },
                    }
                )
                return payload
        time.sleep(1)

    if last_payload and last_payload.get("login_required"):
        raise AppleScriptUnavailableError("当前 Chrome 标签页被重定向到了登录页。")
    raise AppleScriptUnavailableError("AppleScript 路径未在超时时间内拿到正文。")


def fetch_document(
    doc_ref: YuqueDocRef,
    browser_installation: BrowserInstallation,
    profile_directory: str,
    timeout_seconds: int,
    headful: bool,
    no_profile_copy: bool,
    keep_profile_copy: bool,
) -> dict[str, Any]:
    sync_playwright, PlaywrightError, PlaywrightTimeoutError = import_playwright()
    profile_cleanup = lambda: None
    launch_user_data_dir = browser_installation.user_data_dir

    if no_profile_copy:
        ensure_profile_exists(launch_user_data_dir, profile_directory)
    else:
        launch_user_data_dir, profile_cleanup = create_profile_copy(
            browser_installation.user_data_dir, profile_directory, keep_profile_copy
        )

    try:
        with sync_playwright() as playwright:
            browser_type = playwright.chromium
            try:
                context = browser_type.launch_persistent_context(
                    user_data_dir=str(launch_user_data_dir),
                    executable_path=str(browser_installation.executable_path),
                    headless=not headful,
                    args=[f"--profile-directory={profile_directory}"],
                )
            except PlaywrightError as exc:
                raise BrowserLaunchError(
                    f"启动浏览器失败: {exc}. 如果你在直接使用原 profile，请先关闭浏览器或去掉 --no-profile-copy。"
                ) from exc

            try:
                page = context.new_page()
                page.goto(doc_ref.original_url, wait_until="domcontentloaded", timeout=timeout_seconds * 1000)
                try:
                    page.locator(".ne-viewer, article#content, .article-content").first.wait_for(
                        state="visible",
                        timeout=min(timeout_seconds * 1000, 15000),
                    )
                except PlaywrightTimeoutError:
                    pass
                page.wait_for_timeout(3000)
                return extract_structured_content(page, doc_ref, browser_installation, profile_directory)
            finally:
                context.close()
    finally:
        profile_cleanup()


def fetch_document_auto(
    doc_ref: YuqueDocRef,
    browser_installation: BrowserInstallation,
    strategy: str,
    profile_directory: str,
    timeout_seconds: int,
    headful: bool,
    no_profile_copy: bool,
    keep_profile_copy: bool,
) -> dict[str, Any]:
    if strategy in {"auto", "applescript"}:
        try:
            return fetch_via_applescript(doc_ref, timeout_seconds)
        except AppleScriptUnavailableError:
            if strategy == "applescript":
                raise

    return fetch_document(
        doc_ref=doc_ref,
        browser_installation=browser_installation,
        profile_directory=profile_directory,
        timeout_seconds=timeout_seconds,
        headful=headful,
        no_profile_copy=no_profile_copy,
        keep_profile_copy=keep_profile_copy,
    )


def extract_structured_content(
    page: Any,
    doc_ref: YuqueDocRef,
    browser_installation: BrowserInstallation,
    profile_directory: str,
) -> dict[str, Any]:
    payload = page.evaluate(
        """() => {
            const appData = window.appData || {};
            const doc = appData.doc || {};
            const book = appData.book || {};
            const viewerBody = document.querySelector('.ne-viewer-body');
            const article = document.querySelector('article#content, .article-content, .ne-viewer');
            const pageToc = Array.from(document.querySelectorAll('.ne-toc-content .ne-toc-item')).map((item) => {
                const anchor = item.querySelector('a');
                const text = (anchor?.textContent || item.textContent || '').trim();
                const className = item.className || '';
                const depthMatch = className.match(/ne-toc-depth-(\\d+)/);
                return {
                    text,
                    href: anchor?.getAttribute('href') || null,
                    depth: depthMatch ? Number(depthMatch[1]) : null,
                };
            }).filter((item) => item.text);

            return {
                final_url: location.href,
                page_title: document.title,
                title: doc.title || document.querySelector('.doc-article-title')?.textContent?.trim() || document.title,
                description: doc.description || null,
                page_toc: pageToc,
                body_text: (viewerBody?.innerText || article?.innerText || '').trim(),
                body_html: viewerBody?.innerHTML || article?.innerHTML || '',
                metadata: {
                    host: location.host,
                    group_title: appData.group?.name || null,
                    group_login: appData.group?.login || null,
                    book_name: book.name || null,
                    book_slug: book.slug || null,
                    book_toc_count: Array.isArray(book.toc) ? book.toc.length : 0,
                    doc_id: doc.id || null,
                    doc_slug: doc.slug || null,
                    doc_format: doc.format || null,
                    created_at: doc.created_at || null,
                    updated_at: doc.updated_at || null,
                    word_count: doc.word_count || null,
                    public: doc.public ?? null,
                },
            };
        }"""
    )

    body_text = payload.get("body_text", "").strip()
    if not body_text:
        raise FetchError("未能从页面中提取正文。请确认文档已登录可见，且链接指向具体文档页。")

    payload.update(
        {
            "source_url": doc_ref.original_url,
            "requested_host": doc_ref.host,
            "requested_group_login": doc_ref.group_login,
            "requested_repo_slug": doc_ref.repo_slug,
            "requested_doc_slug": doc_ref.doc_slug,
            "browser": {
                "name": browser_installation.name,
                "executable_path": str(browser_installation.executable_path),
                "user_data_dir": str(browser_installation.user_data_dir),
                "profile_directory": profile_directory,
            },
        }
    )
    return payload


def format_markdown(result: dict[str, Any]) -> str:
    metadata = result.get("metadata", {})
    lines = [
        f"# {result.get('title') or result.get('requested_doc_slug') or 'Yuque Document'}",
        "",
        f"- Source URL: {result.get('source_url')}",
        f"- Final URL: {result.get('final_url')}",
        f"- Browser: {result.get('browser', {}).get('name')}",
        f"- Profile: {result.get('browser', {}).get('profile_directory')}",
    ]
    if metadata.get("book_name"):
        lines.append(f"- Book: {metadata['book_name']} ({metadata.get('book_slug') or '-'})")
    if metadata.get("updated_at"):
        lines.append(f"- Updated at: {metadata['updated_at']}")
    if metadata.get("word_count"):
        lines.append(f"- Word count: {metadata['word_count']}")
    if result.get("description"):
        lines.extend(["", "## Description", "", str(result["description"])])

    toc_items = result.get("page_toc") or []
    if toc_items:
        lines.extend(["", "## TOC", ""])
        for item in toc_items:
            indent = "  " * max((item.get("depth") or 1) - 1, 0)
            href = item.get("href") or ""
            suffix = f" ({href})" if href else ""
            lines.append(f"{indent}- {item.get('text', '').strip()}{suffix}")

    lines.extend(["", "## Body", "", result.get("body_text", "")])
    return "\n".join(lines).rstrip() + "\n"


def sanitize_json_result(result: dict[str, Any]) -> dict[str, Any]:
    return result


def main() -> int:
    args = parse_args()
    try:
        doc_ref = parse_yuque_url(args.url)
        browser_installation = resolve_browser(args)
        ensure_profile_exists(browser_installation.user_data_dir, args.profile_directory)
        if args.dry_run:
            print(
                json.dumps(
                    {
                        "source_url": doc_ref.original_url,
                        "host": doc_ref.host,
                        "group_login": doc_ref.group_login,
                        "repo_slug": doc_ref.repo_slug,
                        "doc_slug": doc_ref.doc_slug,
                        "browser": {
                            "strategy": args.strategy,
                            "name": browser_installation.name,
                            "executable_path": str(browser_installation.executable_path),
                            "user_data_dir": str(browser_installation.user_data_dir),
                            "profile_directory": args.profile_directory,
                            "uses_profile_copy": not args.no_profile_copy,
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        result = fetch_document_auto(
            doc_ref=doc_ref,
            browser_installation=browser_installation,
            strategy=args.strategy,
            profile_directory=args.profile_directory,
            timeout_seconds=args.timeout,
            headful=args.headful,
            no_profile_copy=args.no_profile_copy,
            keep_profile_copy=args.keep_profile_copy,
        )
        if args.format == "json":
            print(json.dumps(sanitize_json_result(result), ensure_ascii=False, indent=2))
        else:
            print(format_markdown(result), end="")
        return 0
    except InvalidYuqueUrlError as exc:
        print_error(str(exc))
        return 2
    except BrowserDetectionError as exc:
        print_error(str(exc))
        return 3
    except BrowserLaunchError as exc:
        print_error(str(exc))
        return 4
    except AppleScriptUnavailableError as exc:
        print_error(str(exc))
        return 5
    except FetchError as exc:
        print_error(str(exc))
        return 6


if __name__ == "__main__":
    raise SystemExit(main())
