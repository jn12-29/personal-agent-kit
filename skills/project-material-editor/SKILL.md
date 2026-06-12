---
name: project-material-editor
description: Adapt, revise, and review project materials such as proposals, grant applications, university-industry collaboration materials, project task statements, technical plans, reports, acceptance materials, manuals, and DOCX/Markdown documents. Use when rewriting from prior materials, preserving useful structure, respecting fixed templates, aligning content with the current or proposed project, removing stale claims, or checking tables, figures, and captions.
---

# Project Material Editor

## Why This Exists

Project material edits fail when agents lightly rewrite an old document and leave stale project names, objectives, metrics, partners, responsibilities, figures, or compliance-sensitive claims. The result can look polished while being false for the current project. This skill forces the agent to verify the current authority, preserve binding template structure, and remove unsupported carryover instead of treating prior material as truth.

## Overview

Use this skill to turn project materials into a coherent document for the current application, contract, report, planning, delivery, review, or communication purpose, not a lightly edited copy from another project. Treat user instructions, known facts and planning intent about the current or proposed project, target requirements, provided source materials, and user-confirmed sections as the authority, then make the smallest documentation change that makes the material true and fit for purpose.

## Boundary

This skill does not provide final legal, policy, budget, or external compliance approval. It does not invent missing partners, datasets, experiments, metrics, approvals, or delivered capabilities. It does not own complete visual redesign or figure generation, and it does not reopen user-confirmed sections unless the latest instruction does so.

## Workflow

1. Establish the scope and authorities.
   - Read the user's latest instructions first, especially document type, target use, audience, required structure, confirmed sections, and explicit exclusions.
   - Read the provided source materials before judging the document: prior applications, original project documents, call guidelines, contract requirements, templates, review criteria, meeting notes, data sheets, reference papers, product/project docs, and any reference text the user names.
   - Record user-confirmed immutable sections, target sections, and explicit exclusions before editing. Do not reopen confirmed sections unless the user explicitly does so.
   - Treat required templates as binding structure: preserve fixed fields, table layout, section order, numbering, and word limits unless the user or source requirement permits changes. Leave required fields in place even when content is pending.
   - If the document was adapted from another project, assume stale names, objectives, background, methods, tasks, indicators, organizations, budgets, timelines, tables, and diagrams may remain until verified.

2. Inventory the document.
   - For Markdown, inspect headings, links, image references, tables, and repeated terms with `rg`.
   - For DOCX, use `scripts/docx_inventory.py` to list headings, captions, media files, and stale term hits without relying on visual memory.
   - Build a short map: confirmed content, reusable structure, likely stale content, unsupported claims, missing content, and tables/figures/captions that must stay aligned.

3. Check reasonableness against the project.
   - Verify project identity, background, problem definition, objectives, research or engineering content, technical route, work packages, deliverables, evaluation indicators, schedule, budget-, compliance-, or responsibility-sensitive claims, responsible parties, risks, application scenarios, and figure/table captions against the current or proposed project materials.
   - For application materials, check fit with the call, sponsor, review criteria, discipline/domain expectations, and required format.
   - For execution or delivery materials, check consistency among objectives, tasks, milestones, deliverables, acceptance criteria, resources, and responsibilities.
   - When the material is tied to a codebase, product, dataset, experiment, field work, or external service, verify those concrete claims against the relevant source.
   - Remove or rewrite concepts that the current or proposed project does not include. Do not leave unrelated content as historical notes unless the user explicitly asks for history.
   - Use reasonable drafting judgment where materials are incomplete, but label or surface assumptions instead of presenting unsupported functions, experiments, datasets, partners, achievements, metrics, deliverables, algorithms, implementation scope, or application effects as established facts.
   - Keep responsibility boundaries clear: do not write external platform, partner, outsourced work, cited paper, reference project, or third-party service capability as if it belongs to the current or proposed project.
   - When a figure title is reusable but the figure is wrong, keep or revise the caption only after the content is made true.

4. Edit for the final desired state.
   - Keep changes surgical and consistent with the existing document tone.
   - Preserve confirmed sections as-is unless the user reopens them; only fix obvious mechanical issues when that is clearly safe.
   - Prefer direct, concrete descriptions over vague platform language, empty policy language, generic academic or administrative phrasing, boilerplate filler, or inflated claims.
   - Reuse old structure only when it helps the current document; do not let the old structure force mismatched content.
   - For substantial rewrites, keep reusable outlines, extracted text, notes, or diffable drafts so follow-up edits can patch the work instead of regenerating similar content. Keep intermediate artifacts separate from the final deliverable.
   - Do not delete all figure placeholders just because replacement art is not ready; keep useful captions/placeholders when the user plans to add figures.

5. Verify after editing.
   - Search for obsolete project names, objectives, methods, tasks, indicators, partners, organizations, stale table/figure titles, and terms named by the user.
   - Re-run the DOCX inventory or Markdown searches and compare figure/caption counts.
   - If claims depend on a product, dataset, experiment, policy, call guideline, contract clause, external requirement, or running service, verify the source when practical instead of guessing.
   - Report what was checked, what was not verified, and remaining uncertainty as open questions, not as polished facts.

## Resources

- `scripts/docx_inventory.py`: inspect `.docx` text, heading candidates, captions, media files, and term occurrences.
- `references/doc-review-checklist.md`: detailed review checklist for adapting and validating project materials.

Read the reference when the task involves a full material review, a DOCX, a proposal/application/report, or a document adapted from another project.
