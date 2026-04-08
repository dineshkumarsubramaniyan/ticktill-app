from datetime import datetime
import json
import os
from pathlib import Path
from urllib import parse, request


LOG_FILE = Path(__file__).resolve().parent.parent / "visitor_events.log"


def get_visitor_name(query_params):
    visitor = query_params.get("visitor", "")
    if isinstance(visitor, list):
        visitor = visitor[0] if visitor else ""
    visitor = str(visitor).strip()
    return visitor or "anonymous"


def build_event(visitor_name):
    return {
        "visitor": visitor_name,
        "opened_at": datetime.now().isoformat(timespec="seconds"),
    }


def append_event_log(event):
    try:
        with LOG_FILE.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(event) + "\n")
    except OSError:
        pass


def send_telegram_message(event):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not bot_token or not chat_id:
        return False

    message = f"TickTill opened by {event['visitor']} on {event['opened_at']}"
    payload = parse.urlencode({
        "chat_id": chat_id,
        "text": message,
    }).encode("utf-8")
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    req = request.Request(telegram_url, data=payload, method="POST")

    try:
        with request.urlopen(req, timeout=10) as response:
            return 200 <= response.status < 300
    except Exception:
        return False


def track_visitor_open(visitor_name):
    event = build_event(visitor_name)
    append_event_log(event)
    event["telegram_sent"] = send_telegram_message(event)
    return event