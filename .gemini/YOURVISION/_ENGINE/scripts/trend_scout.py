#!/usr/bin/env python3
import sys
from pytrends.request import TrendReq

def check_trends(keywords):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [keywords] if isinstance(keywords, str) else keywords
        pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='')
        
        data = pytrends.interest_over_time()
        if not data.empty:
            peak = data[kw_list[0]].max()
            print(f"📈 TREND SCORE ({kw_list[0]}): {peak}/100")
            if peak > 80: print("🔥 STATUS: VIRAL BREAKOUT")
            elif peak > 50: print("✅ STATUS: HEALTHY INTEREST")
            else: print("❄️ STATUS: COLD")
        else:
            print("⚠️ No trend data found.")
    except Exception as e:
        print(f"❌ Trend API Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 trend_scout.py 'Keyword'")
    else:
        check_trends(sys.argv[1])