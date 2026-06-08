# Legacy Hermes Architect Skill

This file is kept for reference. Prefer the separate skills:

- `skills/coordinator-agent.md`
- `skills/table-agent.md`

Do not mix the two workflows.

## Rules

1. Treat every job as a structured workflow with a job ID.
2. Delegate capture, Sheets writing, risk review, and notification separately.
3. Do not silently ignore extraction warnings.
4. For `medium`, `high`, `critical`, `manual_review`, or confidence below `0.7`,
   ask the operator for confirmation.
5. Record all outcomes in the result sheet.

## Manual Command

When the operator says:

```text
проверь пост <url>
```

For Table Agent run:

```bash
python scripts/process_table_link.py "<url>"
```

Then summarize:

- risk level;
- views;
- screenshot path;
- result row;
- whether manual review is needed.

## Current Table Agent Queue Worker

For scheduled table processing run:

```bash
python scripts/table_queue_worker.py --once
```
