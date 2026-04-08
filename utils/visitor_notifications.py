from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from urllib import parse, request


LOG_FILE = Path(__file__).resolve().parent.parent / "visitor_events.log"


def _get_telegram_credentials():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    return bot_token, chat_id


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
    bot_token, chat_id = _get_telegram_credentials()
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


def _get_updates():
    bot_token, _ = _get_telegram_credentials()
    if not bot_token:
        return []

    telegram_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    req = request.Request(telegram_url, method="GET")

    try:
        with request.urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if payload.get("ok"):
                return payload.get("result", [])
    except Exception:
        return []

    return []


def get_popup_message(max_age_minutes=15):
    _, chat_id = _get_telegram_credentials()
    if not chat_id:
        return ""

    latest_message = ""
    latest_timestamp = None

    for update in _get_updates():
        message = update.get("message") or update.get("edited_message") or {}
        if str(message.get("chat", {}).get("id", "")) != chat_id:
            continue

        text = str(message.get("text", "")).strip()
        if not text:
            continue

        timestamp = message.get("date")
        if timestamp is None:
            continue

        latest_message = text
        latest_timestamp = datetime.fromtimestamp(timestamp)

    if not latest_message or latest_timestamp is None:
        return ""

    if datetime.now() - latest_timestamp > timedelta(minutes=max_age_minutes):
        return ""

    return latest_message


def track_visitor_open(visitor_name):
    event = build_event(visitor_name)
    append_event_log(event)
    event["telegram_sent"] = send_telegram_message(event)
    return event