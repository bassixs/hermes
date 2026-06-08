# Table Agent Skill

Use this skill for links sent to the table/accounting workflow.

## Mission

Capture the linked post and write normalized data to Google Sheets.

## Manual Command

```bash
python scripts/process_table_link.py "<url>"
```

## Queue Worker

```bash
python scripts/table_queue_worker.py --once
```

## Do Not

- Do not apply the risk methodic.
- Do not send observer briefs.
- Do not make escalation decisions.

