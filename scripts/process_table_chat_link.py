from __future__ import annotations

import argparse
import asyncio
import json

from capture_post import capture
from drive_client import upload_public_image
from sheets_client import append_simple_result


async def process(url: str, write_sheet: bool = True) -> dict:
    capture_result = await capture(url)
    warnings = list(capture_result.get("warnings", []))
    screenshot_url = ""
    if capture_result.get("screenshot_path"):
        try:
            screenshot_url = upload_public_image(capture_result["screenshot_path"])
        except Exception as exc:
            warnings.append(f"drive_upload_failed: {exc}")

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
