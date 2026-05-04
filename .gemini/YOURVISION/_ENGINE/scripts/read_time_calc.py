import sys
import os

def calculate_read_time(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Подсчет знаков без пробелов (для градации)
        char_count = len(content.replace(" ", "").replace("\n", ""))
        
        # Расчет времени (стандарт: ~1000 знаков = 1 мин, или 150 слов = 1 мин)
        # Упрощенная формула: 800 знаков б/п = 1 минута
        read_time = round(char_count / 800, 1)
        if read_time < 0.5: read_time = 0.5

        # Определение Grade
        if char_count < 800:
            grade = "Grade B (Flash)"
        elif 800 <= char_count < 1500:
            grade = "Grade A (Standard)"
        elif 1500 <= char_count < 2500:
            grade = "Grade S (Story)"
        else:
            grade = "Grade SS (Longread)"

        print(f"{read_time}")
        print(f"Stats: {char_count} chars | {grade}")
        
    except FileNotFoundError:
        print("Error: File not found")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        calculate_read_time(sys.argv[1])
    else:
        print("Usage: python3 read_time_calc.py <filepath>")
