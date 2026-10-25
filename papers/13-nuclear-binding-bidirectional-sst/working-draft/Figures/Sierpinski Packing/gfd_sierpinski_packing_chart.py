#!/usr/bin/env python3
"""
GFD Sierpiński Packing — 8-Panel Chart
========================================
Shows how nucleons pack into the 64-position Sierpiński walk
for 8 key elements. Each tile shows the uniform B/A that the
vortex distributes to every nucleon. Tiles colored by gate depth.

Letter size (8.5 × 11"), white background, journal-ready.

Stephen Nelson — Gravity Field Dynamics
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

K = 4; D = 3; KD = K**D

def mu_sst(x):
    if x <= 0: return 0
    return ((2*x + 1) - math.sqrt(4*x + 1)) / (2*x)

SUM64 = sum(mu_sst(i*i) for i in range(1, KD+1))
SCALE = 8.756 * KD / SUM64
BA_ZN = 8.756
CEIL1 = 2 * BA_ZN

def BA_up(A):
    if A < 1: return 0
    return SCALE * sum(mu_sst(i*i) for i in range(1, A+1)) / A

def BA_up_local(n):
    if n < 1: return 0
    return SCALE * sum(mu_sst(i*i) for i in range(1, n+1)) / n

ba_128 = min(BA_up(128), CEIL1 - BA_up(128))
delta = BA_ZN - ba_128
CEIL3 = ba_128 + BA_ZN - delta/2

def BA_model(A):
    if A < 1: return 0
    if A <= 64:
        return min(BA_up(A), CEIL1 - BA_up(A))
    else:
        return min(BA_up(A), CEIL1 - BA_up(A), CEIL3 - BA_up_local(A - 64))

def gate_depth(i):
    F = i // 16; C = (i % 16) // 4; S = i % 4
    return sum(1 for x in (F, C, S) if x == 3)

# Gate depth colors (print-safe)
GD_COLORS = {0: '#1a8a6e', 1: '#2868b0', 2: '#b83050', 3: '#7040a8'}
GD_COLORS_LIGHT = {0: '#d0efe8', 1: '#d0dff0', 2: '#f0d0d8', 3: '#e0d0f0'}
GD_LABELS = ['a', 'b', 'c', 'd']

# 8 elements
ELEMENTS = [
    ('C',   12,  6, 7.680),
    ('O',   16,  8, 7.976),
    ('Si',  28, 14, 8.448),
    ('Ca',  40, 20, 8.551),
    ('Fe',  56, 26, 8.790),
    ('Ni',  58, 28, 8.732),
    ('Cu',  63, 29, 8.752),
    ('Zn',  64, 30, 8.756),
]


def subdivide(p0, p1, p2, is_up):
    m01 = (0.5*(p0[0]+p1[0]), 0.5*(p0[1]+p1[1]))
    m12 = (0.5*(p1[0]+p2[0]), 0.5*(p1[1]+p2[1]))
    m02 = (0.5*(p0[0]+p2[0]), 0.5*(p0[1]+p2[1]))
    if is_up:
        return [
            (p0, m01, m02, True),
            (m01, p1, m12, True),
            (m02, m12, p2, True),
            (m01, m02, m12, False),  # inverted = gate
        ]
    else:
        return [
            (p0, m01, m02, False),
            (m01, p1, m12, False),
            (m02, m12, p2, False),
            (m01, m02, m12, True),
        ]


def build_64_triangles(cx, cy, size):
    """Build 64 sub-triangles centered at (cx, cy) with given size."""
    h = size * math.sqrt(3) / 2
    apex = (cx, cy + h * 0.6)
    bl = (cx - size/2, cy - h * 0.4)
    br = (cx + size/2, cy - h * 0.4)

    # Level 1: 4 faces
    faces = subdivide(apex, bl, br, True)
    # Level 2: 16 channels
    channels = []
    for p0, p1, p2, up in faces:
        channels.extend(subdivide(p0, p1, p2, up))
    # Level 3: 64 subchannels
    subs = []
    for p0, p1, p2, up in channels:
        subs.extend(subdivide(p0, p1, p2, up))

    return [(p0, p1, p2) for p0, p1, p2, up in subs]


def draw_element(ax, sym, A, Z, ba_known):
    ba_pred = BA_model(A)
    err_keV = (ba_pred - ba_known) * 1000

    # Build triangles
    tris = build_64_triangles(0.5, 0.33, 0.88)

    # Fill count: for A > 64, all 64 tiles are filled
    fill_count = min(A, 64)

    for i, (p0, p1, p2) in enumerate(tris):
        pts = np.array([p0, p1, p2])
        cx_t = np.mean(pts[:, 0])
        cy_t = np.mean(pts[:, 1])
        gd = gate_depth(i)

        if i < fill_count:
            # Filled tile
            color = GD_COLORS[gd]
            ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=0.55, zorder=2)
            ax.plot(np.append(pts[:, 0], pts[0, 0]),
                    np.append(pts[:, 1], pts[0, 1]),
                    color=color, linewidth=0.4, alpha=0.8, zorder=3)

            # B/A value in each tile
            fontsize = 4.0
            ax.text(cx_t, cy_t, f'{ba_pred:.2f}',
                    ha='center', va='center', fontsize=fontsize,
                    color='#222222', fontweight='medium', zorder=4)
        else:
            # Empty tile
            ax.fill(pts[:, 0], pts[:, 1], color='#f0f0f0', alpha=0.4, zorder=1)
            ax.plot(np.append(pts[:, 0], pts[0, 0]),
                    np.append(pts[:, 1], pts[0, 1]),
                    color='#d0d0d0', linewidth=0.3, alpha=0.5, zorder=1)

    # Face outlines
    face_tris = build_64_triangles(0.5, 0.45, 0.88)
    # Reconstruct face-level triangles
    h = 0.88 * math.sqrt(3) / 2
    apex = (0.5, 0.33 + h * 0.6)
    bl = (0.5 - 0.88/2, 0.33 - h * 0.4)
    br = (0.5 + 0.88/2, 0.33 - h * 0.4)
    faces = subdivide(apex, bl, br, True)
    for p0, p1, p2, up in faces:
        pts = np.array([p0, p1, p2, p0])
        ax.plot(pts[:, 0], pts[:, 1], color='#888888', linewidth=0.6, alpha=0.5, zorder=5)

    # Outer triangle
    pts = np.array([apex, bl, br, apex])
    ax.plot(pts[:, 0], pts[:, 1], color='#555555', linewidth=1.0, zorder=5)

    # Element label
    cycle_note = ''
    if A <= 64:
        cycle_note = f'Cycle 1 · {A}/64 filled'
    elif A <= 128:
        cycle_note = f'Cycle 2 · 64/64 filled'
    else:
        cycle_note = f'Cycle 3 · 64/64 filled'

    # Element label at top
    ax.text(0.5, 0.92, f'{sym}-{A}', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#111111', fontfamily='serif')
    
    err_pct = abs(ba_pred - ba_known) / ba_known * 100
    ax.text(0.5, 0.86, f'B/A = {ba_known:.3f}     Predicted = {ba_pred:.3f}     Error = {err_pct:.2f}%',
            ha='center', va='center', fontsize=5, color='#555555')

    # Z, cycle, fill at bottom
    ax.text(0.5, -0.02, f'Z={Z}  ·  {cycle_note}',
            ha='center', va='center', fontsize=5, color='#888888')
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.06, 0.98)
    ax.set_aspect('equal')
    ax.axis('off')


# ═══════════════════════════════════════
# BUILD FIGURE — 4×2 grid, letter size
# ═══════════════════════════════════════

fig, axes = plt.subplots(4, 2, figsize=(8.5, 11))
fig.patch.set_facecolor('white')

fig.suptitle('Sierpiński Walk Packing: Binding Energy per Nucleon',
             fontsize=14, fontweight='bold', color='#111111',
             fontfamily='serif', y=0.98)

for idx, (sym, A, Z, ba) in enumerate(ELEMENTS):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    draw_element(ax, sym, A, Z, ba)

# Legend at bottom
legend_y = 0.015
for gd in range(4):
    x = 0.18 + gd * 0.18
    fig.patches.append(plt.Rectangle((x, legend_y), 0.015, 0.012,
                                      facecolor=GD_COLORS[gd], alpha=0.55,
                                      transform=fig.transFigure, zorder=10))
    fig.text(x + 0.02, legend_y + 0.006,
             f'{GD_LABELS[gd]} (gd={gd})', fontsize=6, color='#444444',
             va='center')

fig.text(0.5, 0.005,
         r'$\mu_{\mathrm{SST}}(x) = [(2x\!+\!1) - \sqrt{4x\!+\!1}]\,/\,2x$'
         r'$\qquad K\!=\!4,\ D\!=\!3,\ K^D\!=\!64$',
         ha='center', fontsize=7, color='#888888', style='italic')

plt.subplots_adjust(left=0.03, right=0.97, top=0.94, bottom=0.04,
                    hspace=0.15, wspace=0.05)

plt.savefig('/mnt/user-data/outputs/gfd_sierpinski_packing_8.png', dpi=300,
            bbox_inches='tight', facecolor='white')
plt.savefig('/mnt/user-data/outputs/gfd_sierpinski_packing_8.pdf',
            bbox_inches='tight', facecolor='white')
print('Done. 8-panel Sierpiński packing chart saved.')

for sym, A, Z, ba in ELEMENTS:
    pred = BA_model(A)
    print(f'  {sym:>3}-{A:<3}  pred={pred:.3f}  known={ba:.3f}  Δ={(pred-ba)*1000:+.0f} keV')
