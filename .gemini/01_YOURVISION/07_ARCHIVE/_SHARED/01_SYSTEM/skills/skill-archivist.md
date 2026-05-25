# SKILL: ARCHIVIST & LORE KEEPER
**Trigger:** `@archivist`, `Архивируй`, `Обнови Лор`, `Cleanup`
**Description:** Manages the file system, organizes past posts, and updates the knowledge base (Lore).

---

## 1. FILE ORGANIZATION
*   **Move:** At the end of each day/week, move executed posts from root `posts/` to `archive/[YYYY]/[MM]/[DD]/`.
*   **Naming Convention:** Ensure all files follow `[CHANNEL]-[DD.MM]-[HH-MM]-[TAG]-[Slug].md`.

## 2. LORE UPDATE PROTOCOL
When a post is marked ✅, scan it for new persistent data:
*   **Winners/Results:** Update `YV_Season_2026.md`.
*   **Dates/Events:** Update `YV_ESC_Live_Calendar.md`.
*   **Concepts:** If a new concept (e.g., "Niksen") is explained deeply, add a reference to `AC_Lore.md`.

## 3. WEEKLY DIGEST
*   On Sundays, generate a summary of all ✅ posts.
*   Check for "Ghost Tasks" (tasks marked ⬜ in past plans) and move them to the next `daily_plan`.

## 4. COMMANDS
*   `@archivist cleanup` -> Move files to archive.
*   `@archivist sync` -> Read recent posts and update Lore files.
