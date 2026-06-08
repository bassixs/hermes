from __future__ import annotations

import argparse
import json
import os
from typing import Any

import gspread

from common import get_settings, require


RESULT_HEADERS = [
    "job_id",
    "captured_at",
    "source_type",
    "source_name",
    "post_url",
    "post_datetime",
    "post_text",
    "views",
    "screenshot_path",
    "risk_level",
    "matched_criteria",
    "confidence",
    "recommended_action",
    "risk_reason",
    "status",
    "warnings",
]


QUEUE_HEADERS = [
    "id",
    "status",
    "post_url",
    "created_at",
    "locked_at",
    "result_row",
    "error",
]


def open_spreadsheet():
    settings = get_settings()
    spreadsheet_id = require(settings.spreadsheet_id, "GOOGLE_SPREADSHEET_ID")
    credentials_path = require(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""), "GOOGLE_APPLICATION_CREDENTIALS")
    client = gspread.service_account(filename=credentials_path)
    return client.open_by_key(spreadsheet_id)


def ensure_headers(worksheet, headers: list[str]) -> None:
    first_row = worksheet.row_values(1)
    if first_row != headers:
        worksheet.update("1:1", [headers])


def append_result(record: dict[str, Any]) -> int:
    settings = get_settings()
    spreadsheet = open_spreadsheet()
    worksheet = spreadsheet.worksheet(settings.results_sheet)
    ensure_headers(worksheet, RESULT_HEADERS)

    row = []
    for header in RESULT_HEADERS:
        value = record.get(header, "")
        if isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        row.append(value)
    worksheet.append_row(row, value_input_option="USER_ENTERED")
    return len(worksheet.get_all_values())


def get_queue_records() -> list[dict[str, Any]]:
    settings = get_settings()
    spreadsheet = open_spreadsheet()
    worksheet = spreadsheet.worksheet(settings.queue_sheet)
    ensure_headers(worksheet, QUEUE_HEADERS)
    records = worksheet.get_all_records()
    for index, record in enumerate(records, start=2):
        record["_row_number"] = index
    return records


def update_queue_row(row_number: int, updates: dict[str, Any]) -> None:
    settings = get_settings()
    spreadsheet = open_spreadsheet()
    worksheet = spreadsheet.worksheet(settings.queue_sheet)
    headers = worksheet.row_values(1)
    for key, value in updates.items():
        if key not in headers:
            continue
        col = headers.index(key) + 1
        worksheet.update_cell(row_number, col, value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Sheets helper.")
    parser.add_argument("action", choices=["append-result", "list-queue"])
    parser.add_argument("--json-file")
    args = parser.parse_args()

    if args.action == "append-result":
        if not args.json_file:
            raise SystemExit("--json-file is required")
        with open(args.json_file, "r", encoding="utf-8") as fh:
            record = json.load(fh)
        print(append_result(record))
        return

    if args.action == "list-queue":
        print(json.dumps(get_queue_records(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
