#!/usr/bin/env python3
"""
YourVision Triple Sync
Тройная синхронизация календарей

При появлении нового события обновляет:
1. JSON базу данных
2. Markdown Live Calendar
3. Мастер-план месяца
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class TripleSync:
    """Тройная синхронизация календарей YourVision"""

    def __init__(self, base_path: str = ".gemini"):
        self.base_path = Path(base_path).expanduser()
        self.json_path = self.base_path / "TIMELINE" / "database" / "yv_season_2026.json"
        self.calendar_path = self.base_path / "KNOWLEDGE" / "Live_Calendars" / "YV_ESC_Live_Calendar.md"
        self.plans_path = self.base_path / "TIMELINE" / "master_plans"

    def add_event(self, event: Dict) -> Dict:
        """
        Добавление события во все три источника

        Args:
            event: {
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
                "country": "Код страны (IT, ES, SE...)",
                "country_name": "Название страны",
                "event": "Описание события",
                "type": "RELEASE/FINAL/HEAT/CHART/SEMI",
                "status": "CONFIRMED/TBA",
                "link": "URL (опционально)"
            }

        Returns:
            Результат синхронизации
        """
        result = {
            "success": True,
            "json_updated": False,
            "calendar_updated": False,
            "plan_updated": False,
            "errors": []
        }

        try:
            # 1. Обновление JSON базы
            result["json_updated"] = self._update_json(event)

            # 2. Обновление Markdown календаря
            result["calendar_updated"] = self._update_calendar(event)

            # 3. Обновление мастер-плана
            result["plan_updated"] = self._update_master_plan(event)

        except Exception as e:
            result["success"] = False
            result["errors"].append(str(e))

        return result

    def update_status(self, event_id: str, new_status: str) -> Dict:
        """
        Обновление статуса события

        Args:
            event_id: ID события (например, "EVT001")
            new_status: Новый статус (CONFIRMED, COMPLETED, CANCELLED)
        """
        result = {
            "success": True,
            "errors": []
        }

        try:
            # Обновляем только JSON (календарь и план не требуют обновления статуса)
            if not self.json_path.exists():
                result["success"] = False
                result["errors"].append("JSON database not found")
                return result

            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Поиск и обновление события
            for event in data.get("events", []):
                if event.get("id") == event_id:
                    event["status"] = new_status
                    break

            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            result["success"] = False
            result["errors"].append(str(e))

        return result

    def mark_plan_complete(self, date: datetime, task_text: str) -> bool:
        """
        Отметить задачу в плане как выполненную

        Меняет ⬜ [ОЖИДАНИЕ] на ✅ [ГОТОВО]
        """
        plan_path = self.plans_path / date.strftime("%m") / f"YV_Plan_{date.strftime('%m')}.md"

        if not plan_path.exists():
            return False

        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Замена статуса
        new_content = content.replace(
            f"{task_text} - ⬜ [ОЖИДАНИЕ]",
            f"{task_text} - ✅ [ГОТОВО]"
        )

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    def _update_json(self, event: Dict) -> bool:
        """Обновление JSON базы данных"""
        # Создаём директорию если не существует
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        # Загружаем существующие данные
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"events": [], "version": "2.5"}

        # Генерируем ID если нет
        if "id" not in event:
            event["id"] = f"EVT{len(data['events']) + 1:03d}"

        # Проверяем на дубликаты
        existing_ids = [e.get("id") for e in data.get("events", [])]
        if event["id"] not in existing_ids:
            data["events"].append(event)

        # Сортируем по дате
        data["events"].sort(key=lambda x: x.get("date", ""))

        # Сохраняем
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    def _update_calendar(self, event: Dict) -> bool:
        """Обновление Markdown Live Calendar"""
        # Создаём директорию если не существует
        self.calendar_path.parent.mkdir(parents=True, exist_ok=True)

        # Парсим дату
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        flag = self._get_flag(event.get("country", ""))

        # Формируем строку
        line = f"* {date.strftime('%d.%m')} {flag} **{event.get('country_name', '')}**: {event.get('event', '')} ({event.get('time', '')})\n"

        # Проверяем на дубликаты
        if self.calendar_path.exists():
            with open(self.calendar_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if line.strip() in content:
                return True  # Уже существует

        # Добавляем строку
        with open(self.calendar_path, 'a', encoding='utf-8') as f:
            f.write(line)

        return True

    def _update_master_plan(self, event: Dict) -> bool:
        """Обновление мастер-плана месяца"""
        # Парсим дату
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        month = date.strftime("%m")

        # Путь к плану
        plan_path = self.plans_path / month / f"YV_Plan_{month}.md"
        plan_path.parent.mkdir(parents=True, exist_ok=True)

        # Формируем строку задачи
        flag = self._get_flag(event.get("country", ""))
        time = event.get("time", "")
        country = event.get("country_name", "")
        event_name = event.get("event", "")

        line = f"* {time} | **YV** | ⚡ **#NEWS_WIRE:** {flag} {country}. {event_name}. - ⬜ [ОЖИДАНИЕ]\n"

        # Проверяем на дубликаты
        if plan_path.exists():
            with open(plan_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if line.strip() in content:
                return True

        # Добавляем заголовок если файл новый
        if not plan_path.exists():
            header = f"# 📋 МАСТЕР-ПЛАН: {self._get_month_name(month)} 2026\n\n"
            header += "---\n\n"
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(header)

        # Добавляем задачу
        with open(plan_path, 'a', encoding='utf-8') as f:
            f.write(line)

        return True

    def _get_flag(self, country: str) -> str:
        """Получение флага по коду страны"""
        flags = {
            "IT": "🇮🇹", "Италия": "🇮🇹",
            "ES": "🇪🇸", "Испания": "🇪🇸",
            "SE": "🇸🇪", "Швеция": "🇸🇪",
            "UA": "🇺🇦", "Украина": "🇺🇦",
            "RS": "🇷🇸", "Сербия": "🇷🇸",
            "AU": "🇦🇺", "Австралия": "🇦🇺",
            "GB": "🇬🇧", "UK": "🇬🇧", "Великобритания": "🇬🇧",
            "FR": "🇫🇷", "Франция": "🇫🇷",
            "DE": "🇩🇪", "Германия": "🇩🇪",
            "NO": "🇳🇴", "Норвегия": "🇳🇴",
            "NL": "🇳🇱", "Нидерланды": "🇳🇱",
            "CH": "🇨🇭", "Швейцария": "🇨🇭",
            "PL": "🇵🇱", "Польша": "🇵🇱",
            "CZ": "🇨🇿", "Чехия": "🇨🇿",
            "FI": "🇫🇮", "Финляндия": "🇫🇮",
            "DK": "🇩🇰", "Дания": "🇩🇰",
            "BE": "🇧🇪", "Бельгия": "🇧🇪",
            "AT": "🇦🇹", "Австрия": "🇦🇹",
            "GR": "🇬🇷", "Греция": "🇬🇷",
            "CY": "🇨🇾", "Кипр": "🇨🇾",
            "IL": "🇮🇱", "Израиль": "🇮🇱",
            "HR": "🇭🇷", "Хорватия": "🇭🇷",
            "SI": "🇸🇮", "Словения": "🇸🇮",
            "EE": "🇪🇪", "Эстония": "🇪🇪",
            "LT": "🇱🇹", "Литва": "🇱🇹",
            "LV": "🇱🇻", "Латвия": "🇱🇻",
            "PT": "🇵🇹", "Португалия": "🇵🇹",
            "RO": "🇷🇴", "Румыния": "🇷🇴",
            "MD": "🇲🇩", "Молдова": "🇲🇩",
            "AL": "🇦🇱", "Албания": "🇦🇱",
            "AM": "🇦🇲", "Армения": "🇦🇲",
            "GE": "🇬🇪", "Грузия": "🇬🇪",
            "AZ": "🇦🇿", "Азербайджан": "🇦🇿",
            "SM": "🇸🇲", "Сан-Марино": "🇸🇲",
            "MT": "🇲🇹", "Мальта": "🇲🇹",
            "LU": "🇱🇺", "Люксембург": "🇱🇺",
            "IE": "🇮🇪", "Ирландия": "🇮🇪",
            "IS": "🇮🇸", "Исландия": "🇮🇸",
        }
        return flags.get(country, flags.get(country.upper(), "🏳️"))

    def _get_month_name(self, month: str) -> str:
        """Получение названия месяца на русском"""
        months = {
            "01": "Январь", "02": "Февраль", "03": "Март",
            "04": "Апрель", "05": "Май", "06": "Июнь",
            "07": "Июль", "08": "Август", "09": "Сентябрь",
            "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"
        }
        return months.get(month, month)


# CLI Interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="YourVision Triple Sync")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Добавить событие")
    add_parser.add_argument("--date", required=True, help="Дата YYYY-MM-DD")
    add_parser.add_argument("--time", required=True, help="Время HH:MM")
    add_parser.add_argument("--country", required=True, help="Код страны")
    add_parser.add_argument("--country-name", required=True, help="Название страны")
    add_parser.add_argument("--event", required=True, help="Описание события")
    add_parser.add_argument("--type", default="HEAT", help="Тип события")
    add_parser.add_argument("--link", default="", help="URL")

    # status
    status_parser = subparsers.add_parser("status", help="Обновить статус")
    status_parser.add_argument("--id", required=True, help="ID события")
    status_parser.add_argument("--status", required=True, help="Новый статус")

    # complete
    complete_parser = subparsers.add_parser("complete", help="Отметить задачу выполненной")
    complete_parser.add_argument("--date", required=True, help="Дата DD.MM.YYYY")
    complete_parser.add_argument("--task", required=True, help="Текст задачи")

    args = parser.parse_args()

    sync = TripleSync()

    if args.command == "add":
        event = {
            "date": args.date,
            "time": args.time,
            "country": args.country,
            "country_name": args.country_name,
            "event": args.event,
            "type": args.type,
            "status": "CONFIRMED",
            "link": args.link
        }
        result = sync.add_event(event)

        if result["success"]:
            print("✅ Тройная синхронизация завершена:")
            print(f"   JSON: {'✓' if result['json_updated'] else '✗'}")
            print(f"   Calendar: {'✓' if result['calendar_updated'] else '✗'}")
            print(f"   Plan: {'✓' if result['plan_updated'] else '✗'}")
        else:
            print(f"❌ Ошибка: {result['errors']}")

    elif args.command == "status":
        result = sync.update_status(args.id, args.status)
        if result["success"]:
            print(f"✅ Статус обновлён: {args.id} → {args.status}")
        else:
            print(f"❌ Ошибка: {result['errors']}")

    elif args.command == "complete":
        date = datetime.strptime(args.date, "%d.%m.%Y")
        if sync.mark_plan_complete(date, args.task):
            print("✅ Задача отмечена как выполненная")
        else:
            print("❌ Не удалось найти задачу")


if __name__ == "__main__":
    main()
