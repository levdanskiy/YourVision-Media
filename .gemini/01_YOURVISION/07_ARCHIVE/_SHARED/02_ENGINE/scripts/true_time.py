#!/usr/bin/env python3
import datetime

def get_true_time():
    now = datetime.datetime.now()
    print(f"🕒 TRUE TIME: {now.strftime('%d.%m.%Y | %H:%M:%S')}")
    return now

if __name__ == "__main__":
    get_true_time()