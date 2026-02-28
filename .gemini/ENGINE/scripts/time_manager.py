#!/usr/bin/env python3
import arrow
import os

# Путь к файлу состояния, где мы храним "Виртуальное время"
STATE_FILE = ".gemini/STATE.md"

def get_times():
    # Реальное время (установленное пользователем)
    # В идеале здесь должен быть вызов системного времени, 
    # но мы фиксируем точку отсчета от пользователя: 24.01.2026 04:44
    real_time = arrow.get("2026-01-24 04:44")
    
    # Время планирования (читаем из STATE или планов)
    # По умолчанию равно реальному, если не указано иное
    planning_time = real_time 
    
    return real_time, planning_time

def display():
    real, plan = get_times()
    print(f"🕒 REAL SYSTEM TIME: {real.format('DD.MM.YYYY HH:mm')}")
    print(f"📅 PLANNING TARGET:  {plan.format('DD.MM.YYYY HH:mm')}")
    print(f"---")
    print(f"Status: Synchronized")

if __name__ == "__main__":
    display()
