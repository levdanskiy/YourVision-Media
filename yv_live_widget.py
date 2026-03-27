import requests
import datetime
import time
import sys
import logging

# YourVision Live Pinned Widget Script V1.1
TOKEN = '8687268784:AAEg59N9z0Fryad5MU3lf9BwIXv3RRfi2qg'
CHAT_ID = -1001588837632

# Setup logging
logging.basicConfig(
    filename='/home/levdanskiy/yv_live_widget.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

DATES = {
    'SF1': datetime.datetime(2026, 5, 12, 22, 0),
    'SF2': datetime.datetime(2026, 5, 14, 22, 0),
    'GF': datetime.datetime(2026, 5, 16, 22, 0)
}

def get_countdown():
    now = datetime.datetime.now()
    text = "📊 **YOURVISION 2026: LIVE ROADMAP**\n"
    text += "📍 *Время в Риге: " + now.strftime("%H:%M") + "*\n\n"
    
    for key, target in DATES.items():
        delta = target - now
        name = "1-й Полуфинал" if key == 'SF1' else "2-й Полуфинал" if key == 'SF2' else "Гранд-Финал"
        if delta.total_seconds() > 0:
            text += f"🔹 **{name}:**\n`{delta.days}д {delta.seconds//3600}ч {(delta.seconds//60)%60}m` до эфира\n\n"
        else:
            text += f"🔥 **{name}:** В ЭФИРЕ!\n\n"
            
    text += "---\n`🔄 Обновляется автоматически`"
    return text

def update_message(msg_id):
    url = f"https://api.telegram.org/bot{TOKEN}/editMessageText"
    payload = {
        "chat_id": CHAT_ID,
        "message_id": msg_id,
        "text": get_countdown(),
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        if data.get('ok'):
            logging.info(f"Successfully updated message {msg_id}")
        else:
            logging.error(f"Failed to update message {msg_id}: {data}")
        return data
    except Exception as e:
        logging.error(f"Error connecting to Telegram: {e}")
        return {"ok": False}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg_id = int(sys.argv[1])
        logging.info(f"--- Service Started for Message {msg_id} ---")
        while True:
            update_message(msg_id)
            time.sleep(60) 
    else:
        print("Usage: python3 yv_live_widget.py MSG_ID")
