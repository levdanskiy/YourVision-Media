#!/usr/bin/env python3
"""
YourVision Visual Generator
Генератор промптов для Midjourney и инфографики
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class VisualType(Enum):
    CHART = "chart"
    NEWS = "news"
    WINNER = "winner"
    POLL = "poll"
    ANALYSIS = "analysis"


class Mood(Enum):
    CELEBRATORY = "celebratory"
    DRAMATIC = "dramatic"
    NEUTRAL = "neutral"
    MOODY = "moody"
    ROMANTIC = "romantic"


@dataclass
class VisualConfig:
    visual_type: VisualType
    mood: Mood = Mood.NEUTRAL
    setting: str = "studio"
    subjects: Optional[List[str]] = None
    custom_elements: Optional[List[str]] = None


# Базовые настройки камеры
CAMERA_SETTINGS = {
    "primary": "shot on 35mm film Kodak Portra 800",
    "secondary": "Phase One XF IQ4, 150MP",
    "backup": "shot on medium format film"
}

# Стили
STYLE_ELEMENTS = [
    "cinematic realism",
    "heavy film grain",
    "high-end fashion editorial",
    "Dazed magazine style",
    "i-D magazine aesthetic"
]

# Запрещённые элементы
FORBIDDEN_ELEMENTS = [
    "3D",
    "logos",
    "neon",
    "futuristic",
    "cartoon",
    "anime",
    "digital art",
    "AI generated"
]


class VisualGenerator:
    """Генератор промптов для визуала YourVision"""

    def __init__(self):
        self.brand_text = "YourVision"
        self.creator_tag = "levdanskiy"

    def generate_prompt(self, config: VisualConfig) -> str:
        """Генерация промпта для Midjourney"""

        # Базовые элементы
        elements = []

        # 1. Описание сцены
        scene = self._get_scene_description(config)
        elements.append(scene)

        # 2. Субъекты
        if config.subjects:
            subjects = ", ".join(config.subjects)
            elements.append(subjects)

        # 3. Сеттинг
        elements.append(config.setting)

        # 4. Настроение
        mood_elements = self._get_mood_elements(config.mood)
        elements.extend(mood_elements)

        # 5. Технические параметры
        elements.append(CAMERA_SETTINGS["primary"])

        # 6. Стиль
        elements.extend(STYLE_ELEMENTS[:3])  # Первые 3 элемента стиля

        # 7. Кастомные элементы
        if config.custom_elements:
            elements.extend(config.custom_elements)

        # Сборка промпта
        prompt = ", ".join(elements)
        prompt += " --ar 1:1"

        return prompt

    def _get_scene_description(self, config: VisualConfig) -> str:
        """Получение описания сцены по типу"""

        scenes = {
            VisualType.CHART: "group of stylish young people looking at camera",
            VisualType.NEWS: "editorial portrait photograph",
            VisualType.WINNER: "celebratory moment captured on film",
            VisualType.POLL: "split composition with diverse group of people",
            VisualType.ANALYSIS: "moody editorial shot with dramatic lighting"
        }

        return scenes.get(config.visual_type, "editorial photograph")

    def _get_mood_elements(self, mood: Mood) -> List[str]:
        """Получение элементов настроения"""

        mood_map = {
            Mood.CELEBRATORY: ["joyful expressions", "golden hour lighting", "warm tones"],
            Mood.DRAMATIC: ["intense atmosphere", "high contrast", "shadows"],
            Mood.NEUTRAL: ["natural lighting", "balanced composition"],
            Mood.MOODY: ["moody lighting", "atmospheric haze", "cool tones"],
            Mood.ROMANTIC: ["soft lighting", "dreamy atmosphere", "intimate framing"]
        }

        return mood_map.get(mood, [])

    def generate_for_chart(self, chart_name: str, top_artists: List[str] = None) -> str:
        """Специализированный генератор для чартов"""

        config = VisualConfig(
            visual_type=VisualType.CHART,
            mood=Mood.MOODY,
            setting="minimalist studio with warm backlighting",
            subjects=["a guy in designer clothes", "a girl with fashion makeup", "a romantic couple embracing"]
        )

        return self.generate_prompt(config)

    def generate_for_winner(self, country: str, artist_name: str = None) -> str:
        """Специализированный генератор для победителей"""

        # ВАЖНО: Не включаем имя артиста в промпт!
        config = VisualConfig(
            visual_type=VisualType.WINNER,
            mood=Mood.CELEBRATORY,
            setting="glamorous award ceremony backdrop",
            subjects=["silhouette of winning performer", "confetti in the air", "stage lights"]
        )

        return self.generate_prompt(config)

    def generate_for_news(self, topic: str, is_breaking: bool = False) -> str:
        """Специализированный генератор для новостей"""

        config = VisualConfig(
            visual_type=VisualType.NEWS,
            mood=Mood.DRAMATIC if is_breaking else Mood.NEUTRAL,
            setting="modern news studio" if is_breaking else "editorial backdrop"
        )

        return self.generate_prompt(config)


class InfographicGenerator:
    """Генератор инфографики для результатов голосования"""

    def __init__(self):
        self.colors = {
            "gold": "#FFD700",
            "silver": "#C0C0C0",
            "bronze": "#CD7F32",
            "primary": "#1a1a2e",
            "secondary": "#16213e",
            "accent": "#e94560",
            "text": "#ffffff"
        }

    def generate_results_text(self, results: List[dict]) -> str:
        """Генерация текстового представления результатов"""

        lines = ["📊 РЕЗУЛЬТАТЫ", ""]

        for i, result in enumerate(results[:10], 1):
            # Определение медали для топ-3
            medal = ""
            if i == 1:
                medal = "🥇"
            elif i == 2:
                medal = "🥈"
            elif i == 3:
                medal = "🥉"

            artist = result.get("artist", "Unknown")
            points = result.get("points", 0)
            country = result.get("country", "")

            lines.append(f"{medal}{i}. {artist} ({country}) — {points} pts")

        return "\n".join(lines)

    def generate_jury_televote_split(self, jury_results: List[dict], televote_results: List[dict]) -> str:
        """Генерация разделения жюри/телеголосование"""

        lines = ["📋 РАЗБИВКА ГОЛОСОВ", ""]
        lines.append("👥 ЖЮРИ:")
        for i, r in enumerate(jury_results[:5], 1):
            lines.append(f"  {i}. {r['artist']} — {r['points']}")

        lines.append("")
        lines.append("📞 ТЕЛЕГОЛОСОВАНИЕ:")
        for i, r in enumerate(televote_results[:5], 1):
            lines.append(f"  {i}. {r['artist']} — {r['points']}")

        return "\n".join(lines)


# Шаблоны промптов для быстрого использования
QUICK_PROMPTS = {
    "chart_default": """group of stylish young people, a guy, a girl, and a romantic couple, minimalist studio with warm backlighting, shot on 35mm film Kodak Portra 800, heavy film grain, cinematic realism, high-end fashion editorial, Dazed magazine style, moody lighting --ar 1:1""",

    "news_default": """editorial portrait photograph, natural lighting, shot on 35mm film Kodak Portra 800, heavy film grain, cinematic realism, high-end fashion editorial, balanced composition --ar 1:1""",

    "winner_celebratory": """celebratory moment captured on film, silhouette of performer with arms raised, confetti in the air, glamorous award ceremony backdrop, golden hour lighting, shot on 35mm film Kodak Portra 800, heavy film grain, cinematic realism --ar 1:1""",

    "analysis_moody": """moody editorial shot with dramatic lighting, atmospheric haze, cool tones, shot on 35mm film Kodak Portra 800, heavy film grain, cinematic realism, high-end fashion editorial --ar 1:1""",

    "poll_interactive": """split composition with diverse group of people looking at camera, minimalist studio, shot on 35mm film Kodak Portra 800, heavy film grain, cinematic realism --ar 1:1"""
}


# CLI Interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="YourVision Visual Generator")
    parser.add_argument("--type", choices=["chart", "news", "winner", "poll", "analysis"],
                        default="news", help="Тип визуала")
    parser.add_argument("--mood", choices=["celebratory", "dramatic", "neutral", "moody", "romantic"],
                        default="neutral", help="Настроение")
    parser.add_argument("--quick", choices=list(QUICK_PROMPTS.keys()), help="Быстрый шаблон")
    parser.add_argument("--country", help="Страна (для winner)")
    parser.add_argument("--breaking", action="store_true", help="Breaking news стиль")

    args = parser.parse_args()

    generator = VisualGenerator()

    if args.quick:
        print("\n🎨 QUICK PROMPT:")
        print(QUICK_PROMPTS[args.quick])
        return

    config = VisualConfig(
        visual_type=VisualType(args.type),
        mood=Mood(args.mood)
    )

    if args.type == "winner" and args.country:
        prompt = generator.generate_for_winner(args.country)
    elif args.type == "news" and args.breaking:
        prompt = generator.generate_for_news("", is_breaking=True)
    else:
        prompt = generator.generate_prompt(config)

    print("\n🎨 GENERATED PROMPT:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)


if __name__ == "__main__":
    main()
