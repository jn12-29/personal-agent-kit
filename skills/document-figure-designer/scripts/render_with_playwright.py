#!/usr/bin/env python3
"""Render SVG or HTML figure sources to raster images with Chromium/Playwright."""

from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path


def shell_arg(value: Path) -> str:
    return shlex.quote(str(value))


def renderer_script() -> Path:
    return Path(__file__).resolve()


def install_hint() -> str:
    script = shell_arg(renderer_script())
    return f"""Playwright is required for canonical figure rendering.

Create a project-local virtual environment, then install Playwright and its managed Chromium browser:
  uv venv .venv
  uv pip install playwright
  uv run python -m playwright install chromium
  uv run python {script} --input <figure.svg|figure.html> --out <figure.png>

If uv is unavailable, use Python's built-in venv module:
  python -m venv .venv
  .venv/bin/python -m pip install playwright
  .venv/bin/python -m playwright install chromium
  .venv/bin/python {script} --input <figure.svg|figure.html> --out <figure.png>

Do not use sudo or modify system-wide browser installations for this workflow.
"""


def run_hint() -> str:
    script = shell_arg(renderer_script())
    return (
        "After installing Playwright in a local environment, run this renderer with the same environment: "
        f"uv run python {script} --input <figure.svg|figure.html> --out <figure.png> "
        f"or .venv/bin/python {script} --input <figure.svg|figure.html> --out <figure.png>"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", "-i", type=Path, required=True, help="SVG or HTML source file")
    parser.add_argument("--out", "-o", type=Path, required=True, help="Raster output path (.png, .jpg, or .jpeg)")
    parser.add_argument("--width", type=int, default=1920, help="Viewport width in CSS pixels")
    parser.add_argument("--height", type=int, default=1080, help="Viewport height in CSS pixels")
    parser.add_argument("--scale", type=float, default=1.0, help="Device scale factor for screenshot output")
    parser.add_argument(
        "--background",
        default=None,
        help=(
            "Optional page background override used around SVG sources; "
            "omit to preserve source backgrounds, or use transparent only if the consumer supports alpha"
        ),
    )
    return parser.parse_args()


def import_playwright():
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:
        print(install_hint(), file=sys.stderr)
        return None, None
    return sync_playwright, PlaywrightError


def source_url(source: Path) -> str:
    suffix = source.suffix.lower()
    if suffix in {".svg", ".html", ".htm"}:
        return source.resolve().as_uri()
    raise ValueError(f"Unsupported input type: {source.suffix or '<none>'}. Expected .svg, .html, or .htm.")


def configure_svg_document(page, width: int, height: int, background: str | None) -> None:
    page.evaluate(
        """({ width, height, background }) => {
            const svg = document.documentElement;
            if (!svg || svg.localName.toLowerCase() !== "svg") return;

            const parseSize = (value) => {
                if (!value || String(value).trim().endsWith("%")) return null;
                const match = String(value).match(/^\\s*(\\d+(?:\\.\\d+)?)/);
                return match ? Number(match[1]) : null;
            };

            if (!svg.hasAttribute("viewBox")) {
                const originalWidth = parseSize(svg.getAttribute("width"));
                const originalHeight = parseSize(svg.getAttribute("height"));
                if (originalWidth && originalHeight) {
                    svg.setAttribute("viewBox", `0 0 ${originalWidth} ${originalHeight}`);
                }
            }

            svg.setAttribute("width", String(width));
            svg.setAttribute("height", String(height));
            svg.style.width = `${width}px`;
            svg.style.height = `${height}px`;
            svg.style.display = "block";

            if (background && String(background).trim().toLowerCase() !== "transparent") {
                svg.style.background = background;
                svg.style.backgroundColor = background;
                let backgroundRect = document.getElementById("__playwright_background__");
                if (!backgroundRect) {
                    backgroundRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                    backgroundRect.setAttribute("id", "__playwright_background__");
                    svg.insertBefore(backgroundRect, svg.firstChild);
                }
                backgroundRect.setAttribute("x", "0");
                backgroundRect.setAttribute("y", "0");
                backgroundRect.setAttribute("width", "100%");
                backgroundRect.setAttribute("height", "100%");
                backgroundRect.setAttribute("fill", background);
            }
        }""",
        {"width": width, "height": height, "background": background},
    )


def validate_source_type(source: Path) -> None:
    if source.suffix.lower() not in {".svg", ".html", ".htm"}:
        raise ValueError(f"Unsupported input type: {source.suffix or '<none>'}. Expected .svg, .html, or .htm.")


def screenshot_type(output: Path) -> str:
    suffix = output.suffix.lower()
    if suffix == ".png":
        return "png"
    if suffix in {".jpg", ".jpeg"}:
        return "jpeg"
    raise ValueError(f"Unsupported output type: {output.suffix or '<none>'}. Expected .png, .jpg, or .jpeg.")


def is_transparent_background(background: str | None) -> bool:
    return background is not None and background.strip().lower() == "transparent"


def render() -> int:
    args = parse_args()
    if args.width <= 0 or args.height <= 0:
        print("--width and --height must be positive integers", file=sys.stderr)
        return 2
    if args.scale <= 0:
        print("--scale must be positive", file=sys.stderr)
        return 2
    if not args.input.exists():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 2
    if args.input.is_dir():
        print(f"Input is a directory, expected a file: {args.input}", file=sys.stderr)
        return 2
    try:
        validate_source_type(args.input)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    try:
        output_type = screenshot_type(args.out)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    sync_playwright, PlaywrightError = import_playwright()
    if sync_playwright is None or PlaywrightError is None:
        return 2

    args.out.parent.mkdir(parents=True, exist_ok=True)
    try:
        url = source_url(args.input)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        with sync_playwright() as playwright:
            browser = None
            try:
                browser = playwright.chromium.launch()
                page = browser.new_page(
                    viewport={"width": args.width, "height": args.height},
                    device_scale_factor=args.scale,
                )
                page.goto(url, wait_until="networkidle")
                if args.input.suffix.lower() == ".svg":
                    configure_svg_document(page, args.width, args.height, args.background)
                omit_background = is_transparent_background(args.background)
                page.screenshot(
                    path=str(args.out),
                    full_page=False,
                    omit_background=omit_background,
                    type=output_type,
                )
            finally:
                if browser is not None:
                    browser.close()
    except PlaywrightError as exc:
        print(f"Playwright render failed: {exc}", file=sys.stderr)
        print(f"If Chromium is missing, run: {sys.executable} -m playwright install chromium", file=sys.stderr)
        print(run_hint(), file=sys.stderr)
        return 1

    print(f"Rendered {args.input} -> {args.out} ({args.width}x{args.height}, scale {args.scale:g})")
    return 0


if __name__ == "__main__":
    raise SystemExit(render())
