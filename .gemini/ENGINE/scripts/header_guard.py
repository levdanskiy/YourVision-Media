#!/usr/bin/env python3
import sys

# Словарь принудительной локализации заголовков
GEO_LOCK = {
    "LITHUANIA": {"RU": "ЛИТВА", "UA": "ЛИТВА"},
    "LUXEMBOURG": {"RU": "ЛЮКСЕМБУРГ", "UA": "ЛЮКСЕМБУРГ"},
    "MOLDOVA": {"RU": "МОЛДОВА", "UA": "МОЛДОВА"},
    "MALTA": {"RU": "МАЛЬТА", "UA": "МАЛЬТА"},
    "SWITZERLAND": {"RU": "ШВЕЙЦАРИЯ", "UA": "ШВЕЙЦАРІЯ"},
    "GERMANY": {"RU": "ГЕРМАНИЯ", "UA": "НІМЕЧЧИНА"},
    "SWEDEN": {"RU": "ШВЕЦИЯ", "UA": "ШВЕЦІЯ"},
    "AUSTRIA": {"RU": "АВСТРИЯ", "UA": "АВСТРІЯ"},
    "BULGARIA": {"RU": "БОЛГАРИЯ", "UA": "БОЛГАРІЯ"}
}

def validate_header(header, lang="UA"):
    for eng, loc in GEO_LOCK.items():
        if eng in header.upper():
            return header.upper().replace(eng, loc[lang])
    return header

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(validate_header(sys.argv[1], sys.argv[2]))
