#!/usr/bin/env python3
import yfinance as yf
import json
import os

def get_market_pulse():
    """Пункты 71-72: Анализ глобальной энергии через рынки"""
    try:
        # Золото (GC=F) и Биткоин (BTC-USD)
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
        eur = yf.Ticker("EURUSD=X").history(period="1d")['Close'].iloc[-1]
        
        return {
            "GOLD": round(gold, 2),
            "BTC": round(btc, 2),
            "EUR_USD": round(eur, 4),
            "status": "Market Alchemy Active"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(json.dumps(get_market_pulse(), indent=4))
