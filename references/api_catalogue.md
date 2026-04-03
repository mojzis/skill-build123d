# build123d API Reference (Focused Subset)

Algebra-mode API surface for CAD modeling. Signatures extracted from source.


## 3D Primitives

### `Box`

```python
Box(length: float, width: float, height: float, rotation: RotationLike = (0, 0, 0), align: Align | tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Box  Create a box defined by length, width, and height.


### `Cone`

```python
Cone(bottom_radius: float, top_radius: float, height: float, arc_size: float = 360, rotation: RotationLike = (0, 0, 0), align: Align | tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Cone  Create a cone defined by bottom radius, top radius, and height.


### `CounterBoreHole`

```python
CounterBoreHole(radius: float, counter_bore_radius: float, counter_bore_depth: float, depth: float | None = None, mode: Mode = Mode.SUBTRACT)
```

Counter Bore Hole  Create a counter bore hole defined by radius, counter bore radius, counter bore and depth.


### `CounterSinkHole`

```python
CounterSinkHole(radius: float, counter_sink_radius: float, depth: float | None = None, counter_sink_angle: float = 82, mode: Mode = Mode.SUBTRACT)
```

Counter Sink Hole  Create a countersink hole defined by radius, countersink radius, countersink angle, and depth.


### `Cylinder`

```python
Cylinder(radius: float, height: float, arc_size: float = 360, rotation: RotationLike = (0, 0, 0), align: Align | tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Cylinder  Create a cylinder defined by radius and height.


### `Hole`

```python
Hole(radius: float, depth: float | None = None, mode: Mode = Mode.SUBTRACT)
```

Hole  Create a hole defined by radius and depth.


### `Sphere`

```python
Sphere(radius: float, arc_size1: float = -90, arc_size2: float = 90, arc_size3: float = 360, rotation: RotationLike = (0, 0, 0), align: Align | tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Sphere  Create a sphere defined by a radius.


### `Torus`

```python
Torus(major_radius: float, minor_radius: float, minor_start_angle: float = 0, minor_end_angle: float = 360, major_angle: float = 360, rotation: RotationLike = (0, 0, 0), align: Align | tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Torus  Create a torus defined by major and minor radii.


### `Wedge`

```python
Wedge(xsize: float, ysize: float, zsize: float, xmin: float, zmin: float, xmax: float, zmax: float, rotation: RotationLike = (0, 0, 0), align: Align | tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Wedge  Create a wedge with a near face defined by xsize and z size, a far face defined by xmin to xmax and zmin to zmax, and a depth of ysize.



## 2D Sketch Objects

### `Circle`

```python
Circle(radius: float, arc_size: float = 360.0, align: Align | tuple[Align, Align] | None = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Circle  Create a circle defined by radius.


### `Ellipse`

```python
Ellipse(x_radius: float, y_radius: float, rotation: float = 0, align: Align | tuple[Align, Align] | None = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Ellipse  Create an ellipse defined by x- and y- radii.


### `Polygon`

```python
Polygon(*pts: VectorLike | Iterable[VectorLike], rotation: float = 0, align: Align | tuple[Align, Align] | None = (Align.NONE, Align.NONE), mode: Mode = Mode.ADD)
```

Polygon  Create a polygon defined by given sequence of points.


### `Rectangle`

```python
Rectangle(width: float, height: float, rotation: float = 0, align: Align | tuple[Align, Align] | None = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Rectangle  Create a rectangle defined by width and height.


### `RectangleRounded`

```python
RectangleRounded(width: float, height: float, radius: float, rotation: float = 0, align: Align | tuple[Align, Align] | None = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Rectangle Rounded  Create a rectangle defined by width and height with filleted corners.


### `RegularPolygon`

```python
RegularPolygon(radius: float, side_count: int, major_radius: bool = True, rotation: float = 0, align: tuple[Align, Align] = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Regular Polygon  Create a regular polygon defined by radius and side count. Use major_radius to define whether the polygon circumscribes (along the vertices) or inscribes (along the sides) the radius circle.


### `SlotArc`

```python
SlotArc(arc: Edge | Wire, height: float, rotation: float = 0, mode: Mode = Mode.ADD)
```

Slot Arc  Create a slot defined by a line and height. May be an arc, stright line, spline, etc.


### `SlotCenterPoint`

```python
SlotCenterPoint(center: VectorLike, point: VectorLike, height: float, rotation: float = 0, mode: Mode = Mode.ADD)
```

Slot Center Point  Create a slot defined by the center of the slot and the center of one end arc. The slot will be symmetric about the center point.


### `SlotCenterToCenter`

```python
SlotCenterToCenter(center_separation: float, height: float, rotation: float = 0, mode: Mode = Mode.ADD)
```

Slot Center To Center  Create a slot defined by the distance between the centers of the two end arcs.


### `SlotOverall`

```python
SlotOverall(width: float, height: float, rotation: float = 0, align: Align | tuple[Align, Align] | None = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Slot Overall  Create a slot defined by the overall width and height.


### `Text`

```python
Text(txt: str, font_size: float, font: str = 'Arial', font_path: PathLike[str] | str | None = None, font_style: FontStyle = FontStyle.REGULAR, text_align: tuple[TextAlign, TextAlign] = (TextAlign.CENTER, TextAlign.CENTER), align: Align | tuple[Align, Align] | None = None, path: Edge | Wire | None = None, position_on_path: float = 0.0, single_line_width: float | None = None, rotation: float = 0.0, mode: Mode = Mode.ADD)
```

Text  Create text defined by text string and font size.  Fonts installed to the system can be specified by name and FontStyle. Fonts with subfamilies not in FontStyle should be specified with the subfamily name, e.g. "Arial Black". Alternatively, ...


### `Trapezoid`

```python
Trapezoid(width: float, height: float, left_side_angle: float, right_side_angle: float | None = None, rotation: float = 0, align: Align | tuple[Align, Align] | None = (Align.CENTER, Align.CENTER), mode: Mode = Mode.ADD)
```

Trapezoid  Create a trapezoid defined by major width, height, and interior angle(s).


### `Triangle`

```python
Triangle(a: float | None = None, b: float | None = None, c: float | None = None, A: float | None = None, B: float | None = None, C: float | None = None, align: Align | tuple[Align, Align] | None = None, rotation: float = 0, mode: Mode = Mode.ADD)
```

Triangle  Create a triangle defined by one side length and any of two other side lengths or interior angles. The interior angles are opposite the side with the same designation (i.e. side 'a' is opposite angle 'A'). Side 'a' is the bottom side, fo...



## 1D Curve Objects

### `Bezier`

```python
Bezier(*cntl_pnts: VectorLike, weights: list[float] | None = None, mode: Mode = Mode.ADD)
```

Line Object: Bezier Curve  Create a non-rational bezier curve defined by a sequence of points and include optional weights to create a rational bezier curve. The number of weights must match the number of control points.


### `CenterArc`

```python
CenterArc(center: VectorLike, radius: float, start_angle: float, arc_size: float | Shape | Axis | Location | Plane | VectorLike, mode: Mode = Mode.ADD)
```

Line Object: Center Arc  Create a circular arc defined by a center point and radius.


### `Helix`

```python
Helix(pitch: float, height: float, radius: float, center: VectorLike = (0, 0, 0), direction: VectorLike = (0, 0, 1), cone_angle: float = 0, lefthand: bool = False, mode: Mode = Mode.ADD)
```

Line Object: Helix  Create a helix defined by pitch, height, and radius. The helix may have a taper defined by cone_angle.  If cone_angle is not 0, radius is the initial helix radius at center. cone_angle > 0 increases the final radius. cone_angle...


### `FilletPolyline`

```python
FilletPolyline(*pts: VectorLike | Iterable[VectorLike], radius: float | Iterable[float], close: bool = False, mode: Mode = Mode.ADD)
```

Line Object: Fillet Polyline Create a sequence of straight lines defined by successive points that are filleted to a given radius.


### `Line`

```python
Line(*pts: VectorLike | Iterable[VectorLike], mode: Mode = Mode.ADD)
```

Line Object: Line  Create a straight line defined by two points.


### `PolarLine`

```python
PolarLine(start: VectorLike, length: float | Shape | Axis | Location | Plane | VectorLike, angle: float | None = None, direction: VectorLike | None = None, length_mode: LengthMode = LengthMode.DIAGONAL, mode: Mode = Mode.ADD)
```

Line Object: Polar Line  Create a straight line defined by a start point, length, and angle. The length can specify the DIAGONAL, HORIZONTAL, or VERTICAL component of the triangle defined by the angle.  Alternatively, the length parameter can cont...


### `Polyline`

```python
Polyline(*pts: VectorLike | Iterable[VectorLike], close: bool = False, mode: Mode = Mode.ADD)
```

Line Object: Polyline  Create a sequence of straight lines defined by successive points.


### `RadiusArc`

```python
RadiusArc(start_point: VectorLike, end_point: VectorLike, radius: float, short_sagitta: bool = True, mode: Mode = Mode.ADD)
```

Line Object: Radius Arc  Create a circular arc defined by two points and a radius.


### `SagittaArc`

```python
SagittaArc(start_point: VectorLike, end_point: VectorLike, sagitta: float, mode: Mode = Mode.ADD)
```

Line Object: Sagitta Arc  Create a circular arc defined by two points and the sagitta (height of the arc from chord).


### `Spline`

```python
Spline(*pts: VectorLike | Iterable[VectorLike], tangents: Iterable[VectorLike] | None = None, tangent_scalars: Iterable[float] | None = None, periodic: bool = False, mode: Mode = Mode.ADD)
```

Line Object: Spline  Create a spline defined by a sequence of points, optionally constrained by tangents. Tangents and tangent scalars must have length of 2 for only the end points or a length of the number of points.


### `TangentArc`

```python
TangentArc(*pts: VectorLike | Iterable[VectorLike], tangent: VectorLike, tangent_from_first: bool = True, mode: Mode = Mode.ADD)
```

Line Object: Tangent Arc  Create a circular arc defined by two points and a tangent.


### `ThreePointArc`

```python
ThreePointArc(*pts: VectorLike | Iterable[VectorLike], mode: Mode = Mode.ADD)
```

Line Object: Three Point Arc  Create a circular arc defined by three points.



## Operations

### `extrude()` → Part

```python
extrude(to_extrude: Face | Sketch | None = None, amount: float | None = None, dir: VectorLike | None = None, until: Until | None = None, target: Compound | Solid | None = None, both: bool = False, taper: float = 0.0, clean: bool = True, mode: Mode = Mode.ADD)
```

extrude  Extrude a sketch or face by an amount or until another object.


### `loft()` → Part

```python
loft(sections: Face | Sketch | Iterable[Vertex | Face | Sketch] | None = None, ruled: bool = False, clean: bool = True, mode: Mode = Mode.ADD)
```

loft  Loft the pending sketches/faces, across all workplanes, into a solid.


### `revolve()` → Part

```python
revolve(profiles: Face | Iterable[Face] | None = None, axis: Axis = Axis.Z, revolution_arc: float = 360.0, clean: bool = True, mode: Mode = Mode.ADD)
```

Revolve  Revolve the profile or pending sketches/face about the given axis. Note that the most common use case is when the axis is in the same plane as the face to be revolved but this isn't required.


### `section()` → Sketch

```python
section(obj: Part | None = None, section_by: Plane | Iterable[Plane] = Plane.XZ, height: float = 0.0, clean: bool = True, mode: Mode = Mode.PRIVATE)
```

section  Slices current part at the given height by section_by or current workplane(s).


### `thicken()` → Part

```python
thicken(to_thicken: Face | Sketch | None = None, amount: float | None = None, normal_override: VectorLike | None = None, both: bool = False, clean: bool = True, mode: Mode = Mode.ADD)
```

thicken  Create a solid(s) from a potentially non planar face(s) by thickening along the normals.


### `make_face()` → Sketch

```python
make_face(edges: Edge | Iterable[Edge] | None = None, mode: Mode = Mode.ADD)
```

Sketch Operation: make_face  Create a face from the given perimeter edges.


### `make_hull()` → Sketch

```python
make_hull(edges: Edge | Iterable[Edge] | None = None, mode: Mode = Mode.ADD)
```

Sketch Operation: make_hull  Create a face from the convex hull of the given edges


### `add()` → Compound

```python
add(objects: AddType | Iterable[AddType], rotation: float | RotationLike | None = None, clean: bool = True, mode: Mode = Mode.ADD)
```

Generic Object: Add Object to Part or Sketch  Add an object to a builder.  BuildPart: Edges and Wires are added to pending_edges. Compounds of Face are added to pending_faces. Solids or Compounds of Solid are combined into the part. BuildSketch: E...


### `chamfer()` → Sketch | Part

```python
chamfer(objects: ChamferFilletType | Iterable[ChamferFilletType], length: float, length2: float | None = None, angle: float | None = None, reference: Edge | Face | None = None)
```

Generic Operation: chamfer  Applies to 2 and 3 dimensional objects.  Chamfer the given sequence of edges or vertices.


### `fillet()` → Sketch | Part | Curve

```python
fillet(objects: ChamferFilletType | Iterable[ChamferFilletType], radius: float)
```

Generic Operation: fillet  Applies to 2 and 3 dimensional objects.  Fillet the given sequence of edges or vertices. Note that vertices on either end of an open line will be automatically skipped.


### `mirror()` → Curve | Sketch | Part | Compound

```python
mirror(objects: MirrorType | Iterable[MirrorType] | None = None, about: Plane = Plane.XZ, mode: Mode = Mode.ADD)
```

Generic Operation: mirror  Applies to 1, 2, and 3 dimensional objects.  Mirror a sequence of objects over the given plane.


### `offset()` → Curve | Sketch | Part | Compound

```python
offset(objects: OffsetType | Iterable[OffsetType] | None = None, amount: float = 0, openings: Face | list[Face] | None = None, kind: Kind = Kind.ARC, side: Side = Side.BOTH, closed: bool = True, min_edge_length: float | None = None, mode: Mode = Mode.REPLACE)
```

Generic Operation: offset  Applies to 1, 2, and 3 dimensional objects.  Offset the given sequence of Edges, Faces, Compound of Faces, or Solids. The kind parameter controls the shape of the transitions. For Solid objects, the openings parameter al...


### `scale()` → Curve | Sketch | Part | Compound

```python
scale(objects: Shape | Iterable[Shape] | None = None, by: float | tuple[float, float, float] = 1, mode: Mode = Mode.REPLACE)
```

Generic Operation: scale  Applies to 1, 2, and 3 dimensional objects.  Scale a sequence of objects. Note that when scaling non-uniformly across the three axes, the type of the underlying object may change to bspline from line, circle, etc.


### `split()`

```python
split(objects: SplitType | Iterable[SplitType] | None = None, bisect_by: Plane | Face | Shell = Plane.XZ, keep: Keep = Keep.TOP, mode: Mode = Mode.REPLACE)
```

Generic Operation: split  Applies to 1, 2, and 3 dimensional objects.  Bisect object with plane and keep either top, bottom or both.


### `sweep()` → Part | Sketch

```python
sweep(sections: SweepType | Iterable[SweepType] | None = None, path: Curve | Edge | Wire | Iterable[Edge] | None = None, multisection: bool = False, is_frenet: bool = False, transition: Transition = Transition.TRANSFORMED, normal: VectorLike | None = None, binormal: Edge | Wire | None = None, clean: bool = True, mode: Mode = Mode.ADD)
```

Generic Operation: sweep  Sweep pending 1D or 2D objects along path.



## Geometry & Positioning

### `Vector`

```python
Vector(X: float, Y: float, Z: float)
```

Create a 3-dimensional vector


### `Axis`

```python
Axis(gp_ax1: gp_Ax1)
```

Axis  Axis defined by point and direction


### `BoundBox`

```python
BoundBox(bounding_box: Bnd_Box)
```

A BoundingBox for a Shape


### `Location`

Location in 3D space. Depending on usage can be absolute or relative.  This class wraps the TopLoc_Location class from OCCT. It can be used to move Shape objects in both relative and absolute manner. It is the preferred type to locate objects in b...


### `Rotation`

```python
Rotation(rotation: RotationLike, ordering: Extrinsic | Intrinsic == Intrinsic.XYZ)
```

Subclass of Location used only for object rotation  Attributes: X (float): rotation in degrees about X axis Y (float): rotation in degrees about Y axis Z (float): rotation in degrees about Z axis optionally specify rotation ordering with Intrinsic...


### `Pos`

```python
Pos(v: VectorLike)
```

A position only sub-class of Location


### `Plane`

```python
Plane(gp_pln: gp_Pln)
```

Plane  A plane is positioned in space with a coordinate system such that the plane is defined by the origin, x_dir (X direction), y_dir (Y direction), and z_dir (Z direction) of this coordinate system, which is the "local coordinate system" of the...



## Enums

### `Align`

Align object about Axis


### `GeomType`

CAD geometry object type


### `Keep`

Split options


### `Kind`

Offset corner transition


### `Mode`

Combination Mode


### `FontStyle`

Text Font Styles


### `Side`

2D Offset types


### `SortBy`

Sorting criteria


### `Transition`

Sweep discontinuity handling option


### `Unit`

Standard Units


### `Until`

Extrude limit



## Import / Export

### `import_brep()` → Shape

```python
import_brep(file_name: PathLike | str | bytes)
```

Import shape from a BREP file


### `import_step()` → Compound

```python
import_step(filename: PathLike | str | bytes)
```

import_step  Extract shapes from a STEP file and return them as a Compound object.


### `import_stl()` → Face

```python
import_stl(file_name: PathLike | str | bytes, model_unit: Unit = Unit.MM)
```

import_stl  Extract shape from an STL file and return it as a Face reference object.  Note that importing with this method and creating a reference is very fast while creating an editable model (with Mesher) may take minutes depending on the size ...


### `import_svg()` → ShapeList[Wire | Face]

```python
import_svg(svg_file: str | Path | TextIO, flip_y: bool = True, align: Align | tuple[Align, Align] | None = Align.MIN, ignore_visibility: bool = False, label_by: Literal['id', 'class', 'inkscape:label'] | str = 'id', is_inkscape_label: bool | None = None)
```

import_svg


### `export_brep()` → bool

```python
export_brep(to_export: Shape, file_path: PathLike | str | bytes | BytesIO | BinaryIO)
```

Export this shape to a BREP file


### `export_gltf()` → bool

```python
export_gltf(to_export: Shape, file_path: PathLike | str | bytes, unit: Unit = Unit.MM, binary: bool = False, linear_deflection: float = 0.001, angular_deflection: float = 0.1)
```

export_gltf  The glTF (GL Transmission Format) specification primarily focuses on the efficient transmission and loading of 3D models as a compact, binary format that is directly renderable by graphics APIs like WebGL, OpenGL, and Vulkan. It's des...


### `export_step()` → bool

```python
export_step(to_export: Shape, file_path: PathLike | str | bytes | BytesIO | BinaryIO, unit: Unit = Unit.MM, write_pcurves: bool = True, precision_mode: PrecisionMode = PrecisionMode.AVERAGE, timestamp: str | datetime | None = None)
```

export_step  Export a build123d Shape or assembly with color and label attributes. Note that if the color of a node in an assembly isn't set, it will be assigned the color of its nearest ancestor.


### `export_stl()` → bool

```python
export_stl(to_export: Shape, file_path: PathLike | str | bytes, tolerance: float = 0.001, angular_tolerance: float = 0.1, ascii_format: bool = False)
```

Export STL  Exports a shape to a specified STL file.


