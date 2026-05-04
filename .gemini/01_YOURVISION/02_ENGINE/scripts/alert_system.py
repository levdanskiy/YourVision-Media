#!/usr/bin/env python3
"""
YourVision Alert System
Система оповещений и мониторинга
"""

import json
import re
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Callable
from pathlib import Path


class AlertTier(Enum):
    RED = "red"       # 5 минут реакция
    YELLOW = "yellow" # 30 минут реакция
    GREEN = "green"   # по расписанию


class EventType(Enum):
    WINNER_ANNOUNCED = "winner_announced"
    DISQUALIFICATION = "disqualification"
    WITHDRAWAL = "withdrawal"
    DATE_CHANGE = "date_change"
    CITY_CHANGE = "city_change"
    SONG_RELEASE = "song_release"
    ARTIST_ANNOUNCED = "artist_announced"
    RUMOUR_CONFIRMED = "rumour_confirmed"
    INTERVAL_ACT = "interval_act"
    GENERAL_NEWS = "general_news"


@dataclass
class AlertKeyword:
    keywords: List[str]
    event_type: EventType
    tier: AlertTier
    description: str


# Ключевые слова для определения типа события
ALERT_KEYWORDS = [
    # RED ALERT
    AlertKeyword(
        keywords=["победил", "победитель", "выиграл", "won", "winner"],
        event_type=EventType.WINNER_ANNOUNCED,
        tier=AlertTier.RED,
        description="Объявлен победитель"
    ),
    AlertKeyword(
        keywords=["дисквалифицирован", "дисквалификация", "disqualified", "disqualification"],
        event_type=EventType.DISQUALIFICATION,
        tier=AlertTier.RED,
        description="Дисквалификация"
    ),
    AlertKeyword(
        keywords=["снялся", "отказался", "withdrawal", "withdrew", "снял заявку"],
        event_type=EventType.WITHDRAWAL,
        tier=AlertTier.RED,
        description="Участник снялся"
    ),
    AlertKeyword(
        keywords=["перенос", "новая дата", "changed date", "rescheduled"],
        event_type=EventType.DATE_CHANGE,
        tier=AlertTier.RED,
        description="Изменение даты"
    ),
    AlertKeyword(
        keywords=["новый город", "место проведения", "host city", "venue"],
        event_type=EventType.CITY_CHANGE,
        tier=AlertTier.RED,
        description="Изменение города/места"
    ),

    # YELLOW ALERT
    AlertKeyword(
        keywords=["релиз", "выпустил песню", "новая песня", "released", "new song", "single"],
        event_type=EventType.SONG_RELEASE,
        tier=AlertTier.YELLOW,
        description="Релиз песни"
    ),
    AlertKeyword(
        keywords=["представитель", "участник", "участница", "represent", "participant"],
        event_type=EventType.ARTIST_ANNOUNCED,
        tier=AlertTier.YELLOW,
        description="Объявлен участник"
    ),
    AlertKeyword(
        keywords=["подтверждён", "официально", "confirmed", "official"],
        event_type=EventType.RUMOUR_CONFIRMED,
        tier=AlertTier.YELLOW,
        description="Слух подтверждён"
    ),

    # GREEN ALERT
    AlertKeyword(
        keywords=["интервью", "аналитика", "обзор", "interview", "analysis", "review"],
        event_type=EventType.GENERAL_NEWS,
        tier=AlertTier.GREEN,
        description="Обычная новость"
    ),
]


@dataclass
class Alert:
    event_type: EventType
    tier: AlertTier
    title: str
    content: str
    source: str
    detected_at: datetime
    deadline: datetime
    processed: bool = False

    def time_remaining(self) -> timedelta:
        return self.deadline - datetime.now()


class AlertSystem:
    """Система оповещений YourVision"""

    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path) if config_path else None
        self.alerts: List[Alert] = []
        self.handlers: Dict[AlertTier, List[Callable]] = {
            AlertTier.RED: [],
            AlertTier.YELLOW: [],
            AlertTier.GREEN: [],
        }

    def analyze_content(self, text: str, source: str = "") -> Optional[Alert]:
        """Анализ контента на наличие алерт-триггеров"""
        text_lower = text.lower()
        detected_keywords = []

        for alert_kw in ALERT_KEYWORDS:
            for keyword in alert_kw.keywords:
                if keyword.lower() in text_lower:
                    detected_keywords.append((keyword, alert_kw))

        if not detected_keywords:
            return None

        # Берём наиболее критичный (RED > YELLOW > GREEN)
        detected_keywords.sort(key=lambda x: list(AlertTier).index(x[1].tier))
        _, best_match = detected_keywords[0]

        # Вычисляем дедлайн
        deadline_minutes = {
            AlertTier.RED: 5,
            AlertTier.YELLOW: 30,
            AlertTier.GREEN: 240,  # 4 часа
        }

        deadline = datetime.now() + timedelta(minutes=deadline_minutes[best_match.tier])

        alert = Alert(
            event_type=best_match.event_type,
            tier=best_match.tier,
            title=best_match.description,
            content=text[:500],  # Первые 500 символов
            source=source,
            detected_at=datetime.now(),
            deadline=deadline
        )

        self.alerts.append(alert)
        return alert

    def get_active_alerts(self) -> List[Alert]:
        """Получить активные (необработанные) алерты"""
        return [a for a in self.alerts if not a.processed and a.time_remaining().total_seconds() > 0]

    def get_overdue_alerts(self) -> List[Alert]:
        """Получить просроченные алерты"""
        return [a for a in self.alerts if not a.processed and a.time_remaining().total_seconds() <= 0]

    def mark_processed(self, alert: Alert):
        """Отметить алерт как обработанный"""
        alert.processed = True

    def register_handler(self, tier: AlertTier, handler: Callable):
        """Регистрация обработчика для определённого тира"""
        self.handlers[tier].append(handler)

    def trigger_handlers(self, alert: Alert):
        """Запуск обработчиков для алерта"""
        for handler in self.handlers[alert.tier]:
            try:
                handler(alert)
            except Exception as e:
                print(f"Handler error: {e}")

    def get_status_report(self) -> Dict:
        """Получить отчёт о статусе системы"""
        active = self.get_active_alerts()
        overdue = self.get_overdue_alerts()

        return {
            "total_alerts": len(self.alerts),
            "active_alerts": len(active),
            "overdue_alerts": len(overdue),
            "by_tier": {
                "red": len([a for a in active if a.tier == AlertTier.RED]),
                "yellow": len([a for a in active if a.tier == AlertTier.YELLOW]),
                "green": len([a for a in active if a.tier == AlertTier.GREEN]),
            },
            "overdue_by_tier": {
                "red": len([a for a in overdue if a.tier == AlertTier.RED]),
                "yellow": len([a for a in overdue if a.tier == AlertTier.YELLOW]),
                "green": len([a for a in overdue if a.tier == AlertTier.GREEN]),
            }
        }

    def print_status(self):
        """Вывод статуса в консоль"""
        report = self.get_status_report()

        print("\n" + "="*50)
        print("🔔 ALERT SYSTEM STATUS")
        print("="*50)
        print(f"📊 Total alerts: {report['total_alerts']}")
        print(f"🔴 Active RED: {report['by_tier']['red']}")
        print(f"🟡 Active YELLOW: {report['by_tier']['yellow']}")
        print(f"🟢 Active GREEN: {report['by_tier']['green']}")

        if report['overdue_alerts'] > 0:
            print(f"\n⚠️ OVERDUE ALERTS: {report['overdue_alerts']}")
            print("🔴 Overdue RED:", report['overdue_by_tier']['red'])
            print("🟡 Overdue YELLOW:", report['overdue_by_tier']['yellow'])

        print("="*50 + "\n")


class PostingSchedule:
    """Менеджер расписания публикаций"""

    # Оптимальные окна (UTC+3)
    OPTIMAL_WINDOWS = {
        0: {"day": "Понедельник", "peak": "19:00-21:00", "optimal": "18:30"},
        1: {"day": "Вторник", "peak": "20:00-22:00", "optimal": "19:30"},
        2: {"day": "Среда", "peak": "20:00-22:00", "optimal": "19:30"},
        3: {"day": "Четверг", "peak": "19:00-21:00", "optimal": "18:30"},
        4: {"day": "Пятница", "peak": "18:00-20:00", "optimal": "17:30"},
        5: {"day": "Суббота", "peak": "12:00-14:00, 20:00-23:00", "optimal": "11:30, 20:00"},
        6: {"day": "Воскресенье", "peak": "20:00-22:00", "optimal": "19:30"},
    }

    BLACKOUT_START = 1   # 01:00
    BLACKOUT_END = 6     # 06:00

    @classmethod
    def is_blackout(cls, hour: int, is_live: bool = False) -> bool:
        """Проверка на blackout-период"""
        if is_live:
            return False
        return cls.BLACKOUT_START <= hour < cls.BLACKOUT_END

    @classmethod
    def get_optimal_time(cls, weekday: int) -> str:
        """Получить оптимальное время для публикации"""
        return cls.OPTIMAL_WINDOWS.get(weekday, {}).get("optimal", "19:00")

    @classmethod
    def suggest_posting_time(cls) -> Dict:
        """Предложить время публикации"""
        now = datetime.now()

        if cls.is_blackout(now.hour):
            return {
                "status": "blackout",
                "message": f"Blackout period (01:00-06:00). Wait until 06:00 or mark as LIVE event.",
                "current_hour": now.hour
            }

        optimal = cls.get_optimal_time(now.weekday())
        return {
            "status": "ok",
            "optimal_time": optimal,
            "current_time": now.strftime("%H:%M"),
            "day": cls.OPTIMAL_WINDOWS[now.weekday()]["day"]
        }


# CLI Interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="YourVision Alert System")
    parser.add_argument("--analyze", type=str, help="Текст для анализа")
    parser.add_argument("--status", action="store_true", help="Показать статус")
    parser.add_argument("--schedule", action="store_true", help="Проверить расписание")

    args = parser.parse_args()

    system = AlertSystem()

    if args.analyze:
        alert = system.analyze_content(args.analyze)
        if alert:
            print(f"\n🚨 ALERT DETECTED!")
            print(f"   Tier: {alert.tier.value.upper()}")
            print(f"   Type: {alert.event_type.value}")
            print(f"   Deadline: {alert.deadline.strftime('%H:%M:%S')}")
            print(f"   Time remaining: {alert.time_remaining()}")
        else:
            print("\n✅ No alert triggers detected (GREEN tier)")

    if args.status:
        system.print_status()

    if args.schedule:
        suggestion = PostingSchedule.suggest_posting_time()
        if suggestion["status"] == "blackout":
            print(f"\n⛔ {suggestion['message']}")
        else:
            print(f"\n📅 Optimal posting time: {suggestion['optimal_time']}")
            print(f"   Current time: {suggestion['current_time']}")
            print(f"   Day: {suggestion['day']}")


if __name__ == "__main__":
    main()
