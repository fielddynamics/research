from pathlib import Path
from math import sqrt
from html import escape
import contextlib,io
with contextlib.redirect_stdout(io.StringIO()):
    from verify_recursive_triforce import levels,face
root=Path(__file__).parent
def txt(x,y,s,size=16,b=False,c='#23354a'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{"bold" if b else "normal"}" fill="{c}" text-anchor="middle">{escape(s)}</text>'
def start(w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Arial,sans-serif"><rect width="{w}" height="{h}" fill="white"/>'
s=start(1120,580)+txt(560,35,'Recursive Triforce: fixed-lattice depth rule',26,True)+txt(560,63,'Four retained medial children at every level; green vertices are on the original lattice',16)
for n in range(4):
    ox=140+280*n; oy=205; sc=23
    def proj(p):a,b=map(float,p);return ox+sc*(a-b/2),oy-sc*sqrt(3)*b/2
    for i in range(-8,9):
        for j in range(-8,9):
            x,y=proj((i,j))
            if abs(x-ox)<125 and abs(y-oy)<125:s+=f'<circle cx="{x}" cy="{y}" r="1.6" fill="#aab9c7"/>'
    a=levels(face,n)
    for t,sign in a:
        points=' '.join(f'{x},{y}' for x,y in map(proj,t)); col='#9ed7cf' if sign==1 else '#f6c58d'
        s+=f'<polygon points="{points}" fill="{col}" fill-opacity=".72" stroke="#335b82" stroke-width="1.2"/>'
    for p in {p for t,_ in a for p in t}:
        x,y=proj(p); col='#087b70' if all(v.denominator==1 for v in p) else '#b95017'
        s+=f'<circle cx="{x}" cy="{y}" r="{2.4 if n==3 else 3}" fill="{col}"/>'
    s+=txt(ox,348,f'Depth {n} · {4**n} tiles',18,True)+txt(ox,374,'Off-lattice vertices' if n==3 else 'All vertices on lattice',15,False,'#b95017' if n==3 else '#087b70')
s+='<rect x="110" y="420" width="900" height="116" rx="12" fill="#edf4f8"/>'+txt(560,451,'Depth two: 10 same-pointing + 6 opposite-pointing tiles',22,True)+txt(560,483,'Four coupled faces × 16 addresses = 64 (40 + 24)',21,True)+txt(560,514,'Conditional on the fixed lattice; pointing parity is not yet torsion.',16)+'</svg>'
(root/'recursive_triforce.svg').write_text(s)
s=start(900,620)+txt(450,35,'One physical address hierarchy',26,True)
rows=[(70,'1 · Field Origin / settlement root'),(165,'4 · Coupled face directions'),(260,'16 · Primary Triforce channels'),(355,'64 · Secondary Triforce addresses'),(485,'Walsh / π addressing')]
for i,(y,t) in enumerate(rows):
    s+=f'<rect x="150" y="{y}" width="600" height="58" rx="10" fill="{"#f9ecd9" if i==4 else "#e6f2f6"}" stroke="#7092a6"/>'+txt(450,y+36,t,22,True)
    if i<4:
        end=rows[i+1][0]-7;s+=f'<path d="M450 {y+58} V{end} l-6 -9 m6 9 l6 -9" stroke="#5a7184" stroke-width="2" fill="none"/>'
s+=txt(450,442,'40 / 24 pointing split; transport remains open',15)+txt(450,571,'Candidate computational representation — no physical intertwiner established',15)+'</svg>'
(root/'closure_hierarchy.svg').write_text(s)
