# 08_HUB/tools

Скрипты обслуживания Хаба. Все используют абсолютный `HUB_DIR = /home/levdanskiy/.gemini/01_YOURVISION/08_HUB`, можно запускать из любой cwd.

| Скрипт | Что делает | Когда запускать |
|---|---|---|
| `yv_tg_sync.py` | Тащит свежие посты из Telegram-каналов (@YourEurovision, @almanac_marginalia), парсит в `data.js.news[]`, пишет в `08_HUB/data.js` и `YourEurovision_Hub_Deploy/data.js` | **Автомат** через cron каждые 15 мин |
| `rebuild_perfect.py` | Пересобирает `index.html` из `data.js` по «Titan Platinum» шаблону | Вручную при major-перестройке UI |
| `rebuild_hub.py` | Альтернативный пересборщик `index.html` с другим набором фич (таймеры SF/GF, MyRadio24 cover) | Вручную |
| `restore_render.py` | Точечно восстанавливает `function render()` в HTML | Аварийно, если render сломался |
| `fix_hub_layout.py` | Точечно правит News grid в HTML | Аварийно |

## Cron

Активен только `yv_tg_sync.py`:
```
*/15 * * * * /usr/bin/python3 /home/levdanskiy/.gemini/01_YOURVISION/08_HUB/tools/yv_tg_sync.py >> /home/levdanskiy/yv_sync.log 2>&1
```

Лог: `/home/levdanskiy/yv_sync.log`.

## Безопасность

`yv_tg_sync.py` содержит hardcoded Telegram bot-токен. При компрометации - ротировать через @BotFather.
