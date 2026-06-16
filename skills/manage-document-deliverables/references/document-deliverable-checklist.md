# Document Deliverable Checklist

Use this checklist when a task involves document source files, generated exports, Office files, conversion, regeneration, snapshots, or repository tracking decisions.

## Source And Export Checks

- Prefer Markdown, LaTeX, Quarto, source templates, scripts, structured data, or other editable text sources when they generate final DOCX, PPTX, XLSX, PDF, or similar deliverables.
- When Markdown or another text source generates exported deliverables, keep the export command, required tool, template or reference file, and project-relative output path in project-facing documentation or a generation script.
- Prefer commands run from the project root with relative paths for in-project inputs, templates, scripts, and outputs.
- Avoid user- or machine-specific absolute paths unless an external artifact is required.
- Keep export commands and file-generation notes out of final-facing prose unless the target document is itself a procedure, delivery guide, or maintenance note.
- Treat generated DOCX, PPTX, XLSX, PDF, and similar files as derived deliverables by default.
- Do not recommend normal Git tracking for derived binary deliverables unless project policy requires it, because semantic diffs and merges are not useful.
- When a DOCX, PPTX, or XLSX file is the only authoritative source, preserve timestamped snapshots and keep a text manifest or change note with timestamp, source, purpose, and human-readable change summary.
- Preserve signed, submitted, scanned, or official evidence files as records.
- If repository tracking is required for authoritative binary files, prefer Git LFS or a dedicated snapshots/artifacts directory.
- When both a source file and exported deliverable exist, report whether the export was regenerated, intentionally left stale, or intentionally ignored by repository policy.

## DOCX Checks

- Extract text before editing and after editing; do not rely only on visual inspection.
- Count figures, captions, and media files before replacing images.
- Keep image relationships valid; avoid deleting media blindly.
- Verify section numbering and caption numbering after image insertion.
- Search for stale terms in extracted text and captions.
- Open or convert the final document when practical to catch broken layout, missing images, caption drift, or template damage.
- For substantial rewrites, preserve extracted text, outlines, draft fragments, or other diffable intermediate artifacts so follow-up edits can be patched instead of regenerated.
- Keep intermediate artifacts separate from the final deliverable.

## Verification Terms

```text
authoritative source / derived deliverable / export command / regeneration path
timestamped snapshot / absolute path / project-relative path
generated file / format conversion note / submission coordination
format synchronization / log path / checkpoint / audit trail
```

For DOCX:

```bash
python skills/manage-document-deliverables/scripts/docx_inventory.py docs/document.docx --terms TERM1 TERM2 转换层
```
