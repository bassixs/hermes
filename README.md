# Hermes Automation Stack

This workspace contains the implementation pack for a Hermes Agent based
automation system.

The target design is a coordinator-led multi-agent workflow:

- Hermes Architect coordinates work, routes tasks, checks outputs, and asks for
  human confirmation on sensitive decisions.
- Source Monitor watches the input queue and sources.
- Capture Agent opens VK/Telegram posts, extracts visible metrics, and creates
  screenshots.
- Sheets Agent writes normalized rows to Google Sheets.
- Risk Review Agent applies the duty-officer methodic and returns a structured
  risk triage.
- Notification Agent sends concise Telegram alerts and status updates.

## MVP

The first useful version is intentionally small:

1. Accept a post URL from Telegram or a queue sheet.
2. Capture text, views, date, source, and screenshot.
3. Run risk triage using `methodics/risk_review.md`.
4. Append one row to Google Sheets.
5. Notify the operator when risk is not `low` or when data extraction fails.

See:

- `docs/architecture.md`
- `docs/mvp-workflow.md`
- `docs/server-runbook.md`
- `configs/env.example`

