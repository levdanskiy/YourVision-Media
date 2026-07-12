# ANALYTICS REVIEW

Every intentional format, tone or workflow change must be registered in `04_DATABASES/EXPERIMENT_REGISTRY.json` with hypothesis, baseline, target, metric, review date and final decision. An overdue running experiment is a publishing-blocking debt on its review date.

```bash
python3 tools/almanac experiments list
python3 tools/almanac experiments audit YYYY-MM-DD --strict
```

Almanac uses analytics to improve editorial judgment, not to chase viral behavior.

## Cadence

Run a review every two weeks and after every major series.

Do not rewrite editorial rules from one bad post. Change rules only when a pattern repeats across at least 3 comparable posts or 2 comparable series.

## Required Metrics

For each reviewed post:

| Field | Meaning |
|-------|---------|
| `post_id` | Filename/id. |
| `date_time` | Publication date and slot. |
| `rubric` | AL rubric or SV/SP type. |
| `views_24h` | Views after 24 hours. |
| `subscribers_at_post` | Subscriber count at posting. |
| `er_24h` | `views_24h / subscribers_at_post * 100`. |
| `forwards` | If available. |
| `reactions` | If available. |
| `comments_or_poll` | If available. |
| `notes` | What likely caused performance: source, hook, length, visual, date, poll, series position. |

If subscriber count is unknown, record views only and mark ER as `unknown`.

## Biweekly Template

```text
// ANALYTICS REVIEW: [period]
// STATUS: DRAFT/COMPLETE

Subscribers at start:
Subscribers at end:

Top 3 by ER:
1. [post_id] - [ER] - why it likely worked
2. ...
3. ...

Bottom 3 by ER:
1. [post_id] - [ER] - likely issue
2. ...
3. ...

Best slot:
Weakest slot:
Best rubric:
Weakest rubric:

Series status:
- Continue:
- Adjust:
- Stop:

Next editorial test:
[one change only]
```

## Series Failure Rule

If part 1 of a planned series underperforms:

1. Do not cancel immediately.
2. Publish part 2 only if it adds a new object/source/mechanism, not a repetition.
3. If part 2 also underperforms, stop or compress the rest into one `SV SERIES-NAV` or recap.
4. Do not use `SP` to rescue a weak series.

## What Analytics May Change

Allowed:
- post length bands;
- order of blocks;
- frequency of a rubric;
- whether a series continues;
- whether a service note is useful;
- visual prompt strategy.

Forbidden:
- adding engagement bait;
- ranking cultures or countries by popularity;
- dropping global coverage because familiar zones perform better;
- replacing source discipline with trend hooks.
