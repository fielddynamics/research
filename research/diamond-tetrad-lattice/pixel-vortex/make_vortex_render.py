"""Particle render of the pixel's vortices, in the style of research/universe-is-pixelated/convergent_vortex.png.

What comes from the proofs (computed here from the same models):
 - the axes: the 8 legs (Triforce vortices, triforce-vortex/PROOF.md) and the octahedron axis z
   (core vortex, pixel-vortex/PROOF.md);
 - empty cores: no particle is placed on an axis (the proven zero-amplitude line);
 - the swirl sense at each end of a leg, and the relative swirl strength of the TetA and TetB ends,
   from the bond currents of an exact vortex eigenstate of the 33-tile model;
 - the core: the octahedron's equatorial ring turning, locked to the corner strands (TetA, TetB),
   which zigzag above and below the equator as the rotoreflection requires.
What is drawn for display only (not fixed by the proofs): the funnel shapes, the particle density,
and the direction of the through-flow along an axis (drawn TetA -> Field Origin -> TetB).
Run: python make_vortex_render.py
"""
import contextlib
import io
import os
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb

HERE = os.path.dirname(os.path.abspath(__file__))
BG, WIRE = "#000000", "#2aa8a0"
BLUE, ORANGE, YELLOW, AQUA = "#3987e5", "#e8743f", "#f2c230", "#2fd3a0"
rng = np.random.default_rng(2026)


def run_setup(path, stop_marker):
    src = open(path).read().split(stop_marker)[0]
    ns = {"__name__": "setup"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, path, "exec"), ns)
    return ns


# ---- swirl sense and strength at the two ends of a leg, from the 33-tile model ----
T = run_setup(os.path.join(HERE, "..", "triforce-vortex", "verify_triforce_vortex.py"), "# Theorem: stationary vortices")
tsyms = list(T["site_orb"].values()) + list(T["bond_orb"].values())
r5 = np.random.default_rng(5)
tvals = r5.normal(size=len(tsyms)) * 0.4 + np.where(np.arange(len(tsyms)) < len(T["site_orb"]), 0.0, 1.0)
Ht = np.array(T["H"].subs(dict(zip(tsyms, tvals))).evalf(), dtype=float)
Pw = np.array(T["Pw"].evalf(), dtype=complex)
U, _, _ = np.linalg.svd(Pw); Bw = U[:, :10]
Et, Wt = np.linalg.eigh(Bw.conj().T @ Ht @ Bw)
nt, starA = T["n"], T["starA"]
keyB = T["key"](-T["TA"][0])
starB = [q for q in range(nt) if T["sites"][q][0] == "outer" and keyB in T["sites"][q][2]]
tpos = [np.array([float(c) for c in v]) for v in T["cent"]]
m = int(np.argmax([np.linalg.norm((Bw @ Wt[:, q])[starA]) for q in range(10)]))
psi = Bw @ Wt[:, m]
nleg = np.ones(3) / np.sqrt(3)
def circ(ring):
    tot = 0.0
    for a in ring:
        for b in ring:
            if a < b and Ht[a, b] != 0:
                J = 2 * np.imag(np.conj(psi[b]) * Ht[b, a] * psi[a])     # physical flow a -> b (i dpsi/dt = H psi)
                tot += J * np.dot(np.cross(tpos[a], tpos[b]), nleg)
    return tot
cA, cB = circ(starA), circ(starB)
# sense about each end's own outward axis (TetA end points along +n, TetB end along -n)
senseA, senseB = np.sign(cA), -np.sign(cB)
strengthB = abs(cB) / abs(cA)
print(f"leg (1,1,1): circulation TetA end {cA:+.4f}, TetB end {cB:+.4f}; "
      f"about their own outward axes: TetA {senseA:+.0f}, TetB {senseB:+.0f}; TetB/TetA strength {strengthB:.3f}")

# ---- the 15-site pixel: sense of the core-ring rotation about z ----
P = run_setup(os.path.join(HERE, "verify_pixel_vortex.py"), "# --- Theorem 2")
syms = [P["D"], P["Df"], P["eA"], P["eB"], P["tf"], P["tA"], P["tB"], P["cA"], P["cB"]]
vals = [0.0, 0.4, -0.5, 0.7, 1.0, 1.0, 0.8, 1.0, 0.7]
Hn = np.array(P["H"].subs(dict(zip(syms, vals))).evalf(), dtype=float)
B = np.array(P["B"].evalf(), dtype=complex)
E, W = np.linalg.eigh(B.conj().T @ Hn @ B)
k = int(np.argmax([abs(W[0, q]) for q in range(3)]))
ps = B @ W[:, k]
sites = [np.array(s, float) for s in P["sites"]]
Lz = sum(2 * np.imag(np.conj(ps[j]) * Hn[j, i] * ps[i]) * np.cross(sites[i], sites[j])[2]   # flow i -> j
         for i in range(len(ps)) for j in range(i + 1, len(ps)) if Hn[i, j] != 0)
sense_core = np.sign(Lz)
print(f"core vortex about z: L = {Lz:+.4f}, sense {sense_core:+.0f}")


# ---- particle generators ----
def basis(axis):
    a = axis / np.linalg.norm(axis)
    t = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(a, t); e1 /= np.linalg.norm(e1)
    return a, e1, np.cross(a, e1)


def funnel(axis, length, sense, strength=1.0, n_lines=260, pts=140, r_throat=0.035, r_mouth=0.42, twist=3.6, ax=None, col=None):
    """Particles along log-spiral streamlines of a funnel from the Field Origin out along `axis`.
    Swirl sense about the outward axis = sense; the core line (radius < r_throat) is left empty."""
    a, e1, e2 = basis(axis)
    s = np.linspace(0.06, 1.0, pts)
    out, frac = [], []
    for _ in range(n_lines):
        phi0 = rng.uniform(0, 2 * np.pi)
        rad = r_throat + (r_mouth * rng.uniform(0.55, 1.0) - r_throat) * s ** 1.7
        phi = phi0 + sense * twist * strength * np.log(s)          # tighter winding toward the throat
        jitter = rng.normal(scale=0.008, size=(pts, 3))
        p = (s * length)[:, None] * a + (rad * np.cos(phi))[:, None] * e1 + (rad * np.sin(phi))[:, None] * e2 + jitter
        out.append(p); frac.append(s)
    if ax is not None:                                              # a few bright streamlines show the spiral
        for phi0 in np.linspace(0, 2 * np.pi, 7)[:-1]:
            rad = r_throat + (r_mouth * 0.85 - r_throat) * s ** 1.7
            phi = phi0 + sense * twist * strength * np.log(s)
            q = (s * length)[:, None] * a + (rad * np.cos(phi))[:, None] * e1 + (rad * np.sin(phi))[:, None] * e2
            for i in range(len(s) - 1):
                ax.plot(*q[i:i + 2].T, color=cmap_for(col)(s[i]), lw=0.7, alpha=0.9)
    return np.vstack(out), np.concatenate(frac)


def core_ring(sense, n_lines=420, pts=160, R=0.62, width=0.11):
    """The octahedron's equatorial ring turning about z: a swirling torus of particles, empty on the axis."""
    out, frac = [], []
    for _ in range(n_lines):
        r0 = R + rng.normal(scale=width * 0.5)
        z0 = rng.normal(scale=width * 0.45)
        phi0 = rng.uniform(0, 2 * np.pi)
        t = np.linspace(0, 1, pts)
        phi = phi0 + sense * 2.2 * t
        wob = 0.05 * np.sin(4 * phi)                               # fourfold modulation (the ring's 4 vertices)
        p = np.c_[(r0 + wob) * np.cos(phi), (r0 + wob) * np.sin(phi), z0 + 0.03 * np.sin(2 * phi)]
        out.append(p); frac.append(t)
    return np.vstack(out), np.concatenate(frac)


def corner_strand(chamber, sense, n_lines=90, pts=220):
    """The corner flywheel: each chamber's strand zigzags above and below the equator (rotoreflection)."""
    out, frac = [], []
    base = np.pi / 4 if chamber == "A" else -np.pi / 4
    for _ in range(n_lines):
        t = np.linspace(0, 1, pts)
        phi = base + sense * 2 * np.pi * t + rng.normal(scale=0.02)
        Rr = np.sqrt(2) * 0.93 + rng.normal(scale=0.07)
        zz = 0.93 * np.cos(2 * (phi - base)) * (1 if chamber == "A" else -1) + rng.normal(scale=0.06) + rng.normal(scale=0.02, size=pts)
        out.append(np.c_[Rr * np.cos(phi), Rr * np.sin(phi), zz]); frac.append(t)
    return np.vstack(out), np.concatenate(frac)


def cmap_for(col):
    return LinearSegmentedColormap.from_list("c", [(0, "#ffffff"), (0.45, "#dff3ff"), (1, col)])


def draw_points(ax, P_, f, col, size=0.35, alpha=0.55):
    c = cmap_for(col)(np.clip(f, 0, 1))
    ax.scatter(P_[:, 0], P_[:, 1], P_[:, 2], s=size, c=c, alpha=alpha, linewidths=0, depthshade=False)


def wire(ax, lw=0.7):
    TA = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
    for Tt in (TA, -TA):
        for i in range(4):
            for j in range(i + 1, 4):
                ax.plot(*zip(Tt[i], Tt[j]), color=WIRE, lw=lw, alpha=0.75)
    O = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)
    for i in range(6):
        for j in range(i + 1, 6):
            if abs(O[i] @ O[j]) < 1e-9:
                ax.plot(*zip(O[i], O[j]), color=WIRE, lw=lw * 0.8, alpha=0.55)


def finish(ax, elev, azim, title):
    ax.set_facecolor(BG)
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1, 1, 1))
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-1.15, 1.15)
    ax.set_axis_off()
    ax.set_title(title, color="#e6e6e6", fontsize=10.5, loc="left", pad=2)


TAc = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
fig = plt.figure(figsize=(16, 6.0), dpi=170, facecolor=BG)

# panel 1: the eight leg (Triforce) vortices converging on the Field Origin
ax = fig.add_subplot(1, 3, 1, projection="3d")
for v in TAc:
    Pp, f = funnel(v, np.sqrt(3) * 0.97, senseA, 1.0, ax=ax, col=BLUE)
    draw_points(ax, Pp, f, BLUE)
    Pp, f = funnel(-v, np.sqrt(3) * 0.97, senseB, max(strengthB, 0.25), n_lines=150, ax=ax, col=ORANGE)
    draw_points(ax, Pp, f, ORANGE, alpha=0.45)
wire(ax)
finish(ax, 18, 35, "Eight Triforce vortices, one along each leg,\nconverging on the Field Origin (empty cores)")

# panel 2: the core vortex about an octahedron axis, with the corner strands locked to the ring
ax = fig.add_subplot(1, 3, 2, projection="3d")
Pp, f = core_ring(sense_core); draw_points(ax, Pp, f, AQUA, size=0.45, alpha=0.6)
for ch, col in (("A", BLUE), ("B", ORANGE)):
    Pp, f = corner_strand(ch, sense_core); draw_points(ax, Pp, f, col, size=0.4, alpha=0.5)
for sgn in (1, -1):
    Pp, f = funnel(np.array([0, 0, sgn * 1.0]), 1.05, sense_core * sgn, 0.8, n_lines=170, r_mouth=0.3, r_throat=0.03, ax=ax, col=YELLOW)
    draw_points(ax, Pp, f, YELLOW, size=0.4, alpha=0.55)
wire(ax)
finish(ax, 24, 30, "Core vortex about an octahedron axis:\nTetA, TetB corner strands locked to the turning octahedron ring,\naxial pair along the empty axis")

# panel 3: together
ax = fig.add_subplot(1, 3, 3, projection="3d")
for v in TAc:
    Pp, f = funnel(v, np.sqrt(3) * 0.97, senseA, 1.0, n_lines=200)
    draw_points(ax, Pp, f, BLUE, alpha=0.5)
    Pp, f = funnel(-v, np.sqrt(3) * 0.97, senseB, max(strengthB, 0.25), n_lines=120)
    draw_points(ax, Pp, f, ORANGE, alpha=0.42)
Pp, f = core_ring(sense_core, n_lines=300); draw_points(ax, Pp, f, AQUA, size=0.45, alpha=0.6)
for sgn in (1, -1):
    Pp, f = funnel(np.array([0, 0, sgn * 1.0]), 1.05, sense_core * sgn, 0.8, n_lines=150, r_mouth=0.3, r_throat=0.03)
    draw_points(ax, Pp, f, YELLOW, size=0.4, alpha=0.55)
wire(ax)
finish(ax, 8, 55, "Together: the leg vortices and the core vortex\n(ten funnels with the axial pair)")

fig.text(0.5, 0.035,
         "Axes, empty cores, the turning octahedron ring, the corner strands, and each end's swirl sense and relative strength come from "
         "exact vortex states of the proofs' models.\nFunnel shapes, particle density and the through-flow direction are drawn for display; "
         "the proofs do not fix them. Blue: TetA; orange: TetB; aqua: octahedron core; yellow: axial pair.",
         ha="center", color="#bdbdbd", fontsize=8.5)
fig.subplots_adjust(left=0.0, right=1.0, top=0.9, bottom=0.1, wspace=0.0)
out = os.path.join(HERE, "vortex_render.png")
fig.savefig(out, facecolor=BG)
shutil.copy(out, os.path.join(HERE, "..", "triforce-vortex", "vortex_render.png"))
print("wrote", out)
