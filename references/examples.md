# build123d Examples & Patterns (Algebra Mode)

All examples use `from build123d import *`. All use algebra mode exclusively.

## Table of Contents
1. Primitives & Booleans
2. Sketch → Extrude
3. Custom Profile (Lines → Face → Extrude)
4. Revolve
5. Sweep
6. Loft
7. Fillet & Chamfer
8. Shell (Hollowing)
9. Holes & Fastener Features
10. Positioning & Patterns
11. Selectors & Filtering
12. Mirror & Symmetry
13. Working on Existing Faces
14. Part Composition (Multi-file)
15. Import & Export
16. Topology Quick Reference

---

## 1. Primitives & Booleans

```python
from build123d import *

box = Box(50, 40, 30)
cyl = Cylinder(10, 30)

union    = box + cyl          # combine
cut      = box - cyl          # subtract
common   = box & cyl          # intersect

# Position before combining
result = box - Pos(15, 0, 0) * Cylinder(5, 30)
```

## 2. Sketch → Extrude

The core workflow: build a 2D shape, extrude to 3D.

```python
from build123d import *

# Simple: single shape
part = extrude(Circle(25), amount=10)

# Compound sketch with boolean
sketch = Circle(30) - Rectangle(20, 20)
part = extrude(sketch, amount=15)

# Extrude both directions
part = extrude(Circle(20), amount=10, both=True)  # ±10

# Extrude with taper
part = extrude(Rectangle(40, 40), amount=20, taper=10)  # 10° draft
```

## 3. Custom Profile (Lines → Face → Extrude)

```python
from build123d import *

# Build a wire from line segments, convert to face, extrude
wire = Curve() + [
    Line((0, 0), (80, 0)),
    Line((80, 0), (80, 40)),
    ThreePointArc((80, 40), (40, 70), (0, 40)),
    Line((0, 40), (0, 0)),
]
profile = make_face(wire)
part = extrude(profile, amount=10)
```

## 4. Revolve

Create a cross-section on the XZ plane, revolve around Z axis.

```python
from build123d import *

# Wine glass-ish shape
wire = Curve() + [
    Line((0, 0), (30, 0)),
    Line((30, 0), (5, 40)),
    Line((5, 40), (10, 45)),
    Spline((10, 45), (15, 80), (12, 100), tangents=((1, 2), (0, 1))),
    Line((12, 100), (0, 100)),
]
profile = make_face(wire)
glass = revolve(profile, axis=Axis.Z)
```

## 5. Sweep

Sweep a cross-section along a path.

```python
from build123d import *

# Define a 3D path
path = Spline(
    (0, 0, 0), (20, 20, 20), (40, -10, 40),
    tangents=((0, 0, 1), (0, 0, 1))
)

# Create cross-section at the start of the path
# ^ operator gives Location at a parameter along the curve
cross_section = Plane(path ^ 0) * Circle(5)

# Sweep
pipe = sweep(cross_section, path=path)
```

## 6. Loft

Transition between sketches at different heights.

```python
from build123d import *

# Bottom: rectangle. Top: circle.
bottom = Rectangle(40, 40)
top = Pos(0, 0, 30) * Circle(15)
part = loft([bottom, top])

# With intermediate sections
mid = Pos(0, 0, 15) * RegularPolygon(radius=25, side_count=6)
part = loft([bottom, mid, top])
```

## 7. Fillet & Chamfer

Apply last. Select edges with selectors.

```python
from build123d import *

box = Box(50, 50, 30)

# Fillet specific edges (vertical edges = parallel to Z)
box = fillet(box.edges().filter_by(Axis.Z), radius=5)

# Chamfer bottom edges
box = chamfer(box.edges().sort_by(Axis.Z)[:4], length=2)

# Fillet ALL edges (risky — start with small radius)
# box = fillet(box.edges(), radius=1)
```

## 8. Shell (Hollowing)

```python
from build123d import *

box = Box(50, 50, 30)
top_face = box.faces().sort_by(Axis.Z)[-1]

# Hollow with 2mm walls, opening on top
shelled = offset(box, amount=-2, openings=[top_face])

# Open on top AND bottom
top_and_bottom = box.faces().filter_by(GeomType.PLANE)
shelled = offset(box, amount=-2, openings=top_and_bottom)
```

## 9. Holes & Fastener Features

```python
from build123d import *

plate = Box(80, 60, 10)

# Simple through-hole
plate -= Pos(20, 0, 0) * Cylinder(5, 10)

# Counterbore hole (builder-mode only for CounterBoreHole/CounterSinkHole,
# but in algebra mode just stack cylinders)
plate -= Pos(-20, 0, 0) * Cylinder(3, 10)       # through hole
plate -= Pos(-20, 0, 2) * Cylinder(6, 10)        # counterbore from top

# Pattern of holes
for x, y in [(20, 20), (-20, 20), (-20, -20), (20, -20)]:
    plate -= Pos(x, y, 0) * Cylinder(3, 10)

# Using Locations for patterns
locs = GridLocations(15, 15, 3, 3)
holes = [loc * Cylinder(2, 10) for loc in locs]
plate -= holes
```

## 10. Positioning & Patterns

```python
from build123d import *

# Pos(x, y, z) — translate
moved = Pos(10, 20, 0) * Box(5, 5, 5)

# Rot(rx, ry, rz) — rotate (degrees)
rotated = Rot(0, 0, 45) * Rectangle(20, 10)

# Combine: translate then rotate
placed = Pos(30, 0, 0) * Rot(0, 0, 45) * Box(10, 10, 10)

# Location(position, orientation) — full transform
placed = Location((10, 20, 0), (0, 0, 45)) * Box(10, 10, 10)

# Grid pattern
locs = GridLocations(x_spacing=20, y_spacing=20, x_count=3, y_count=3)
grid_of_cylinders = [loc * Cylinder(3, 10) for loc in locs]

# Polar pattern
locs = PolarLocations(radius=30, count=6)
ring_of_holes = [loc * Cylinder(2, 10) for loc in locs]

# Hex pattern
locs = HexLocations(apothem=10, x_count=4, y_count=4)
hex_grid = [loc * Circle(4) for loc in locs]
```

## 11. Selectors & Filtering

Every Shape has `.vertices()`, `.edges()`, `.wires()`, `.faces()`, `.solids()` returning a `ShapeList`.

```python
from build123d import *

box = Box(50, 40, 30)

# --- filter_by: keep items matching criterion ---
box.edges().filter_by(Axis.Z)           # edges parallel to Z axis
box.faces().filter_by(GeomType.PLANE)   # planar faces only
box.faces().filter_by(Axis.Z)           # faces whose normal is along Z

# --- filter_by_position: keep items in a position range ---
box.edges().filter_by_position(Axis.Z, 0, 15)              # edges with Z in [0, 15]
box.edges().filter_by_position(Axis.Z, 0, 15, inclusive=(False, True))

# --- sort_by: order by position along axis ---
box.faces().sort_by(Axis.Z)             # sorted low→high; [-1] = topmost
box.edges().sort_by(Axis.Z)[:4]         # 4 lowest edges

# --- group_by: cluster by position, returns list of ShapeLists ---
box.faces().group_by(Axis.Z)[-1]        # all faces at the maximum Z
box.faces().group_by(Axis.Z)[0]         # all faces at the minimum Z

# --- Operator shortcuts ---
# |   → filter_by         box.edges() | Axis.Z
# >   → sort_by (asc)     box.faces() > Axis.Z
# >>  → group_by last     box.faces() >> Axis.Z
# <<  → group_by first    box.faces() << Axis.Z
```

### Edge/Wire Operators

```python
from build123d import *

edge = Line((0, 0), (10, 10))

edge @ 0.0    # → Vector: position at start
edge @ 0.5    # → Vector: position at midpoint
edge @ 1.0    # → Vector: position at end
edge % 0.5    # → Vector: tangent direction at midpoint
edge ^ 0.0    # → Location: full location (position + orientation) at start
```

## 12. Mirror & Symmetry

```python
from build123d import *

half = Box(50, 20, 10)
half -= Pos(20, 5, 0) * Cylinder(3, 10)

# Mirror about YZ plane → full symmetric part
full = mirror(half, about=Plane.YZ) + half

# Mirror about XZ
full = mirror(half, about=Plane.XZ) + half
```

## 13. Working on Existing Faces

Build new geometry on a face of an existing part.

```python
from build123d import *

base = Box(60, 60, 10)

# Get the top face, use it as a construction plane
top = base.faces().sort_by(Axis.Z)[-1]

# Extrude a boss on the top face
boss_sketch = Plane(top) * Circle(15)
base += extrude(boss_sketch, amount=20)

# Extrude onto a side face
side = base.faces().sort_by(Axis.X)[-1]
rib_sketch = Plane(side) * Rectangle(10, 5)
base += extrude(rib_sketch, amount=3)
```

## 14. Part Composition (Multi-file)

Parts are just Python objects. Import and combine them.

```python
# file: bracket.py
from build123d import *

def make_bracket(width=40, height=30, thickness=5, hole_r=4):
    """L-shaped bracket with mounting hole."""
    # Vertical plate
    plate = Box(width, thickness, height, align=(Align.CENTER, Align.MIN, Align.MIN))
    # Base flange
    flange = Box(width, height, thickness, align=(Align.CENTER, Align.MIN, Align.MIN))
    bracket = plate + flange
    # Fillet the inner corner
    inner_edges = bracket.edges().filter_by(Axis.X).filter_by_position(
        Axis.Z, thickness * 0.9, thickness * 1.1
    )
    bracket = fillet(inner_edges, radius=thickness * 0.8)
    # Mounting hole in flange
    bracket -= Pos(0, height / 2, 0) * Cylinder(hole_r, thickness)
    return bracket

# file: assembly.py
from build123d import *
from bracket import make_bracket

base_plate = Box(200, 200, 5)
b1 = Pos(50, 0, 2.5) * make_bracket()
b2 = Pos(-50, 0, 2.5) * Rot(0, 0, 180) * make_bracket()
assembly = base_plate + b1 + b2

export_step(assembly, "assembly.step")
```

**STEP file interchange** for pre-made components:

```python
from build123d import *

motor = import_step("nema17_motor.step")
bracket = make_bracket()
assembly = bracket + Pos(0, 0, 30) * motor
```

## 15. Import & Export

```python
from build123d import *

# Export (always do this so the user can view results)
export_step(part, "output.step")     # CAD interchange (recommended)
export_stl(part, "output.stl")       # 3D printing
export_brep(part, "output.brep")     # exact OpenCascade geometry

# Import
part = import_step("part.step")      # → Compound
mesh = import_stl("mesh.stl")        # → Face (triangulated)
part = import_brep("part.brep")      # → Shape
```

## 16. Topology Quick Reference

Hierarchy: `Vertex` → `Edge` → `Wire` → `Face` → `Shell` → `Solid` → `Compound`

| Type | Dimension | What it is | Access from Part |
|------|-----------|-----------|-----------------|
| `Vertex` | 0D | Point | `part.vertices()` |
| `Edge` | 1D | Line/arc/spline segment | `part.edges()` |
| `Wire` | 1D | Connected sequence of edges | `part.wires()` |
| `Face` | 2D | Bounded surface | `part.faces()` |
| `Shell` | 2D | Connected faces | `part.shells()` |
| `Solid` | 3D | Closed watertight volume | `part.solids()` |
| `Compound` | mixed | Container of any shapes | — |

Key type aliases:
- `Part` = `Compound` containing `Solid`(s) — result of 3D operations
- `Sketch` = `Compound` containing `Face`(s) — result of 2D operations
- `Curve` = `Compound` containing `Edge`(s) — result of 1D operations
- `Rot` = `Rotation` (shorthand alias)
