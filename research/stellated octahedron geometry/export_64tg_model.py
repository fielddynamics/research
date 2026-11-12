"""Export the 64-Tetrahedron Grid as a 3D model (Wavefront OBJ + MTL) from the same exact geometry as
verify_64_tetrahedron_grid.py. Opens in Blender, FreeCAD, MeshLab, GeoGebra 3D (import), Windows 3D Viewer, etc.

Units: small-cube edge 1 (whole block = 2 x 2 x 2, Field Origin at (1,1,1)); small tetrahedra have edge sqrt2/2 = a/2.
Objects (one per OBJ group, so each can be hidden or recoloured on its own):
  A0_outward_8      spikes tipped at the 8 points of the large star          (d(star, spike) = 0)
  A1_vector_24      spikes tipped at the 12 cuboctahedron (VE) vertices      (d = 1)  outside the large star
  A2_within_24      spikes tipped at the 6 core-octahedron vertices          (d = 2)
  A3_origin_8       spikes tipped at the Field Origin                        (d = 3)
  octa_cores_8      the 8 star cores (octahedral cavities at small-cube centres)
  octa_central_6    the 6 cavities around the Field Origin
  large_star_ref    reference outline: the large stellated octahedron (2a), two tetrahedra
Also writes 64tg_geogebra.txt: one GeoGebra command (Execute) that draws all 64 tetrahedra and 14 octahedra in GeoGebra 3D.
Run: python3 export_64tg_model.py   ->  64tg.obj, 64tg.mtl, 64tg_geogebra.txt
"""
import itertools
from fractions import Fraction as Fr

bits = list(itertools.product((0, 1), repeat=3))
d = lambda c, f: sum(ci != fi for ci, fi in zip(c, f))


def face_centre(c, k, s):
    p = [Fr(ci) + Fr(1, 2) for ci in c]; p[k] = Fr(c[k] + s); return tuple(p)


def spike(c, f):
    return [tuple(Fr(ci + fi) for ci, fi in zip(c, f))] + [face_centre(c, k, f[k]) for k in range(3)]


def octa(cen, r=Fr(1, 2)):
    return [tuple(cen[i] + (r * s if i == k else 0) for i in range(3)) for k in range(3) for s in (1, -1)]


def tet_faces(vs):
    return [tuple(t) for t in itertools.combinations(range(4), 3)]


def oct_faces(vs):
    # vertices ordered +x,-x,+y,-y,+z,-z ; faces = one of each axis pair
    return [(a, b, c) for a in (0, 1) for b in (2, 3) for c in (4, 5)]


groups = {"A0_outward_8": [], "A1_vector_24": [], "A2_within_24": [], "A3_origin_8": []}
names = list(groups)
for c in bits:
    for f in bits:
        groups[names[d(c, f)]].append((spike(c, f), tet_faces))
groups["octa_cores_8"] = [(octa(tuple(Fr(ci) + Fr(1, 2) for ci in c)), oct_faces) for c in bits]
groups["octa_central_6"] = [(octa(tuple(Fr(1) + (Fr(s, 2) if i == k else 0) for i in range(3))), oct_faces)
                            for k in range(3) for s in (1, -1)]
big = [p for p in itertools.product((0, 2), repeat=3)]
groups["large_star_ref"] = [([tuple(map(Fr, p)) for p in big if sum(p) % 4 == 0], tet_faces),
                            ([tuple(map(Fr, p)) for p in big if sum(p) % 4 == 2], tet_faces)]

colours = {"A0_outward_8": (0.85, 0.36, 0.20), "A1_vector_24": (0.93, 0.70, 0.22), "A2_within_24": (0.22, 0.56, 0.78),
           "A3_origin_8": (0.48, 0.30, 0.72), "octa_cores_8": (0.55, 0.60, 0.62), "octa_central_6": (0.30, 0.70, 0.55),
           "large_star_ref": (0.9, 0.9, 0.9)}

with open("64tg.mtl", "w") as m:
    for g, (r, gg, b) in colours.items():
        m.write(f"newmtl {g}\nKd {r:.3f} {gg:.3f} {b:.3f}\nd {0.25 if g == 'large_star_ref' else 1.0}\n\n")

with open("64tg.obj", "w") as o:
    o.write("# 64-Tetrahedron Grid (Galeffi) - exact model from verify_64_tetrahedron_grid.py; small-cube edge = 1\nmtllib 64tg.mtl\n")
    n = 0
    for g, solids in groups.items():
        o.write(f"\ng {g}\nusemtl {g}\n")
        for vs, facefn in solids:
            cen = [sum(v[i] for v in vs) / len(vs) for i in range(3)]
            for v in vs:
                o.write("v " + " ".join(f"{float(x):.6f}" for x in v) + "\n")
            for t in facefn(vs):
                a, b, c = (vs[i] for i in t)
                nrm = [(b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1]), (b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]),
                       (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])]
                out = sum(nrm[i] * (a[i] - cen[i]) for i in range(3)) > 0       # orient every face outward
                idx = [n + i + 1 for i in (t if out else (t[0], t[2], t[1]))]
                o.write("f " + " ".join(map(str, idx)) + "\n")
            n += len(vs)
print("wrote 64tg.obj, 64tg.mtl:", {g: len(s) for g, s in groups.items()})

# GeoGebra 3D: paste the single line into the Input bar of https://www.geogebra.org/3d
pt = lambda v: "(" + ",".join(f"{float(x):g}" for x in v) + ")"
cmds = []
for g, solids in groups.items():
    if g == "large_star_ref":
        continue
    tag = {"A0_outward_8": "A0", "A1_vector_24": "A1", "A2_within_24": "A2", "A3_origin_8": "A3",
           "octa_cores_8": "core", "octa_central_6": "cen"}[g]
    r, gg, b = colours[g]
    for i, (vs, _) in enumerate(solids):
        name = f"{tag}_{i + 1}"
        if len(vs) == 4:
            cmds.append(f"{name}=Pyramid({pt(vs[1])},{pt(vs[2])},{pt(vs[3])},{pt(vs[0])})")
        else:
            eq = ",".join(pt(vs[j]) for j in (0, 2, 1, 3))          # square equator +x, +y, -x, -y; apexes +z, -z
            cmds += [f"{name}a=Pyramid({eq},{pt(vs[4])})", f"{name}b=Pyramid({eq},{pt(vs[5])})",
                     f"SetColor({name}a,{r},{gg},{b})", f"SetColor({name}b,{r},{gg},{b})"]
            continue
        cmds.append(f"SetColor({name},{r},{gg},{b})")
with open("64tg_geogebra.txt", "w") as o:
    o.write("Execute({" + ",".join('"' + c + '"' for c in cmds) + "})\n")
print("wrote 64tg_geogebra.txt:", sum(c.startswith(("A", "core", "cen")) and "=" in c for c in cmds), "GeoGebra objects")
