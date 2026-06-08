from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    spreadsheet_id: str
    queue_sheet: str
    results_sheet: str
    screenshot_dir: Path
    capture_headless: bool
    capture_timeout_ms: int


def get_settings() -> Settings:
    screenshot_dir = Path(os.getenv("SCREENSHOT_DIR", "screenshots")).resolve()
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        spreadsheet_id=os.getenv("GOOGLE_SPREADSHEET_ID", ""),
        queue_sheet=os.getenv("GOOGLE_QUEUE_SHEET", "Queue"),
        results_sheet=os.getenv("GOOGLE_RESULTS_SHEET", "Results"),
        screenshot_dir=screenshot_dir,
        capture_headless=os.getenv("CAPTURE_HEADLESS", "true").lower() == "true",
        capture_timeout_ms=int(os.getenv("CAPTURE_TIMEOUT_MS", "45000")),
    )


def require(value: str, name: str) -> str:
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value

