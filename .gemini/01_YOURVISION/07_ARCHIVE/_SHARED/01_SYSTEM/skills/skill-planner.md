# SKILL: DAILY PLANNER
**Trigger:** `@planner`, `Сводный план`, `План на завтра`
**Description:** Automates the creation of the daily content plan, ensuring continuity and structure.

---

## 1. ANALYSIS PHASE (BEFORE WRITING)
1.  **Date Check:** Identify the target date and day of the week.
2.  **Debt Scan:** Check the *previous* `daily_plan` file.
    *   Any task marked `⬜` or `⚠️` MUST be moved to the "Recovery Queue" of the new plan.
3.  **Language Rotation ("Chessboard"):**
    *   Check the last post language for `AC`, `NB`, `SW`.
    *   **Rule:** If yesterday ended RU -> today starts UA. If ended UA -> starts RU.
4.  **Source Sync:** Read the monthly calendars (`AC_Plan`, `NB_Plan`, `SW_Plan`, `YV_Plan`) to get the scheduled topics for the target date.

## 2. FORMAT STRUCTURE (MANDATORY)

```markdown
# 📆 СВОДНЫЙ ПЛАН: [DD.MM.YYYY] ([DAY]) - [MAIN_THEMES]
**Статус:** Active
**Концепция:** "[Concept_Name]"
**Языковой режим:** Chessboard (Strict, starts from [Prev_Date] final state)

---

#### **ДОЛГИ И ОЧЕРЕДЬ НАГОНА (Recovery Queue)**
*   ⚠️ `[Old_Date]` - `[Time]` | **[Lang]** | **[Type]:** [Topic]. - ⬜ [ОЖИДАНИЕ]

---

### 🏛️ ALMANAC (Main)
*AC ([Prev_Date] ended [Lang]) -> Start [New_Lang]*
| Время | Язык | Тема | Статус |
| :--- | :--- | :--- | :--- |
| `09:00` | **[Lang]** | **#GREETING (EXTRA):** [Topic]. | ⬜ |
...

### 🌍 ALMANAC: NEIGHBORS
...

### 🍰 ALMANAC: SWEET
...

### 🎤 YOURVISION
| Время | Язык | Тема | Статус |
| :--- | :--- | :--- | :--- |
| `[Time]` | **BI** | **#[TYPE]:** [Topic]. | ⬜ |
```

## 3. EXECUTION RULES
*   **YourVision:** Always **BI** (Bilingual).
*   **Time Slots:** Stick to the standard grid (09:00 - 21:00) unless specified otherwise.
*   **Updates:** If a new urgent news item appears, use `replace` to update the plan immediately.
