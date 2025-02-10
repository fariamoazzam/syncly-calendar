### app/utils.py
# app/utils.py
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime

def get_calendar_service(credentials_data):
    creds = Credentials(
        token=credentials_data['token'],
        refresh_token=credentials_data['refresh_token'],
        token_uri=credentials_data['token_uri'],
        client_id=credentials_data['client_id'],
        client_secret=credentials_data['client_secret'],
        scopes=credentials_data['scopes']
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update session with new credentials
        from flask import session
        session['credentials'] = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
    return build('calendar', 'v3', credentials=creds)

def sync_events(service):
    # Fetch events from the user's calendar
    events_result = service.events().list(calendarId='primary').execute()
    return events_result.get('items', [])