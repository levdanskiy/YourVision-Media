#!/usr/bin/env python3
"""
YourVision Publish Tool
Скрипт валидации и публикации постов
Версия: 2.5

Запуск: python3 publish_tool.py [путь_к_файлу]
"""

import sys
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Границы грейдов по количеству знаков
GRADE_LIMITS = {
    "Q": (100, 300),
    "S": (301, 500),
    "F": (501, 1000),
    "B": (1001, 1300),
    "C": (1301, 1800),
    "A": (1801, 2400),
}

# Запрещённые слова
FORBIDDEN_WORDS = [
    "невероятный", "потрясающий", "ошеломительный", "долгожданный",
    "невероятная", "потрясающая", "ошеломительная",
    "невероятное", "потрясающее", "ошеломительное",
]

# Запрещённая пунктуация
FORBIDDEN_PUNCTUATION = [
    ("—", "длинное тире"),
    ("–", "среднее тире"),
]


class PostValidator:
    """Валидатор постов YourVision"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = ""
        self.metadata = {}
        self.body = ""
        self.errors = []
        self.warnings = []

    def load(self) -> bool:
        """Загрузка файла"""
        if not self.filepath.exists():
            self.errors.append(f"Файл не найден: {self.filepath}")
            return False

        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()

        return True

    def parse(self) -> bool:
        """Парсинг метаданных и тела"""
        lines = self.content.split('\n')

        # Парсинг системного заголовка
        for line in lines[:10]:
            if line.startswith("//"):
                key_match = re.match(r'//\s*(\w+[^:]*):\s*(.+)', line)
                if key_match:
                    key = key_match.group(1).strip()
                    value = key_match.group(2).strip()
                    self.metadata[key] = value

        # Поиск тела (после последней строки с //)
        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith("//"):
                body_start = i + 1

        self.body = '\n'.join(lines[body_start:])

        # Удаление метрик футера для подсчёта
        self.body_clean = re.sub(r'---\n`⏱.*?`', '', self.body)
        self.body_clean = re.sub(r'\*\*\*.*', '', self.body_clean, flags=re.DOTALL)

        return True

    def validate_all(self) -> Dict:
        """Полная валидация"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "metadata": self.metadata,
            "stats": {},
        }

        # 1. Проверка системного заголовка
        header_valid = self._validate_header()
        if not header_valid:
            results["valid"] = False

        # 2. Проверка грейда
        grade_valid, grade_info = self._validate_grade()
        if not grade_valid:
            results["valid"] = False
        results["stats"]["grade"] = grade_info

        # 3. Проверка запрещённых слов
        words_valid, words_found = self._validate_words()
        if not words_valid:
            results["warnings"].extend(words_found)

        # 4. Проверка пунктуации
        punct_valid, punct_errors = self._validate_punctuation()
        if not punct_valid:
            results["errors"].extend(punct_errors)
            results["valid"] = False

        # 5. Проверка структуры
        struct_valid, struct_errors = self._validate_structure()
        if not struct_valid:
            results["warnings"].extend(struct_errors)

        # 6. Статистика
        results["stats"]["char_count"] = len(self.body_clean)
        results["stats"]["word_count"] = len(self.body_clean.split())

        results["errors"].extend(self.errors)
        results["warnings"].extend(self.warnings)

        return results

    def _validate_header(self) -> bool:
        """Проверка системного заголовка"""
        required_fields = ["ИД-ПОСТА", "ТЕМА", "ДАТА ПУБЛИКАЦИИ", "СТАТУС"]
        missing = []

        for field in required_fields:
            if field not in self.metadata:
                missing.append(field)

        if missing:
            self.errors.append(f"Отсутствуют поля заголовка: {', '.join(missing)}")
            return False

        return True

    def _validate_grade(self) -> Tuple[bool, Dict]:
        """Проверка соответствия грейда"""
        grade_info = {}

        # Поиск грейда в файле
        grade_match = re.search(r'\*\*Grade:\*\*\s*(\w)', self.content)
        if not grade_match:
            self.errors.append("Grade не указан в футере")
            return False, grade_info

        stated_grade = grade_match.group(1)
        char_count = len(self.body_clean)

        grade_info["stated"] = stated_grade
        grade_info["char_count"] = char_count

        # Проверка соответствия
        if stated_grade not in GRADE_LIMITS:
            self.errors.append(f"Неизвестный грейд: {stated_grade}")
            return False, grade_info

        min_len, max_len = GRADE_LIMITS[stated_grade]
        grade_info["expected_range"] = f"{min_len}-{max_len}"

        if min_len <= char_count <= max_len:
            grade_info["match"] = True
            return True, grade_info

        # Предлагаем правильный грейд
        for g, (mn, mx) in GRADE_LIMITS.items():
            if mn <= char_count <= mx:
                grade_info["suggested_grade"] = g
                break

        self.errors.append(
            f"REJECTED: {char_count} chars doesn't match Grade {stated_grade} ({min_len}-{max_len}). "
            f"Suggested: Grade {grade_info.get('suggested_grade', '?')}"
        )
        return False, grade_info

    def _validate_words(self) -> Tuple[bool, List[str]]:
        """Проверка на запрещённые слова"""
        found = []
        content_lower = self.content.lower()

        for word in FORBIDDEN_WORDS:
            if word in content_lower:
                found.append(f"Запрещённое слово: «{word}»")

        return len(found) == 0, found

    def _validate_punctuation(self) -> Tuple[bool, List[str]]:
        """Проверка пунктуации"""
        errors = []

        for char, name in FORBIDDEN_PUNCTUATION:
            if char in self.content:
                # Подсчёт вхождений
                count = self.content.count(char)
                errors.append(f"Запрещено {name} ({char}): найдено {count} вхождений. Используйте дефис (-)")

        return len(errors) == 0, errors

    def _validate_structure(self) -> Tuple[bool, List[str]]:
        """Проверка структуры поста"""
        warnings = []

        # Проверка футера
        if "⏱ Время чтения:" not in self.content:
            warnings.append("Отсутствует метрика времени чтения в футере")

        if "***" not in self.content:
            warnings.append("Отсутствует разделитель *** в футере")

        # Проверка промпта (только для не-POLL постов)
        if "POLL" not in self.metadata.get("ПРОТОКОЛЫ", ""):
            if "**Prompt:**" not in self.content:
                warnings.append("Отсутствует промпт для Midjourney")

        return True, warnings


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 publish_tool.py [путь_к_файлу]")
        sys.exit(1)

    filepath = sys.argv[1]
    validator = PostValidator(filepath)

    # Загрузка и парсинг
    if not validator.load():
        print(f"❌ ОШИБКА: Файл не найден")
        sys.exit(1)

    validator.parse()

    # Валидация
    results = validator.validate_all()

    # Вывод результатов
    print("\n" + "=" * 60)
    print("📋 ВАЛИДАЦИЯ ПОСТА")
    print("=" * 60)
    print(f"📄 Файл: {filepath}")
    print(f"📊 Символов: {results['stats']['char_count']}")
    print(f"📝 Слов: {results['stats']['word_count']}")

    if results["stats"]["grade"]:
        grade = results["stats"]["grade"]
        print(f"📏 Grade: {grade['stated']} (диапазон: {grade.get('expected_range', '?')})")
        if grade.get("suggested_grade"):
            print(f"   💡 Рекомендуемый: Grade {grade['suggested_grade']}")

    print("=" * 60)

    if results["valid"]:
        print("\n✅ СТАТУС: VALIDATED")
        print("   Пост готов к публикации")

        # Команда для Git
        print("\n📌 Следующий шаг:")
        print("   git add . && git commit -m \"feat: post published\" && git push")
    else:
        print("\n❌ СТАТУС: REJECTED")
        print("   Требуются исправления:")

        for error in results["errors"]:
            print(f"   🔴 {error}")

    if results["warnings"]:
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
        for warning in results["warnings"]:
            print(f"   🟡 {warning}")

    print("=" * 60 + "\n")

    # Код возврата
    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()
