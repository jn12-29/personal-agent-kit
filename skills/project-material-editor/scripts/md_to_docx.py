#!/usr/bin/env python3
"""Convert Markdown to DOCX for project/report materials.

The default path uses python-docx so common report styles are controlled inside
the generated DOCX. Pandoc is available as an opt-in path when a reference DOCX
or full Markdown coverage is more important than the built-in report styles.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
CAPTION_NUMBER = r"\d+(?:[-.．]\d+)*"
FIGURE_CAPTION_RE = re.compile(rf"^(图|Figure|Fig\.?)\s*{CAPTION_NUMBER}([.\s、:：]|$)", re.IGNORECASE)
TABLE_CAPTION_RE = re.compile(rf"^(表|Table)\s*{CAPTION_NUMBER}([.\s、:：]|$)", re.IGNORECASE)
DEFAULT_EAST_ASIA_FONT = "仿宋"
DEFAULT_LATIN_FONT = "Times New Roman"
HEADING_EAST_ASIA_FONT = "黑体"
MAX_IMAGE_WIDTH_INCHES = 5.8
MAX_IMAGE_HEIGHT_INCHES = 4.5


@dataclass(frozen=True)
class Block:
    kind: str
    text: str = ""
    level: int = 0
    target: str = ""
    rows: tuple[tuple[str, ...], ...] = ()


def run_pandoc(markdown: Path, output: Path, reference_doc: Path | None) -> int:
    command = ["pandoc", str(markdown), "-o", str(output), "--resource-path", str(markdown.parent)]
    if reference_doc:
        command.extend(["--reference-doc", str(reference_doc)])
    subprocess.run(command, check=True)
    return 0


def ensure_python_docx() -> None:
    try:
        import docx  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            "python-docx is required for fallback conversion. "
            "Use a temporary run such as: uv run --with python-docx python md_to_docx.py input.md"
        ) from exc


def split_table_row(line: str) -> tuple[str, ...]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return tuple(cell.strip() for cell in stripped.split("|"))


def normalize_table_row(values: tuple[str, ...], width: int) -> tuple[str, ...]:
    if len(values) < width:
        return values + ("",) * (width - len(values))
    if len(values) > width:
        return values[: width - 1] + (" | ".join(values[width - 1 :]),)
    return values


def warn_uneven_table_row(row_index: int, actual: int, expected: int) -> None:
    if actual != expected:
        print(
            f"Warning: table row {row_index} has {actual} cell(s); expected {expected}.",
            file=sys.stderr,
        )


def flush_paragraph(blocks: list[Block], lines: list[str]) -> None:
    if not lines:
        return
    text = " ".join(line.strip() for line in lines if line.strip())
    if text:
        blocks.append(Block("paragraph", text=text))
    lines.clear()


def parse_blocks(markdown: Path) -> list[Block]:
    lines = markdown.read_text(encoding="utf-8").splitlines()
    blocks: list[Block] = []
    paragraph_lines: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            flush_paragraph(blocks, paragraph_lines)
            index += 1
            continue

        heading = HEADING_RE.match(stripped)
        if heading:
            flush_paragraph(blocks, paragraph_lines)
            blocks.append(Block("heading", text=heading.group(2).strip(), level=min(len(heading.group(1)), 6)))
            index += 1
            continue

        image = IMAGE_RE.fullmatch(stripped)
        if image:
            flush_paragraph(blocks, paragraph_lines)
            blocks.append(Block("image", text=image.group(1).strip(), target=image.group(2).strip()))
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and TABLE_SEPARATOR_RE.match(lines[index + 1]):
            flush_paragraph(blocks, paragraph_lines)
            rows = [split_table_row(stripped)]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(split_table_row(lines[index]))
                index += 1
            blocks.append(Block("table", rows=tuple(rows)))
            continue

        list_item = LIST_RE.match(line)
        if list_item:
            flush_paragraph(blocks, paragraph_lines)
            marker = list_item.group(2)
            style = "ordered_list" if marker[0].isdigit() else "unordered_list"
            blocks.append(Block(style, text=list_item.group(3).strip()))
            index += 1
            continue

        paragraph_lines.append(stripped)
        index += 1

    flush_paragraph(blocks, paragraph_lines)
    return classify_caption_blocks(blocks)


def classify_caption_blocks(blocks: list[Block]) -> list[Block]:
    result: list[Block] = []
    for index, block in enumerate(blocks):
        if block.kind == "paragraph":
            if FIGURE_CAPTION_RE.match(block.text):
                result.append(Block("figure_caption", text=block.text))
                continue
            if TABLE_CAPTION_RE.match(block.text):
                result.append(Block("table_caption", text=block.text))
                continue
            if index + 1 < len(blocks) and blocks[index + 1].kind == "table":
                prefix, caption = split_trailing_table_caption(block.text)
                if caption:
                    if prefix:
                        result.append(Block("paragraph", text=prefix))
                    result.append(Block("table_caption", text=caption))
                    continue
        result.append(block)
    return result


def split_trailing_table_caption(text: str) -> tuple[str, str]:
    if TABLE_CAPTION_RE.match(text):
        return "", text

    markers = [
        match.start()
        for match in re.finditer(rf"(?:表|Table)\s*{CAPTION_NUMBER}([.\s、:：]|$)", text, re.IGNORECASE)
    ]
    for start in reversed(markers):
        prefix = text[:start].rstrip()
        caption = text[start:].strip()
        if not prefix:
            return "", caption
        if prefix[-1] in "。.!?！？；;":
            return prefix, caption
    return text, ""


def set_cell_text(cell: object, text: str) -> None:
    cell.text = text
    for paragraph in cell.paragraphs:
        paragraph.style = "Table Body"


def add_caption(document: object, text: str, caption_kind: str) -> None:
    style_name = "Table Caption" if caption_kind == "table" else "Figure Caption"
    document.add_paragraph(text, style=style_name)


def add_picture(document: object, markdown: Path, target: str) -> bool:
    image_path = Path(target)
    if not image_path.is_absolute():
        image_path = markdown.parent / image_path
    if not image_path.exists():
        document.add_paragraph(f"[Missing image: {target}]", style="Missing Image")
        return False
    paragraph = document.add_paragraph(style="Figure Image")
    run = paragraph.add_run()
    width, height = scaled_image_size(image_path)
    run.add_picture(str(image_path), width=width, height=height)
    return True


def add_table(document: object, rows: tuple[tuple[str, ...], ...]) -> None:
    if not rows:
        return
    width = max(len(row) for row in rows)
    normalized = [normalize_table_row(row, width) for row in rows]
    table = document.add_table(rows=1, cols=width)
    table.style = "Report Table"

    for cell, text in zip(table.rows[0].cells, normalized[0]):
        set_cell_text(cell, text)
        for paragraph in cell.paragraphs:
            paragraph.style = "Table Header"

    for row_index, row_values in enumerate(rows, start=1):
        warn_uneven_table_row(row_index, len(row_values), width)

    for row_values in normalized[1:]:
        row = table.add_row()
        for cell, text in zip(row.cells, row_values):
            set_cell_text(cell, text)

    document.add_paragraph(style="Table Spacer")


def setup_document_styles(document: object) -> None:
    from docx.enum.style import WD_STYLE_TYPE
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.section import WD_SECTION_START
    from docx.shared import Cm, Pt

    section = document.sections[0]
    section.start_type = WD_SECTION_START.NEW_PAGE
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    normal = document.styles["Normal"]
    set_style_fonts(normal, DEFAULT_LATIN_FONT, DEFAULT_EAST_ASIA_FONT)
    normal.font.size = Pt(11)
    normal.paragraph_format.first_line_indent = Cm(0.74)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)

    configure_heading_styles(document)
    configure_body_styles(document, WD_STYLE_TYPE, WD_ALIGN_PARAGRAPH)
    ensure_table_style(document, "Report Table", WD_STYLE_TYPE)

    ensure_paragraph_style(
        document,
        "Figure Caption",
        WD_STYLE_TYPE.PARAGRAPH,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=10,
        bold=False,
        italic=False,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=0,
        space_after=6,
        keep_together=True,
    )
    ensure_paragraph_style(
        document,
        "Table Caption",
        WD_STYLE_TYPE.PARAGRAPH,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=10,
        bold=True,
        italic=False,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=6,
        space_after=3,
        keep_together=True,
    )


def ensure_paragraph_style(
    document: object,
    name: str,
    style_type: object,
    *,
    alignment: int,
    latin_font: str,
    east_asia_font: str,
    font_size: int,
    bold: bool,
    italic: bool,
    first_line_indent: bool,
    line_spacing: float | None = None,
    space_before: float = 0,
    space_after: float = 0,
    first_line_indent_cm: float | None = None,
    left_indent_cm: float | None = None,
    keep_next: bool = False,
    keep_together: bool = False,
) -> None:
    from docx.shared import Cm, Pt

    if name in document.styles:
        style = document.styles[name]
    else:
        style = document.styles.add_style(name, style_type)
    set_style_fonts(style, latin_font, east_asia_font)
    style.font.size = Pt(font_size)
    style.font.bold = bold
    style.font.italic = italic
    style.paragraph_format.alignment = alignment
    if first_line_indent_cm is not None:
        style.paragraph_format.first_line_indent = Cm(first_line_indent_cm)
    else:
        style.paragraph_format.first_line_indent = Cm(0.74) if first_line_indent else None
    style.paragraph_format.left_indent = Cm(left_indent_cm) if left_indent_cm is not None else None
    if line_spacing is not None:
        style.paragraph_format.line_spacing = line_spacing
    style.paragraph_format.space_before = Pt(space_before)
    style.paragraph_format.space_after = Pt(space_after)
    if keep_next:
        set_style_keep_next(style)
    if keep_together:
        set_style_keep_together(style)


def configure_body_styles(document: object, style_type: object, align: object) -> None:
    ensure_paragraph_style(
        document,
        "Body Text",
        style_type.PARAGRAPH,
        alignment=align.LEFT,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=11,
        bold=False,
        italic=False,
        first_line_indent=True,
        line_spacing=1.5,
        space_before=0,
        space_after=6,
    )
    ensure_paragraph_style(
        document,
        "Figure Image",
        style_type.PARAGRAPH,
        alignment=align.CENTER,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=11,
        bold=False,
        italic=False,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=6,
        space_after=3,
        keep_next=True,
    )
    ensure_paragraph_style(
        document,
        "Missing Image",
        style_type.PARAGRAPH,
        alignment=align.CENTER,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=10,
        bold=False,
        italic=True,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=6,
        space_after=3,
        keep_next=True,
    )
    ensure_paragraph_style(
        document,
        "Table Header",
        style_type.PARAGRAPH,
        alignment=align.CENTER,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=10,
        bold=True,
        italic=False,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=0,
        space_after=0,
    )
    ensure_paragraph_style(
        document,
        "Table Body",
        style_type.PARAGRAPH,
        alignment=align.LEFT,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=10,
        bold=False,
        italic=False,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=0,
        space_after=0,
    )
    ensure_paragraph_style(
        document,
        "Table Spacer",
        style_type.PARAGRAPH,
        alignment=align.LEFT,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=1,
        bold=False,
        italic=False,
        first_line_indent=False,
        line_spacing=1.0,
        space_before=0,
        space_after=6,
    )
    ensure_paragraph_style(
        document,
        "List Bullet",
        style_type.PARAGRAPH,
        alignment=align.LEFT,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=11,
        bold=False,
        italic=False,
        first_line_indent=False,
        first_line_indent_cm=-0.37,
        left_indent_cm=0.74,
        line_spacing=1.5,
        space_before=0,
        space_after=3,
    )
    ensure_paragraph_style(
        document,
        "List Number",
        style_type.PARAGRAPH,
        alignment=align.LEFT,
        latin_font=DEFAULT_LATIN_FONT,
        east_asia_font=DEFAULT_EAST_ASIA_FONT,
        font_size=11,
        bold=False,
        italic=False,
        first_line_indent=False,
        first_line_indent_cm=-0.37,
        left_indent_cm=0.74,
        line_spacing=1.5,
        space_before=0,
        space_after=3,
    )


def ensure_table_style(document: object, name: str, style_type: object) -> None:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt

    if name in document.styles:
        style = document.styles[name]
    else:
        style = document.styles.add_style(name, style_type.TABLE)
    if "Table Grid" in document.styles:
        style.base_style = document.styles["Table Grid"]
    set_style_fonts(style, DEFAULT_LATIN_FONT, DEFAULT_EAST_ASIA_FONT)
    style.font.size = Pt(10)

    existing = style.element.find(qn("w:tblPr"))
    if existing is not None:
        style.element.remove(existing)
    tbl_pr = OxmlElement("w:tblPr")
    tbl_pr.append(make_style_value_element("w:jc", "center"))
    tbl_pr.append(make_table_borders())
    tbl_pr.append(make_table_cell_margins())
    style.element.append(tbl_pr)


def make_style_value_element(tag: str, value: str):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    element = OxmlElement(tag)
    element.set(qn("w:val"), value)
    return element


def make_table_borders():
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement(f"w:{side}")
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "4")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), "auto")
        borders.append(border)
    return borders


def make_table_cell_margins():
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    margins = OxmlElement("w:tblCellMar")
    for side, width in (("top", "80"), ("left", "108"), ("bottom", "80"), ("right", "108")):
        margin = OxmlElement(f"w:{side}")
        margin.set(qn("w:w"), width)
        margin.set(qn("w:type"), "dxa")
        margins.append(margin)
    return margins


def configure_heading_styles(document: object) -> None:
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    heading_specs = {
        "Heading 1": (16, WD_ALIGN_PARAGRAPH.CENTER, 12, 12),
        "Heading 2": (14, WD_ALIGN_PARAGRAPH.LEFT, 10, 6),
        "Heading 3": (12, WD_ALIGN_PARAGRAPH.LEFT, 8, 4),
        "Heading 4": (11, WD_ALIGN_PARAGRAPH.LEFT, 6, 3),
        "Heading 5": (11, WD_ALIGN_PARAGRAPH.LEFT, 6, 3),
        "Heading 6": (11, WD_ALIGN_PARAGRAPH.LEFT, 6, 3),
    }
    for style_name, (font_size, alignment, before, after) in heading_specs.items():
        if style_name not in document.styles:
            continue
        style = document.styles[style_name]
        set_style_fonts(style, DEFAULT_LATIN_FONT, HEADING_EAST_ASIA_FONT)
        style.font.size = pt(font_size)
        style.font.bold = True
        style.paragraph_format.alignment = alignment
        style.paragraph_format.first_line_indent = None
        style.paragraph_format.line_spacing = 1.0
        style.paragraph_format.space_before = pt(before)
        style.paragraph_format.space_after = pt(after)


def set_style_fonts(style: object, latin_font: str, east_asia_font: str) -> None:
    from docx.oxml.ns import qn

    style.font.name = latin_font
    r_fonts = style.element.rPr.rFonts
    r_fonts.set(qn("w:ascii"), latin_font)
    r_fonts.set(qn("w:hAnsi"), latin_font)
    r_fonts.set(qn("w:eastAsia"), east_asia_font)


def set_style_keep_next(style: object) -> None:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    p_pr = style.element.get_or_add_pPr()
    if p_pr.find(qn("w:keepNext")) is None:
        p_pr.append(OxmlElement("w:keepNext"))


def set_style_keep_together(style: object) -> None:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    p_pr = style.element.get_or_add_pPr()
    if p_pr.find(qn("w:keepLines")) is None:
        p_pr.append(OxmlElement("w:keepLines"))


def pt(value: float):
    from docx.shared import Pt

    return Pt(value)


def scaled_image_size(image_path: Path):
    from docx.shared import Inches

    max_width = Inches(MAX_IMAGE_WIDTH_INCHES)
    max_height = Inches(MAX_IMAGE_HEIGHT_INCHES)
    try:
        from PIL import Image

        with Image.open(image_path) as image:
            width_px, height_px = image.size
        if width_px <= 0 or height_px <= 0:
            return max_width, None
        image_width = Inches(width_px / 96)
        image_height = Inches(height_px / 96)
        scale = min(max_width / image_width, max_height / image_height, 1.0)
        return int(image_width * scale), int(image_height * scale)
    except Exception:
        return max_width, None


def render_blocks(markdown: Path, output: Path, blocks: list[Block]) -> int:
    ensure_python_docx()
    from docx import Document

    document = Document()
    setup_document_styles(document)
    missing_images = 0
    index = 0

    while index < len(blocks):
        block = blocks[index]

        if block.kind == "heading":
            document.add_heading(block.text, level=block.level)
        elif block.kind == "paragraph":
            document.add_paragraph(block.text, style="Body Text")
        elif block.kind == "ordered_list":
            document.add_paragraph(block.text, style="List Number")
        elif block.kind == "unordered_list":
            document.add_paragraph(block.text, style="List Bullet")
        elif block.kind == "table_caption":
            add_caption(document, block.text, "table")
        elif block.kind == "figure_caption":
            add_caption(document, block.text, "figure")
        elif block.kind == "table":
            add_table(document, block.rows)
        elif block.kind == "image":
            if not add_picture(document, markdown, block.target):
                missing_images += 1
            if index + 1 < len(blocks) and blocks[index + 1].kind == "figure_caption":
                index += 1
                add_caption(document, blocks[index].text, "figure")
            elif block.text:
                add_caption(document, block.text, "figure")
        else:
            document.add_paragraph(block.text, style="Body Text")
        index += 1

    document.save(output)
    if missing_images:
        print(f"Warning: {missing_images} image(s) were missing.", file=sys.stderr)
    return 0


def run_fallback(markdown: Path, output: Path) -> int:
    return render_blocks(markdown, output, parse_blocks(markdown))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, help="Markdown source file.")
    parser.add_argument("-o", "--output", type=Path, help="DOCX output path. Defaults to the Markdown stem.")
    parser.add_argument("--reference-doc", type=Path, help="Optional pandoc reference DOCX.")
    parser.add_argument(
        "--pandoc",
        action="store_true",
        help="Use Pandoc instead of the built-in python-docx report renderer.",
    )
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="Use the built-in python-docx report renderer. This is the default without --pandoc.",
    )
    args = parser.parse_args()

    markdown = args.markdown.resolve()
    if not markdown.exists():
        print(f"File not found: {markdown}", file=sys.stderr)
        return 2
    output = (args.output or markdown.with_suffix(".docx")).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    if args.reference_doc and not args.reference_doc.exists():
        print(f"Reference DOCX not found: {args.reference_doc}", file=sys.stderr)
        return 2

    use_pandoc = (args.pandoc or args.reference_doc) and not args.fallback
    if use_pandoc and shutil.which("pandoc"):
        return run_pandoc(markdown, output, args.reference_doc)
    if use_pandoc:
        print("Pandoc was requested but is not available; using built-in renderer.", file=sys.stderr)
    return run_fallback(markdown, output)


if __name__ == "__main__":
    raise SystemExit(main())
