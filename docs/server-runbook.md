# Server Runbook

Target: Ubuntu VPS, separate unprivileged `hermes` user, Telegram gateway, Docker
backend for command execution.

## Install Hermes

```bash
sudo adduser hermes
sudo usermod -aG docker hermes
su - hermes

curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc

hermes setup
hermes model
hermes tools
hermes doctor
```

## Gateway

```bash
hermes gateway setup
hermes gateway install
hermes gateway start
hermes gateway status
sudo loginctl enable-linger hermes
```

Logs:

```bash
journalctl --user -u hermes-gateway -f
```

## Cron

Manual test:

```bash
hermes cron create "every 15m" "Process one new post from the Google Sheets queue using the post monitoring workflow." --name "post-queue-worker"
hermes cron list
hermes cron status
```

## Automation Project Setup

Copy this workspace to the server, for example:

```bash
/home/hermes/hermes-automation
```

Create `.env`:

```bash
cp configs/env.example .env
nano .env
```

Install Python dependencies inside the Hermes/server Python environment:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Smoke tests:

```bash
python scripts/process_table_link.py "POST_URL" --no-sheet
python scripts/risk_review.py --text "test"
python scripts/table_queue_worker.py --once
```

The queue worker requires Google credentials and spreadsheet settings before it
can run successfully.

Recommended safety:

- run as user `hermes`, not root;
- use Docker terminal backend for risky shell work;
- keep dangerous cron commands denied;
- restrict Telegram access to your own user ID;
- keep Google service account permissions minimal.
