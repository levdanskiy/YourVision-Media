#!/usr/bin/env python3
"""
YourVision Aliases Handler
Обработчик системных команд (алиасов)
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List


class YVAliases:
    """Обработчик алиасов YourVision"""

    def __init__(self, base_path: str = ".gemini"):
        self.base_path = Path(base_path).expanduser()
        self.database_path = self.base_path / "TIMELINE" / "database" / "yv_season_2026.json"
        self.plans_path = self.base_path / "TIMELINE" / "master_plans"

    def yv_plan(self, date_str: Optional[str] = None) -> Dict:
        """
        yv_plan [ДД.ММ.ГГГГ] - Генерация плана на день

        Генерирует план на основе базы событий.
        Проверяет незакрытые задачи за прошлые дни (долги).
        """
        # Парсинг даты
        if date_str:
            target_date = datetime.strptime(date_str, "%d.%m.%Y")
        else:
            target_date = datetime.now()

        result = {
            "date": target_date.strftime("%d.%m.%Y"),
            "weekday": self._get_weekday_ru(target_date),
            "events": [],
            "debts": [],
        }

        # Загрузка событий из JSON
        events = self._load_events_for_date(target_date)
        result["events"] = events

        # Проверка долгов
        debts = self._check_debts(target_date)
        result["debts"] = debts

        # Генерация markdown плана
        plan_md = self._generate_plan_md(result)

        # Сохранение плана
        plan_path = self._save_plan(target_date, plan_md)
        result["plan_path"] = str(plan_path)

        return result

    def yv_guide(self) -> Dict:
        """
        yv_guide - Гид по эфирам на сегодня

        Создаёт пост Grade F со списком шоу на вечер.
        Проверяет актуальность ссылок.
        """
        today = datetime.now()
        events = self._load_events_for_date(today)

        # Фильтруем только события на вечер
        evening_events = [e for e in events if self._is_evening_event(e)]

        # Генерация гида
        guide_lines = [
            f"📺 **ГИД ПО ЭФИРАМ - {today.strftime('%d.%m.%Y')}**",
            "",
        ]

        for event in evening_events:
            flag = self._get_flag(event.get("country", ""))
            time = event.get("time", "")
            name = event.get("event", "")
            link = event.get("link", "")

            guide_lines.append(f"• {time} {flag} **{name}**")
            if link:
                guide_lines.append(f"  🔗 [{link}]({link})")

        guide_lines.append("")
        guide_lines.append("🎧 **СЛУШАТЬ ЭФИР:** [levdanskiy](https://myradio24.com/levdanskiy)")

        content = "\n".join(guide_lines)

        return {
            "content": content,
            "grade": "F",
            "events_count": len(evening_events),
        }

    def yv_week(self) -> Dict:
        """
        yv_week - Roadmap на неделю

        Генерирует пост Grade B/C со списком главных событий недели.
        """
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        result = {
            "week_start": week_start.strftime("%d.%m"),
            "week_end": week_end.strftime("%d.%m"),
            "days": {},
        }

        for i in range(7):
            day = week_start + timedelta(days=i)
            events = self._load_events_for_date(day)
            if events:
                result["days"][day.strftime("%d.%m")] = events

        # Генерация roadmap
        roadmap_lines = [
            f"📅 **ROADMAP НЕДЕЛИ: {week_start.strftime('%d.%m')} - {week_end.strftime('%d.%m')}**",
            "",
        ]

        for date_str, events in result["days"].items():
            roadmap_lines.append(f"**{date_str}**")
            for event in events:
                flag = self._get_flag(event.get("country", ""))
                time = event.get("time", "")
                name = event.get("event", "")
                roadmap_lines.append(f"  • {time} {flag} {name}")
            roadmap_lines.append("")

        content = "\n".join(roadmap_lines)

        return {
            "content": content,
            "grade": "B",
            "days_with_events": len(result["days"]),
        }

    def yv_history(self, date_str: str) -> Dict:
        """
        yv_history [ДД.ММ.] - Исторический пост

        Генерирует пост #EUROFLASHBACK для указанной даты.
        При отсутствии данных предлагает веб-поиск.
        """
        # Парсинг даты
        day, month = date_str.split(".")
        target_date = datetime(2024, int(month), int(day))  # Год не важен

        # Поиск исторических событий
        history_events = self._load_history_events(day, month)

        if not history_events:
            return {
                "content": None,
                "needs_web_search": True,
                "search_query": f"Eurovision history {day} {month} events",
            }

        # Генерация поста
        lines = [f"🕰️ **#EUROFLASHBACK: {day}.{month}**", ""]

        for event in history_events:
            year = event.get("year", "")
            text = event.get("event", "")
            lines.append(f"• **{year}:** {text}")

        content = "\n".join(lines)

        return {
            "content": content,
            "grade": "S",
            "events_found": len(history_events),
        }

    def yv_pub(self, text: str, source_url: Optional[str] = None) -> Dict:
        """
        yv_pub [текст/ссылка] - Срочная публикация

        Оценивает инфоповод, выбирает грейд, пишет пост, валидирует, сохраняет.
        """
        from yv_publisher import YVPublisher, Post, PostType, AlertTier, Grade

        # Анализ контента
        alert_tier = self._analyze_content_tier(text)
        post_type = self._determine_post_type(text)

        # Определение страны и флага
        country, flag = self._extract_country(text)

        # Создание поста
        post = Post(
            post_type=post_type,
            title=self._generate_title(text),
            content=text,
            country=country,
            country_flag=flag,
            alert_tier=alert_tier,
        )

        # Публикация
        publisher = YVPublisher()
        result = publisher.validate_and_publish(post)

        if result["success"]:
            publisher.git_sync(f"feat: {post_type.value} - {country}")

        return result

    # Вспомогательные методы

    def _load_events_for_date(self, date: datetime) -> List[Dict]:
        """Загрузка событий из JSON для указанной даты"""
        if not self.database_path.exists():
            return []

        with open(self.database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        date_str = date.strftime("%Y-%m-%d")
        return [e for e in data.get("events", []) if e.get("date") == date_str]

    def _check_debts(self, current_date: datetime) -> List[Dict]:
        """Проверка незакрытых задач за прошлые дни"""
        debts = []

        # Проверяем последние 7 дней
        for i in range(1, 8):
            check_date = current_date - timedelta(days=i)
            plan_path = self.plans_path / check_date.strftime("%m") / f"YV_Plan_{check_date.strftime('%m')}.md"

            if plan_path.exists():
                with open(plan_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Ищем незакрытые задачи
                if "⬜ [ОЖИДАНИЕ]" in content:
                    debts.append({
                        "date": check_date.strftime("%d.%m.%Y"),
                        "plan_path": str(plan_path),
                    })

        return debts

    def _generate_plan_md(self, plan_data: Dict) -> str:
        """Генерация markdown плана"""
        lines = [
            f"# 📋 ПЛАН НА {plan_data['date']} ({plan_data['weekday']})",
            "",
        ]

        if plan_data["debts"]:
            lines.append("## ⚠️ ДОЛГИ")
            for debt in plan_data["debts"]:
                lines.append(f"- [ ] {debt['date']}")
            lines.append("")

        lines.append("## 📅 СОБЫТИЯ ДНЯ")
        for event in plan_data["events"]:
            flag = self._get_flag(event.get("country", ""))
            time = event.get("time", "")
            name = event.get("event", "")
            lines.append(f"* {time} | **YV** | ⚡ **#NEWS_WIRE:** {flag} {name}. - ⬜ [ОЖИДАНИЕ]")

        lines.append("")
        lines.append("---")
        lines.append("*Сгенерировано yv_plan*")

        return "\n".join(lines)

    def _save_plan(self, date: datetime, content: str) -> Path:
        """Сохранение плана"""
        plan_dir = self.plans_path / date.strftime("%m")
        plan_dir.mkdir(parents=True, exist_ok=True)

        plan_path = plan_dir / f"daily_plan_{date.strftime('%d.%m')}.md"
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return plan_path

    def _is_evening_event(self, event: Dict) -> bool:
        """Проверка, является ли событие вечерним"""
        time_str = event.get("time", "")
        if not time_str:
            return False

        try:
            hour = int(time_str.split(":")[0])
            return hour >= 18
        except:
            return False

    def _load_history_events(self, day: str, month: str) -> List[Dict]:
        """Загрузка исторических событий"""
        # Здесь должна быть база исторических событий
        # Для демонстрации возвращаем пустой список
        return []

    def _analyze_content_tier(self, text: str) -> "AlertTier":
        """Анализ тира контента"""
        from yv_publisher import AlertTier

        red_keywords = ["победил", "победитель", "дисквалифи", "снял", "перенос"]
        yellow_keywords = ["релиз", "новая песня", "представитель", "подтвержд"]

        text_lower = text.lower()

        for kw in red_keywords:
            if kw in text_lower:
                return AlertTier.RED

        for kw in yellow_keywords:
            if kw in text_lower:
                return AlertTier.YELLOW

        return AlertTier.GREEN

    def _determine_post_type(self, text: str) -> "PostType":
        """Определение типа поста"""
        from yv_publisher import PostType

        length = len(text)

        if length <= 500:
            return PostType.FLASH
        elif length <= 1300:
            return PostType.SNAP
        else:
            return PostType.STANDARD

    def _extract_country(self, text: str) -> tuple:
        """Извлечение страны из текста"""
        countries = {
            "Сан-Ремо": ("Италия", "🇮🇹"),
            "Sanremo": ("Италия", "🇮🇹"),
            "Benidorm": ("Испания", "🇪🇸"),
            "Мелодифестивален": ("Швеция", "🇸🇪"),
            "Melodifestivalen": ("Швеция", "🇸🇪"),
            "Відбір": ("Украина", "🇺🇦"),
            "Песма": ("Сербия", "🇷🇸"),
        }

        for keyword, (country, flag) in countries.items():
            if keyword in text:
                return country, flag

        return "", ""

    def _generate_title(self, text: str) -> str:
        """Генерация заголовка из текста"""
        # Берём первое предложение
        sentences = text.split(".")
        if sentences:
            return sentences[0][:50]
        return text[:50]

    def _get_weekday_ru(self, date: datetime) -> str:
        """Получение дня недели на русском"""
        weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        return weekdays[date.weekday()]

    def _get_flag(self, country: str) -> str:
        """Получение флага по стране"""
        flags = {
            "Италия": "🇮🇹", "Italy": "🇮🇹", "IT": "🇮🇹",
            "Испания": "🇪🇸", "Spain": "🇪🇸", "ES": "🇪🇸",
            "Швеция": "🇸🇪", "Sweden": "🇸🇪", "SE": "🇸🇪",
            "Украина": "🇺🇦", "Ukraine": "🇺🇦", "UA": "🇺🇦",
            "Сербия": "🇷🇸", "Serbia": "🇷🇸", "RS": "🇷🇸",
            "Австралия": "🇦🇺", "Australia": "🇦🇺", "AU": "🇦🇺",
            "Великобритания": "🇬🇧", "UK": "🇬🇧",
            "Франция": "🇫🇷", "France": "🇫🇷", "FR": "🇫🇷",
            "Германия": "🇩🇪", "Germany": "🇩🇪", "DE": "🇩🇪",
            "Норвегия": "🇳🇴", "Norway": "🇳🇴", "NO": "🇳🇴",
            "Нидерланды": "🇳🇱", "Netherlands": "🇳🇱", "NL": "🇳🇱",
            "Швейцария": "🇨🇭", "Switzerland": "🇨🇭", "CH": "🇨🇭",
        }
        return flags.get(country, flags.get(country.upper(), "🏳️"))


# CLI Interface
def main():
    parser = argparse.ArgumentParser(description="YourVision Aliases Handler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # yv_plan
    plan_parser = subparsers.add_parser("plan", help="Сгенерировать план на день")
    plan_parser.add_argument("date", nargs="?", help="Дата в формате ДД.ММ.ГГГГ")

    # yv_guide
    subparsers.add_parser("guide", help="Создать гид по эфирам")

    # yv_week
    subparsers.add_parser("week", help="Сгенерировать roadmap на неделю")

    # yv_history
    history_parser = subparsers.add_parser("history", help="Сгенерировать исторический пост")
    history_parser.add_argument("date", help="Дата в формате ДД.ММ.")

    # yv_pub
    pub_parser = subparsers.add_parser("pub", help="Срочная публикация")
    pub_parser.add_argument("text", help="Текст или ссылка")
    pub_parser.add_argument("--source", help="URL источника")

    args = parser.parse_args()

    aliases = YVAliases()

    if args.command == "plan":
        result = aliases.yv_plan(args.date)
        print(f"📅 План на {result['date']} ({result['weekday']})")
        print(f"   Событий: {len(result['events'])}")
        if result['debts']:
            print(f"   ⚠️ Долгов: {len(result['debts'])}")
        print(f"   📄 Файл: {result['plan_path']}")

    elif args.command == "guide":
        result = aliases.yv_guide()
        print(result['content'])

    elif args.command == "week":
        result = aliases.yv_week()
        print(result['content'])

    elif args.command == "history":
        result = aliases.yv_history(args.date)
        if result.get("needs_web_search"):
            print(f"🔍 Требуется веб-поиск: {result['search_query']}")
        else:
            print(result['content'])

    elif args.command == "pub":
        result = aliases.yv_pub(args.text, args.source)
        if result['success']:
            print(f"✅ Опубликовано: {result['filepath']}")
        else:
            print(f"❌ Ошибка: {result['errors']}")


if __name__ == "__main__":
    main()
