#!/usr/bin/env python3
import json
import urllib.parse

# Найденный Client ID
CLIENT_ID = "681255809395-oo8ft2oprdnrp9e3aqf6av3hmdib135j.apps.googleusercontent.com"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
SCOPE = "https://www.googleapis.com/auth/calendar.readonly"

def generate_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    
    print("\n⚠️  ДЕЙСТВИЕ ТРЕБУЕТСЯ ОТ ПОЛЬЗОВАТЕЛЯ ⚠️")
    print("1. Скопируйте эту ссылку и откройте в браузере:")
    print(f"\n{url}\n")
    print("2. Авторизуйтесь и скопируйте полученный КОД.")
    print("3. Отправьте мне сообщение: 'КОД КАЛЕНДАРЯ: [Ваш Код]'")

if __name__ == "__main__":
    generate_url()

