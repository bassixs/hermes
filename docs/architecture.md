# Architecture

## Two-Agent Boundary

### Agent 1: Coordinator Agent

Purpose: replace the manual coordinator check for posts forwarded by duty
officers.

Responsibilities:

- receives a post link from the duty/coordinator chat;
- captures the post text, metadata, and screenshot;
- applies the duty-officer methodic from `methodics/risk_review.md`;
- decides whether the post should be escalated to observers;
- prepares a short observer brief when escalation criteria are met;
- asks for human confirmation when confidence is low or the methodic is unclear;
- keeps a separate risk-review log.

This agent should not fill the routine accounting table. Its output is a
coordination decision and, when needed, an observer-facing brief.

### Agent 2: Table Agent

Purpose: automate the existing link-to-table routine.

Responsibilities:

- receives a post link from a links chat or queue sheet;
- captures post text, visible views, date, source, and screenshot;
- writes the record to Google Sheets;
- updates queue status;
- reports extraction errors.

This agent should not apply the risk methodic and should not decide whether to
send anything to observers.

## Shared Helpers

Both agents may use shared deterministic helpers:

### Capture Helper

Receives one post URL and returns normalized capture data:

- source type: `vk`, `telegram`, or `unknown`;
- source name;
- post URL;
- post text;
- visible view count;
- post datetime when available;
- local screenshot path;
- extraction warnings.

### Sheets Helper

Writes normalized records to Google Sheets. It should be deterministic and
script-backed, not a free-form browser workflow.

### Risk Review Helper

Used only by Coordinator Agent. Applies `methodics/risk_review.md` as a rubric
and returns structured triage.

Output fields:

- `risk_level`: `low`, `medium`, `high`, `critical`, `manual_review`;
- `matched_criteria`;
- `reasoning_summary`;
- `confidence`;
- `recommended_action`.

## Table Agent Flow

1. Human sends a link to the links chat or adds a `new` queue row.
2. Table Agent creates a job ID.
3. Capture Helper extracts post data and stores a screenshot.
4. Sheets Helper appends the result row.
5. Table Agent marks the queue item `done` or `error`.

## Coordinator Agent Flow

1. Duty officer forwards a questionable/risky post to the coordinator chat.
2. Coordinator Agent captures the post and reads the methodic.
3. Coordinator Agent classifies the post against the methodic.
4. If it does not match escalation criteria, it replies with a short reason.
5. If it matches, it prepares a brief for observers.
6. If confidence is low, it asks the human coordinator for confirmation.

## Manual Review Rule

Coordinator Agent can classify and summarize. For low-confidence or ambiguous
items, it should ask a human coordinator before sending an observer brief.
