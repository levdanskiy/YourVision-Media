#!/usr/bin/env python3
import datetime
import math

def get_moon_phase(date):
    """Рассчитывает фазу луны (0-7: Новолуние, Растущая, Первая четверть и т.д.)"""
    # Известное новолуние: 6 января 2000 года
    diff = date - datetime.datetime(2000, 1, 6, 18, 14)
    days = diff.total_seconds() / 86400
    lunation = days / 29.53058867
    phase_index = int((lunation - math.floor(lunation)) * 8 + 0.5) % 8
    
    phases = [
        "Новолуние", "Растущий серп", "Первая четверть", "Растущая луна",
        "Полнолуние", "Убывающая луна", "Последняя четверть", "Старая луна"
    ]
    return phases[phase_index]

def get_solar_event(date):
    """Определяет ближайшую точку Колеса Года"""
    events = [
        (datetime.datetime(date.year, 3, 20), "Остара (Равноденствие)"),
        (datetime.datetime(date.year, 6, 21), "Лита (Солнцестояние)"),
        (datetime.datetime(date.year, 9, 22), "Мабон (Равноденствие)"),
        (datetime.datetime(date.year, 12, 21), "Йоль (Солнцестояние)")
    ]
    # Находим ближайшее событие в будущем
    for event_date, name in events:
        if event_date > date:
            days_left = (event_date - date).days
            return f"{name} через {days_left} дн."
    return "Колесо года завершает цикл"

if __name__ == "__main__":
    now = datetime.datetime.now()
    print(f"Фаза Луны: {get_moon_phase(now)}")
    print(f"Солнечный цикл: {get_solar_event(now)}")
