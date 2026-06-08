# Table Agent

## Real-World Role

Table Agent automates the link accounting workflow.

A human posts a link in the Telegram links chat. The agent captures post
metadata, uploads the screenshot to Google Drive, and writes the result to
Google Sheets.

## Inputs

- post URL from Telegram links chat.

## Outputs

One row in the simple `Results` sheet:

- `Ссылка`;
- `Количество просмотров`;
- `Скрин поста`.

`Скрин поста` is written as a Google Sheets `IMAGE(...)` formula that points to
the uploaded Google Drive image.

## Bot Setup

1. Create a Telegram bot via `@BotFather`.
2. Disable privacy mode if the bot must read ordinary group messages:

```text
/setprivacy -> choose bot -> Disable
```

3. Add the bot to the links chat.
4. Put these values in `.env`:

```env
TELEGRAM_TABLE_BOT_TOKEN=123456:...
TELEGRAM_TABLE_ALLOWED_CHAT_IDS=-1001234567890
GOOGLE_DRIVE_SCREENSHOT_FOLDER_ID=...
GOOGLE_SIMPLE_RESULTS_SHEET=Results
```

5. Start the bot:

```bash
python scripts/telegram_table_bot.py
```

Manual test without Telegram:

```bash
python scripts/process_table_chat_link.py "https://t.me/readovkanews/108685"
```

## Google Drive

Create a Drive folder for screenshots. Share that folder with the service
account email as `Editor`. The bot uploads screenshots there and makes each
uploaded image readable by link.

## Guardrails

- Do not apply the risk methodic.
- Do not send briefs to observers.
- Do not make operational decisions.
- Only capture, normalize, write, and report errors.

