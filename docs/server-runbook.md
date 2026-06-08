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
python scripts/process_table_chat_link.py "POST_URL"
python scripts/risk_review.py --text "test"
python scripts/table_queue_worker.py --once
```

The table chat command requires Google credentials, Drive folder ID, and
spreadsheet settings before it can run successfully.

## Table Agent Telegram Bot

After `.env` is filled, run a foreground test:

```bash
cd /home/hermes/hermes-automation
source .venv/bin/activate
python scripts/telegram_table_bot.py
```

Send a post URL to the configured Telegram links chat. The bot should reply and
append a row with:

- `Ссылка`;
- `Количество просмотров`;
- `Скрин поста`.

For continuous operation, use a user service or supervisor after the foreground
test passes.

Recommended safety:

- run as user `hermes`, not root;
- use Docker terminal backend for risky shell work;
- keep dangerous cron commands denied;
- restrict Telegram access to your own user ID;
- keep Google service account permissions minimal.
