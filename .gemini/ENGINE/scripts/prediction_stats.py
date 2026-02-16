#!/usr/bin/env python3
import random

def get_win_probability(country, year=2026):
    """Рассчитывает шанс победы на основе исторических паттернов"""
    # В будущем здесь будет реальный анализ из EurovisionDataset
    base_odds = {
        "SWEDEN": 15.5,
        "ITALY": 12.2,
        "UKRAINE": 10.8,
        "NORWAY": 8.5,
        "LUXEMBOURG": 5.0
    }
    prob = base_odds.get(country.upper(), random.uniform(1.0, 4.0))
    return f"{prob}% chance of Victory"

if __name__ == "__main__":
    import sys
    country = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    print(get_win_probability(country))
