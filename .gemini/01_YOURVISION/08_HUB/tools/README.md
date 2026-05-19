# 08_HUB/tools

Скрипты обслуживания Хаба. Все используют абсолютный `HUB_DIR = /home/levdanskiy/.gemini/01_YOURVISION/08_HUB`, можно запускать из любой cwd.

| Скрипт | Что делает | Когда запускать |
|---|---|---|
| `yv_tg_sync.py` | Тащит свежие посты из Telegram (@YourEurovision, @almanac_marginalia), мержит с локальными постами в `data.js.news[]` | **Автомат** через cron каждые 15 мин |
| `sync_local_posts.py` | Подтягивает .md-посты из `04_CONTENT/` за последние 30 дней, добавляет в `news[]` с пометкой `id="local"` | Вручную после написания/правки поста (опц. из pre-commit) |
| `rebuild_perfect.py` | Пересобирает `index.html` из `data.js` по «Titan Platinum» шаблону | Вручную при major-перестройке UI |
| `rebuild_hub.py` | Альтернативный пересборщик `index.html` с другим набором фич | Вручную |
| `restore_render.py` | Точечно восстанавливает `function render()` в HTML | Аварийно, если render сломался |
| `fix_hub_layout.py` | Точечно правит News grid в HTML | Аварийно |

## Кооперативный sync (TG + local)

`yv_tg_sync.py` и `sync_local_posts.py` работают вместе через общий ключ `id` в `news[]`:

- `id="70"` (или другой TG-channel id) - пост пришёл из Telegram.
- `id="local"` - пост подтянут из `04_CONTENT/*.md` напрямую.

При cron-цикле `yv_tg_sync.py` **сохраняет** локальные записи и добавляет к ним свежие TG-посты, сортирует по `ts` и обрезает до 25. То есть локальный пост видим в Hub до того, как опубликуешь в Telegram, и не пропадает после публикации.

**Workflow:**

1. Написал пост → `04_CONTENT/2026/MM/DD/YV-*.md`.
2. Запустил `python3 sync_local_posts.py` → пост появился в Hub.
3. Опубликовал в Telegram → cron при следующем тике подтянет TG-версию, локальная останется (если её `ts` свежее).

Если оба представления нежелательны - после публикации в TG можно удалить или переименовать локальный .md, локальная версия исчезнет на следующем `sync_local_posts.py`.

## Cron

Активен только `yv_tg_sync.py`:
```
*/15 * * * * /usr/bin/python3 /home/levdanskiy/.gemini/01_YOURVISION/08_HUB/tools/yv_tg_sync.py >> /home/levdanskiy/yv_sync.log 2>&1
```

Лог: `/home/levdanskiy/yv_sync.log`.

## Безопасность

`yv_tg_sync.py` содержит hardcoded Telegram bot-токен. При компрометации - ротировать через @BotFather.
