# 🛡 NOVELLS - GIT WORKFLOW / ЗАЩИТА ОТ ЗАТИРАНИЯ

**Проблема (09.06.2026):** репозиторий общий (под `.gemini` живут YourVision, ALMANAC, Novells). Параллельный YourVision-поток периодически делает `git reset` на `main` и перестраивает историю - при этом **затирает Novells-коммиты**, лежащие на `main` (так уже случилось: 6 коммитов слетели, восстановлены cherry-pick'ом из reflog).

**Решение:** ветка-сейф `novells` + авто-страж.

---

## Как это работает

- **Ветка `novells`** - durable «сейф» Novells-работы. `git reset` на `main` двигает ТОЛЬКО `main`; ref `novells` он не трогает, поэтому коммиты остаются живы и достижимы.
- **post-commit страж** (`tools/post-commit-novells-guard.sh`, симлинкнут в `.git/hooks/post-commit`): при каждом коммите, который трогает `03_NOVELLS/`, **fast-forward**'ит `novells` к новому HEAD. Назад не двигает; если видит расхождение (значит `main` откатили) - НЕ трогает ref и печатает подсказку для восстановления.
- Работать продолжаем на `main` (общее дерево, файлы на месте для постинга) - страж сам поддерживает `novells` в актуальном состоянии.

## Если Novells-файлы снова «пропали» (main откатили)

1. Убедиться, что сейф цел: `git log --oneline novells -8`
2. Вернуть работу на main:
   - быстрый случай: `git merge novells`
   - если main ушёл по YV: `git merge novells` (обычный merge; конфликтов не будет - пути не пересекаются) либо `git cherry-pick <range>` нужных коммитов.
3. Проверить файлы на диске.

## Ручной бэкап (опционально, надёжнее всего)

Пушить сейф на удалёнку, чтобы пережить и локальные сбросы:
```
git push -u origin novells
```
(origin - тот же GitHub-remote; новая ветка, на `main` не влияет.)

## Восстановление хука после переустановки

Если YV-инструменты перезапишут `.git/hooks`, переустановить страж:
```
ln -sf /home/levdanskiy/.gemini/03_NOVELLS/09_GENERAL/tools/post-commit-novells-guard.sh \
       "$(git rev-parse --git-path hooks)/post-commit"
```

*Не удалять. Сейф `novells` и страж - инфраструктура Novells.*
