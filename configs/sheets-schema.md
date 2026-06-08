# Google Sheets Schema

Create two sheets: `Queue` and `Results`.

## Queue

| column | purpose |
| --- | --- |
| id | Unique job ID. Can be empty before ingestion. |
| status | `new`, `processing`, `done`, `error`. |
| post_url | VK or Telegram post URL. |
| created_at | When the row was created. |
| locked_at | When the worker started processing it. |
| result_row | Result row number or link. |
| error | Last error, if any. |

## Results For Telegram Table Agent

Primary Table Agent output uses a simple operator-facing sheet:

| column | purpose |
| --- | --- |
| Ссылка | Original post URL as a clickable hyperlink. |
| Количество просмотров | Visible post view count. |
| Скрин поста | Screenshot preview using `IMAGE(...)`. |

## Technical Results

This sheet is primarily for Table Agent. Risk columns may stay empty for this
agent. If later we want a separate coordinator audit log, create another sheet
named `CoordinatorReviews`.

| column | purpose |
| --- | --- |
| job_id | Queue job ID or generated ID. |
| captured_at | Capture timestamp. |
| source_type | `vk`, `telegram`, `unknown`. |
| source_name | Channel/group/user name if available. |
| post_url | Original post URL. |
| post_datetime | Post datetime if available. |
| post_text | Extracted text. |
| views | Visible view count if available. |
| screenshot_path | Local path or uploaded Drive URL. |
| risk_level | Empty for Table Agent. Used only by Coordinator Agent if writing audit rows here. |
| matched_criteria | Empty for Table Agent. |
| confidence | Empty for Table Agent. |
| recommended_action | Empty for Table Agent. |
| risk_reason | Empty for Table Agent. |
| status | `done` or `error` for Table Agent. |
| warnings | Extraction or review warnings. |
