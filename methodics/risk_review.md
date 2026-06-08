# Risk Review Methodic

This is a placeholder rubric. Replace it with the real duty-officer methodic
before production use.

## Output Format

Return JSON-compatible fields:

- `risk_level`: one of `low`, `medium`, `high`, `critical`, `manual_review`;
- `matched_criteria`: list of criteria IDs;
- `reasoning_summary`: short explanation for the operator;
- `confidence`: number from `0` to `1`;
- `recommended_action`: one of `pass`, `watch`, `manual_review`, `escalate_to_operator`.

## Default Rules

Use `manual_review` when:

- the text is incomplete;
- the post is image-only and OCR is unavailable;
- the content is ambiguous;
- confidence is below `0.7`;
- the post matches any sensitive criterion but evidence is weak.

Use `low` when:

- no criteria match;
- the post is routine, informational, or unrelated to the monitored domain.

Use `medium` or higher only when the methodic contains a clear criterion and the
post text or screenshot supports it.

## Human Confirmation

For `medium`, `high`, `critical`, and `manual_review`, the system must notify a
human operator. It must not treat the triage result as a final operational
decision.

