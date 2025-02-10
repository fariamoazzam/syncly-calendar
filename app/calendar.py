### app/calendar.py
# Avoid importing anything from app/routes.py or app/__init__.py here
from datetime import datetime

def parse_event_time(event_time_str):
    return datetime.strptime(event_time_str, '%Y-%m-%dT%H:%M:%S%z')

def check_event_conflict(existing_events, new_event):
    new_event_start = parse_event_time(new_event['start']['dateTime'])
    new_event_end = parse_event_time(new_event['end']['dateTime'])
    for event in existing_events:
        existing_start = parse_event_time(event['start']['dateTime'])
        existing_end = parse_event_time(event['end']['dateTime'])
        if new_event_start < existing_end and new_event_end > existing_start:
            return True
    return False