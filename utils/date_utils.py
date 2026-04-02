from datetime import datetime

def get_event_date():
    now = datetime.now()
    event = datetime(now.year, 9, 13, 0, 0, 0)

    if now > event:
        event = datetime(now.year + 1, 9, 13, 0, 0, 0)

    return event