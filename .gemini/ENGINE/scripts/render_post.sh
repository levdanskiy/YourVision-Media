#!/bin/bash
# Пункт 4: Рендеринг через Glow
FILE=$1
if [ -f "$FILE" ]; then
    glow "$FILE" --style dark
else
    echo "❌ File not found"
fi
