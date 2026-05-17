# YV HUB

Editorial dashboard "Vienna 2026 Insider Hub" - визуальная витрина YourVision.

## Структура

```
08_HUB/
├── index.html      ← UI (Dazed-стиль: pink/cyan/acid, PWA-ready)
├── data.js         ← модель сезона (battles, qualifiers, odds, rehearsals, awards)
├── assets/         ← логотип, флаги SF, JPG-обложки SF/GF, иконки сердец
└── README.md       ← этот файл
```

## Deploy

Зеркало для GitHub Pages: `/home/levdanskiy/YourEurovision_Hub_Deploy/` (отдельный git-репозиторий, remote: `github.com/levdanskiy/YourEurovision-Hub`). Деплой публикует через GitHub Pages.

Деплой содержит дополнительно: `manifest.json`, `sw.js` (PWA), `update_odds.py` (авто-скрипт).

## Workflow обновления

1. Правим source: `08_HUB/data.js` (новые odds, results, qualifiers).
2. Опционально - правим UI: `08_HUB/index.html`.
3. Синхронизация в deploy:
   ```bash
   cp .gemini/01_YOURVISION/08_HUB/data.js /home/levdanskiy/YourEurovision_Hub_Deploy/
   cp .gemini/01_YOURVISION/08_HUB/index.html /home/levdanskiy/YourEurovision_Hub_Deploy/
   cp .gemini/01_YOURVISION/08_HUB/index.html /home/levdanskiy/YourEurovision_Hub_Deploy/YV_Editor_Hub.html
   # assets обычно стабильны - копировать при добавлении
   ```
4. Коммит и пуш в deploy-репо:
   ```bash
   cd /home/levdanskiy/YourEurovision_Hub_Deploy/
   git add data.js index.html YV_Editor_Hub.html
   git commit -m "sync: <что обновлено>"
   git push
   ```

## Связь с базами YV

data.js - это срез state'а сезона для визуализации. Источник правды: `02_KNOWLEDGE/YV_Season_2026.md` / `YV_Season_2027.md` + `06_TIMELINE/database/yv_season_2026.json`.

**Правило:** при изменении результатов / котировок / квалификаций сначала обновляем `.md` базы (см. OS §9bis), потом руками переносим в `data.js`. Не наоборот.

## Безопасность

⚠️ В git remote деплой-репо вшит GitHub PAT в открытом виде (видно в `git remote -v`). Рекомендация - перевести на SSH-remote или хранить токен в `git credential helper`. Архивированный `07_ARCHIVE/02_ENGINE/scripts/hub_bot_sync.py` содержит Telegram bot-токен hardcoded - токен надо ротировать если планируется снова использовать.

## Что в data.js

Структура DATA-объекта (JS):
- `battles[]` - QF/SF баттлы голосования в Telegram опросах (id, n, t1/t2, a1/a2, scores, w (winner), status)
- `qualifiers[]` - кто прошёл
- `eliminated[]` - кто отвалился
- `odds[]` - топ букмекеров
- `awards`, `rehearsals` и др. поля по сезону

При создании сезона 2027 - аналогичная структура, но `battles[]` начнётся с QF #1 нового цикла.
