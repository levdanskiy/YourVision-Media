# CORRECTIONS AND INCIDENTS

## Principle

A published post is not silently rewritten when a meaningful factual, attribution, rights, cultural-context or safety problem is discovered. Preserve the original record, correct the public surface when necessary, and log the decision.

## Severity

| Severity | Examples | Response |
|---|---|---|
| `critical` | Dangerous advice, serious defamation, unlawful image use, fabricated source | Halt scheduling and act immediately |
| `high` | Central factual claim false, wrong sacred attribution, material translation error | Correct the same day |
| `medium` | Important date, spelling, context or image mismatch | Correct within 48 hours |
| `low` | Typo or formatting issue that does not change meaning | Correct in maintenance cycle |

## Public Correction

- Add a dated correction note when meaning changed or the original claim may already have circulated.
- Do not delete a post merely to hide an editorial error. Removal is allowed for safety, legal, privacy or rights reasons and must remain in the incident log.
- A disputed source is not automatically false. Pause the claim, compare source hierarchy and state uncertainty.
- A forecast or tarot interpretation failing to occur is not an incident by itself. Incorrect astronomical inputs, concealed automation, deterministic harmful advice or false claims about a tradition are incidents.
- For image-rights problems, remove or replace the asset first, then resolve attribution and public notice.

## Workflow

```bash
python3 tools/incident_manager.py add POST_ID --severity high --issue "..." --public-correction yes
python3 tools/incident_manager.py resolve INCIDENT_ID --correction "..." --public-notice "..."
python3 tools/incident_manager.py audit YYYY-MM-DD --strict
```

Resolved meaningful corrections are appended to `03_REPORTS/CORRECTIONS.md`, and a published registry record moves to `corrected`.
