# VISUAL PIPELINE

The visual prompt is part of the post package, but the image has its own state.

The actual file state lives in `04_DATABASES/ASSET_REGISTRY.json`. The registry stores its post link, SHA-256, dimensions, MIME type, ALT, rights and approval/use status.

## Required Prompt Rule

Every post prompt should:

- describe the scene plainly;
- avoid people, visible text, logos, UI, watermarks;
- avoid Midjourney flags such as `--ar`, `--v`, `--style`, `--s`;
- end with `shot on 35mm film Kodak Portra 800`.

## Image Status

Use one of these values in new YAML frontmatter or service metadata:

| Status | Meaning |
|--------|---------|
| `needed` | Prompt exists, image not generated. |
| `generated` | Image exists but not approved. |
| `approved` | Image approved for scheduling. |
| `used` | Image was published. |
| `rejected` | Image failed visual or factual fit. |

## Asset Naming

If assets are added later, use this pattern:

```text
03_ASSETS/2026/MM/DD/AL-DD.MM-HH-MM-RUBRIC-Slug.jpg
```

Keep the markdown post as the source record. The image file should not become the only place where the prompt lives.

From `2026-07-21`, a post marked `SCHEDULED`, `PUBLISHED` or `CORRECTED` must have a registered image. Scheduled assets must be `approved`; published assets must be `used`. Approved/used assets require ALT and rights metadata.

```bash
python3 tools/almanac assets sync
python3 tools/almanac assets register 03_ASSETS/2026/MM/DD/POST_ID.jpg --post-id POST_ID --status approved --alt "..." --rights "..."
python3 tools/almanac assets audit YYYY-MM-DD --strict
```

## Alt Text

For each approved visual, add one factual alt text line:

```text
// ALT: Fading purple lilac blossoms in warm late-evening light.
```
