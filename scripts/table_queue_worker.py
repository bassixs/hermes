from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone

from process_table_link import process
from sheets_client import get_queue_records, update_queue_row


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def first_new_job() -> dict | None:
    for record in get_queue_records():
        if str(record.get("status", "")).strip().lower() == "new":
            return record
    return None


async def run_once() -> str:
    job = first_new_job()
    if not job:
        return "No new queue rows."

    row_number = int(job["_row_number"])
    job_id = str(job.get("id") or f"table_{row_number}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}")
    post_url = str(job.get("post_url", "")).strip()

    if not post_url:
        update_queue_row(row_number, {"status": "error", "error": "post_url is empty"})
        return f"Queue row {row_number} has no post_url."

    update_queue_row(row_number, {"id": job_id, "status": "processing", "locked_at": utc_now(), "error": ""})

    try:
        result = await process(post_url, job_id=job_id, write_sheet=True)
    except Exception as exc:
        update_queue_row(row_number, {"status": "error", "error": str(exc)})
        raise

    update_queue_row(
        row_number,
        {
            "status": result.get("status", "done"),
            "result_row": result.get("result_row", ""),
            "error": "",
        },
    )
    return f"Processed {job_id}: {result.get('status')}."


def main() -> None:
    parser = argparse.ArgumentParser(description="Table Agent: process one new queue row.")
    parser.add_argument("--once", action="store_true", help="Process at most one queue row.")
    args = parser.parse_args()

    if not args.once:
        raise SystemExit("Only --once is implemented for MVP.")

    print(asyncio.run(run_once()))


if __name__ == "__main__":
    main()

