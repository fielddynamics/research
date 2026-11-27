from pathlib import Path
from html import escape
P=Path(__file__).parent/'figures'; P.mkdir(exist_ok=True)
def txt(x,y,t,size=18,fill='#dce8f4',anchor='middle'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{escape(str(t))}</text>'
def rect(x,y,w,h,c,op=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" opacity="{op}"/>'
def line(x,y,X,Y,c='#7e99b7',w=2):return f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{c}" stroke-width="{w}"/>'
def save(name,title,body,h=400):
    (P/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {h}" font-family="system-ui,sans-serif"><rect width="800" height="{h}" rx="18" fill="#111d2e"/>'+txt(32,42,title,25,anchor='start')+body+'</svg>')
b=rect(45,92,330,174,'#25588b',.5)+rect(385,92,90,174,'#cb9a42',.65)+rect(485,92,265,174,'#146c70',.6)
for i in range(8):
    x=65+i*95
    if i<7:b+=line(x,184,x+95,184)
    b+=f'<circle cx="{x}" cy="184" r="14" fill="'+('#9ba8b9' if i in (0,7) else '#f5d67b' if i==4 else '#94d6ee')+'"/>'+txt(x,218,i,15)
b+=txt(210,130,'Child I: 1, 2, 3',18)+txt(430,130,'B: 4',18)+txt(618,130,'Exterior O: 5, 6',18)+txt(400,304,'Read: g = u₄   •   Interior: x = A⁻¹(f − Cg)',22)+txt(400,340,'One interface coordinate is sufficient for all exterior changes.',17)
save('information_01_separator.svg','Local interface, global dependence',b,375)
b=''; X=84;Y=91;d=43
for i in range(6):
    b+=txt(X-17,Y+i*d+27,i+1,15)
    b+=txt(X+i*d+20,Y-9,i+1,15)
    for j in range(6):
        v=(min(i,j)+1)*(6-max(i,j));b+=rect(X+j*d,Y+i*d,d-3,d-3,'#3286c6',.25+.7*v/12)+txt(X+j*d+20,Y+i*d+25,v,15,'white')
b+=f'<rect x="{X+4*d-2}" y="{Y-2}" width="{2*d+1}" height="{3*d+1}" fill="none" stroke="#f4cd78" stroke-width="3"/>'
b+=txt(213,376,'All entries of 7 L⁻¹',18)+txt(560,105,'Cross block × 7',20)
for i,row in enumerate([[2,1],[4,2],[6,3]]):
    for j,v in enumerate(row):b+=rect(477+j*82,128+i*62,76,56,'#be8e3d',.8)+txt(515+j*82,162+i*62,v,22,'white')
b+=txt(560,342,'rank = 1',27,'#f4cd78')+txt(560,375,'Dense response ≠ full raw read',16)
save('information_02_green.svg','Exact six-node Green function',b,410)
b=txt(400,82,'F(r) = −q² m₁m₂ / (4πκr²)',21)+line(82,320,740,320)+line(82,120,82,320)
for scale,c in [(1,'#6cd0e9'),(2,'#f5ca71')]:
    pts=[]
    for j in range(201):
        r=1+4*j/200; x=82+658*j/200;y=320-90*scale/r**2;pts.append(f'{x:.2f},{y:.2f}')
    b+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="3"/>'
for i in range(1,6):b+=txt(82+(i-1)*658/4,344,i,14)
b+=txt(410,371,'Separation r',16)+txt(100,113,'|F|',16)+line(485,117,520,117,'#6cd0e9',3)+txt(530,122,'E',16,anchor='start')+line(585,117,620,117,'#f5ca71',3)+txt(630,122,'2E',16,anchor='start')+txt(400,408,'Identical stationary state maps; different mechanical force scales.',16)
save('information_03_force.svg','Closure force requires a calibrated energy scale',b,438)
