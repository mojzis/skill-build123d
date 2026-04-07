#!/usr/bin/env python3
"""
sketch_to_png.py — Rasterize an SVG sketch to PNG for the figure workflow.

Used as the first step of the Figure & Assembly Workflow described in
SKILL.md: draft a 2D silhouette of a figure in SVG, rasterize it with
this script, then look at the resulting PNG before writing any
build123d code or the parts manifest.

Usage:
    python sketch_to_png.py sketches/snowman.svg
    python sketch_to_png.py sketches/robot.svg -o sketches/robot_preview.png
    python sketch_to_png.py sketches/figure.svg -w 1200 --background "#f0f0f0"

Defaults:
    output     -> <svg_file>.with_suffix(".png")  (next to the SVG)
    width      -> 800 px
    background -> white

Dependencies: cairosvg

Part of the Claude x build123d skill toolkit. Mirrors the style of
render_preview.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def svg_to_png(
    svg_path: Path,
    png_path: Path,
    width: int = 800,
    background: str = "white",
) -> Path:
    """Convert an SVG sketch to a fixed-width PNG. Returns the PNG path."""
    import cairosvg

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=width,
        background_color=background,
    )
    return png_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Rasterize an SVG figure sketch to PNG for visual review.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s sketches/snowman.svg\n"
               "  %(prog)s sketches/robot.svg -o sketches/robot_preview.png\n"
               "  %(prog)s sketches/figure.svg -w 1200 --background \"#f0f0f0\"\n",
    )
    parser.add_argument("svg_file", type=Path, help="Path to the input SVG sketch")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output PNG path (default: <svg_file>.png next to the SVG)",
    )
    parser.add_argument(
        "-w", "--width", type=int, default=800,
        help="Pixel width of the output PNG (default: 800)",
    )
    parser.add_argument(
        "--background", default="white",
        help="Background color (CSS name or #rrggbb, default: white)",
    )
    args = parser.parse_args(argv)

    svg_path = args.svg_file.resolve()
    if not svg_path.exists():
        parser.error(f"SVG file not found: {svg_path}")

    png_path = (args.output or svg_path.with_suffix(".png")).resolve()
    png_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        svg_to_png(svg_path, png_path, width=args.width, background=args.background)
    except Exception as e:
        print(f"Error rasterizing {svg_path.name}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote: {png_path}")


if __name__ == "__main__":
    main()
