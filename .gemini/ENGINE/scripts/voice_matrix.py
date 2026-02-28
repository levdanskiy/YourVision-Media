#!/usr/bin/env python3
import sys
from textblob import TextBlob

def analyze_voice(text, channel):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity # -1.0 to 1.0
    subjectivity = blob.sentiment.subjectivity # 0.0 to 1.0
    
    # Идеальные параметры для каналов
    standards = {
        "AC": {"sentiment": (0.0, 0.3), "subjectivity": (0.0, 0.4)}, # Нейтрально, объективно
        "SW": {"sentiment": (0.4, 1.0), "subjectivity": (0.6, 1.0)}, # Позитивно, чувственно
        "NB": {"sentiment": (0.1, 0.6), "subjectivity": (0.4, 0.8)}, # Умеренно, описательно
        "YV": {"sentiment": (-0.2, 0.5), "subjectivity": (0.2, 0.7)} # Динамично, экспертно
    }
    
    std = standards.get(channel, {"sentiment": (0,0), "subjectivity": (0,0)})
    
    # Мягкая проверка (вывод предупреждений)
    status = "VERIFIED"
    if not (std["sentiment"][0] <= sentiment <= std["sentiment"][1]):
        status = "OUT OF TONE"
        
    return f"Voice: {channel} | Polarity: {sentiment:.2f} | Subjectivity: {subjectivity:.2f} | Status: {status}"

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    print(analyze_voice(sys.argv[1], sys.argv[2]))
