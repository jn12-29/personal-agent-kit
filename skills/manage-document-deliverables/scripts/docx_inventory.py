#!/usr/bin/env python3
"""Inspect a DOCX for headings, captions, media files, and stale terms."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import Sequence
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
HEADING_RE = re.compile(r"^(\d+(\.\d+)*[\.、\s]+|第[一二三四五六七八九十百]+[章节]|[一二三四五六七八九十]+[、.])")
FIGURE_RE = re.compile(r"^(图|Figure|Fig\.?)\s*\d+", re.IGNORECASE)
TABLE_RE = re.compile(r"^(表|Table)\s*\d+", re.IGNORECASE)


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """Keep examples readable while showing defaults."""


def parse_paragraphs(docx: Path) -> list[tuple[int, str, str]]:
    with zipfile.ZipFile(docx) as archive:
        try:
            xml = archive.read("word/document.xml")
        except KeyError as exc:
            raise SystemExit(f"{docx} does not look like a DOCX: missing word/document.xml") from exc

    root = ET.fromstring(xml)
    paragraphs: list[tuple[int, str, str]] = []
    for index, para in enumerate(root.findall(".//w:p", NS), start=1):
        text = "".join(node.text or "" for node in para.findall(".//w:t", NS)).strip()
        style_node = para.find("./w:pPr/w:pStyle", NS)
        style = ""
        if style_node is not None:
            style = style_node.attrib.get(f"{{{NS['w']}}}val", "")
        if text:
            paragraphs.append((index, style, text))
    return paragraphs


def list_media(docx: Path) -> list[tuple[str, int]]:
    with zipfile.ZipFile(docx) as archive:
        return sorted(
            (info.filename, info.file_size)
            for info in archive.infolist()
            if info.filename.startswith("word/media/")
            and not info.is_dir()
        )


def print_matches(title: str, rows: list[tuple[int, str, str]]) -> None:
    print(f"\n{title} ({len(rows)})")
    for index, style, text in rows:
        style_suffix = f" [{style}]" if style else ""
        print(f"  p{index}{style_suffix}: {text}")


def build_parser() -> argparse.ArgumentParser:
    epilog = """\
Examples:
  Inventory headings, captions, and media:
    python skills/manage-document-deliverables/scripts/docx_inventory.py docs/report.docx

  Locate stale project names or process-leak terms:
    python skills/manage-document-deliverables/scripts/docx_inventory.py docs/report.docx --terms OLD_NAME TODO 转换层

  Dump all non-empty paragraphs for manual review:
    python skills/manage-document-deliverables/scripts/docx_inventory.py docs/report.docx --dump-text

Defaults and behavior:
  - Run from the project root with project-relative paths when possible.
  - The script prints paragraph indexes such as p42 so findings can be checked against DOCX text.
  - Heading detection combines Word heading styles with short numbered heading-like paragraphs.
  - Terms are counted case-insensitively and located by paragraph.
  - This script reads the DOCX package directly and does not require Word, LibreOffice, Pandoc,
    or python-docx.
  - Exit codes: 0 success, 2 invalid input or unreadable DOCX.
"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=epilog,
        formatter_class=HelpFormatter,
    )
    parser.add_argument("docx", type=Path, help="DOCX source file to inspect.")
    parser.add_argument("--terms", nargs="*", default=[], help="Terms to count and locate in document text.")
    parser.add_argument("--dump-text", action="store_true", help="Print all non-empty paragraphs.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.docx.exists():
        print(f"File not found: {args.docx}", file=sys.stderr)
        return 2

    try:
        paragraphs = parse_paragraphs(args.docx)
        media = list_media(args.docx)
    except (zipfile.BadZipFile, ET.ParseError, RuntimeError, SystemExit) as exc:
        print(f"Could not inspect DOCX: {exc}", file=sys.stderr)
        return 2
    headings = []
    for row in paragraphs:
        _, style, text = row
        is_styled_heading = style.lower().startswith("heading")
        is_short_numbered_heading = bool(HEADING_RE.match(text)) and len(text) <= 80
        if is_styled_heading or is_short_numbered_heading:
            headings.append(row)
    figures = [row for row in paragraphs if FIGURE_RE.match(row[2])]
    tables = [row for row in paragraphs if TABLE_RE.match(row[2])]

    print(f"DOCX: {args.docx}")
    print(f"Non-empty paragraphs: {len(paragraphs)}")
    print(f"Media files: {len(media)}")
    for name, size in media:
        print(f"  {name}: {size} bytes")

    print_matches("Heading candidates", headings)
    print_matches("Figure captions", figures)
    print_matches("Table captions", tables)

    if args.terms:
        print("\nTerm hits")
        whole_text = "\n".join(text for _, _, text in paragraphs)
        for term in args.terms:
            count = whole_text.lower().count(term.lower())
            print(f"  {term}: {count}")
            for index, _, text in paragraphs:
                if term.lower() in text.lower():
                    print(f"    p{index}: {text}")

    if args.dump_text:
        print_matches("All paragraphs", paragraphs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
