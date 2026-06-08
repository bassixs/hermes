# Table Agent

## Real-World Role

Table Agent automates the link accounting workflow.

A human posts a link in the links chat or adds it to the `Queue` sheet. The agent
captures post metadata and writes the result to Google Sheets.

## Inputs

- post URL from links chat;
- or row with `status=new` in `Queue`.

## Outputs

One row in `Results`:

- job ID;
- capture timestamp;
- source type;
- source name;
- post URL;
- post datetime;
- post text;
- views;
- screenshot path or URL;
- status;
- warnings.

## Guardrails

- Do not apply the risk methodic.
- Do not send briefs to observers.
- Do not make operational decisions.
- Only capture, normalize, write, and report errors.

