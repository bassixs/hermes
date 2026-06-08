# Coordinator Agent

## Real-World Role

Before automation:

- duty officers watch news mentioning Kaluga Oblast, districts, and the
  Governor;
- routine problems go to the duty chat where ministries respond;
- risky posts go to the coordinator;
- coordinator checks whether the item is truly risky;
- if yes, coordinator sends observers a short brief.

Coordinator Agent automates the coordinator check for posts forwarded by duty
officers.

## Inputs

- post URL;
- optional duty officer comment;
- `methodics/risk_review.md`.

## Outputs

Coordinator decision:

- `no_escalation`;
- `needs_human_coordinator`;
- `send_to_observers`.

Observer brief fields:

- post URL;
- source;
- date/time;
- short post summary;
- matched methodic criteria;
- why this is risky;
- confidence;
- screenshot link/path.

## Guardrails

- Do not send observer briefs when the methodic is missing.
- Ask the human coordinator when confidence is below the configured threshold.
- Keep the explanation short and tied to methodic criteria.
- Do not write routine accounting rows; that belongs to Table Agent.

