from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from playwright.async_api import async_playwright

from common import get_settings


VIEW_PATTERNS = [
    re.compile(
        r"([\d\s.,]+[KMBKM\u041a\u041c\u0412]?)\s*(?:views|\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u043e\u0432|\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430|\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440)",
        re.I,
    ),
    re.compile(r"\U0001f441\s*([\d\s.,]+[KMBKM\u041a\u041c\u0412]?)", re.I),
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
    value = raw.replace(" ", "").replace(",", ".").strip().upper()
    value = value.replace("\u041a", "K").replace("\u041c", "M").replace("\u0412", "B")
    return value


def find_views(text: str) -> str:
    for pattern in VIEW_PATTERNS:
        match = pattern.search(text)
        if match:
            return normalize_views(match.group(1))
    return ""


async def wait_for_visuals(locator, timeout_ms: int = 10000) -> None:
    try:
        await locator.evaluate(
            """
            async (element, timeoutMs) => {
              const deadline = Date.now() + timeoutMs;
              const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

              while (Date.now() < deadline) {
                const images = Array.from(element.querySelectorAll("img"));
                const unloadedImages = images.filter((img) => !img.complete || img.naturalWidth === 0);
                const bgNodes = Array.from(element.querySelectorAll("*")).filter((node) => {
                  const bg = getComputedStyle(node).backgroundImage;
                  return bg && bg !== "none" && bg.includes("url(");
                });

                if (unloadedImages.length === 0 || bgNodes.length > 0) {
                  await sleep(800);
                  return;
                }
                await sleep(300);
              }
            }
            """,
            timeout_ms,
        )
    except Exception:
        return


def telegram_public_url(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if "t.me" not in host:
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2 or parts[0] in {"s", "c"}:
        return None

    channel, post_id = parts[0], parts[1]
    if not post_id.isdigit():
        return None

    return urlunparse((parsed.scheme or "https", parsed.netloc, f"/s/{channel}/{post_id}", "", "", ""))


def telegram_post_ref(url: str) -> str | None:
    parsed = urlparse(url)
    if "t.me" not in parsed.netloc.lower():
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if parts and parts[0] == "s":
        parts = parts[1:]
    if len(parts) < 2:
        return None

    channel, post_id = parts[0], parts[1]
    if channel == "c" or not post_id.isdigit():
        return None
    return f"{channel}/{post_id}"


def candidate_urls(url: str, source_type: str) -> list[str]:
    candidates = [url]
    if source_type == "telegram":
        public_url = telegram_public_url(url)
        if public_url:
            candidates.insert(0, public_url)
    return candidates


def looks_like_telegram_stub(text: str) -> bool:
    compact = " ".join(text.upper().split())
    return compact in {
        "DOWNLOAD CONTEXT EMBED VIEW IN CHANNEL",
        "VIEW IN TELEGRAM",
    }


async def extract_telegram_post(page, url: str, screenshot_path: Path) -> dict | None:
    post_ref = telegram_post_ref(url)
    if not post_ref:
        return None

    selector = f".tgme_widget_message[data-post='{post_ref}']"
    message = page.locator(selector).first
    if await message.count() == 0:
        return None

    await message.scroll_into_view_if_needed()
    await wait_for_visuals(message)
    await page.wait_for_timeout(1500)
    await message.screenshot(path=str(screenshot_path))

    text_locator = message.locator(".tgme_widget_message_text").first
    views_locator = message.locator(".tgme_widget_message_views").first
    author_locator = message.locator(".tgme_widget_message_author_name").first
    time_locator = message.locator("time").first

    post_text = ""
    views = ""
    source_name = ""
    post_datetime = ""

    if await text_locator.count():
        post_text = await text_locator.inner_text(timeout=5000)
    if await views_locator.count():
        views = normalize_views(await views_locator.inner_text(timeout=5000))
    if await author_locator.count():
        source_name = await author_locator.inner_text(timeout=5000)
    if await time_locator.count():
        post_datetime = await time_locator.get_attribute("datetime") or ""

    return {
        "source_name": source_name,
        "post_datetime": post_datetime,
        "post_text": post_text,
        "views": views,
    }


async def first_existing_locator(page, selectors: list[str]):
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            if await locator.count():
                return locator
        except Exception:
            continue
    return None


async def extract_vk_views_from_hover(page, post) -> str:
    hover_selectors = [
        "a.PostHeaderSubtitle__link",
        "a.PostHeaderSubtitle__item",
        "a[href*='wall']",
        "time",
    ]

    for selector in hover_selectors:
        locator = post.locator(selector).last
        try:
            if not await locator.count():
                continue
            await locator.hover(timeout=5000)
            await page.wait_for_timeout(1200)
            body_text = await page.locator("body").inner_text(timeout=5000)
            views = find_views(body_text)
            if views:
                return views
        except Exception:
            continue
    return ""


async def extract_vk_post(page, screenshot_path: Path) -> dict | None:
    post = await first_existing_locator(
        page,
        [
            "[id^='post-']",
            ".wall_post",
            ".post",
            ".Post",
        ],
    )
    if not post:
        return None

    await post.scroll_into_view_if_needed()
    await wait_for_visuals(post)
    await page.wait_for_timeout(1500)

    views = await extract_vk_views_from_hover(page, post)
    post_text = await post.inner_text(timeout=10000)
    await post.screenshot(path=str(screenshot_path))

    return {
        "source_name": await page.title(),
        "post_datetime": "",
        "post_text": post_text,
        "views": views,
    }


async def capture(url: str) -> dict:
    settings = get_settings()
    source_type = detect_source_type(url)
    captured_at = datetime.now(timezone.utc).isoformat()
    safe_stamp = captured_at.replace(":", "-").replace("+", "Z")
    screenshot_path = settings.screenshot_dir / f"{source_type}_{safe_stamp}.png"
    warnings: list[str] = []

    title = ""
    body_text = ""
    final_url = url
    extracted: dict | None = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.capture_headless)
        page = await browser.new_page(viewport={"width": 1440, "height": 1600})
        for candidate in candidate_urls(url, source_type):
            final_url = candidate
            try:
                await page.goto(candidate, wait_until="domcontentloaded", timeout=settings.capture_timeout_ms)
                await page.wait_for_timeout(3000)
                title = await page.title()
                body_text = await page.locator("body").inner_text(timeout=10000)
                if source_type == "telegram":
                    extracted = await extract_telegram_post(page, url, screenshot_path)
                if source_type == "vk":
                    extracted = await extract_vk_post(page, screenshot_path)
            except Exception as exc:
                warnings.append(f"navigation_warning: {candidate}: {exc}")
                continue

            if extracted:
                break

            if source_type == "telegram" and looks_like_telegram_stub(body_text):
                warnings.append(f"telegram_stub_page: {candidate}")
                continue
            break

        if not extracted:
            await page.screenshot(path=str(screenshot_path), full_page=True)
        await browser.close()

    body_text = re.sub(r"\n{3,}", "\n\n", body_text).strip()
    post_text = body_text
    views = find_views(body_text)
    post_datetime = ""
    source_name = title

    if extracted:
        post_text = re.sub(r"\n{3,}", "\n\n", extracted.get("post_text", "")).strip()
        views = extracted.get("views") or views
        post_datetime = extracted.get("post_datetime", "")
        source_name = extracted.get("source_name") or title

    if not views:
        warnings.append("views_not_found")
    if source_type == "telegram" and not extracted:
        warnings.append("telegram_post_selector_not_found")

    return {
        "captured_at": captured_at,
        "source_type": source_type,
        "source_name": source_name,
        "post_url": url,
        "capture_url": final_url,
        "post_datetime": post_datetime,
        "post_text": post_text[:12000],
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
