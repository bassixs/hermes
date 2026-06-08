# MVP Workflow

## Manual Command

Operator command:

```text
проверь пост https://...
```

Expected behavior:

1. Detect platform from URL.
2. Open the post with browser automation.
3. Save screenshot under `screenshots/`.
4. Extract text and views.
5. Evaluate risk using `methodics/risk_review.md`.
6. Append a row to Google Sheets.
7. Reply with a short summary:

```text
Готово.
Риск: medium
Просмотры: 12 431
Строка: <sheet row/link>
Скрин: <drive link or local path>
Нужно решение дежурного: да
```

## Queue Mode

The queue sheet should contain at least:

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
- `manual_review`
- `error`

Cron runs every 5-15 minutes:

1. Read the first `new` row.
2. Lock it by setting `processing`.
3. Run the manual-command workflow.
4. Write result fields.
5. Set final status.

## Failure Handling

If text or views cannot be extracted, still save the screenshot and write a row
with warnings. The item should become `manual_review` when the screenshot exists
but machine-readable data is incomplete.

