from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from cloudinary_client import upload_image as upload_cloudinary_image
from capture_post import capture
from drive_client import upload_public_image
from sheets_client import append_simple_result


def public_screenshot_url(path: str) -> str:
    base_url = os.getenv("SCREENSHOT_PUBLIC_BASE_URL", "").strip().rstrip("/")
    if not base_url:
        return ""
    return f"{base_url}/{Path(path).name}"


def screenshot_storage() -> str:
    return os.getenv("SCREENSHOT_STORAGE", "cloudinary").strip().lower()


def upload_screenshot(path: str, warnings: list[str]) -> str:
    storage = screenshot_storage()
    if storage == "cloudinary":
        try:
            return upload_cloudinary_image(path)
        except Exception as exc:
            warnings.append(f"cloudinary_upload_failed: {exc}")
            return ""

    if storage == "server":
        url = public_screenshot_url(path)
        if not url:
            warnings.append("screenshot_public_base_url_missing")
        return url

    if storage == "drive":
        try:
            return upload_public_image(path)
        except Exception as exc:
            warnings.append(f"drive_upload_failed: {exc}")
            return ""

    warnings.append(f"unknown_screenshot_storage: {storage}")
    return ""


async def process(url: str, write_sheet: bool = True) -> dict:
    capture_result = await capture(url)
    warnings = list(capture_result.get("warnings", []))
    screenshot_url = ""
    if capture_result.get("screenshot_path"):
        screenshot_url = upload_screenshot(capture_result["screenshot_path"], warnings)

    row_number = ""
    if write_sheet:
        row_number = append_simple_result(
            post_url=capture_result.get("post_url", url),
            views=capture_result.get("views", ""),
            screenshot_url=screenshot_url,
        )

    return {
        "post_url": capture_result.get("post_url", url),
        "views": capture_result.get("views", ""),
        "screenshot_url": screenshot_url,
        "screenshot_path": capture_result.get("screenshot_path", ""),
        "row_number": row_number,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Table Agent chat flow: link, views, screenshot preview.")
    parser.add_argument("url")
    parser.add_argument("--no-sheet", action="store_true")
    args = parser.parse_args()

    result = asyncio.run(process(args.url, write_sheet=not args.no_sheet))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
