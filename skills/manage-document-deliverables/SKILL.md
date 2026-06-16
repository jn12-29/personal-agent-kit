---
name: manage-document-deliverables
description: Use when document source files and exported deliverables must be inspected, converted, regenerated, or preserved. Owns DOCX, Markdown, PDF, and similar source-vs-derived file roles, inventory, conversion, snapshots, and regeneration decisions.
---

# Manage Document Deliverables

## Why This Exists

Document files are easy to mishandle: agents overwrite the only authoritative copy, edit generated binaries instead of source text, lose structure during conversion, or leave stale exports in place without saying so. This skill keeps file-role decisions explicit and reproducible.

## Boundary

Own document file operations, conversion, inventory, extraction, regeneration, and artifact handling.

Does not own final-facing prose quality, project truth, or document content editing.

## Workflow

1. Classify the file role: editable source, generated deliverable, authoritative binary source, evidence-only record, or submitted artifact.
2. Inventory the document before risky operations.
3. Choose the safest action: extract, convert, regenerate, snapshot, preserve, or ignore.
4. Use the bundled scripts when they are the right tool.
5. Verify the output structure and state whether deliverables are current, stale, or intentionally untouched.

## File-Role Rules

- Prefer editable text sources when they generate final deliverables.
- Treat DOCX, PPTX, XLSX, PDF, and similar exports as derived deliverables unless the file is the only authoritative source.
- Preserve timestamped snapshots when a binary file is authoritative.
- Keep a short manifest or change note when a binary source must be preserved.
- Prefer relative project paths in documented commands.

## Included Scripts

- `scripts/docx_inventory.py`: inspect headings, captions, media files, and term hits.
- `scripts/docx_to_md.py`: convert DOCX to reviewable Markdown.
- `scripts/md_to_docx.py`: convert Markdown to DOCX from project sources.

## Resources

- `references/document-deliverable-checklist.md`: detailed checks for source/export decisions, DOCX handling, snapshots, and verification terms.

## Verification

- Confirm file role and output path.
- Compare heading, table, figure, and caption structure when relevant.
- Re-run inventory after conversion or regeneration when practical.
- Report whether an exported file was regenerated, preserved, or intentionally left stale.
