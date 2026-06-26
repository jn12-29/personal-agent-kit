---
name: diagram-creator
description: Use when the requested output is maintainable text diagram source for docs, specs, architecture notes, workflows, data flows, sequences, models, or lightweight timelines. Supports Mermaid, PlantUML, D2, and ASCII. Do not use for polished document/slide figure assets, raster visual-reference passes, or UI mockups.
---

# Diagram Creator

## Why This Exists

Diagram requests fail when agents dump generic examples instead of modeling the actual system, mix abstraction levels, preserve weak old layouts, or create image-only artifacts that cannot be revised. This skill keeps diagrams source-controlled, focused on one question, and easy to update.

Prefer the smallest diagram that answers the user's request. Mermaid, PlantUML, or D2 can be useful as source-only outputs or intermediate sources for simple figure diagrams, but polished DOCX/PPT-ready figure assets and full slide-deck layout are outside this source-diagram workflow.

## Decision Gate

- Architecture, C4, deployment, component, sequence, data-flow, ER, class, state, flowchart, timeline, or process source: use this skill.
- Figure asset inserted into a report, proposal, Word document, PDF, or slide: outside this skill unless the user only asks for Mermaid/PlantUML/D2 source. Text-based diagram source may still be an intermediate artifact, but final document/slide readability and layout QA are separate figure-asset work.
- Visual redesign, polished infographic, raster image, rendered PNG, screenshot, presentation-ready figure, or AI-generated visual reference: outside this text-diagram workflow.
- Documentation contract, plan, or cross-module spec that happens to include a diagram: this skill owns only the diagram artifact, not the contract or plan structure.
- Raster image, illustration, screenshot, or visual mockup: outside this text-diagram workflow.

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
7. If editing an existing diagram, treat the prior version as evidence, not as a layout contract. Preserve the existing tool only when the destination still needs maintainable text source and the tool is not the source of the problem.
8. Validate the syntax when a renderer or CLI is available; otherwise do a focused source review for unclosed blocks, invalid identifiers, and stale names.

## Redraw Gate

When revising an existing source diagram, assume the old design may be wrong until checked. Extract the facts first: purpose, audience, nodes, relationships, direction, labels, and must-preserve constraints. Then name any old-diagram failures that would justify a structural redraw: mixed abstraction levels, unclear direction, crowded labels, irrelevant detail, stale names, tangled edges, or a diagram type that no longer answers the question.

Do not make cosmetic edits to a flawed source diagram. Rebuild the diagram with the smallest source representation that answers the current question. If the requested outcome is visual polish, presentation quality, raster output, or a design reference image, stop at the source facts or intermediate text diagram and hand off to a figure-asset workflow instead of forcing that work into Mermaid, PlantUML, D2, or ASCII.

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
- Existing diagrams were checked as source facts, not blindly preserved as design templates.
- Obsolete names from the source material or prior diagram version have been searched when editing existing docs.

## Resources

- `references/architecture-patterns.md`: compact patterns for architecture, C4-style, sequence, data-flow, component, deployment, ER, class, and state diagrams.

Read the reference when creating architecture or system diagrams, when choosing between diagram types, or when revising an existing architecture diagram for consistency.
