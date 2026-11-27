from pathlib import Path
from math import sqrt
p=Path(__file__).resolve().parents[2]/'figures'
p.mkdir(exist_ok=True)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="940" height="470" viewBox="0 0 940 470"><rect width="940" height="470" fill="#f7fafc"/><g font-family="Arial,sans-serif" fill="#172b40"><text x="35" y="44" font-size="25" font-weight="bold">Three independent snapshots complete the invariant register</text><text x="35" y="73" font-size="15">Fixed trace; spectral blocks of sizes 2, 3, 3</text>']
for i,(r,d) in enumerate([(1,12),(2,19),(3,21)]):
 y=116+i*100
 svg.append(f'<text x="35" y="{y+25}" font-size="18">{r} snapshot{"s" if r>1 else ""}</text>')
 for j,m in enumerate([2,3,3]):
  x=215+j*82
  for a in range(m):
   for b in range(m):
    fill='#477aa6' if a<min(r,m) and b<min(r,m) else '#d6e0e8'
    svg.append(f'<rect x="{x+20*b}" y="{y+20*a}" width="17" height="17" rx="2" fill="{fill}"/>')
 svg.append(f'<rect x="490" y="{y+10}" width="340" height="30" rx="4" fill="#d6e0e8"/><rect x="490" y="{y+10}" width="{340*d/21}" height="30" rx="4" fill="#477aa6"/><text x="846" y="{y+31}" font-size="19" font-weight="bold">{d}/21</text>')
svg.append('<text x="35" y="438" font-size="15">Block rank illustration in a suitable basis; transformed copies of one state are not independent.</text></g></svg>')
p.joinpath('three_snapshot_rank.svg').write_text(''.join(svg))
p.joinpath('density_common_modes.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="940" height="475" viewBox="0 0 940 475"><rect width="940" height="475" fill="#f7fafc"/><g font-family="Arial,sans-serif" fill="#172b40"><text x="35" y="44" font-size="25" font-weight="bold">The physical trace and Walsh common mode are different lines</text><text x="35" y="73" font-size="15">Two-dimensional section of the invariant 22-dimensional register</text><g stroke="#477aa6" stroke-width="3"><path d="M90 330 H375"/><path d="M210 400 V112" stroke-dasharray="8 7"/></g><g stroke="#b88a3e" stroke-width="3"><path d="M210 330 L330.5 145.9"/><path d="M80 245 L340 415" stroke-dasharray="8 7"/></g><path d="M250 330 A40 40 0 0 0 232 297" fill="none" stroke="#526577" stroke-width="1.5"/><circle cx="210" cy="330" r="5" fill="#172b40"/><text x="385" y="335" font-size="17" fill="#477aa6">e (trace)</text><text x="338" y="145" font-size="17" fill="#9c722e">f (Walsh seed)</text><text x="220" y="116" font-size="16" fill="#477aa6">e⊥</text><text x="43" y="240" font-size="16" fill="#9c722e">f⊥</text><text x="248" y="301" font-size="15">cos² θ = 3/10</text><rect x="480" y="125" width="420" height="266" rx="12" fill="#e8eef3"/><text x="502" y="158" font-size="19" font-weight="bold">Two different 21-dimensional spaces</text><text x="502" y="196" font-size="17">Orthogonal projection e⊥ → f⊥</text><text x="502" y="229" font-size="17">Singular values: 1 (20), √(3/10) (1)</text><text x="502" y="270" font-size="17">Induced metric: I + (7/3) vvᵀ</text><text x="502" y="309" font-size="17">Ranks: 17 and 13 in either space</text><text x="502" y="347" font-size="16">Weighted-trace prescription need not agree.</text><text x="35" y="448" font-size="15">Ordinary operator traces are coordinate invariant; metric-weighted observables require a specified physical law.</text></g></svg>''')
