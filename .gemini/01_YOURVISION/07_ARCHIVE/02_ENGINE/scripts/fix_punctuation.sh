#!/bin/bash

# Скрипт для принудительной замены тире на дефисы
# Путь: .gemini/system/scripts/fix_punctuation.sh

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: ./fix_punctuation.sh <file_or_directory>"
    exit 1
fi

# Замена длинного тире (—) и среднего тире (–) на дефис (-)
# Работает рекурсивно, если указана директория

if [ -d "$TARGET" ]; then
    find "$TARGET" -type f -name "*.md" -exec sed -i 's/—/-/g' {} +
    find "$TARGET" -type f -name "*.md" -exec sed -i 's/–/-/g' {} +
    echo "✅ ПУНКТУАЦИЯ ИСПРАВЛЕНА во всех файлах в папке: $TARGET"
elif [ -f "$TARGET" ]; then
    sed -i 's/—/-/g' "$TARGET"
    sed -i 's/–/-/g' "$TARGET"
    echo "✅ ПУНКТУАЦИЯ ИСПРАВЛЕНА в файле: $TARGET"
else
    echo "❌ Ошибка: Путь не найден."
    exit 1
fi
