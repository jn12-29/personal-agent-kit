# Document Figure Quality Reference

## Source Decision Table

| Figure intent | Preferred source | Avoid |
|---|---|---|
| Show current UI or feature page | Screenshot from the actual reachable frontend | Mocked pages, old screenshots, invented modules |
| Explain architecture, API, data flow, or file layout | AI-generated visual reference followed by controlled SVG or HTML/CSS rendered to raster image with Chromium/Playwright | Auto-layout diagrams that create tiny text or tangled arrows |
| Explain algorithm steps | Structured diagram with a small number of stages | Dense formulas as tiny labels |
| Create a polished infographic, educational visual, or presentation-style figure where bitmap delivery is acceptable | AI-generated raster image with exact text/data review | Treating generated labels, arrows, or facts as authoritative |
| Add non-product visual texture | Raster image generation | Images that look like product screenshots but are not real |

## Critical Redraw Checklist

- Existing figures are evidence, not design templates.
- Extract the figure message, audience, target size, nodes, relationships, direction, labels, and must-preserve facts before drawing.
- Name the old design failures before revising: mixed abstraction levels, weak hierarchy, crowded labels, tangled connectors, tiny legends, stale terms, misleading emphasis, decorative clutter, or poor canvas use.
- Redraw instead of patching when the old figure cannot pass readability, accuracy, layout, and figure-boundary checks with small local edits.
- Preserve an old visual choice only when it is a true requirement from the source material, target document, or user request.

## AI Visual Reference Checklist

- Run a visual-reference pass for every new, redesigned, or materially revised generated diagram, infographic, concept figure, or text-heavy raster figure unless the user explicitly requires a source-only/offline workflow or generation is technically unavailable.
- Do not run the visual-reference pass for real screenshots or evidence-only figures that must show current UI or product state. Capture the actual state and QA the screenshot directly.
- Prompt with intended use, audience, asset type, canvas shape, layout flow, exact text, must-preserve facts, constraints, and avoid rules.
- Use the reference for layout, visual hierarchy, palette direction, spacing, and composition ideas.
- Do not trust the reference for facts. Check every node, arrow direction, count, label, number, axis, legend, and relationship against the source material.
- Reject or regenerate references that add extra text, omit required text, invent entities, reverse relationships, create unreadable microtext, or imply false data.
- If a raster output is the final asset, review the final raster image directly. If factual or text errors persist, switch to controlled SVG/HTML/CSS instead of explaining around the errors.

## Diagram Acceptance Checklist

- Smallest generated text remains readable at final Word/PDF/slide insertion size.
- Every label remains legible and understandable; if text becomes small, simplify the figure instead of shrinking labels.
- Exact text, data values, labels, axes, legends, and relationship directions match the approved source facts.
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
- Editable source files are the source of truth for later edits; do not patch exported raster files when a source file exists.

## Must Redraw Conditions

- The figure mixes context, component, sequence, deployment, data-model, or business-process levels in one crowded view.
- More than one main reading order competes for attention.
- Arrow direction is ambiguous, reversed, unlabeled where needed, or crosses unrelated blocks.
- Labels are too small, too many, inconsistent, clipped, or placed on top of lines and borders.
- The figure relies on a tiny legend or many badges to explain core meaning.
- The canvas leaves large unused margins while important content is cramped.
- Auto-layout output looks generic, tangled, or visually unintentional.
- The source preview and exported raster file do not match.
- A generated raster image contains wrong, missing, or extra text or data that cannot be corrected reliably.

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
- Use explicit marker definitions for arrowheads; visually inspect after raster export because some renderers scale markers differently.
- If static checks pass but the image still looks crowded, simplify the diagram rather than shrinking text.
- Preserve both editable source and exported raster/SVG outputs for generated figures.
- After insertion into DOCX, PDF, or slides, inspect the final page because application scaling can make acceptable source art unreadable.

## Chromium Export Checklist

- Use Chromium/Playwright as the canonical renderer for SVG and HTML/CSS preview and raster export.
- Treat `scripts/svg_readability_check.py` as a static precheck, not as proof of final visual quality.
- Review the raster file exported by the same Chromium/Playwright path that will be delivered or inserted.
- Check font fallback, line wrapping, clipping, shadows, filters, masks, clip paths, gradients, external images, and relative resource paths in the exported raster file.
- Omit renderer background overrides unless intentionally replacing the source-defined SVG canvas or letterbox background.
- Do not use ImageMagick, CairoSVG, librsvg, Inkscape, Batik, or Office conversion output as the default authority for final rendered QA. Use them only for compatibility checks when explicitly needed.
- If Chromium/Playwright or its managed Chromium browser cannot be installed, report that canonical rendering was skipped and do not claim final rendered QA passed.
