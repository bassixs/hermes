# MVP Workflow

There are two independent MVP workflows.

## 1. Table Agent

Input:

```text
<post_url>
```

Expected behavior:

1. Detect platform from URL.
2. Open the post with browser automation.
3. Save screenshot under `screenshots/`.
4. Extract text, views, date, and source.
5. Upload screenshot to Google Drive.
6. Append a simple row to Google Sheets:
   - `Ссылка`;
   - `Количество просмотров`;
   - `Скрин поста`.
7. Reply in Telegram with a short technical summary.

Server command:

```bash
python scripts/process_table_chat_link.py "https://t.me/readovkanews/108685"
```

Telegram bot command:

```bash
python scripts/telegram_table_bot.py
```

## 2. Coordinator Agent

Input:

```text
<post_url forwarded by duty officer>
```

Expected behavior:

1. Capture the post text and screenshot.
2. Apply `methodics/risk_review.md`.
3. Decide one of:
   - `no_escalation`;
   - `needs_human_coordinator`;
   - `send_to_observers`.
4. If escalation is needed, generate a short observer brief:
   - what happened;
   - where it happened;
   - why it matters according to the methodic;
   - link and screenshot;
   - confidence and matched criteria.

This workflow is not active until the real methodic is provided.

## Legacy Queue Sheet

The queue flow is kept as a fallback. The primary Table Agent flow is now
Telegram chat ingestion.

For legacy queue mode, the `Queue` sheet should contain:

- `id`
- `status`
- `post_url`
- `created_at`
- `locked_at`
- `result_row`
- `error`

Statuses:

- `new`
- `processing`
- `done`
- `error`

## Failure Handling

Table Agent should still write a row when a screenshot exists but text/views are
incomplete. The row status should be `error` only when the post could not be
captured or the table could not be updated.
