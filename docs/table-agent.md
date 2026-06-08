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
SCREENSHOT_STORAGE=cloudinary
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
CLOUDINARY_FOLDER=hermes-screenshots
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

## Screenshot Hosting With Cloudinary

Preferred MVP option: upload screenshots to Cloudinary.

1. Open Cloudinary dashboard.
2. Copy:
   - `Cloud name`;
   - `API Key`;
   - `API Secret`.
3. Put them in `.env`.
4. Run:

```bash
python scripts/process_table_chat_link.py "https://t.me/readovkanews/108685"
```

The sheet cell will contain `IMAGE("https://res.cloudinary.com/...")`, so the
screenshot appears inside the table.

## Alternative Screenshot Hosting

If Cloudinary is not available, screenshots can be served from the VPS with
`nginx`.

Set:

```env
SCREENSHOT_STORAGE=server
SCREENSHOT_PUBLIC_BASE_URL=http://SERVER_IP/screenshots
```

Google Drive upload is still supported, but a personal Google Drive cannot be
used by a service account for file uploads. Google Drive upload works only with
Shared Drives or user OAuth.

## Guardrails

- Do not apply the risk methodic.
- Do not send briefs to observers.
- Do not make operational decisions.
- Only capture, normalize, write, and report errors.
