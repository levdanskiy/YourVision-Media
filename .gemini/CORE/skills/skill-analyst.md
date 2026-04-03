# SKILL: DEEP ANALYST
**Trigger:** `@analyst`, `Найди инфо`, `Проверь факты`
**Description:** Performs deep research for Almanac posts and fact-checks YourVision data (if requested).

---

## 1. RESEARCH PROTOCOL (ALMANAC)
*   **Depth:** Don't just find "what". Find "why", "who", and "symbolism".
*   **Sources:** Prioritize academic sources, cultural heritage sites, and native language sources (e.g., use Spanish query for Tamborrada).
*   **Structure:** Return data in bullet points:
    1.  Core Fact.
    2.  Historical Context.
    3.  Modern Relevance.
    4.  Visual Details (for prompts).

## 2. FACT-CHECKING (YOURVISION)
*   **Trigger:** Only when explicitly asked to verify user input.
*   **Action:** Verify dates, names spelling, and song titles against official EBU/Broadcaster sources.

## 3. TREND WATCHING
*   **Action:** Identify global trends relevant to `Global Trend` or `Costume Code` slots.
*   **Output:** A short brief with 3 potential topics.

## 4. COMMANDS
*   `@analyst research [Topic]` -> Deep dive.
*   `@analyst verify [Text]` -> Fact check.
