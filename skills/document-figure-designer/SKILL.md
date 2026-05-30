---
name: document-figure-designer
description: Create, revise, and quality-check explanatory figures for documents and slides. Use for architecture, workflow, process, API, data-flow, algorithm, and concept figures; DOCX/PPT-ready PNG/SVG assets; caption cleanup; readability QA; arrow routing; or replacing inaccurate illustrations. Not for whole-slide-deck design.
---

# Document Figure Designer

## Overview

Use this skill to produce figures that are accurate, readable at document scale, and easy to revise. It applies to figures embedded in documents or slides, but not to overall slide theme or deck beautification. The figure should explain the surrounding content clearly, sit naturally in its container, avoid decorative backgrounds by default, and remain legible after insertion into DOCX, PDF, or slides.

## Workflow

1. Inventory scope before drawing.
   - List figure numbers, captions, source files, and document sections in scope.
   - Respect explicit exclusions such as "only figures before section X" or "do not modify figure N and later."
   - Captions and inherited titles guide the figure, but they are not constraints. Rename them when accuracy or clarity requires it.

2. Choose the right figure source.
   - Structured explanatory figures such as architecture, workflow, process, API, file layout, data-flow, algorithm, or concept diagrams: draw with SVG/HTML/CSS and controlled layout.
   - Product UI state: use a real screenshot only when the figure needs to show actual UI; see the reference checklist for screenshot QA.
   - Abstract concept or cover art: use raster image generation only if product accuracy is not implied.

3. Design for document scale.
   - Every label must remain legible at the final inserted size; if text becomes small, simplify the figure instead of shrinking labels. Screenshots are exempt from generated-label font-size rules, but must still be readable at the inserted size.
   - Use a stable canvas and fill the page area. Avoid decorative backgrounds by default; use subtle fills or section bands only when they clarify grouping or reading order without reducing text contrast.
   - Use larger cards and fewer tiny labels instead of dense microtext.
   - Route arrows directly when possible. Arrowheads must be visibly large, have unambiguous direction, and never cover labels or blocks. Leave visible clearance between arrowheads, labels, and block edges.
   - Do not let connector lines pass through unrelated blocks; adjust spacing or routing instead of accepting overlap.

4. Export source and final assets.
   - Keep editable sources and intermediate artifacts for generated figures, so small corrections can be patched and reviewed without regenerating the whole figure.
   - Treat editable source files as the source of truth for later edits; do not patch exported PNGs when a source file exists.
   - Preserve both SVG/HTML/CSS source and PNG exports when the figure is generated from code.
   - Export raster images at enough resolution for Word/PDF/slides; prefer 1600-2400 px wide for full-width document figures.
   - Name files by figure number and purpose, not by temporary attempts.

5. QA before insertion.
   - Render and inspect each figure at the approximate size it will appear in the document.
   - Use `scripts/svg_readability_check.py` for SVG diagrams, then still perform visual inspection for overlap and aesthetics.
   - Re-check captions and nearby prose after replacing a figure.
   - Open the final DOCX, PDF, or slide deck when practical and inspect the inserted figure in context.

## Visual Standards

- Generated diagram body text: usually at least 24 px in the source canvas; prefer 26-32 px for Chinese labels. Every label must remain legible at the final inserted size.
- Section titles and major node labels: usually 34 px or larger.
- Arrowheads: visually obvious at final document size; as a starting point, marker width/height should be 14 px or larger in SVG. Keep arrowheads clear of labels and block edges.
- Line weight: thick enough to survive Word/PDF compression, usually 3-5 px for full-width diagrams.
- Layout: no nested cards for page sections, no decorative background unless it clarifies grouping or reading order without reducing contrast, no tiny legends, no text touching borders or connector lines.
- Palette: polished and restrained, with enough contrast; avoid one-note palettes that make every block look the same.

## Resources

- `scripts/svg_readability_check.py`: static QA for SVG dimensions, explicit font sizes, arrow markers, and simple connector/block crossings.
- `references/figure-quality.md`: detailed decision table and acceptance checklist.

Read the reference when more than one figure is being created or when the user criticizes readability, routing, screenshots, or visual polish.
