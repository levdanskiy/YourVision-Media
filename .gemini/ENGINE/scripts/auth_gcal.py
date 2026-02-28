#!/usr/bin/env python3
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = '/home/levdanskiy/.gemini/oauth_creds.json'
TOKEN_FILE = '/home/levdanskiy/.gemini/token.json'

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Запускаем локальный сервер для перехвата колбэка
            # Если это удаленный сервер, нужно использовать console strategy
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    print("✅ Authentication successful! Token saved.")

if __name__ == "__main__":
    authenticate()
