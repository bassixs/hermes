from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from common import get_settings


VIEW_PATTERNS = [
    re.compile(r"([\d\s.,]+)\s*(?:views|просмотров|просмотра|просмотр)", re.I),
    re.compile(r"👁\s*([\d\s.,]+)", re.I),
]


def detect_source_type(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "vk.com" in host:
        return "vk"
    if "t.me" in host or "telegram" in host:
        return "telegram"
    return "unknown"


def normalize_views(raw: str | None) -> str:
    if not raw:
        return ""
    return raw.replace(" ", "").replace(",", ".").strip()


def find_views(text: str) -> str:
    for pattern in VIEW_PATTERNS:
        match = pattern.search(text)
        if match:
            return normalize_views(match.group(1))
    return ""


async def capture(url: str) -> dict:
    settings = get_settings()
    source_type = detect_source_type(url)
    captured_at = datetime.now(timezone.utc).isoformat()
    safe_stamp = captured_at.replace(":", "-").replace("+", "Z")
    screenshot_path = settings.screenshot_dir / f"{source_type}_{safe_stamp}.png"
    warnings: list[str] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.capture_headless)
        page = await browser.new_page(viewport={"width": 1440, "height": 1600})
        try:
            await page.goto(url, wait_until="networkidle", timeout=settings.capture_timeout_ms)
        except Exception as exc:
            warnings.append(f"navigation_warning: {exc}")
            await page.goto(url, wait_until="domcontentloaded", timeout=settings.capture_timeout_ms)

        await page.screenshot(path=str(screenshot_path), full_page=True)
        title = await page.title()
        body_text = await page.locator("body").inner_text(timeout=10000)
        await browser.close()

    body_text = re.sub(r"\n{3,}", "\n\n", body_text).strip()
    views = find_views(body_text)
    if not views:
        warnings.append("views_not_found")

    return {
        "captured_at": captured_at,
        "source_type": source_type,
        "source_name": title,
        "post_url": url,
        "post_datetime": "",
        "post_text": body_text[:12000],
        "views": views,
        "screenshot_path": str(Path(screenshot_path).resolve()),
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a VK/Telegram post.")
    parser.add_argument("url")
    args = parser.parse_args()
    result = asyncio.run(capture(args.url))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

