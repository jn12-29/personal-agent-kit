# Final Material Review Checklist

Use this checklist when a project proposal, grant application, university-industry collaboration material, project task statement, technical plan, midterm/final report, acceptance material, manual, or other project document needs more than a small wording fix.

## Scope Anchors

- Identify user-confirmed sections that must not be rewritten.
- Identify section or figure ranges that are explicitly in scope.
- Identify sections excluded by the user, even if they look stale.
- Identify the target use: application, contract, planning, review, technical design, execution, report, acceptance, delivery, communication, or presentation material.
- Identify source materials that can be reused for structure versus materials that are only references.
- Classify source materials as evidence, constraints, or process metadata before reusing them. Evidence can support content; constraints guide structure and coverage; process metadata is excluded from final-facing prose unless the target document is meant to expose that process.
- Identify required templates, fixed fields, section order, numbering, table layout, and word limits that must not be changed.
- Leave required template fields in place even when content is pending.
- Preserve useful figure captions/placeholders when the user plans to add art later.
- Do not force old figure titles if they no longer match the actual system.

## Current-State Checks

- Project name, purpose, audience, document type, and target context match the current or proposed project.
- Background, problem definition, objectives, technical/research route, work packages, deliverables, indicators, schedule, resources, risks, budget/compliance/responsibility-sensitive claims, and responsibilities match the provided materials.
- Old project names, objectives, methods, tasks, indicators, organizations, partners, tables, and figure titles are absent unless they are intentionally reused.
- Capabilities from reference projects, external platforms, partners, outsourced work, cited papers, or third-party services are not claimed as current or proposed project work.
- Codebase, product, dataset, experiment, field work, or service-specific claims, when present, match the relevant source.
- Dependency claims do not add tools, libraries, datasets, devices, partners, organizations, or services the project does not actually use.
- Figures, tables, screenshots, formulas, and metrics match the current or proposed project instead of imagined or leftover content.
- Dates, version numbers, model names, standards, policies, and call requirements are current or clearly scoped as examples.
- Claims are concrete enough to be credible and not inflated beyond source material.
- Drafted expansions distinguish established facts from plans, reasonable inferences, assumptions, and items needing confirmation.
- Required template structure, form fields, numbering, tables, and word limits are preserved unless the requirement or user allows changes.
- The old document structure is reused only where it helps the current material; mismatched sections are rewritten or removed.

## Final-Facing Content Checks

- The document reads as the deliverable it claims to be, not as a task plan, drafting note, review log, file-generation note, or internal audit trail.
- Source constraints such as rubrics, templates, scoring criteria, formatting rules, and review checklists shape the document but are not restated as body content unless the target format explicitly requires a visible response.
- Authoring or delivery process details are omitted from final-facing prose by default: drafting workflow, edit steps, internal acceptance checks, generated formats, file synchronization, submission coordination, log paths, checkpoints, unresolved author questions, TODOs, placeholders, and draft status.
- Workflow, checklist, acceptance, compliance, or procedure language is included only when the target document itself is a plan, procedure, manual, response matrix, acceptance document, audit artifact, or similar reader-facing process deliverable.
- Useful process facts are converted into reader-relevant substance. For example, an internal reproducibility concern becomes a concise limitation or method boundary, not a note about logs, paths, or how the document was checked.
- Each paragraph serves the target reader's decision, understanding, compliance need, or operating task.

## Verification Prompts

Useful search terms usually include the project-specific stale terms plus high-signal process-leak phrases. Do not treat generic words such as review, template, log, or path as deletion triggers without context.

```text
old project name
obsolete objective/task/method names
invented deliverables or indicators
old organization/partner/platform names
invented experiments, datasets, pages, or APIs
external responsibilities claimed as current or proposed project work
TODO / placeholder / 原项目 / 转换层 / 待补充
draft status / pending confirmation / authoring workflow / internal review checklist / scoring rubric / template instruction
file-generation note / generated file / format conversion note / submission coordination / format synchronization / log path / checkpoint / audit trail
```

For Markdown:

```bash
rg -n "TERM1|TERM2|TODO|原项目|转换层|待补充|待确认|草稿|占位|draft status|pending confirmation|file-generation|generated file|submission coordination|format synchronization|checkpoint|audit trail" docs README.md
```
