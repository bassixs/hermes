from __future__ import annotations

import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import requests

from common import require
from process_table_chat_link import process


URL_RE = re.compile(r"https?://[^\s<>\"]+")
STATE_PATH = Path("data/telegram-table-bot-state.json")


def bot_token() -> str:
    return require(os.getenv("TELEGRAM_TABLE_BOT_TOKEN", ""), "TELEGRAM_TABLE_BOT_TOKEN")


def allowed_chat_ids() -> set[int]:
    raw = os.getenv("TELEGRAM_TABLE_ALLOWED_CHAT_IDS", "").strip()
    if not raw:
        return set()
    return {int(item.strip()) for item in raw.split(",") if item.strip()}


def api(method: str, **params):
    response = requests.post(f"https://api.telegram.org/bot{bot_token()}/{method}", json=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError(payload)
    return payload["result"]


def load_offset() -> int | None:
    if not STATE_PATH.exists():
        return None
    return json.loads(STATE_PATH.read_text(encoding="utf-8")).get("offset")


def save_offset(offset: int) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"offset": offset}), encoding="utf-8")


def message_text(message: dict[str, Any]) -> str:
    parts = [
        message.get("text", ""),
        message.get("caption", ""),
    ]
    return "\n".join(part for part in parts if part)


def extract_urls(text: str) -> list[str]:
    urls = []
    for match in URL_RE.finditer(text):
        url = match.group(0).rstrip(").,;]")
        if url not in urls:
            urls.append(url)
    return urls


async def handle_message(message: dict[str, Any]) -> None:
    chat = message.get("chat", {})
    chat_id = int(chat.get("id"))
    allowed = allowed_chat_ids()
    if allowed and chat_id not in allowed:
        return

    urls = extract_urls(message_text(message))
    if not urls:
        return

    api("sendMessage", chat_id=chat_id, text=f"Принял ссылок: {len(urls)}. Обрабатываю.")
    for url in urls:
        try:
            result = await process(url, write_sheet=True)
            text = (
                "Готово.\n"
                f"Ссылка: {result['post_url']}\n"
                f"Просмотры: {result.get('views') or 'не найдены'}\n"
                f"Строка: {result.get('row_number')}\n"
                f"Скрин: {result.get('screenshot_url')}"
            )
        except Exception as exc:
            text = f"Ошибка при обработке {url}: {exc}"
        api("sendMessage", chat_id=chat_id, text=text)


async def poll_forever() -> None:
    offset = load_offset()
    timeout = int(os.getenv("TELEGRAM_TABLE_POLL_TIMEOUT", "30"))

    while True:
        try:
            updates = api("getUpdates", offset=offset, timeout=timeout, allowed_updates=["message"])
            for update in updates:
                offset = int(update["update_id"]) + 1
                save_offset(offset)
                message = update.get("message")
                if message:
                    await handle_message(message)
        except Exception as exc:
            print(f"telegram_table_bot_error: {exc}", flush=True)
            time.sleep(5)


def main() -> None:
    asyncio.run(poll_forever())


if __name__ == "__main__":
    main()

