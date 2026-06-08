# VISUAL PIPELINE

The visual prompt is part of the post package, but the image has its own state.

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

## Alt Text

For each approved visual, add one factual alt text line:

```text
// ALT: Fading purple lilac blossoms in warm late-evening light.
```
