from pathlib import Path
from xml.sax.saxutils import escape
import itertools, math
p=Path(__file__).resolve().parent
s=[]
def init(w,h,title):
    global s
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><rect width="100%" height="100%" rx="16" fill="#f8fafc"/><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#64748b"/></marker></defs>']
def tx(x,y,t,size=18,weight='400',color='#17263c'):
    s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(t)}</text>')
def box(x,y,w,h,title,sub,color='#2563eb'):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="white" stroke="{color}" stroke-width="1.5"/>');tx(x+w/2,y+28,title,18,'700',color);tx(x+w/2,y+51,sub,14)
def arrow(d):s.append(f'<path d="{d}" fill="none" stroke="#64748b" stroke-width="1.8" marker-end="url(#a)"/>')
def line(a,b,color='#64748b',width=1.5):s.append(f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" stroke="{color}" stroke-width="{width}" fill="none"/>')
def save(name): (p/name).write_text(''.join(s)+ '</svg>')
init(1080,660,'Common closure space and exact frame transports')
tx(540,36,'Proof 25 • One normed closure space',28,'700');tx(540,61,'Five realizations, explicit isometries, no independent physical derivation implied',16)
for x,t,sub in [(25,'Tetrad / Hadamard','MᵀM = 4I − J'),(290,'Four-leg cut frame','BBᵀ = 4I − J'),(555,'Oriented cycle frame','DᵀD = 4I − J'),(820,'Flywheel column frame','FᵀF = 4I − J')]:
    box(x,90,235,76,t,sub,'#2563eb' if x<500 else '#087f75');arrow(f'M{x+117.5} 166V190H540V223')
box(275,225,530,96,'Common closure space: sum q = 0','P = I − J/4 • G = 4P','#7048ba');tx(540,303,'Transport YXᵀ/4 • composition independent of path',15)
arrow('M540 321V361');box(275,363,530,80,'Two parity-related simplices','qᵢ ≥ −1 and qᵢ ≤ 1, with Σqᵢ = 0','#2563eb')
arrow('M540 443V465H280V487');arrow('M540 443V465H800V487')
box(25,490,510,84,'Shared octahedral core','6 pair vertices • 12 edges • 8 faces','#087f75');box(545,490,510,84,'Eight stellations','4 apex regions in each chamber','#2563eb');tx(540,609,'Proof 23: recursive subdivision is downstream of this geometry.',17,'700');tx(540,635,'Physical metric selection, geometry-forming dynamics and gravitational coupling remain open.',14)
save('convergence.svg')
init(1080,470,'Core incidence from four labels')
tx(540,34,'From four labels to the octahedral core',27,'700');tx(540,60,'Each pair of labels becomes a core vertex; the face-dual graph is a cube.',16)
# Draw actual projections of the pair vertices, plus K4 and bipartite dual.
from itertools import combinations
es=list(combinations(range(4),2)); sp=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
# explicit oblique projection no coincident points
u=(0.91,-0.39,0.15); v=(0.12,0.49,-0.86)
def proj(x,cx,cy,k): return (cx+k*sum(a*b for a,b in zip(x,u)),cy+k*sum(a*b for a,b in zip(x,v)))
loc=[proj(x,180,243,85) for x in sp]
for a,b in es:line(loc[a],loc[b],'#2563eb',2)
for i,(x,y) in enumerate(loc):s.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#2563eb"/>');tx(x,y+5,str(i),15,'700','white')
tx(180,104,'Four-leg graph K₄',18,'700');tx(180,397,'4 labels · 6 edges',16)
mid=[tuple((sp[i][k]+sp[j][k])/2 for k in range(3)) for i,j in es];pos=[proj(x,540,243,117) for x in mid]
for i,j in combinations(range(6),2):
    if set(es[i])&set(es[j]):line(pos[i],pos[j],'#087f75',2)
for e,(x,y) in zip(es,pos):s.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#087f75"/>');tx(x,y+5,''.join(map(str,e)),15,'700','white')
tx(540,104,'Octahedral graph L(K₄)',18,'700');tx(540,397,'6 pair vertices · 12 edges',16)
# cube as bipartite opposite face labels
left=[(800,145+65*i) for i in range(4)];right=[(985,145+65*i) for i in range(4)]
for i,j in itertools.product(range(4),repeat=2):
    if i!=j:line(left[i],right[j],'#94a3b8',1.6)
for k,pts in enumerate([left,right]):
    for i,(x,y) in enumerate(pts):s.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{"#2563eb" if k==0 else "#d97706"}"/>');tx(x,y+5,('+' if k==0 else '−')+str(i),13,'700','white')
tx(893,104,'Core face-dual graph',18,'700');tx(893,397,'8 faces · 12 shared edges',16);tx(540,448,'Edge (i,j) exists exactly when i ≠ j. Chamber inversion exchanges the two face families.',15)
save('core-incidence.svg')
