#!/usr/bin/env python3
"""Extract focused API catalogue from build123d source code.

Only extracts the subset relevant to algebra-mode CAD modeling.
Skips: drafting, technical drawing, DXF/SVG exporters, mesher,
constrained lines, airfoil, joints, persistence, jupyter, vtk.
"""

import ast
import os

REPO_ROOT = os.environ.get("BUILD123D_REPO", "/home/claude/build123d")
SRC_DIR = os.path.join(REPO_ROOT, "src", "build123d")

INCLUDE = {
    "Box", "Cylinder", "Sphere", "Cone", "Torus", "Wedge",
    "Hole", "CounterBoreHole", "CounterSinkHole",
    "Circle", "Ellipse", "Rectangle", "RectangleRounded", "Polygon",
    "RegularPolygon", "Trapezoid", "Triangle", "Text",
    "SlotArc", "SlotCenterPoint", "SlotCenterToCenter", "SlotOverall",
    "Line", "Polyline", "Spline", "Bezier", "Helix",
    "CenterArc", "RadiusArc", "SagittaArc", "TangentArc", "ThreePointArc",
    "FilletPolyline", "PolarLine",
    "extrude", "revolve", "sweep", "loft",
    "fillet", "chamfer", "offset", "mirror", "split", "scale",
    "make_face", "make_hull", "add", "thicken", "section",
    "Vector", "Axis", "Plane", "Location", "Pos", "Rot", "Rotation",
    "BoundBox",
    "Vertex", "Edge", "Wire", "Face", "Shell", "Solid", "Compound",
    "Part", "Sketch", "Curve", "ShapeList",
    "Locations", "GridLocations", "PolarLocations", "HexLocations",
    "Align", "Mode", "Kind", "Keep", "Until", "Side",
    "GeomType", "SortBy", "Transition", "FontStyle", "Unit",
    "import_step", "import_stl", "import_brep", "import_svg",
    "export_step", "export_stl", "export_brep", "export_gltf",
}

MODULES = [
    ("3D Primitives", ["objects_part.py"]),
    ("2D Sketch Objects", ["objects_sketch.py"]),
    ("1D Curve Objects", ["objects_curve.py"]),
    ("Operations", ["operations_part.py", "operations_sketch.py", "operations_generic.py"]),
    ("Geometry & Positioning", ["geometry.py"]),
    ("Enums", ["build_enums.py"]),
    ("Import / Export", ["importers.py", "exporters3d.py"]),
]


def format_signature(node):
    args = node.args
    parts = []
    num_defaults = len(args.defaults)
    num_args = len(args.args)
    non_default_count = num_args - num_defaults
    for i, arg in enumerate(args.args):
        if arg.arg in ("self", "cls"):
            continue
        name = arg.arg
        annotation = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
        default_idx = i - non_default_count
        if 0 <= default_idx < len(args.defaults):
            default_val = ast.unparse(args.defaults[default_idx])
            if len(default_val) > 50:
                default_val = default_val[:47] + "..."
            parts.append(f"{name}{annotation} = {default_val}")
        else:
            parts.append(f"{name}{annotation}")
    if args.vararg:
        ann = f": {ast.unparse(args.vararg.annotation)}" if args.vararg.annotation else ""
        parts.append(f"*{args.vararg.arg}{ann}")
    for i, arg in enumerate(args.kwonlyargs):
        annotation = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
        if i < len(args.kw_defaults) and args.kw_defaults[i] is not None:
            default_val = ast.unparse(args.kw_defaults[i])
            if len(default_val) > 50:
                default_val = default_val[:47] + "..."
            parts.append(f"{arg.arg}{annotation} = {default_val}")
        else:
            parts.append(f"{arg.arg}{annotation}")
    if args.kwarg:
        ann = f": {ast.unparse(args.kwarg.annotation)}" if args.kwarg.annotation else ""
        parts.append(f"**{args.kwarg.arg}{ann}")
    return ", ".join(parts)


def get_description(docstring):
    if not docstring:
        return ""
    lines = docstring.strip().split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith(("args:", "raises:", "returns:", "example:", "note:")):
            break
        result.append(stripped)
    text = " ".join(result).strip()
    for prefix in ("Part Object:", "Part Operation:", "Sketch Object:", "Curve Object:"):
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    if len(text) > 250:
        text = text[:247] + "..."
    return text


def process_module(filepath):
    with open(filepath) as f:
        tree = ast.parse(f.read())
    classes, functions = [], []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in INCLUDE:
            docstring = ast.get_docstring(node) or ""
            init_sig = ""
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    init_sig = format_signature(item)
                    break
            classes.append({"name": node.name, "description": get_description(docstring), "signature": init_sig})
        elif isinstance(node, ast.FunctionDef) and node.name in INCLUDE:
            docstring = ast.get_docstring(node) or ""
            ret = ast.unparse(node.returns) if node.returns else ""
            functions.append({"name": node.name, "description": get_description(docstring), "signature": format_signature(node), "returns": ret})
    return classes, functions


def main():
    output = ["# build123d API Reference (Focused Subset)\n",
              "Algebra-mode API surface for CAD modeling. Signatures extracted from source.\n"]
    for category, module_files in MODULES:
        items = []
        for mf in module_files:
            fp = os.path.join(SRC_DIR, mf)
            if not os.path.exists(fp):
                continue
            c, f = process_module(fp)
            items.extend([(x, False) for x in c])
            items.extend([(x, True) for x in f])
        if not items:
            continue
        output.append(f"\n## {category}\n")
        for item, is_func in items:
            name = item["name"]
            if is_func:
                ret = f" → {item['returns']}" if item['returns'] else ""
                output.append(f"### `{name}()`{ret}\n")
            else:
                output.append(f"### `{name}`\n")
            if item["signature"]:
                output.append(f"```python\n{name}({item['signature']})\n```\n")
            if item["description"]:
                output.append(f"{item['description']}\n")
            output.append("")
    return "\n".join(output)


if __name__ == "__main__":
    print(main())
