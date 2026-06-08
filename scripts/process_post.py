from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone

from capture_post import capture
from risk_review import review
from sheets_client import append_result


def make_job_id() -> str:
    return datetime.now(timezone.utc).strftime("job_%Y%m%d_%H%M%S")


async def process(url: str, job_id: str | None = None, write_sheet: bool = True) -> dict:
    job_id = job_id or make_job_id()
    capture_result = await capture(url)
    risk = review(capture_result.get("post_text", ""))

    warnings = []
    warnings.extend(capture_result.get("warnings", []))
    warnings.extend(risk.get("warnings", []))

    status = "done"
    if risk["risk_level"] != "low" or warnings:
        status = "manual_review"

    record = {
        "job_id": job_id,
        "captured_at": capture_result.get("captured_at", ""),
        "source_type": capture_result.get("source_type", ""),
        "source_name": capture_result.get("source_name", ""),
        "post_url": capture_result.get("post_url", url),
        "post_datetime": capture_result.get("post_datetime", ""),
        "post_text": capture_result.get("post_text", ""),
        "views": capture_result.get("views", ""),
        "screenshot_path": capture_result.get("screenshot_path", ""),
        "risk_level": risk.get("risk_level", "manual_review"),
        "matched_criteria": risk.get("matched_criteria", []),
        "confidence": risk.get("confidence", ""),
        "recommended_action": risk.get("recommended_action", "manual_review"),
        "risk_reason": risk.get("reasoning_summary", ""),
        "status": status,
        "warnings": warnings,
    }

    if write_sheet:
        row_number = append_result(record)
        record["result_row"] = row_number

    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="Process one post end to end.")
    parser.add_argument("url")
    parser.add_argument("--job-id")
    parser.add_argument("--no-sheet", action="store_true")
    args = parser.parse_args()

    result = asyncio.run(process(args.url, args.job_id, write_sheet=not args.no_sheet))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

