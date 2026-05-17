#!/usr/bin/env python3
"""
YourVision Publisher 2.5
Главный модуль публикации для Gemini CLI
Версия: 2.5 (Maximal Detail)
"""

import os
import re
import json
import subprocess
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Tuple
from pathlib import Path


class PostType(Enum):
    FLASH = "flash"
    SNAP = "snap"
    POLL = "poll"
    STANDARD = "standard"
    DEEP_DIVE = "deep_dive"


class Grade(Enum):
    Q = "Q"  # 100-300 знаков
    S = "S"  # 301-500 знаков
    F = "F"  # 501-1000 знаков
    B = "B"  # 1001-1300 знаков
    C = "C"  # 1301-1800 знаков
    A = "A"  # 1801-2400 знаков


class AlertTier(Enum):
    RED = "red"      # 5 минут
    YELLOW = "yellow"  # 30 минут
    GREEN = "green"   # по расписанию


class EventType(Enum):
    RELEASE = "RELEASE"
    FINAL = "FINAL"
    HEAT = "HEAT"
    CHART = "CHART"
    SEMI = "SEMI"
    ANNOUNCEMENT = "ANNOUNCEMENT"


# Границы грейдов по количеству знаков
GRADE_LIMITS = {
    Grade.Q: (100, 300),
    Grade.S: (301, 500),
    Grade.F: (501, 1000),
    Grade.B: (1001, 1300),
    Grade.C: (1301, 1800),
    Grade.A: (1801, 2400),
}


@dataclass
class Source:
    url: str
    name: str
    tier: int = 2  # 1=официальный, 2=СМИ, 3=слухи


@dataclass
class FactSheet:
    artist: Optional[str] = None
    song: Optional[str] = None
    release_date: Optional[str] = None
    country: Optional[str] = None
    event: Optional[str] = None
    sources: List[Source] = field(default_factory=list)


@dataclass
class Post:
    post_type: PostType
    title: str
    content: str
    country: str = ""
    country_flag: str = ""
    theme: str = ""
    subtheme: str = ""
    fact_sheet: Optional[FactSheet] = None
    grade: Optional[Grade] = None
    visual_prompt: Optional[str] = None
    alert_tier: AlertTier = AlertTier.GREEN
    links: List[Dict] = field(default_factory=list)
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            # Время по Риге (EET)
            self.created_at = datetime.now()
        if self.grade is None:
            self.grade = self._calculate_grade()

    def _calculate_grade(self) -> Grade:
        """Автоматический расчёт грейда по длине контента"""
        length = len(self.content)
        for grade, (min_len, max_len) in GRADE_LIMITS.items():
            if min_len <= length <= max_len:
                return grade
        if length < 100:
            return Grade.Q
        return Grade.A  # Если больше 2400

    def validate_grade(self) -> Tuple[bool, str]:
        """Валидация соответствия грейда"""
        length = len(self.content)
        if self.grade is None:
            return False, "Grade not specified"

        min_len, max_len = GRADE_LIMITS.get(self.grade, (0, 0))
        if min_len <= length <= max_len:
            return True, f"OK: {length} chars matches Grade {self.grade.value}"

        return False, f"REJECTED: {length} chars doesn't match Grade {self.grade.value} ({min_len}-{max_len})"


class PostGenerator:
    """Генератор постов по шаблонам"""

    @staticmethod
    def generate_system_header(post: Post) -> str:
        """Генерация системного заголовка"""
        now = post.created_at
        date_str = now.strftime("%d.%m")
        time_str = now.strftime("%H-%M")
        pub_date = now.strftime("%d.%m.%Y, %H:%M")

        post_id = f"YV-{date_str}-{time_str}-{post.country}-{post.theme[:20]}"

        return f"""// ИД-ПОСТА: {post_id}
// ТЕМА: {post.theme}
// ДАТА ПУБЛИКАЦИИ: {pub_date} (Europe/Рига)
// ПРОТОКОЛЫ: YourVision, {post.post_type.value.upper()}
// СТАТУС: ГОТОВ (EDITORIAL ANALYST V4.0)"""

    @staticmethod
    def generate_footer(post: Post) -> str:
        """Генерация футера"""
        # Расчёт времени чтения (средняя скорость ~1000 знаков/мин)
        reading_time = max(0.1, round(len(post.content) / 1000, 1))

        lines = []

        # Ссылки
        if post.links:
            for link in post.links:
                emoji = link.get("emoji", "🔗")
                label = link.get("label", "ССЫЛКА")
                url = link.get("url", "")
                platform = link.get("platform", "")
                lines.append(f"{emoji} **{label}:** [{platform}]({url})")

        if lines:
            lines.append("---")

        lines.append(f"`⏱ Время чтения: {reading_time} мин | {post.country_flag} YourVision: {post.theme}`")
        lines.append("***")
        lines.append("")
        lines.append(f"**Grade:** {post.grade.value}")

        if post.visual_prompt:
            lines.append(f"**Prompt:** {post.visual_prompt}")

        return "\n".join(lines)

    @staticmethod
    def generate_full_post(post: Post) -> str:
        """Генерация полного поста"""
        parts = []

        # Системный заголовок
        parts.append(PostGenerator.generate_system_header(post))
        parts.append("")

        # Основной заголовок
        if post.alert_tier == AlertTier.RED:
            parts.append(f"🚨 BREAKING: {post.country_flag} **{post.country.upper()}: {post.theme} - {post.subtheme}**")
        else:
            parts.append(f"{post.country_flag} **{post.country.upper()}: {post.theme} - {post.subtheme}**")
        parts.append("")

        # Контент
        parts.append(post.content)
        parts.append("")

        # Футер
        parts.append(PostGenerator.generate_footer(post))

        return "\n".join(parts)


class YVPublisher:
    """Главный класс публикации YourVision 2.5"""

    def __init__(self, base_path: str = ".gemini"):
        self.base_path = Path(base_path).expanduser()
        self._ensure_directories()

    def _ensure_directories(self):
        """Создание структуры директорий"""
        dirs = [
            self.base_path / "CONTENT" / "posts",
            self.base_path / "ENGINE" / "scripts",
            self.base_path / "KNOWLEDGE" / "Live_Calendars",
            self.base_path / "TIMELINE" / "database",
            self.base_path / "TIMELINE" / "master_plans",
            self.base_path / "system",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def get_post_path(self, post: Post) -> Path:
        """Получение пути для сохранения поста"""
        now = post.created_at
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        post_dir = self.base_path / "CONTENT" / "posts" / year / month / day
        post_dir.mkdir(parents=True, exist_ok=True)

        time_str = now.strftime("%H%M")
        filename = f"YV-{now.strftime('%d.%m')}-{time_str}-{post.country}-{post.post_type.value}.md"

        return post_dir / filename

    def validate_and_publish(self, post: Post, auto_fix: bool = True) -> Dict:
        """Валидация и публикация поста"""
        result = {
            "success": False,
            "valid": False,
            "filepath": None,
            "errors": [],
            "warnings": [],
        }

        # Проверка грейда
        valid, message = post.validate_grade()
        if not valid:
            if auto_fix:
                # Автоисправление грейда
                post.grade = post._calculate_grade()
                result["warnings"].append(f"Grade auto-corrected to {post.grade.value}")
            else:
                result["errors"].append(message)
                return result

        result["valid"] = True

        # Генерация полного поста
        content = PostGenerator.generate_full_post(post)

        # Сохранение
        filepath = self.get_post_path(post)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        result["filepath"] = str(filepath)
        result["success"] = True

        return result

    def git_sync(self, message: str) -> bool:
        """Синхронизация с Git"""
        try:
            subprocess.run(["git", "add", "."], cwd=self.base_path, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", message], cwd=self.base_path, check=True, capture_output=True)
            subprocess.run(["git", "push"], cwd=self.base_path, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e.stderr.decode() if e.stderr else str(e)}")
            return False


class TripleSync:
    """Тройная синхронизация календарей"""

    def __init__(self, base_path: str = ".gemini"):
        self.base_path = Path(base_path).expanduser()
        self.json_path = self.base_path / "TIMELINE" / "database" / "yv_season_2026.json"
        self.calendar_path = self.base_path / "KNOWLEDGE" / "Live_Calendars" / "YV_ESC_Live_Calendar.md"

    def add_event(self, event: Dict) -> bool:
        """Добавление события во все три источника"""
        try:
            # 1. JSON база
            self._update_json(event)

            # 2. Markdown календарь
            self._update_calendar(event)

            # 3. Мастер-план месяца
            self._update_master_plan(event)

            return True
        except Exception as e:
            print(f"Sync error: {e}")
            return False

    def _update_json(self, event: Dict):
        """Обновление JSON базы"""
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"events": []}

        data["events"].append(event)

        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _update_calendar(self, event: Dict):
        """Обновление Markdown календаря"""
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        flag = self._get_flag(event.get("country", ""))

        line = f"* {date.strftime('%d.%m')} {flag} **{event.get('country', '')}**: {event.get('event', '')} ({event.get('time', '')})\n"

        with open(self.calendar_path, 'a', encoding='utf-8') as f:
            f.write(line)

    def _update_master_plan(self, event: Dict):
        """Обновление мастер-плана месяца"""
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        month = date.strftime("%m")
        plan_path = self.base_path / "TIMELINE" / "master_plans" / month / f"YV_Plan_{month}.md"

        plan_path.parent.mkdir(parents=True, exist_ok=True)

        flag = self._get_flag(event.get("country", ""))
        time = event.get("time", "")
        country = event.get("country", "")
        event_name = event.get("event", "")

        line = f"* {time} | **YV** | ⚡ **#NEWS_WIRE:** {country}. {event_name}. - ⬜ [ОЖИДАНИЕ]\n"

        with open(plan_path, 'a', encoding='utf-8') as f:
            f.write(line)

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
        }
        return flags.get(country, flags.get(country.upper(), "🏳️"))


# CLI Interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="YourVision Publisher 2.5")
    parser.add_argument("--type", choices=["flash", "snap", "poll", "standard", "deep_dive"], required=True)
    parser.add_argument("--title", required=True, help="Заголовок поста")
    parser.add_argument("--content", required=True, help="Содержание поста")
    parser.add_argument("--country", default="", help="Страна")
    parser.add_argument("--flag", default="", help="Флаг страны")
    parser.add_argument("--theme", default="", help="Тема")
    parser.add_argument("--subtheme", default="", help="Подтема")
    parser.add_argument("--grade", choices=["Q", "S", "F", "B", "C", "A"], help="Грейд (авто если не указан)")
    parser.add_argument("--alert", choices=["red", "yellow", "green"], default="green")
    parser.add_argument("--prompt", default="", help="Midjourney prompt")
    parser.add_argument("--base-path", default=".gemini", help="Базовый путь")

    args = parser.parse_args()

    # Создание поста
    post = Post(
        post_type=PostType(args.type),
        title=args.title,
        content=args.content,
        country=args.country,
        country_flag=args.flag,
        theme=args.theme or args.title[:30],
        subtheme=args.subtheme,
        grade=Grade(args.grade) if args.grade else None,
        visual_prompt=args.prompt if args.prompt else None,
        alert_tier=AlertTier(args.alert),
    )

    # Публикация
    publisher = YVPublisher(args.base_path)
    result = publisher.validate_and_publish(post)

    if result["success"]:
        print(f"✅ Пост создан: {result['filepath']}")

        if result["warnings"]:
            for w in result["warnings"]:
                print(f"⚠️ {w}")

        # Git sync
        commit_msg = f"feat: {args.type} post - {args.country} {args.theme[:30]}"
        if publisher.git_sync(commit_msg):
            print("✅ Git sync completed")
    else:
        print(f"❌ Ошибка: {result['errors']}")


if __name__ == "__main__":
    main()
