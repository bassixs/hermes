# Architecture

## Roles

### Hermes Architect

Owns the full workflow. It should not do every step directly. It delegates
specialized work, validates outputs, writes a final event record, and escalates
uncertain or sensitive cases to a human operator.

Responsibilities:

- accept operator commands;
- start scheduled queue processing;
- assign work to specialized agents or scripts;
- enforce manual review rules;
- keep the status log coherent;
- summarize failures in plain language.

### Source Monitor Agent

Finds new inputs. In MVP it reads rows with status `new` from a Google Sheet.
Later it can monitor channel lists directly.

### Capture Agent

Receives one post URL and returns normalized capture data:

- source type: `vk`, `telegram`, or `unknown`;
- source name;
- post URL;
- post text;
- visible view count;
- post datetime when available;
- local screenshot path;
- extraction warnings.

### Sheets Agent

Writes normalized records to Google Sheets. It should be deterministic and
script-backed, not a free-form browser workflow.

### Risk Review Agent

Applies `methodics/risk_review.md` as a rubric. It returns structured triage,
not a final political or operational action.

Output fields:

- `risk_level`: `low`, `medium`, `high`, `critical`, `manual_review`;
- `matched_criteria`;
- `reasoning_summary`;
- `confidence`;
- `recommended_action`.

### Notification Agent

Sends concise operator notifications. It avoids duplicate noise and only alerts
when configured rules say the operator should see the item.

## Data Flow

1. Operator sends `check post <url>` or cron reads a `new` queue item.
2. Architect creates a job ID.
3. Capture Agent extracts data and stores a screenshot.
4. Risk Review Agent evaluates text and context.
5. Sheets Agent appends or updates the row.
6. Notification Agent reports if the item needs attention.
7. Architect marks the queue item `done`, `error`, or `manual_review`.

## Manual Review Rule

The system can classify and summarize. For `medium`, `high`, `critical`, or
low-confidence results, it should notify the operator and wait for confirmation
before any external escalation or final decision.

