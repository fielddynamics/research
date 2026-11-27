from pathlib import Path
from math import cos,sin,pi
from itertools import combinations
out=Path(__file__).resolve().parents[2]/'figures';out.mkdir(exist_ok=True)
def svg(name,w,h,body):
    (out/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#f8fafc"/><g font-family="Arial,sans-serif" fill="#162b42">{body}</g></svg>')
def text(x,y,t,size=16,bold=False):return f'<text x="{x}" y="{y}" font-size="{size}"'+(' font-weight="bold"' if bold else '')+f'>{t}</text>'
def line(a,b,col,width=1,opacity=1):return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{col}" stroke-width="{width}" opacity="{opacity}"/>'
def dot(a,col,r=7):return f'<circle cx="{a[0]}" cy="{a[1]}" r="{r}" fill="{col}"/>'
pts=[(235+175*cos(2*pi*i/17-pi/2),240+175*sin(2*pi*i/17-pi/2)) for i in range(17)]
b=text(24,34,'Frobenius symmetry of the reciprocal K17',24,True)+text(24,58,'Schematic vertex ordering; all 136 edges are present.',14)
for i,j in combinations(range(17),2):b+=line(pts[i],pts[j],'#9cacc1',.65,.23)
for i,j in combinations(range(5),2):b+=line(pts[i],pts[j],'#326fa9',2.4)
for i in range(5,17,2):b+=line(pts[i],pts[i+1],'#b7782e',4)
for i,p in enumerate(pts):b+=dot(p,'#326fa9' if i<5 else '#b7782e')
b+=text(450,125,'5 rational directions',20,True)+text(450,153,'10 reciprocal K5 edges',16)+text(450,205,'12 external directions',20,True)+text(450,233,'6 conjugate matching edges',16)+text(450,287,'13 = 1 + 2 × 6',25,True)+text(450,316,'Norm kernel: origin + oriented matching',15)+text(450,364,'137 = 1 + 10 + 6 + 120',21,True)+text(450,393,'120 remaining unordered edges',15)
svg('frobenius_matching.svg',850,450,b)
# K8 star + Fano triangles, all graph edges colored by their unique Fano line.
pts={0:(245,245),**{i+1:(245+165*cos(2*pi*i/7-pi/2),245+165*sin(2*pi*i/7-pi/2)) for i in range(7)}}
tri=sorted({tuple(sorted((a,b,a^b))) for a,b in combinations(range(1,8),2)})
cols=['#306d9a','#bf7d29','#397b69','#9955a0','#b94c53','#526bb2','#8b7926']
b=text(24,32,'The 28 trigram pairs decompose into Fano triangles',23,True)+text(24,56,'Seven star edges plus seven edge-disjoint triangles on nonzero trigrams.',14)
for i in range(1,8):b+=line(pts[0],pts[i],'#708095',1.8)
for t,c in zip(tri,cols):
    for a,d in combinations(t,2):b+=line(pts[a],pts[d],c,2.5,.82)
for i,p in pts.items():
    b+=dot(p,'#162b42',14)+f'<text x="{p[0]}" y="{p[1]+5}" text-anchor="middle" font-size="11" fill="white">{i:03b}</text>'
b+=text(470,105,'28 = 7 + 7 × 3',24,True)
for i,(t,c) in enumerate(zip(tri,cols)):
    y=145+31*i;b+=line((470,y-5),(495,y-5),c,4)+text(507,y,'  '.join(f'{x:03b}' for x in t),16)
b+=text(470,385,'Every nonzero XOR difference',15)+text(470,407,'has one star edge and three Fano edges.',15)
svg('fano_edge_decomposition.svg',850,450,b)
