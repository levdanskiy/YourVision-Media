# Series Keeper Agent

## Purpose

Track recurring formats without letting them crowd out global rubric rotation.

## Contract

- Maintain `04_DATABASES/SERIES_REGISTRY.json` after every installment.
- From 20.07.2026 through 22.07.2026, keep the transition ORACLE-NOTE/CALENDAR-RADAR obligation if it is already scheduled.
- From 23.07.2026, standalone ORACLE-NOTE, CALENDAR-RADAR and all non-recipe series route to Almanac: Calendar (`/home/levdanskiy/.gemini/05_Almanac: Calendar`, https://t.me/AlmanacCalendar). Track Almanac recipe-service formats instead: MENU-RADAR, SHOPPING-LIST, TECHNIQUE-POLL, RECIPE-INDEX, PREP-NOTE. Keep SP at 2-4 per month.
- Pause a weak series after its first underperforming installment; do not force promised parts.
- Run `python3 tools/almanac series YYYY-MM-DD` before planning service posts.
