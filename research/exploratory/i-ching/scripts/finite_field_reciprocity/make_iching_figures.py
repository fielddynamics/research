"""Generate exact incidence/reciprocity schematic SVGs (not physical geometry)."""
from pathlib import Path
import math
from test_iching_bridge import N
out=Path(__file__).resolve().parents[2]/'figures';out.mkdir(exist_ok=True)
head=lambda w,h:f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#f8fafc"/><g font-family="Arial,sans-serif" fill="#17334d">'
tail='</g></svg>'
a=[head(950,570),'<text x="25" y="40" font-size="25" font-weight="bold">Reciprocal edges of the 17-direction pencil</text>','<text x="25" y="66" font-size="15">Every pair of directions has one reciprocal pair of projective points.</text>']
coords=[(275+205*math.cos(-math.pi/2+2*math.pi*i/17),300+205*math.sin(-math.pi/2+2*math.pi*i/17)) for i in range(17)]
for i in range(17):
 for j in range(i+1,17):
  x,y=coords[i];u,v=coords[j];c='#b78539' if i<5 and j<5 else '#6b94b9';opacity='.8' if i<5 and j<5 else '.23';a.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="{c}" stroke-width="1.4" opacity="{opacity}"/>')
for i,(x,y) in enumerate(coords):
 a.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{"#b78539" if i<5 else "#386b9b"}"/><text x="{x}" y="{y+4}" text-anchor="middle" font-size="10" fill="white">{i+1}</text>')
a.extend(['<text x="540" y="150" font-size="20" font-weight="bold">17 pencil directions</text>','<text x="540" y="187" font-size="18">272 oriented edges</text>','<text x="540" y="222" font-size="18">136 reciprocal pairs</text>','<rect x="540" y="250" width="375" height="100" rx="8" fill="#e6eef7"/>','<text x="557" y="282" font-size="16">Include the fixed origin:</text>','<text x="557" y="325" font-size="29" font-weight="bold">1 + 136 = 137</text>','<text x="540" y="398" font-size="15" fill="#906625">Gold: five rational directions, K5</text>','<text x="540" y="430" font-size="15">Blue: twelve external directions</text>','<text x="25" y="550" font-size="14">Exact abstract incidence graph; not 17 spatial rays, not a physical derivation of alpha.</text>',tail]);(out/'iching_reciprocal_graph.svg').write_text(''.join(a))
a=[head(960,575),'<text x="25" y="40" font-size="25" font-weight="bold">The threefold hexagram read is a projective incidence transform</text>','<text x="25" y="68" font-size="15">Hermitian polarity on PG(2,4): 21 × 21 incidence matrix N</text>']
for i in range(21):
 for j in range(21):a.append(f'<rect x="{45+20*j}" y="{100+20*i}" width="19" height="19" fill="{"#386b9b" if N[i,j] else "#e5eaf0"}"/>')
a.extend(['<text x="510" y="135" font-size="18" font-weight="bold">Exact identities</text>','<text x="510" y="175" font-size="20">N² = 4I + J</text>','<text x="510" y="212" font-size="18">Each row has 5 points</text>','<text x="510" y="246" font-size="18">9 absolute points</text>','<text x="510" y="295" font-size="18" font-weight="bold">Full 22-mode Walsh spectrum</text>','<text x="510" y="330" font-size="19">+1 × 12; −1 × 10</text>','<text x="510" y="365" font-size="16">Lossless; no electromagnetic gain.</text>','<text x="510" y="420" font-size="16">Nonzero projective block alone:</text>','<text x="510" y="455" font-size="18">20 unit singular values, one 1/8</text>','<text x="25" y="555" font-size="14">The singleton zero and common record must be retained or correctly transferred.</text>',tail]);(out/'iching_walsh_incidence.svg').write_text(''.join(a))
