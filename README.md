# Hermes Automation Stack

This workspace contains the implementation pack for a Hermes Agent based
automation system.

The target design has two separate Hermes agents. They can share low-level
capture scripts, but they must not share decision logic.

- Coordinator Agent reviews posts forwarded by duty officers. It applies the
  methodic, decides whether the item should go to observers, and prepares a
  short brief. It does not maintain the public accounting table.
- Table Agent receives post links from a Telegram links chat, captures metadata,
  uploads screenshots to Cloudinary, and writes rows to Google Sheets. It does
  not evaluate political/operational risk.

## MVP

The first useful version is split in two:

1. Table Agent:
   - accept a post URL from a Telegram links chat;
   - capture text, views, date, source, and screenshot;
   - upload screenshot to Cloudinary;
   - append a simple row to Google Sheets: link, views, screenshot preview.
2. Coordinator Agent:
   - accept a post URL from the duty/coordinator chat;
   - capture text and screenshot;
   - apply `methodics/risk_review.md`;
   - forward a brief only when the methodic says the item matches escalation
     criteria.

See:

- `docs/architecture.md`
- `docs/mvp-workflow.md`
- `docs/coordinator-agent.md`
- `docs/table-agent.md`
- `docs/server-runbook.md`
- `configs/env.example`
