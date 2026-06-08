# Next Steps

## What I Need From You

1. Google Sheet URL or desired table layout confirmation.
2. Google service account JSON, placed on the server only, not committed here.
3. Three to five VK/Telegram test post links.
4. The real duty-officer methodic text for `methodics/risk_review.md`.
5. Preferred Telegram operator chat/user ID.

## First Implementation Milestone

1. Put the project on the server.
2. Fill `.env`.
3. Install `requirements.txt`.
4. Run one capture without Sheets:

```bash
python scripts/process_post.py "POST_URL" --no-sheet
```

5. Fix source-specific extraction selectors for VK and Telegram based on real
   screenshots and page text.
6. Connect Google Sheets and run:

```bash
python scripts/process_post.py "POST_URL"
```

7. Add a `new` row to the queue and run:

```bash
python scripts/queue_worker.py --once
```

## Open Design Choices

- Where screenshots should live long-term: local disk, Google Drive, S3, or both.
- Whether Telegram/VK should be accessed as anonymous web pages or through
  authenticated browser profiles.
- Whether the queue is Google Sheets only or also accepts Telegram commands.
- How strict the manual-review threshold should be.

