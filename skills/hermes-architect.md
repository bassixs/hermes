# Hermes Architect Skill

Use this skill when coordinating the post monitoring automation.

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

Run:

```bash
python scripts/process_post.py "<url>"
```

Then summarize:

- risk level;
- views;
- screenshot path;
- result row;
- whether manual review is needed.

## Queue Worker

For scheduled processing run:

```bash
python scripts/queue_worker.py --once
```

