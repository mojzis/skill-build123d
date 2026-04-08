---
name: build123d
description: Use this skill when the user wants to create 3D CAD models, parts, or assemblies using Python and the build123d library. Trigger on any mention of build123d, parametric CAD, BREP modeling, 3D printing models, CNC part design, CAD scripting, or when asked to design/model/create a physical object programmatically — brackets, enclosures, housings, gears, mounts, fixtures, adapters, or any mechanical part. Also trigger for STEP/STL file work, OpenCascade, or scripted geometry. Even "model this shape" or "design a part" in a programmatic context should trigger this skill.
---

# build123d — Python CAD Modeling

build123d is a Python BREP CAD library on OpenCascade. Install: `uv add build123d b3d-validate`.

This skill uses **algebra mode** exclusively — shapes are values, combined with Python operators. No context managers, no implicit state.

## Script Template

Always start from this skeleton:

```python
from build123d import *
from b3d_validate import full_check
from datetime import datetime
from pathlib import Path

# --- Parameters ---
width = 60
height = 40
thickness = 5
hole_radius = 4

# --- Build ---
part = Box(width, height, thickness)
part -= Cylinder(hole_radius, thickness)

# --- Validate ---
report = full_check(part)
print(report)

# --- Export ---
script_name = Path(__file__).stem
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

steps_dir = Path("steps")
steps_dir.mkdir(exist_ok=True)
step_path = steps_dir / f"{script_name}_{timestamp}.step"
export_step(part, str(step_path))
print(f"Exported: {step_path}")

stls_dir = Path("stls")
stls_dir.mkdir(exist_ok=True)
stl_path = stls_dir / f"{script_name}_{timestamp}.stl"
try:
    export_stl(part, str(stl_path))
    print(f"Exported: {stl_path}")
except Exception as e:
    print(f"STL export skipped: {e}")
```

Every script must validate then export. If `full_check()` reports geometry errors, **fix the model before exporting**. Printability warnings are informational — export can proceed, but address them if the part is meant for manufacturing.

Both files use the naming convention `{script_name}_{timestamp}.{ext}`:
- `steps/` — STEP for CAD interchange (authoritative geometry)
- `stls/` — STL for fast preview / slicer import (best-effort tessellation)

STL export is wrapped in `try/except` because tessellation can fail or be slow on dense / non-manifold parts. The STEP file is the source of truth; STL is the convenience preview.

## Validation & Preview Workflow

Every build script includes a `full_check(part)` call that validates geometry and printability **before** export. The workflow is:

1. **Run the script.** Check the `full_check()` output in stdout.
2. **If geometry errors** (verdict is not "READY TO PRINT" or "GEOMETRY OK"): fix the model and re-run. Do **not** export or preview broken geometry.
3. **If validation passes**, the script exports the STEP and STL files. Then generate a visual preview:

```bash
python scripts/render_preview.py steps/<exported>.step -o previews --composite --prefix <script_name>_<timestamp>
```

This renders multi-view wireframe PNGs into the `previews/` directory. The `--composite` flag creates a single labeled grid image for quick review.

4. **Read the composite image** to visually verify the model matches the user's intent. If the geometry looks wrong, iterate on the script before presenting the result.
5. **Connection review (assemblies only).** If the part is composed from more than one named sub-part or imports any external STEP, examine each joint in the composite. Watch for visible gaps, zero-overlap seams, floating sub-parts, and sharp discontinuities. Prefer elegantly blended joints — a small `fillet` on the boundary edges, or a ≥ 0.2 mm overlap before `+` union. Skip only when a blocky / low-poly look is intended. If there is room for improvement, iterate on the script and re-render before presenting.
6. **Fast-preview STL.** Confirm the `stls/` file landed for the final iteration. This is the artifact the user loads in a slicer or mesh viewer.

All directories serve as a timeline:
- `steps/` — STEP file history, one per build run, for comparison and rollback
- `stls/` — STL history for fast preview / slicer import
- `previews/` — visual snapshots matching each STEP export

## How It Works

```python
from build123d import *

# Shapes are values
box = Box(50, 40, 30)
cyl = Cylinder(10, 30)

# Boolean operators
result = box - cyl          # subtract
result = box + cyl          # union
result = box & cyl          # intersect

# Positioning
result = box - Pos(15, 0, 0) * Cylinder(5, 30)

# 2D → 3D: sketch then extrude
sketch = Circle(30) - Rectangle(20, 20)
part = extrude(sketch, amount=15)

# Select sub-geometry for operations
part = fillet(part.edges().filter_by(Axis.Z), radius=3)
```

## Translating User Intent to Geometry

When someone describes a physical object, decompose it:

### Step 1: Identify the Base Form

What is the overall envelope?
- Rectangular block → `Box(l, w, h)`
- Cylindrical → `Cylinder(r, h)`
- Rotationally symmetric (vase, cup, nozzle) → profile sketch + `revolve()`
- Constant cross-section along a path → sketch + `sweep()`
- Varying cross-section → multiple sketches + `loft()`
- Custom 2D shape → `Line`/`Polyline`/`Spline` → `make_face()` → `extrude()`

### Step 2: Add and Subtract Features

Build up the part with booleans:
- Holes → `part -= Pos(x,y,z) * Cylinder(r, h)`
- Slots → `part -= Pos(...) * SlotOverall(l, w)` extruded, or `part -= Pos(...) * Box(l, w, h)`
- Bosses/posts → `part += Pos(x,y,z) * Cylinder(r, h)`
- Pockets → `part -= Pos(...) * Box(l, w, depth)`

### Step 3: Refine

Apply finishing operations last:
- Rounded edges → `fillet(part.edges()..., radius=r)`
- Beveled edges → `chamfer(part.edges()..., length=l)`
- Hollow/shell → `offset(part, amount=-wall, openings=[face])`
- Draft angles → `extrude(sketch, amount=h, taper=angle)`

### Intent → Operation Mapping

| User says | build123d approach |
|-----------|-------------------|
| "hole", "bore" | `part -= Pos(...) * Cylinder(r, h)` |
| "slot", "groove" | `part -= Pos(...) * extrude(SlotOverall(l, w), h)` |
| "rounded edges", "fillet" | `fillet(part.edges()..., radius=r)` |
| "beveled", "chamfer" | `chamfer(part.edges()..., length=l)` |
| "hollow", "shell", "wall thickness" | `offset(part, amount=-t, openings=[face])` |
| "tube", "pipe" | `sweep(Plane(path^0) * Circle(r), path=path)` |
| "tapered", "draft angle" | `extrude(sketch, amount=h, taper=angle)` |
| "symmetrical" | build half, `mirror(half, about=Plane.YZ) + half` |
| "array", "grid", "pattern of" | `[loc * feature for loc in GridLocations(...)]` |
| "ring of", "circular pattern" | `[loc * feature for loc in PolarLocations(r, n)]` |
| "lip", "rim", "flange" | extrude a thin ring/rectangle on a face |
| "rib", "stiffener" | thin extruded rectangle between walls |
| "mounting hole" | `part -= Pos(...) * Cylinder(r, h)` with counterbore/countersink |
| "thread" | `Helix` + `sweep` (visual threads), or just model the hole |
| "text", "label", "engraving" | `part -= extrude(Plane(face) * Text("...", font_size=s), amount=-depth)` |
| "rounded box", "enclosure" | `Box` → `fillet` edges → `offset` to shell |

## Figure & Assembly Workflow

When the request is a **figure** — a character, robot, mascot, snowman, figurine, or any visually distinct creation with three or more sub-parts — do **not** jump straight into build123d code. The decomposition is the hard part, and writing it down before coding catches problems early. Single brackets, adapters, and enclosures may skip this flow.

### Step 1 — Sketch in SVG

Draft a 2D silhouette of the figure in `sketches/<name>.svg` using simple primitives — `<circle>`, `<ellipse>`, `<rect>`, `<line>`, `<path>`. One shape per intended 3D sub-part. This is for layout and proportion, not for dimensions; rough is fine.

### Step 2 — Rasterize and look

```bash
python scripts/sketch_to_png.py sketches/<name>.svg
```

Open `sketches/<name>.png` and **read it**. Do not write any build123d code yet. Confirm the layout matches what the user asked for; if not, iterate on the SVG and re-rasterize before continuing.

### Step 3 — Write the parts manifest

Create `sketches/<name>.parts.md` listing every part the figure will be built from. This file is the contract between the sketch and the build script. It persists the decomposition so later iterations (or the human user) can read what was intended without re-deriving it from the code.

Header lines: source sketch path, front-facing axis (default `-Y`), up axis (default `+Z`). Then one block per part — `## <name>` followed by `shape:`, `dimensions:`, `anchor:`, `connects to:`, `notes:` lines. Note any intentional non-elegant joints in the `notes:` line.

```markdown
# snowman — parts manifest
Sketch: sketches/snowman.svg
Front-facing axis: -Y
Up axis: +Z

## body
shape: Sphere
dimensions: r=30
anchor: (0, 0, 30)
connects to: head (top)
notes: sits on Z=0

## head
shape: Sphere
dimensions: r=18
anchor: (0, 0, 30 + 30 + 18*0.9)
connects to: body, nose
notes: 0.9 overlap with body = blended seam

## nose
shape: Cone
dimensions: r1=2, r2=0, h=8
anchor: (0, -18*0.9, head_z)
connects to: head (front)
notes: points -Y
```

### Step 4 — Decompose into functions

From the manifest, write one `make_<part>()` function per row (see Part Composition below). Each function returns a `Part`. The function's local origin should match the anchor convention in the manifest, so the assembly step is pure positioning.

### Step 5 — Orient to the preview's front view

The preview "front" view (`b3d_validate.rendering`) places the camera at **−Y** looking toward **+Y** (verified empirically against `project_to_viewport`). Therefore the figure's face / visual front should point toward **−Y**, with **+Z** up and **+X** to the figure's left (the viewer's right).

If the first front render shows the **back** of the figure, the convention has flipped — wrap the **top-level assembly** in `Rot(0, 0, 180)` and re-export, then update the manifest's "Front-facing axis" line. Apply the rotation to the assembly, never to individual parts.

### Step 6 — Build and combine

Call each `make_<part>()`, place with `Pos(x, y, z)` from the manifest, union with `+`. Prefer a **small overlap** between touching parts (≥ 0.2 mm, or a fraction of the smaller part's radius) so the union creates a single blended volume rather than a razor-thin seam.

### Step 7 — Preview, review joints, iterate

Follow the main Validation & Preview Workflow above. On the connection-review step, look specifically at where the figure's parts meet — neck, shoulders, wrists, joins, etc. Improve with `fillet` on the boundary edges or by tweaking overlap, then re-run and present the improved preview.

When you change a part's dimensions or position during iteration, **update the manifest** as well. The manifest should always reflect the latest build.

### Step 8 — Final STL

Confirm the `stls/<name>_<timestamp>.stl` file landed for the final iteration. The STL is the fast-preview artifact for the user.

See `references/examples.md §17` for an end-to-end example.

## Part Composition

Parts are Python objects. Compose with functions and imports:

```python
# parts/bracket.py
from build123d import *

def make_bracket(width=40, height=30, thickness=5):
    plate = Box(width, thickness, height, align=(Align.CENTER, Align.MIN, Align.MIN))
    base = Box(width, height, thickness, align=(Align.CENTER, Align.MIN, Align.MIN))
    bracket = plate + base
    bracket = fillet(
        bracket.edges().filter_by(Axis.X).filter_by_position(Axis.Z, thickness * 0.9, thickness * 1.1),
        radius=thickness * 0.8
    )
    return bracket

# main.py
from bracket import make_bracket

plate = Box(200, 200, 5)
assembly = plate + Pos(50, 0, 2.5) * make_bracket()
export_step(assembly, "assembly.step")
```

For external parts: `motor = import_step("nema17.step")`

## Tips & Pitfalls

1. **Fillet/chamfer last.** They add complexity that breaks subsequent booleans.
2. **make_face() required.** Lines/arcs form a wire, not a face. Call `make_face(wire)` before extruding.
3. **Extrude direction** is perpendicular to the sketch plane. Negative `amount` = opposite direction. `both=True` = symmetric.
4. **Small fillets first.** If fillet fails, reduce the radius. Must be < half the shortest adjacent edge.
5. **2D before 3D.** Build complex cross-sections as 2D sketches, then extrude/revolve. Avoid complex 3D booleans when a single extrude would work.
6. **Parameterize everything.** Put dimensions in variables at the top. This is the whole point of programmatic CAD.
7. **Close your wires.** For `make_face()`, the wire must form a closed loop. Last point must connect back to first.
8. **Align controls origin.** Default is `Align.CENTER` on all axes. Use `align=(Align.CENTER, Align.CENTER, Align.MIN)` to sit a box on the XY plane.
9. **OpenCascade can fail.** If an operation produces weird results or errors, try a different construction strategy (e.g., loft instead of sweep, split the operation into smaller steps).
10. **Always validate + export + preview.** Every script must call `full_check(part)` before exporting. Fix geometry errors before proceeding. Then export to `steps/` and run `render_preview.py` to verify visually.

## Reference Files

- **`references/examples.md`** — Full code examples for every pattern: booleans, extrude, revolve, sweep, loft, selectors, patterns, shell, composition, import/export. **Read this first when writing a part.**
- **`references/api_catalogue.md`** — Constructor signatures for every shape, operation, and geometry class. **Search this when you need exact parameter names/types/defaults.**
- **`b3d_validate`** — Validation library. `full_check(part)` validates geometry and printability in one call. Use `validate_geometry(part)` or `validate_printability(part, process="fdm")` individually for targeted checks.
- **`scripts/render_preview.py`** — Headless multi-view wireframe renderer. Converts STEP → PNG previews. Use after every export to visually verify the model.
- **`scripts/sketch_to_png.py`** — SVG → PNG helper for the sketch-first figure workflow. Use **before** writing any 3D code for a figure or assembly: draft the layout in `sketches/<name>.svg`, rasterize, look at the image, then write the parts manifest and the build script.
