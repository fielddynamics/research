from pathlib import Path
from math import cos,sin,pi,sqrt
from itertools import combinations
D=Path(__file__).resolve().parents[2]/'figures';D.mkdir(exist_ok=True)
def save(name,parts,w=680,h=520):
    (D/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#fff"/>'+''.join(parts)+'</svg>')
def text(x,y,s,size=15,c='#24344a'):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{c}">{s}</text>'
def line(a,b,c='#a0aaba',w=1,op=1):return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'
def circle(p,r,c):return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{c}"/>'
blue='#357cba';gold='#b88933';green='#378671';center=(340,248)
vs=[1,3,2,6,4,5] # hexagon order: adjacent subset bit patterns
ps=[center]+[(340+r*cos(i*pi/3-pi/2),248+r*sin(i*pi/3-pi/2)) for r in (85,170) for i in range(6)]
parts=[text(340,25,'Shared-zone labels: two nested cube projections',20)]
parts += [line(a,b,op=.34) for a,b in combinations(ps,2)]
for k,c in [(1,blue),(7,gold)]:
    for i in range(6):
        p=ps[k+i];parts += [line(p,ps[k+(i+1)%6],c,2.5),circle(p,7,c)]
        r=110 if k==1 else 198;angle=i*pi/3-pi/2
        parts += [text(340+r*cos(angle),253+r*sin(angle),f'[{"0" if k==1 else "u"},{vs[i]:03b}]',13,c)]
parts += [circle(center,9,green),text(340,268,'[0,u]',13,green),text(340,478,'13 = 1 + 6 + 6 = 1 + 3 × 4',21),text(340,503,'Outer radius = 2 × inner radius (geometric convention)',13)]
save('metatron_shared_zone.svg',parts)
# projected cube and four diagonals, oblique orthographic view
verts=[tuple(1-2*((v>>i)&1) for i in range(3)) for v in range(8)]
def pr(v):x,y,z=v;return (340+100*x+42*z,225-100*y+35*z)
parts=[text(340,30,'Four exterior Fano planes give the tetrahedral normals',20)]
for i,j in combinations(range(8),2):
    if (i^j).bit_count()==1:parts += [line(pr(verts[i]),pr(verts[j]),'#a0aaba',1.8)]
ns=[1,2,4,7]
for i,j in combinations(ns,2):parts += [line(pr(verts[i]),pr(verts[j]),blue,2.5)]
for i in ns:parts += [line(pr(verts[i]),pr(verts[i^7]),gold,2.5),circle(pr(verts[i]),8,blue),circle(pr(verts[i^7]),4,'#a0aaba'),text(pr(verts[i])[0],pr(verts[i])[1]-13,f'{i:03b}',13,blue)]
parts += [circle((340,225),6,green),text(340,430,'8 oriented exterior labels → 4 body diagonals',19),text(340,460,'13 shared + 4 unoriented exterior = 17',20),text(340,490,'Blue: tetrahedral representatives · Gold: opposite corner axes',13)]
save('metatron_exterior_axes.svg',parts)
