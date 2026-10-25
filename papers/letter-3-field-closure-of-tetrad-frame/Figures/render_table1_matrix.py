import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(5, 5.4), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

shared_color = '#6B4C9A'
tetA_color = '#1A6AAF'
tetB_color = '#B03030'
shared_bg = '#EDE6F5'
tetA_bg = '#E0EEF8'
tetB_bg = '#F5E0E0'

labels = [
    ['tt', 'tx', 'ty', 'tz'],
    ['xt', 'xx', 'xy', 'xz'],
    ['yt', 'yx', 'yy', 'yz'],
    ['zt', 'zx', 'zy', 'zz'],
]

types = [
    ['shared', 'tetA', 'tetA', 'tetA'],
    ['tetB', 'shared', 'tetA', 'tetA'],
    ['tetB', 'tetB', 'shared', 'tetA'],
    ['tetB', 'tetB', 'tetB', 'shared'],
]

sublabels = [
    ['shared', 'kept ✓', 'kept ✓', 'kept ✓'],
    ['discarded', 'shared', 'kept ✓', 'kept ✓'],
    ['discarded', 'discarded', 'shared', 'kept ✓'],
    ['discarded', 'discarded', 'discarded', 'shared'],
]

dirs = ['t', 'x', 'y', 'z']
cell = 1.0
margin = 0.6

def draw_hatch(ax, x, y, w, h, direction, color, density=8):
    clip = patches.Rectangle((x, y), w, h, transform=ax.transData)
    spacing = w / density
    if direction == '\\':
        for i in range(-density*2, density*4):
            x0 = x + i * spacing
            y0 = y
            x1 = x0 + h
            y1 = y + h
            line, = ax.plot([x0, x1], [y0, y1], color=color, 
                          linewidth=0.4, alpha=0.25)
            line.set_clip_path(clip)
    elif direction == '/':
        for i in range(-density*2, density*4):
            x0 = x + i * spacing
            y0 = y + h
            x1 = x0 + h
            y1 = y
            line, = ax.plot([x0, x1], [y0, y1], color=color,
                          linewidth=0.4, alpha=0.25)
            line.set_clip_path(clip)
    elif direction == '+':
        for i in range(density + 1):
            for j in range(density + 1):
                cx = x + (i / density) * w
                cy = y + (j / density) * h
                if x < cx < x + w and y < cy < y + h:
                    ax.plot(cx, cy, '.', color=color, markersize=0.5, alpha=0.2)

for row in range(4):
    for col in range(4):
        x = margin + col * cell
        y = margin + (3 - row) * cell
        
        t = types[row][col]
        if t == 'shared':
            bg, tc, hatch_dir = shared_bg, shared_color, '+'
        elif t == 'tetA':
            bg, tc, hatch_dir = tetA_bg, tetA_color, '\\'
        else:
            bg, tc, hatch_dir = tetB_bg, tetB_color, '/'
        
        rect = patches.FancyBboxPatch(
            (x + 0.03, y + 0.03), cell - 0.06, cell - 0.06,
            boxstyle="round,pad=0.04",
            facecolor=bg, edgecolor='#888888', linewidth=0.6
        )
        ax.add_patch(rect)
        
        draw_hatch(ax, x + 0.06, y + 0.06, cell - 0.12, cell - 0.12, 
                   hatch_dir, tc)
        
        # Main label — NO white background
        lbl = labels[row][col]
        if t == 'tetB':
            lbl = f'({lbl})'
        weight = 'bold' if t == 'shared' else 'normal'
        fs = 13.5 if t != 'tetB' else 12.5
        
        ax.text(x + cell/2, y + cell/2 + 0.08, lbl,
                ha='center', va='center', fontsize=fs,
                fontweight=weight, color=tc, family='serif')
        
        # Sublabel — keep white background for legibility
        sub = sublabels[row][col]
        ax.text(x + cell/2, y + cell/2 - 0.22, sub,
                ha='center', va='center', fontsize=6.5,
                color=tc, alpha=0.65,
                bbox=dict(boxstyle='round,pad=0.04', facecolor='white',
                         edgecolor='none', alpha=0.7))

for i, d in enumerate(dirs):
    ax.text(margin + i * cell + cell/2, margin + 4 * cell + 0.22, d,
            ha='center', va='center', fontsize=14,
            fontweight='bold', color='#222', family='serif')
    ax.text(margin - 0.28, margin + (3-i) * cell + cell/2, d,
            ha='center', va='center', fontsize=14,
            fontweight='bold', color='#222', family='serif')

ax.text(margin + 2*cell, margin + 4*cell + 0.55, 'ν',
        ha='center', va='center', fontsize=12, color='#555',
        family='serif', style='italic')
ax.text(margin - 0.6, margin + 2*cell, 'μ',
        ha='center', va='center', fontsize=12, color='#555',
        family='serif', style='italic')

legend_y = -0.1
legend_items = [
    (shared_bg, shared_color, '+',  'Diagonal (4) — shared, root-blind'),
    (tetA_bg, tetA_color, '\\',    'Upper triangle (6) — TetA, s = +1, retained'),
    (tetB_bg, tetB_color, '/',     'Lower triangle (6) — TetB, s = −1, discarded'),
]
for i, (bg, tc, hd, text) in enumerate(legend_items):
    lx = margin + 0.05
    ly = legend_y - i * 0.32
    rect = patches.FancyBboxPatch(
        (lx, ly), 0.28, 0.22,
        boxstyle="round,pad=0.02",
        facecolor=bg, edgecolor='#888', linewidth=0.5
    )
    ax.add_patch(rect)
    draw_hatch(ax, lx + 0.02, ly + 0.02, 0.24, 0.18, hd, tc)
    ax.text(lx + 0.42, ly + 0.11, text,
            ha='left', va='center', fontsize=7.5, color='#333')

ax.set_xlim(-0.4, margin + 4*cell + 0.3)
ax.set_ylim(legend_y - 1.1, margin + 4*cell + 0.8)
ax.set_aspect('equal')
ax.axis('off')

plt.savefig('/mnt/user-data/outputs/table1_matrix.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('/mnt/user-data/outputs/table1_matrix.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved")
