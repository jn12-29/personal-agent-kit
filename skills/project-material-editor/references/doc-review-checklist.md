# Project Material Review Checklist

Use this checklist when a project proposal, grant application, university-industry collaboration material, project task statement, technical plan, midterm/final report, acceptance material, manual, or other project document needs more than a small wording fix.

## Scope Anchors

- Identify user-confirmed sections that must not be rewritten.
- Identify section or figure ranges that are explicitly in scope.
- Identify sections excluded by the user, even if they look stale.
- Identify the target use: application, contract, planning, review, technical design, execution, report, acceptance, delivery, communication, or presentation material.
- Identify source materials that can be reused for structure versus materials that are only references.
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

## DOCX-Specific Checks

- Extract text before editing and after editing; do not rely only on visual inspection.
- Count figures, captions, and media files before replacing images.
- Keep image relationships valid; avoid deleting media blindly.
- Verify section numbering and caption numbering after image insertion.
- Search for stale terms in extracted text and captions.
- Open or convert the final document when practical to catch broken layout, missing images, caption drift, or template damage.
- For substantial rewrites, preserve extracted text, outlines, draft fragments, or other diffable intermediate artifacts so follow-up edits can be patched instead of regenerated. Keep intermediate artifacts separate from the final deliverable.

## Verification Prompts

Useful search terms usually include:

```text
old project name
obsolete objective/task/method names
invented deliverables or indicators
old organization/partner/platform names
invented experiments, datasets, pages, or APIs
external responsibilities claimed as current or proposed project work
TODO / placeholder / 原项目 / 转换层 / 待补充
```

For Markdown:

```bash
rg -n "TERM1|TERM2|TODO|原项目|转换层" docs README.md
```

For DOCX:

```bash
python path/to/project-material-editor/scripts/docx_inventory.py document.docx --terms TERM1 TERM2 转换层
```
