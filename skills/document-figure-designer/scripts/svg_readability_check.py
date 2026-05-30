#!/usr/bin/env python3
"""Static readability checks for SVG figures intended for documents."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


SIZE_RE = re.compile(r"(-?\d+(?:\.\d+)?)")
STYLE_RE = re.compile(r"([a-zA-Z-]+)\s*:\s*([^;]+)")
TAG_RE = re.compile(r"\{.*\}")
PATH_LINE_RE = re.compile(
    r"M\s*(-?\d+(?:\.\d+)?)\s*[, ]\s*(-?\d+(?:\.\d+)?)\s*L\s*(-?\d+(?:\.\d+)?)\s*[, ]\s*(-?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def local_name(tag: str) -> str:
    return TAG_RE.sub("", tag)


def parse_size(value: str | None) -> float | None:
    if not value:
        return None
    match = SIZE_RE.search(value)
    if not match:
        return None
    number = float(match.group(1))
    if value.strip().endswith("pt"):
        return number * 4 / 3
    return number


def parse_style(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    return {key: val.strip() for key, val in STYLE_RE.findall(value)}


def inherited_props(node: ET.Element, parent: dict[str, str]) -> dict[str, str]:
    props = dict(parent)
    props.update(parse_style(node.attrib.get("style")))
    for key in ("font-size", "font-family", "fill", "stroke"):
        if key in node.attrib:
            props[key] = node.attrib[key]
    return props


def text_content(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def parse_rect(node: ET.Element) -> tuple[float, float, float, float] | None:
    values = [parse_size(node.attrib.get(key)) for key in ("x", "y", "width", "height")]
    if any(value is None for value in values):
        return None
    x, y, width, height = [float(value) for value in values if value is not None]
    return x, y, x + width, y + height


def parse_line(node: ET.Element) -> tuple[float, float, float, float] | None:
    name = local_name(node.tag)
    if name == "line":
        values = [parse_size(node.attrib.get(key)) for key in ("x1", "y1", "x2", "y2")]
        if any(value is None for value in values):
            return None
        return tuple(float(value) for value in values if value is not None)  # type: ignore[return-value]
    if name == "path":
        match = PATH_LINE_RE.search(node.attrib.get("d", ""))
        if match:
            return tuple(float(group) for group in match.groups())  # type: ignore[return-value]
    return None


def point_inside_rect(x: float, y: float, rect: tuple[float, float, float, float]) -> bool:
    left, top, right, bottom = rect
    return left < x < right and top < y < bottom


def line_hits_rect(line: tuple[float, float, float, float], rect: tuple[float, float, float, float]) -> bool:
    x1, y1, x2, y2 = line
    if point_inside_rect(x1, y1, rect) or point_inside_rect(x2, y2, rect):
        return False

    left, top, right, bottom = rect
    dx = x2 - x1
    dy = y2 - y1
    u1, u2 = 0.0, 1.0
    for p, q in ((-dx, x1 - left), (dx, right - x1), (-dy, y1 - top), (dy, bottom - y1)):
        if p == 0:
            if q < 0:
                return False
            continue
        ratio = q / p
        if p < 0:
            if ratio > u2:
                return False
            u1 = max(u1, ratio)
        else:
            if ratio < u1:
                return False
            u2 = min(u2, ratio)
    return u2 > u1


def walk_text(node: ET.Element, parent_props: dict[str, str], out: list[tuple[str, float | None]]) -> None:
    props = inherited_props(node, parent_props)
    if local_name(node.tag) in {"text", "tspan"}:
        content = text_content(node)
        if content:
            out.append((content, parse_size(props.get("font-size"))))
    for child in node:
        walk_text(child, props, out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--min-font-px", type=float, default=24.0)
    parser.add_argument("--min-marker-px", type=float, default=14.0)
    parser.add_argument("--min-width", type=float, default=1200.0)
    parser.add_argument("--min-height", type=float, default=700.0)
    parser.add_argument("--check-line-rects", action="store_true")
    args = parser.parse_args()

    if not args.svg.exists():
        print(f"File not found: {args.svg}", file=sys.stderr)
        return 2

    root = ET.parse(args.svg).getroot()
    failures: list[str] = []
    warnings: list[str] = []

    width = parse_size(root.attrib.get("width"))
    height = parse_size(root.attrib.get("height"))
    view_box = root.attrib.get("viewBox")
    if view_box:
        parts = [float(part) for part in re.findall(r"-?\d+(?:\.\d+)?", view_box)]
        if len(parts) == 4:
            width = width or parts[2]
            height = height or parts[3]

    if width is not None and width < args.min_width:
        warnings.append(f"canvas width {width:g}px is below suggested {args.min_width:g}px")
    if height is not None and height < args.min_height:
        warnings.append(f"canvas height {height:g}px is below suggested {args.min_height:g}px")

    text_rows: list[tuple[str, float | None]] = []
    walk_text(root, {}, text_rows)
    for text, font_size in text_rows:
        preview = text[:50].replace("\n", " ")
        if font_size is None:
            warnings.append(f"text has no explicit/inherited font-size: {preview!r}")
        elif font_size < args.min_font_px:
            failures.append(f"text below {args.min_font_px:g}px: {font_size:g}px {preview!r}")

    for marker in root.iter():
        if local_name(marker.tag) != "marker":
            continue
        marker_id = marker.attrib.get("id", "<unnamed>")
        marker_width = parse_size(marker.attrib.get("markerWidth"))
        marker_height = parse_size(marker.attrib.get("markerHeight"))
        if marker_width is not None and marker_width < args.min_marker_px:
            failures.append(f"marker {marker_id} width below {args.min_marker_px:g}px: {marker_width:g}px")
        if marker_height is not None and marker_height < args.min_marker_px:
            failures.append(f"marker {marker_id} height below {args.min_marker_px:g}px: {marker_height:g}px")

    if args.check_line_rects:
        rects = [rect for node in root.iter() if local_name(node.tag) == "rect" for rect in [parse_rect(node)] if rect]
        lines = [line for node in root.iter() if local_name(node.tag) in {"line", "path"} for line in [parse_line(node)] if line]
        for line in lines:
            for rect in rects:
                if line_hits_rect(line, rect):
                    warnings.append(f"connector {line} appears to cross rectangle {rect}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for failure in failures:
        print(f"FAIL: {failure}")

    print(f"Checked {args.svg}: {len(text_rows)} text nodes, {len(failures)} failures, {len(warnings)} warnings")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
