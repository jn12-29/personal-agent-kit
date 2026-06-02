---
name: diagram-creator
description: Create or revise text-based diagrams for documentation, specs, architecture notes, workflows, data flows, sequence interactions, C4 views, ER/class/state models, and lightweight timelines using Mermaid, PlantUML, D2, or ASCII. Use when the requested output is diagram source code or a maintainable diagram embedded in Markdown/docs. Do not own final quality for polished document/PPT figures, raster image generation, slide-deck design, or UI mockups.
---

# Diagram Creator

## Why This Exists

Diagram requests fail when agents dump generic examples instead of modeling the actual system, mix abstraction levels, or create image-only artifacts that cannot be revised. This skill keeps diagrams source-controlled, focused on one question, and easy to update.

Prefer the smallest diagram that answers the user's request. Mermaid, PlantUML, or D2 can be useful as source-only outputs or intermediate sources for simple figure diagrams, but if the user needs a polished DOCX/PPT-ready asset, `document-figure-designer` owns the final rendered quality; if the task is a full slide deck, use the presentation workflow.

## Decision Gate

- Architecture, C4, deployment, component, sequence, data-flow, ER, class, state, flowchart, timeline, or process source: use this skill.
- Figure asset inserted into a report, proposal, Word document, PDF, or slide: use `document-figure-designer`, unless the user only asks for Mermaid/PlantUML/D2 source. Text-based diagram source may still be an intermediate artifact, but final document/slide readability and layout QA belong to `document-figure-designer`.
- Documentation contract, plan, or cross-module spec that happens to include a diagram: use `spec-driven-planning` for the contract and this skill only for the diagram artifact.
- Raster image, illustration, screenshot, or visual mockup: use the relevant image, browser, document, or frontend workflow instead.

## Workflow

1. Identify the purpose, audience, target format, and where the diagram will live.
2. Read the source material before drawing: code, docs, architecture notes, schemas, APIs, workflows, or user-provided facts.
3. Pick one diagram type and one abstraction level. Do not combine context, component, deployment, and sequence details into one crowded diagram.
4. Use stable names from the source material. Mark assumptions explicitly instead of inventing services, tables, states, or relationships.
5. Choose the format that best fits the destination:
   - Mermaid for Markdown, GitHub, lightweight docs, ER, state, sequence, and flowcharts.
   - PlantUML for UML-heavy, C4-style, or large component diagrams when Mermaid becomes awkward.
   - D2 when the repo already uses it or when layout readability matters more than GitHub-native rendering.
   - ASCII only for quick terminal-safe sketches.
6. Keep labels short, directional arrows clear, and grouping meaningful. Add a legend only when symbols or colors carry semantics.
7. If editing an existing diagram, preserve the existing tool and style unless it is the source of the problem.
8. Validate the syntax when a renderer or CLI is available; otherwise do a focused source review for unclosed blocks, invalid identifiers, and stale names.

## Architecture And System Diagrams

For system design, prefer a sequence of focused views over one large diagram:

- Context view: actors, external systems, and the system boundary.
- Container or component view: deployable units, modules, services, stores, and major dependencies.
- Sequence view: one runtime scenario or API interaction.
- Data-flow view: source, transformation, storage, and consumers.
- Deployment view: runtime nodes, networks, infrastructure services, and ownership boundaries.

Keep each view honest about its level. A context diagram should not show database tables; a deployment diagram should not explain business workflow decisions.

## Quality Gate

- The diagram answers a specific question and has a clear title or surrounding prose context.
- Every node, actor, table, state, and edge is grounded in provided source material or clearly marked as an assumption.
- The diagram uses one abstraction level and avoids unrelated implementation detail.
- Directionality is clear; arrows are labeled when the relationship is not obvious.
- Naming matches the repo or source docs.
- The diagram remains maintainable as text source and is not only a rendered image.
- Obsolete names from the source material or prior diagram version have been searched when editing existing docs.

## Resources

- `references/architecture-patterns.md`: compact patterns for architecture, C4-style, sequence, data-flow, component, deployment, ER, class, and state diagrams.

Read the reference when creating architecture or system diagrams, when choosing between diagram types, or when revising an existing architecture diagram for consistency.
