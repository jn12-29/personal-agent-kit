---
name: document-figure-designer
description: Use when creating, redesigning, revising, or quality-checking explanatory figure assets for documents or slides, including architecture, workflow, process, API, data-flow, algorithm, concept, infographic, and text-heavy figures. Owns DOCX/PDF/PPT-ready raster/SVG assets, mandatory AI-generated visual-reference passes for generated figures, Chromium/Playwright rendering, and readability QA, not whole-slide, page, or deck layout.
---

# Document Figure Designer

## Overview

Use this skill to produce figures that are accurate, readable at document scale, and easy to revise. It applies to figures embedded in documents or slides, but not to overall slide theme or deck beautification. The figure should explain the surrounding content clearly, sit naturally in its container, avoid decorative backgrounds by default, and remain legible after insertion into DOCX, PDF, or slides.

Figure work fails when agents preserve weak old layouts, accept auto-layout output as final, trust image-generated facts, or review SVG/HTML source instead of the exported asset readers will see. This skill forces a critical redraw mindset, a visual-reference pass for design exploration, a single browser rendering engine for preview and export, and rendered-output QA before delivery.

## Figure Boundary

This skill produces figure assets, not slide or page layouts. Agents often make figures look self-contained by adding global slide titles, subtitles, captions, logos, or explanatory prose into the exported canvas. That makes the asset fight the surrounding PPT/DOCX/PDF layout and wastes figure space that should carry the diagram itself.

By default, do not include slide-level or page-level titles, subtitles, captions, logos, headers, footers, or surrounding explanatory prose inside the exported figure. Assume those belong outside the figure in the target document or slide layout.

Allowed inside the figure: panel headers, swimlane labels, axis labels, stage labels, legends, node labels, and short group labels required to understand the diagram structure.

Not allowed by default: global page titles, deck-style subtitles, prose summaries, decorative title bands, captions, logos, or other text that describes the figure from outside the diagram. Include them only when the user explicitly asks for a complete slide/page design or for those elements to be part of the figure itself.

## Workflow

1. Inventory scope before drawing.
   - List figure numbers, captions, source files, and document sections in scope.
   - Respect explicit exclusions such as "only figures before section X" or "do not modify figure N and later."
   - Figure captions and figure-internal titles guide the figure, but they are not constraints. Rename those figure-specific labels when accuracy or clarity requires it.

2. Extract facts and criticize the current design.
   - Treat existing figures, sketches, screenshots, Mermaid, SVG, or generated images as evidence, not as design templates.
   - Extract the message, audience, target insertion size, nodes, relationships, direction, exact labels, and must-preserve facts before drawing.
   - Name the current design failures that must not be carried forward: mixed abstraction levels, weak hierarchy, cramped labels, tangled arrows, tiny legends, decorative clutter, stale text, poor canvas use, misleading emphasis, or preview/export mismatch.
   - Default to rebuilding the visual model instead of making local cosmetic edits when any blocker is present.

3. Run the mandatory visual-reference pass for generated figures.
   - For every new, redesigned, or materially revised generated diagram, infographic, concept figure, or text-heavy raster figure, generate or request an AI-generated raster visual reference before finalizing the editable source or final raster asset.
   - Do not run the visual-reference pass for real screenshots or evidence-only figures that must show current UI or product state. Capture the actual UI or product state and QA that screenshot directly.
   - The visual-reference prompt must include intended use, audience, asset type, canvas shape, layout flow, exact text, must-preserve facts, and avoid rules. For unusual terms or labels, quote the exact text and spell out that no extra text is allowed.
   - Use the reference for layout, hierarchy, spacing, palette direction, and visual language. Do not treat reference-image text, arrows, counts, relationships, or data as authoritative.
   - Skip the visual-reference pass only when the user explicitly requires a source-only/offline workflow or image generation is technically unavailable. State the skip reason in the final response.

4. Choose the right figure source.
   - Structured explanatory figures such as architecture, workflow, process, API, file layout, data-flow, algorithm, or concept diagrams: draw with SVG/HTML/CSS and controlled layout when precise visual control is needed.
   - Simple Mermaid, PlantUML, or D2 diagrams can be rendered into PPT/DOCX-ready SVG or PNG when the generated layout remains readable at the final insertion size. If the rendered output becomes crowded, tangled, or visually generic, redraw with controlled SVG/HTML/CSS instead of accepting the auto-layout.
   - Product UI state: use a real screenshot only when the figure needs to show actual UI; see the reference checklist for screenshot QA.
   - Raster image generation is valid for polished infographics, conceptual figures, text-heavy educational visuals, and presentation-style figure assets when a bitmap deliverable is acceptable and every label, relationship, and data point can be reviewed from the rendered output. Non-figure art and full presentation design are outside this figure-asset workflow.

5. Design for document scale.
   - For standalone figure assets intended for Word, PDF, or slides, default to a 16:9 canvas at 1920x1080 unless the user, target placeholder, or document template requires another size. Treat the canvas as the figure itself, not the surrounding document or slide layout: do not reserve empty outer space for titles, logos, captions, or nearby prose. Keep only the internal padding needed so labels, arrows, and blocks do not touch the canvas edge or get cropped.
   - Do not draw slide/page titles or subtitles inside the figure canvas by default. This is not only about avoiding reserved whitespace; title-like text that belongs to the surrounding document must stay outside the exported figure.
   - Before rendering, classify every large text element as either a diagram-internal label or surrounding layout text. Keep labels required to interpret panels, groups, axes, stages, or nodes. Remove slide/page titles, subtitles, captions, logos, and nearby prose unless explicitly requested.
   - Every label must remain legible at the final inserted size; if text becomes small, simplify the figure instead of shrinking labels. Screenshots are exempt from generated-label font-size rules, but must still be readable at the inserted size.
   - Use a stable canvas and fill the figure canvas. Avoid decorative backgrounds by default; use subtle fills or section bands only when they clarify grouping or reading order without reducing text contrast.
   - Use larger cards and fewer tiny labels instead of dense microtext.
   - Route arrows directly when possible. Arrowheads must be visibly large, have unambiguous direction, and never cover labels or blocks. Leave visible clearance between arrowheads, labels, and block edges.
   - Do not let connector lines pass through unrelated blocks; adjust spacing or routing instead of accepting overlap.

6. Export source and final assets.
   - Keep editable sources and intermediate artifacts for generated figures, so small corrections can be patched and reviewed without regenerating the whole figure.
   - Treat editable source files as the source of truth for later edits; do not patch exported raster files when a source file exists.
   - Preserve both editable diagram source such as SVG, HTML/CSS, Mermaid, PlantUML, or D2 and raster/SVG exports when the figure is generated from code.
   - Export raster images at enough resolution for the final inserted size; 1920x1080 is the default for standalone 16:9 figure assets.
   - Name files by figure number and purpose, not by temporary attempts.
   - For SVG or HTML/CSS figures, use Chromium/Playwright as the canonical preview and raster export engine. Use PNG by default, but respect an explicit supported `.jpg` or `.jpeg` output request. Do not use ImageMagick, CairoSVG, librsvg, Inkscape, Batik, or Office conversion as the default authority for final rendered QA.

7. QA before insertion.
   - Render and inspect each figure at the approximate size it will appear in the document.
   - For generated or materially revised figures, complete the Visual Review Loop below before final delivery.
   - Use `scripts/svg_readability_check.py` for SVG diagrams as a static precheck, then use `scripts/render_with_playwright.py` for canonical Chromium/Playwright raster rendering and visual inspection.
   - Re-check captions and nearby prose after replacing a figure.
   - Open the final DOCX, PDF, or slide deck when practical and inspect the inserted figure in context.

## Renderer Dependency Policy

If Chromium/Playwright is missing, the agent may install the Python Playwright package and its managed Chromium browser in the current project or active Python environment. Do not use `sudo`, do not modify system-wide browser installations, and do not silently change global Node/Python environments. Report the install commands, then verify the renderer before using it.

Preferred commands:

```sh
FIGURE_RENDERER="${FIGURE_RENDERER:-}"
if [ -z "$FIGURE_RENDERER" ]; then
  for candidate in \
    "$PWD/skills/document-figure-designer/scripts/render_with_playwright.py" \
    "$HOME/.agents/skills/document-figure-designer/scripts/render_with_playwright.py" \
    "$HOME/.claude/skills/document-figure-designer/scripts/render_with_playwright.py"
  do
    if [ -f "$candidate" ]; then
      FIGURE_RENDERER="$candidate"
      break
    fi
  done
fi
[ -n "$FIGURE_RENDERER" ] || { echo "render_with_playwright.py not found; set FIGURE_RENDERER to the script path" >&2; exit 1; }

uv venv .venv
uv pip install playwright
uv run python -m playwright install chromium
uv run python "$FIGURE_RENDERER" --input <figure.svg|figure.html> --out <figure.png>
```

Use `.png` by default for document figures. If the caller explicitly requests `.jpg` or `.jpeg`, pass that suffix in `--out` and inspect the exported file for compression artifacts.

Omit `--background` to preserve source-defined SVG backgrounds. Pass `--background <color>` only when intentionally overriding the exported canvas and letterbox background; pass `--background transparent` only when the consumer supports alpha and the source itself does not draw an opaque background.

If `uv` is unavailable, resolve `FIGURE_RENDERER` the same way, then run `python -m venv .venv`, `.venv/bin/python -m pip install playwright`, `.venv/bin/python -m playwright install chromium`, and `.venv/bin/python "$FIGURE_RENDERER" --input <figure.svg|figure.html> --out <figure.png>`. Keep the virtual environment out of tracked files. If installation is impossible or blocked, report that canonical Chromium/Playwright rendering was not completed and do not claim final rendered QA passed.

## Visual Review Loop

Agents tend to treat a rendered figure as complete once it resembles a diagram. That is the failure point: figure defects are visual, not just structural. Tiny labels, weak hierarchy, cramped spacing, unclear arrows, misleading emphasis, generic styling, and poor use of the canvas often become obvious only after the source is rendered at the intended output size. Self-review is biased because the agent remembers what it meant to draw, while readers only see what the image communicates.

Generated or materially revised figures are not complete after the first render. The rendered asset must be visually reviewed, confirmed blockers must be fixed in the editable source, and the fixed source must be re-rendered and reviewed again.

For generated or materially revised figures:

1. Render the figure at the intended output size before final delivery. For SVG or HTML/CSS sources, render with Chromium/Playwright.
2. Review the rendered image, not only the SVG, HTML/CSS, Mermaid, PlantUML, D2, prompt, or reference image.
3. When subagents are available, use independent read-only visual reviewers with distinct perspectives:
   - Readability and layout: font size, contrast, spacing, cropping, arrow clearance, and line/block overlap.
   - Communication accuracy: whether the figure answers the caption or prose goal, preserves true relationships, and avoids misleading emphasis.
   - Visual polish: hierarchy, balance, rhythm, palette, consistency, and whether the result looks intentional rather than auto-generated.
   - Text and data fidelity: exact text, labels, numbers, axes, legends, and relationship direction match the source facts.
   If subagents are unavailable, self-review the rendered image across the same perspectives.
4. Fix confirmed blockers in the editable source, then re-render.
5. Re-review after each blocker fix. Do not stop immediately after applying the fix.
6. Stop when the latest rendered review has no blockers. Do not chase unlimited subjective preferences; record unresolved taste differences as non-blocking concerns once readability, accuracy, and layout quality are acceptable.

Reviewer prompt shape:

```text
You are a READ-ONLY visual reviewer. Do not edit files.
Review the rendered figure image, not only the source.

Context:
- Rendered image: attach the image or provide its absolute path
- Editable source: ...
- Intended use: Word/PDF/slide figure
- Target size: ...
- Caption or message: ...
- Must-preserve facts: ...
- Exact text/data to verify: ...

Perspective:
- readability/layout | communication accuracy | visual polish | text/data fidelity | figure-boundary

For figure-boundary, check:
- Does the exported figure include slide/page-level title, subtitle, caption, logo, header/footer, or surrounding prose?
- Are all large labels necessary diagram-internal labels?
- Does the figure reserve or consume space for content that should live outside the figure?

Report only:
- [blocker] <region/element> - <visible problem> - <actionable fix direction>
- [non-blocking concern] <region/element> - <subjective or low-risk improvement>
- [assumption] context you had to infer

If there are no blockers, concerns, or assumptions, output exactly:
No blockers.
```

## Visual Standards

- Generated diagram body text: usually at least 24 px in the source canvas; prefer 26-32 px for Chinese labels. Every label must remain legible at the final inserted size.
- Figure section/group titles and major node labels: usually 34 px or larger.
- Arrowheads: visually obvious at final document size; as a starting point, marker width/height should be 14 px or larger in SVG. Keep arrowheads clear of labels and block edges.
- Line weight: thick enough to survive Word/PDF compression, usually 3-5 px for full-width diagrams.
- Layout: no nested cards for page sections, no decorative background unless it clarifies grouping or reading order without reducing contrast, no tiny legends, no text touching borders or connector lines.
- Figure boundary: standalone figure exports must not include slide/page titles, subtitles, captions, logos, headers/footers, or surrounding explanatory prose by default. Panel titles and diagram-internal labels are allowed only when they are necessary to understand the figure structure.
- Palette: polished and restrained, with enough contrast; avoid one-note palettes that make every block look the same.
- AI-generated raster figures and references must be checked for extra text, missing text, invented entities, wrong arrow direction, and data drift. If the generated image cannot be corrected reliably, rebuild the figure in controlled SVG/HTML/CSS.

Examples:
- Allowed: "v1 Baseline", "v2 Upgrade", "Input", "Verifier", "Shared JSONL" when these label parts of the diagram.
- Not allowed by default: "Contrastive Text Dataset Construction" as a page title, "Two pipelines produce..." as a slide subtitle, or a caption explaining the figure from outside the diagram.

## Resources

- `scripts/svg_readability_check.py`: static QA for SVG dimensions, explicit font sizes, arrow markers, and simple connector/block crossings.
- `scripts/render_with_playwright.py`: canonical Chromium/Playwright rendering for SVG and HTML/CSS figure sources.
- `references/figure-quality.md`: detailed decision table and acceptance checklist.

Read the reference when more than one figure is being created or when the user criticizes readability, routing, screenshots, or visual polish.
