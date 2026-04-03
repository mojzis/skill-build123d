---
name: build123d
description: Use this skill when the user wants to create 3D CAD models, parts, or assemblies using Python and the build123d library. Trigger on any mention of build123d, parametric CAD, BREP modeling, 3D printing models, CNC part design, CAD scripting, or when asked to design/model/create a physical object programmatically — brackets, enclosures, housings, gears, mounts, fixtures, adapters, or any mechanical part. Also trigger for STEP/STL file work, OpenCascade, or scripted geometry. Even "model this shape" or "design a part" in a programmatic context should trigger this skill.
---

# build123d — Python CAD Modeling

build123d is a Python BREP CAD library on OpenCascade. Install: `pip install build123d`.

This skill uses **algebra mode** exclusively — shapes are values, combined with Python operators. No context managers, no implicit state.

## Script Template

Always start from this skeleton:

```python
from build123d import *

# --- Parameters ---
width = 60
height = 40
thickness = 5
hole_radius = 4

# --- Build ---
part = Box(width, height, thickness)
part -= Cylinder(hole_radius, thickness)

# --- Export ---
export_step(part, "output.step")
export_stl(part, "output.stl")
```

Every script must end with `export_step()` and/or `export_stl()` so the result is viewable.

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
10. **Always export.** End every script with `export_step()` or `export_stl()`.

## Reference Files

- **`references/examples.md`** — Full code examples for every pattern: booleans, extrude, revolve, sweep, loft, selectors, patterns, shell, composition, import/export. **Read this first when writing a part.**
- **`references/api_catalogue.md`** — Constructor signatures for every shape, operation, and geometry class. **Search this when you need exact parameter names/types/defaults.**
