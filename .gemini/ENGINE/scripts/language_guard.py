#!/usr/bin/env python3
import sys
import re

def check_language(text):
    # Если в тексте есть специфические украинские буквы (і, ї, є, ґ) вне блоков контента
    # или слишком много английских слов (вне кода/тегов), это триггер.
    
    ua_specific = re.findall(r'[ііїєґІЇЄҐ]', text)
    if ua_specific and "ID-ПОСТА" not in text:
        return False, "LANGUAGE BREACH: Обнаружен украинский язык в коммуникации."
    
    # Проверка на кириллицу (должна доминировать в чате)
    cyrillic = re.findall(r'[а-яА-Я]', text)
    if len(cyrillic) < 5 and len(text) > 20:
        return False, "LANGUAGE BREACH: Ответ должен быть на русском языке."
        
    return True, "Communication language verified: RU."

if __name__ == "__main__":
    content = sys.stdin.read()
    ok, msg = check_language(content)
    if not ok:
        print(f"❌ {msg}")
        sys.exit(1)
    else:
        sys.exit(0)
