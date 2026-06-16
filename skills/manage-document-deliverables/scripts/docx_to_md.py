#!/usr/bin/env python3
"""Convert DOCX files to clean, reviewable Markdown.

The converter reads the DOCX package directly, so it does not require Word,
LibreOffice, or python-docx. It focuses on common project/report material:
headings, paragraphs, lists, tables, hyperlinks, basic inline emphasis, and
embedded images.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}

DOCUMENT_PART = "word/document.xml"
DOCUMENT_RELS_PART = "word/_rels/document.xml.rels"
STYLES_PART = "word/styles.xml"
NUMBERING_PART = "word/numbering.xml"
REL_HYPERLINK = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
REL_IMAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """Keep examples readable while showing defaults."""


@dataclass(frozen=True)
class Relationship:
    rel_type: str
    target: str
    target_mode: str = ""


@dataclass(frozen=True)
class MarkdownBlock:
    kind: str
    text: str


@dataclass
class ConversionContext:
    source: Path
    archive: zipfile.ZipFile
    output: Path
    media_dir: Path | None
    extract_media: bool
    relationships: dict[str, Relationship]
    styles: dict[str, str]
    numbering: dict[tuple[str, str], str]
    num_to_abstract: dict[str, str]
    media_paths: dict[str, str]
    heading_offset: int = 0
    inline_styles: bool = True


def w_attr(name: str) -> str:
    return f"{{{NS['w']}}}{name}"


def r_attr(name: str) -> str:
    return f"{{{NS['r']}}}{name}"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_xml(archive: zipfile.ZipFile, part: str) -> ET.Element | None:
    try:
        return ET.fromstring(archive.read(part))
    except KeyError:
        return None


def parse_relationships(archive: zipfile.ZipFile, rels_part: str) -> dict[str, Relationship]:
    root = read_xml(archive, rels_part)
    if root is None:
        return {}
    relationships: dict[str, Relationship] = {}
    for rel in root.findall("rel:Relationship", NS):
        rel_id = rel.attrib.get("Id", "")
        if not rel_id:
            continue
        relationships[rel_id] = Relationship(
            rel_type=rel.attrib.get("Type", ""),
            target=rel.attrib.get("Target", ""),
            target_mode=rel.attrib.get("TargetMode", ""),
        )
    return relationships


def parse_styles(archive: zipfile.ZipFile) -> dict[str, str]:
    root = read_xml(archive, STYLES_PART)
    if root is None:
        return {}
    styles: dict[str, str] = {}
    for style in root.findall("w:style", NS):
        if style.attrib.get(w_attr("type")) != "paragraph":
            continue
        style_id = style.attrib.get(w_attr("styleId"), "")
        name_node = style.find("w:name", NS)
        if style_id and name_node is not None:
            styles[style_id] = name_node.attrib.get(w_attr("val"), "")
    return styles


def parse_numbering(archive: zipfile.ZipFile) -> tuple[dict[tuple[str, str], str], dict[str, str]]:
    root = read_xml(archive, NUMBERING_PART)
    if root is None:
        return {}, {}

    formats: dict[tuple[str, str], str] = {}
    for abstract in root.findall("w:abstractNum", NS):
        abstract_id = abstract.attrib.get(w_attr("abstractNumId"), "")
        for level in abstract.findall("w:lvl", NS):
            ilvl = level.attrib.get(w_attr("ilvl"), "0")
            fmt = level.find("w:numFmt", NS)
            formats[(abstract_id, ilvl)] = fmt.attrib.get(w_attr("val"), "bullet") if fmt is not None else "bullet"

    num_to_abstract: dict[str, str] = {}
    for num in root.findall("w:num", NS):
        num_id = num.attrib.get(w_attr("numId"), "")
        abstract = num.find("w:abstractNumId", NS)
        if num_id and abstract is not None:
            num_to_abstract[num_id] = abstract.attrib.get(w_attr("val"), "")
    return formats, num_to_abstract


def style_name(ctx: ConversionContext, style_id: str) -> str:
    return ctx.styles.get(style_id, style_id)


def paragraph_style_id(paragraph: ET.Element) -> str:
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    return style.attrib.get(w_attr("val"), "") if style is not None else ""


def heading_level(ctx: ConversionContext, paragraph: ET.Element) -> int | None:
    style_id = paragraph_style_id(paragraph)
    name = style_name(ctx, style_id).lower().replace("_", " ")
    candidates = [style_id.lower(), name]
    for candidate in candidates:
        match = re.search(r"heading\s*([1-6])", candidate)
        if match:
            return clamp_heading(int(match.group(1)) + ctx.heading_offset)
    if name in {"title", "document title"} or style_id.lower() == "title":
        return clamp_heading(1 + ctx.heading_offset)
    return None


def clamp_heading(level: int) -> int:
    return max(1, min(6, level))


def numbering_marker(ctx: ConversionContext, paragraph: ET.Element) -> tuple[str, str] | None:
    num_pr = paragraph.find("./w:pPr/w:numPr", NS)
    if num_pr is not None:
        ilvl_node = num_pr.find("w:ilvl", NS)
        num_id_node = num_pr.find("w:numId", NS)
        ilvl = ilvl_node.attrib.get(w_attr("val"), "0") if ilvl_node is not None else "0"
        num_id = num_id_node.attrib.get(w_attr("val"), "") if num_id_node is not None else ""
        abstract_id = ctx.num_to_abstract.get(num_id, "")
        fmt = ctx.numbering.get((abstract_id, ilvl), "bullet")
        indent = "  " * safe_int(ilvl)
        return indent, "1." if fmt != "bullet" else "-"

    name = style_name(ctx, paragraph_style_id(paragraph)).lower()
    if "list bullet" in name:
        return "", "-"
    if "list number" in name:
        return "", "1."
    return None


def safe_int(value: str) -> int:
    try:
        return max(0, int(value))
    except ValueError:
        return 0


def resolve_part_target(base_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    base_dir = posixpath.dirname(base_part)
    return posixpath.normpath(posixpath.join(base_dir, target))


def markdown_media_path(ctx: ConversionContext, rid: str) -> str:
    if rid in ctx.media_paths:
        return ctx.media_paths[rid]

    rel = ctx.relationships.get(rid)
    if rel is None:
        ctx.media_paths[rid] = f"missing-{rid}"
        return ctx.media_paths[rid]
    if rel.target_mode.lower() == "external":
        ctx.media_paths[rid] = rel.target
        return rel.target

    package_path = resolve_part_target(DOCUMENT_PART, rel.target)
    filename = Path(package_path).name or f"{rid}.bin"
    if not ctx.extract_media or ctx.media_dir is None:
        ctx.media_paths[rid] = package_path
        return package_path

    ctx.media_dir.mkdir(parents=True, exist_ok=True)
    try:
        payload = ctx.archive.read(package_path)
    except KeyError:
        ctx.media_paths[rid] = f"missing-{filename}"
        return ctx.media_paths[rid]

    destination = reusable_media_path(ctx.media_dir / filename, payload)
    destination.write_bytes(payload)
    rel_path = os.path.relpath(destination, ctx.output.parent).replace(os.sep, "/")
    ctx.media_paths[rid] = rel_path
    return rel_path


def reusable_media_path(path: Path, payload: bytes) -> Path:
    if not path.exists():
        return path
    if path.read_bytes() == payload:
        return path
    return unique_path(path)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 10000):
        candidate = path.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Unable to choose a unique filename near {path}")


def render_paragraph(ctx: ConversionContext, paragraph: ET.Element) -> MarkdownBlock | None:
    text = render_inline_children(ctx, paragraph).strip()
    if not text:
        return None

    level = heading_level(ctx, paragraph)
    if level is not None:
        return MarkdownBlock("heading", f"{'#' * level} {text}")

    marker = numbering_marker(ctx, paragraph)
    if marker is not None:
        indent, bullet = marker
        return MarkdownBlock("list", f"{indent}{bullet} {text}")

    return MarkdownBlock("paragraph", text)


def render_inline_children(ctx: ConversionContext, parent: ET.Element) -> str:
    pieces: list[str] = []
    for child in list(parent):
        name = local_name(child.tag)
        if name == "pPr":
            continue
        if name == "r":
            pieces.append(render_run(ctx, child))
        elif name == "hyperlink":
            pieces.append(render_hyperlink(ctx, child))
        else:
            nested = render_inline_children(ctx, child)
            if nested:
                pieces.append(nested)
    return "".join(pieces)


def render_hyperlink(ctx: ConversionContext, hyperlink: ET.Element) -> str:
    text = render_inline_children(ctx, hyperlink)
    if not text:
        return ""
    rid = hyperlink.attrib.get(r_attr("id"), "")
    anchor = hyperlink.attrib.get(w_attr("anchor"), "")
    rel = ctx.relationships.get(rid)
    if rel and rel.rel_type == REL_HYPERLINK:
        return f"[{escape_link_text(text)}]({rel.target})"
    if anchor:
        return f"[{escape_link_text(text)}](#{anchor})"
    return text


def render_run(ctx: ConversionContext, run: ET.Element) -> str:
    text_parts: list[str] = []
    pieces: list[str] = []

    def flush_text() -> None:
        if text_parts:
            pieces.append(format_run_text(ctx, run, "".join(text_parts)))
            text_parts.clear()

    for child in list(run):
        name = local_name(child.tag)
        if name == "t":
            text_parts.append(child.text or "")
        elif name == "tab":
            text_parts.append(" ")
        elif name in {"br", "cr"}:
            text_parts.append("  \n")
        elif name in {"drawing", "pict"}:
            flush_text()
            pieces.extend(render_images(ctx, child))
    flush_text()
    return "".join(pieces)


def format_run_text(ctx: ConversionContext, run: ET.Element, text: str) -> str:
    if not ctx.inline_styles or not text or text.isspace():
        return text
    run_props = run.find("w:rPr", NS)
    if run_props is None:
        return text
    leading = re.match(r"^\s*", text).group(0)
    trailing = re.search(r"\s*$", text).group(0)
    core = text[len(leading) : len(text) - len(trailing) if trailing else len(text)]
    if not core:
        return text
    if has_on_property(run_props, "b") and has_on_property(run_props, "i"):
        return f"{leading}***{core}***{trailing}"
    if has_on_property(run_props, "b"):
        return f"{leading}**{core}**{trailing}"
    if has_on_property(run_props, "i"):
        return f"{leading}*{core}*{trailing}"
    return text


def has_on_property(run_props: ET.Element, property_name: str) -> bool:
    prop = run_props.find(f"w:{property_name}", NS)
    if prop is None:
        return False
    value = prop.attrib.get(w_attr("val"), "true")
    return value.lower() not in {"0", "false", "off"}


def render_images(ctx: ConversionContext, element: ET.Element) -> list[str]:
    images: list[str] = []
    for blip in element.findall(".//a:blip", NS):
        rid = blip.attrib.get(r_attr("embed")) or blip.attrib.get(r_attr("link"))
        if not rid:
            continue
        images.append(f"![{image_alt_text(element)}]({markdown_media_path(ctx, rid)})")
    for image_data in element.findall(".//v:imagedata", NS):
        rid = image_data.attrib.get(r_attr("id"))
        if not rid:
            continue
        alt = image_data.attrib.get("title", "") or image_alt_text(element)
        images.append(f"![{escape_alt_text(alt)}]({markdown_media_path(ctx, rid)})")
    return images


def image_alt_text(element: ET.Element) -> str:
    doc_pr = element.find(".//wp:docPr", NS)
    if doc_pr is None:
        return ""
    return escape_alt_text(
        doc_pr.attrib.get("descr", "")
        or doc_pr.attrib.get("title", "")
        or doc_pr.attrib.get("name", "")
    )


def escape_alt_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("]", "\\]")


def escape_link_text(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def render_table(ctx: ConversionContext, table: ET.Element) -> MarkdownBlock | None:
    rows: list[list[str]] = []
    for row in table.findall("w:tr", NS):
        cells: list[str] = []
        for cell in row.findall("w:tc", NS):
            cells.append(render_cell(ctx, cell))
        if cells:
            rows.append(cells)
    if not rows:
        return None

    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    lines = [pipe_row(normalized[0]), pipe_row(["---"] * width)]
    lines.extend(pipe_row(row) for row in normalized[1:])
    return MarkdownBlock("table", "\n".join(lines))


def render_cell(ctx: ConversionContext, cell: ET.Element) -> str:
    parts: list[str] = []
    for paragraph in cell.findall("w:p", NS):
        rendered = render_inline_children(ctx, paragraph).strip()
        if rendered:
            parts.append(rendered)
    return "<br>".join(parts)


def pipe_row(values: list[str]) -> str:
    return "| " + " | ".join(escape_table_cell(value) for value in values) + " |"


def escape_table_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def render_document(ctx: ConversionContext) -> list[MarkdownBlock]:
    root = read_xml(ctx.archive, DOCUMENT_PART)
    if root is None:
        raise SystemExit(f"{ctx.source} does not look like a DOCX: missing {DOCUMENT_PART}")
    body = root.find("w:body", NS)
    if body is None:
        return []

    blocks: list[MarkdownBlock] = []
    for child in list(body):
        name = local_name(child.tag)
        if name == "p":
            block = render_paragraph(ctx, child)
            if block is not None:
                blocks.append(block)
        elif name == "tbl":
            block = render_table(ctx, child)
            if block is not None:
                blocks.append(block)
    return blocks


def emit_markdown(blocks: list[MarkdownBlock]) -> str:
    output: list[str] = []
    previous_kind = ""
    for block in blocks:
        if not block.text.strip():
            continue
        if output and not (block.kind == "list" and previous_kind == "list"):
            output.append("")
        output.extend(block.text.rstrip().splitlines())
        previous_kind = block.kind
    return "\n".join(output).rstrip() + "\n"


def convert_docx(
    docx: Path,
    output: Path,
    media_dir: Path | None,
    extract_media: bool,
    heading_offset: int,
    inline_styles: bool,
) -> int:
    with zipfile.ZipFile(docx) as archive:
        numbering, num_to_abstract = parse_numbering(archive)
        ctx = ConversionContext(
            source=docx,
            archive=archive,
            output=output,
            media_dir=media_dir,
            extract_media=extract_media,
            relationships=parse_relationships(archive, DOCUMENT_RELS_PART),
            styles=parse_styles(archive),
            numbering=numbering,
            num_to_abstract=num_to_abstract,
            media_paths={},
            heading_offset=heading_offset,
            inline_styles=inline_styles,
        )
        markdown = emit_markdown(render_document(ctx))
    output.write_text(markdown, encoding="utf-8")
    return 0


def default_output(docx: Path) -> Path:
    candidate = docx.with_suffix(".md")
    if not candidate.exists():
        return candidate
    return docx.with_name(f"{docx.stem}.from-docx.md")


def build_parser() -> argparse.ArgumentParser:
    epilog = """\
Examples:
  Convert a DOCX to Markdown without overwriting an existing .md:
    python skills/manage-document-deliverables/scripts/docx_to_md.py docs/report.docx

  Choose output and media locations explicitly:
    python skills/manage-document-deliverables/scripts/docx_to_md.py docs/report.docx -o review/report.md --media-dir review/report_media

  Replace an existing Markdown output intentionally:
    python skills/manage-document-deliverables/scripts/docx_to_md.py docs/report.docx -o docs/report.md --overwrite

  Extract text only:
    python skills/manage-document-deliverables/scripts/docx_to_md.py docs/report.docx --no-media --plain-inline

Defaults and behavior:
  - Run from the project root with project-relative paths when possible.
  - Default output is <docx stem>.md when that file is free; otherwise it is
    <docx stem>.from-docx.md.
  - Existing Markdown output is not overwritten unless --overwrite is passed.
  - Media is extracted by default to <output stem>_media and linked relative to the output file.
  - This script reads the DOCX package directly and does not require Word, LibreOffice, Pandoc,
    or python-docx.
  - Exit codes: 0 success, 2 invalid input, unsafe overwrite, or unreadable DOCX.
"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=epilog,
        formatter_class=HelpFormatter,
    )
    parser.add_argument("docx", type=Path, help="DOCX source file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Markdown output path. Default avoids overwriting an existing same-stem .md.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting an existing Markdown output file.")
    parser.add_argument(
        "--media-dir",
        type=Path,
        help="Directory for extracted media. Defaults to '<output stem>_media'.",
    )
    parser.add_argument("--no-media", action="store_true", help="Do not extract embedded media files.")
    parser.add_argument(
        "--heading-offset",
        type=int,
        default=0,
        help="Shift detected heading levels by this amount, clamped to 1-6.",
    )
    parser.add_argument(
        "--plain-inline",
        action="store_true",
        help="Do not emit Markdown bold/italic markers from DOCX run formatting.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    docx = args.docx.resolve()
    if not docx.exists():
        print(f"File not found: {docx}", file=sys.stderr)
        return 2
    output = (args.output or default_output(docx)).resolve()
    if output.exists() and not args.overwrite:
        print(f"Output already exists, use --overwrite to replace it: {output}", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    media_dir = None if args.no_media else (args.media_dir or output.with_name(f"{output.stem}_media")).resolve()

    try:
        return convert_docx(
            docx=docx,
            output=output,
            media_dir=media_dir,
            extract_media=not args.no_media,
            heading_offset=args.heading_offset,
            inline_styles=not args.plain_inline,
        )
    except (zipfile.BadZipFile, ET.ParseError, RuntimeError, SystemExit) as exc:
        print(f"Could not convert DOCX: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
