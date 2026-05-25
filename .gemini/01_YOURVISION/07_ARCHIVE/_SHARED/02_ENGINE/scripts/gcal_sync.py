#!/usr/bin/env python3
import datetime
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TOKEN_PATH = '/home/levdanskiy/.gemini/oauth_creds.json'

def get_calendar_events():
    creds = None
    if os.path.exists(TOKEN_PATH):
        # Загружаем данные из oauth_creds.json как Credentials
        with open(TOKEN_PATH, 'r') as f:
            token_data = json.load(f)
            creds = Credentials(
                token=token_data.get('access_token'),
                refresh_token=token_data.get('refresh_token'),
                token_uri='https://oauth2.googleapis.com/token',
                client_id=token_data.get('client_id', '681255809395-oo8ft2oprdnrp9e3aqf6av3hmdib135j.apps.googleusercontent.com'),
                client_secret=token_data.get('client_secret'),
                scopes=token_data.get('scope', SCOPES)
            )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Сохраняем обновленный токен обратно
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('⏳ Fetching events from Google Calendar...')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('📭 No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"📅 {start} - {event['summary']}")

    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    get_calendar_events()