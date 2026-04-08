from datetime import datetime
import json
import os
from pathlib import Path
from urllib import parse, request


BASE_DIR = Path(__file__).resolve().parent.parent
VISITOR_LOG_FILE = BASE_DIR / "visitor_events.log"
CHAT_LOG_FILE = BASE_DIR / "chat_events.log"
OPEN_PREFIX = "TickTill opened by "


def _get_telegram_credentials():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    return bot_token, chat_id


def _telegram_api_request(method, data=None):
    bot_token, _ = _get_telegram_credentials()
    if not bot_token:
        return None

    telegram_url = f"https://api.telegram.org/bot{bot_token}/{method}"
    payload = None
    if data is not None:
        payload = parse.urlencode(data).encode("utf-8")
    req = request.Request(telegram_url, data=payload, method="POST" if payload else "GET")

    try:
        with request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")
            parsed = json.loads(raw)
            if parsed.get("ok"):
                return parsed.get("result")
    except Exception:
        return None

    return None


def _append_jsonl(path, event):
    try:
        with path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(event) + "\n")
    except OSError:
        pass


def get_visitor_name(query_params):
    visitor = query_params.get("visitor", "")
    if isinstance(visitor, list):
        visitor = visitor[0] if visitor else ""
    visitor = str(visitor).strip()
    return visitor or "anonymous"


def track_visitor_open(visitor_name):
    event = {
        "visitor": visitor_name,
        "opened_at": datetime.now().isoformat(timespec="seconds"),
    }
    _append_jsonl(VISITOR_LOG_FILE, event)
    event["telegram_sent"] = send_open_notification(event)
    return event


def send_open_notification(event):
    _, chat_id = _get_telegram_credentials()
    if not chat_id:
        return False

    text = f"TickTill opened by {event['visitor']} on {event['opened_at']}"
    return bool(_telegram_api_request("sendMessage", {"chat_id": chat_id, "text": text}))


def send_visitor_reply(visitor_name, message_text):
    _, chat_id = _get_telegram_credentials()
    clean_text = str(message_text).strip()
    if not chat_id or not clean_text:
        return False

    event = {
        "visitor": visitor_name,
        "direction": "visitor_to_owner",
        "text": clean_text,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _append_jsonl(CHAT_LOG_FILE, event)

    telegram_text = f"[{visitor_name}] {clean_text}"
    return bool(_telegram_api_request("sendMessage", {"chat_id": chat_id, "text": telegram_text}))


def _get_updates():
    result = _telegram_api_request("getUpdates")
    return result or []


def get_owner_messages(limit=20):
    _, chat_id = _get_telegram_credentials()
    if not chat_id:
        return []

    messages = []
    for update in _get_updates():
        message = update.get("message") or update.get("edited_message") or {}
        if str(message.get("chat", {}).get("id", "")) != chat_id:
            continue

        text = str(message.get("text", "")).strip()
        if not text or text.startswith(OPEN_PREFIX):
            continue

        created_at = message.get("date")
        messages.append({
            "direction": "owner_to_visitor",
            "text": text,
            "created_at": datetime.fromtimestamp(created_at).isoformat(timespec="seconds") if created_at else "",
            "update_id": update.get("update_id", 0),
        })

    messages.sort(key=lambda item: item.get("update_id", 0))
    return messages[-limit:]


def get_visitor_replies(visitor_name, limit=20):
    if not CHAT_LOG_FILE.exists():
        return []

    replies = []
    try:
        with CHAT_LOG_FILE.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                line = line.strip()
                if not line:
                    continue
                event = json.loads(line)
                if event.get("direction") != "visitor_to_owner":
                    continue
                if event.get("visitor") != visitor_name:
                    continue
                replies.append(event)
    except (OSError, json.JSONDecodeError):
        return []

    return replies[-limit:]


def get_chat_thread(visitor_name, limit=30):
    owner_messages = get_owner_messages(limit=limit)
    visitor_messages = get_visitor_replies(visitor_name, limit=limit)

    combined = owner_messages + visitor_messages
    combined.sort(key=lambda item: item.get("created_at", ""))
    return combined[-limit:]