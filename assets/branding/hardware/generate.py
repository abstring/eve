#!/usr/bin/env python3
"""Rebuild the original, font-independent 15 mm hardware attribution mark.
Development-only dependency: Shapely 2.x. Runtime CAD assets need no Shapely.
"""
import json
import math
from pathlib import Path
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent
parts = []
def stroke(points, width):
    parts.append(LineString(points).buffer(width / 2, quad_segs=4))
def loop(points, width):
    stroke(points + [points[0]], width)
# Original simple stroke lettering; no font files or font licensing involved.
letters = {
 'C': [[(1,0),(0,0),(0,1),(1,1)]],
 'O': [[(0,0),(1,0),(1,1),(0,1),(0,0)]],
 'D': [[(0,0),(.65,0),(1,.25),(1,.75),(.65,1),(0,1),(0,0)]],
 'E': [[(1,0),(0,0),(0,1),(1,1)],[(0,.5),(.8,.5)]],
 'S': [[(1,0),(0,0),(0,.5),(1,.5),(1,1),(0,1)]],
 'I': [[(.5,0),(.5,1)],[(0,0),(1,0)],[(0,1),(1,1)]],
 'G': [[(1,0),(0,0),(0,1),(1,1),(1,.5),(.55,.5)]],
 'N': [[(0,1),(0,0),(1,1),(1,0)]],
 'W': [[(0,0),(.2,1),(.5,.55),(.8,1),(1,0)]],
 'T': [[(0,0),(1,0)],[(.5,0),(.5,1)]],
 'H': [[(0,0),(0,1)],[(1,0),(1,1)],[(0,.5),(1,.5)]],
 'V': [[(0,0),(.5,1),(1,0)]],
 'R': [[(0,1),(0,0),(1,0),(1,.5),(0,.5)],[(.45,.5),(1,1)]],
 '-': [[(.1,.5),(.9,.5)]],
 '.': [[(.45,.95),(.55,.95)]],
}
def text(value, y, height, width, pitch, weight):
    x = (15 - ((len(value)-1)*pitch + width))/2
    for char in value:
        for line in letters[char]:
            stroke([(x+a*width,y+b*height) for a,b in line],weight)
        x += pitch
# Square perimeter has an exact 15 x 15 mm outer boundary.
loop([(.125,.125),(14.875,.125),(14.875,14.875),(.125,14.875)],.25)
# A compact E, PCB, and natural leaf motif complements the portrait logo.
loop([(7.5+3.0*math.cos(t*math.pi/40),4.45+3.0*math.sin(t*math.pi/40)) for t in range(80)],.25)
for line in letters['E']:
    stroke([(6.4+x*2.2,2.8+y*3.2) for x,y in line],.4)
loop([(9.3,5.8),(10.35,5.8),(10.35,6.85),(9.3,6.85)],.22)
stroke([(9.5,6.05),(10.1,6.05),(10.1,6.6)],.18)
stroke([(4.9,6.7),(4.0,5.8),(3.7,4.5)],.24)
parts.append(Polygon([(4.15,5.9),(3.3,5.8),(2.8,5.05),(3.7,5.05)]))
parts.append(Polygon([(3.8,5.15),(3.0,4.8),(2.8,4.05),(3.6,4.3)]))
text('CO-DESIGNED',8.65,.95,.53,.82,.16)
text('WITH',10.05,.8,.55,.82,.16)
text('EVE.ENGINEER',11.75,1.5,.78,1.12,.20)
shape=unary_union(parts)
polys=list(shape.geoms) if shape.geom_type=='MultiPolygon' else [shape]
contours=[]
for poly in polys:
    contours.append([list(p) for p in list(poly.exterior.coords)[:-1]])
    contours.extend([[list(p) for p in list(r.coords)[:-1]] for r in poly.interiors])
(ROOT/'geometry.json').write_text(json.dumps({'size_mm':15,'contours':contours},indent=2)+'\n')
path=' '.join('M '+' L '.join(f'{x:.5f},{y:.5f}' for x,y in c)+' Z' for c in contours)
(ROOT/'eve-co-designed-15mm.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="15mm" height="15mm" viewBox="0 0 15 15"><title>Co-designed with eve.engineer — 15 mm attribution mark</title><path fill="#193E2C" fill-rule="evenodd" d="{path}"/></svg>\n')
# Fracture polygons with holes into solid pieces for KiCad's filled fp_poly.
from shapely.ops import triangulate
faces=[]
for poly in polys:
    if poly.interiors:
        for triangle in triangulate(poly):
            clipped = triangle.intersection(poly)
            if clipped.geom_type == "Polygon" and clipped.area > 1e-10:
                faces.append(clipped)
            elif clipped.geom_type in ("MultiPolygon", "GeometryCollection"):
                faces.extend(p for p in clipped.geoms if p.geom_type == "Polygon" and p.area > 1e-10)
    else:
        faces.append(poly)
assert all(not face.interiors for face in faces)
lines=['(footprint "Eve_CoDesigned_15mm" (version 20240108) (generator "eve_hardware_mark")',
 '  (layer "F.Cu")', '  (descr "Optional co-designed with eve.engineer attribution; 15 x 15 mm; silkscreen only")',
 '  (attr board_only exclude_from_pos_files exclude_from_bom)',
 '  (fp_text reference "REF**" (at 0 -8.5) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15))))',
 '  (fp_text value "Eve_CoDesigned_15mm" (at 0 8.5) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15))))']
for face in faces:
    pts=' '.join(f'(xy {x-7.5:.5f} {y-7.5:.5f})' for x,y in list(face.exterior.coords)[:-1])
    lines.append(f'  (fp_poly (pts {pts}) (stroke (width 0) (type solid)) (fill solid) (layer "F.SilkS"))')
lines.append(')')
(ROOT/'kicad/Eve.pretty/Eve_CoDesigned_15mm.kicad_mod').write_text('\n'.join(lines)+'\n')
assert shape.is_valid and shape.bounds == (0,0,15,15)
assert abs(unary_union(faces).area-shape.area)<1e-8
print(f'Created {len(contours)} closed contours; exact 15 mm square; minimum lettering stroke 0.16 mm.')
