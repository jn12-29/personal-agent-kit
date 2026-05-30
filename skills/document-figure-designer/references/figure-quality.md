# Document Figure Quality Reference

## Source Decision Table

| Figure intent | Preferred source | Avoid |
|---|---|---|
| Show current UI or feature page | Screenshot from the actual reachable frontend | Mocked pages, old screenshots, invented modules |
| Explain architecture, API, data flow, or file layout | SVG or HTML/CSS rendered to PNG | Auto-layout diagrams that create tiny text or tangled arrows |
| Explain algorithm steps | Structured diagram with a small number of stages | Dense formulas as tiny labels |
| Add non-product visual texture | Raster image generation | Images that look like product screenshots but are not real |

## Diagram Acceptance Checklist

- Smallest generated text remains readable at final Word/PDF/slide insertion size.
- Every label remains legible and understandable; if text becomes small, simplify the figure instead of shrinking labels.
- Text does not touch borders, arrows, or adjacent content.
- Cards have enough internal padding and use the full canvas instead of leaving large unused margins.
- Arrows have visible arrowheads and clear direction.
- Connector lines do not pass through unrelated blocks.
- Direct horizontal or vertical connectors are preferred over decorative routing when the relationship is simple.
- Labels are fewer and larger; avoid splitting one concept into many tiny badges.
- The palette has clear hierarchy and contrast without becoming a one-color theme.
- The diagram avoids decorative backgrounds by default; use subtle fills or section bands only when they clarify grouping or reading order without reducing text contrast.
- Arrowheads, labels, and block edges have visible clearance.
- Captions and inherited titles guide the figure, but they are not constraints. Rename them when accuracy or clarity requires it.
- Editable sources and intermediate artifacts are kept when possible, so later small corrections can be patched and reviewed instead of redrawing or regenerating the whole figure.
- Editable source files are the source of truth for later edits; do not patch exported PNGs when a source file exists.

## Screenshot Acceptance Checklist

- The image comes from the actual frontend service or product state.
- The page has loaded data or intentionally shows an empty state relevant to the text.
- The crop shows the UI being discussed and removes browser chrome unless it is relevant.
- Sensitive or local-only tokens are not visible.
- The screenshot is sharp at insertion size and is not distorted by resizing.
- If the UI is wrong, fix or choose a different accurate screenshot; do not document a fake UI as reality.
- Screenshots are exempt from generated-label font-size rules, but must still be readable at the inserted size.

## Practical Rendering Notes

- For SVG diagrams, prefer a viewBox around 1600x900 or larger for wide figures.
- Use explicit `font-size` values on text elements or inherited groups so static checks can catch tiny text.
- Use explicit marker definitions for arrowheads; visually inspect after PNG export because some renderers scale markers differently.
- If static checks pass but the image still looks crowded, simplify the diagram rather than shrinking text.
- Preserve both editable source and exported PNG/SVG outputs for generated figures.
- After insertion into DOCX, PDF, or slides, inspect the final page because application scaling can make acceptable source art unreadable.
