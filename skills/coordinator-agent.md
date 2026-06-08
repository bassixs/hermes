# Coordinator Agent Skill

Use this skill for posts forwarded by duty officers to the coordinator chat.

## Mission

Evaluate whether a forwarded post matches the escalation methodic and, only when
it does, prepare a concise observer brief.

## Do

1. Capture the post.
2. Read `methodics/risk_review.md`.
3. Match the post to methodic criteria.
4. Return a structured decision:
   - `no_escalation`;
   - `needs_human_coordinator`;
   - `send_to_observers`.
5. Include a short reason tied to specific criteria.

## Do Not

- Do not fill the routine Google Sheet.
- Do not treat missing methodic as permission to escalate.
- Do not send ambiguous items directly to observers.

