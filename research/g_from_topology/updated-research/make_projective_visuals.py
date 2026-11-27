"""Generate six standalone SVGs and embedded exact enumeration data for the explorer."""
from pathlib import Path
import contextlib, io, runpy, json, math, html
P=Path(__file__).resolve().parent; F=P/'figures'; F.mkdir(exist_ok=True)
with contextlib.redirect_stdout(io.StringIO()): v=runpy.run_path(str(P/'verify_projective_bridge.py'))
points=v['points']; norm=v['norm']; project=v['project']; canon=v['canon']; pairs=v['pairs']; grade=v['grade']; base=v['base']; blocks=[base]+[b for b in v['blocks'] if b!=base]; X=v['X'];
byclass={canon(z):z for z in pairs}; rows=[]
for b in blocks:
    byf={project(norm(z)):z for z in b}; rows.append([list(byclass[byf[p]]) for p in points])
assert len(rows)==13 and all(len(r)==21 for r in rows)
data={'points':points,'grades':[grade(p) for p in points],'rows':rows,'planes':X.T.tolist()}
C=['#1279b7','#008d82','#8054b3']; ink='#17304a'; muted='#536b82'; gold='#c28414'; pale='#eaf1f7'
def esc(s):return html.escape(str(s))
def txt(x,y,s,size=18,fill=ink,anchor='start',weight=400):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>'
def rect(x,y,w,h,fill,stroke='none',rx=7):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def line(x,y,X,Y,stroke=muted,arrow=False):return f'<path d="M{x} {y} L{X} {Y}" stroke="{stroke}" stroke-width="2" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def box(x,y,w,h,title,sub,color):return rect(x,y,w,h,'#f4f8fb',color)+txt(x+w/2,y+31,title,20,color,'middle',700)+txt(x+w/2,y+57,sub,15,muted,'middle')
def save(name,title,sub,body,h=540):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}" role="img" aria-label="{esc(title)}"><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0 0 L8 3 L0 6Z" fill="{muted}"/></marker></defs><rect width="1000" height="{h}" fill="white"/><g font-family="Arial, sans-serif">{txt(35,37,"GFD  /  PROJECTIVE NORM & WALSH RESEARCH",13,muted,weight=700)}{txt(35,77,title,30,ink,weight=700)}{txt(35,106,sub,16,muted)}{body}{txt(35,h-17,"Exact algebra for the specified construction; physical source and gain selection remain open.",13,muted)}</g></svg>'
    (F/name).write_text(svg)
# 1
b=''; xs=[35,230,425,620,815]; titles=['Truth table','Forward H','Spectral bridge','Inverse H','Registered table']; subs=['64 records','W = H₆₄/8','1 | 3 | 12 | 48','W⁻¹ = W','64 records'];
for i,x in enumerate(xs):
    b+=box(x,165,150,80,titles[i],subs[i],C[i%3]);
    if i<4:b+=line(x+150,205,x+190,205,arrow=True)
b+=txt(500,290,'J = W Λ W⁻¹',30,ink,'middle',700)
for i,(n,g) in enumerate(zip([1,3,12,48],['DC','t₀','t₁','t₂'])):
    x=150+sum([1,3,12,48][:i])*11;b+=rect(x,320,n*11-2,48,[gold]+C if False else ([gold]+C)[i],rx=2)
    if i>1:b+=txt(x+n*5.5,351,f'{n} · {g}',18,'white','middle',700)
b+=txt(150,397,'DC = 1; grade 0 = 3',16,muted)+txt(850,397,'64 spectral coordinates',16,muted,'end')
b+=txt(500,443,'Invariant contrasts: 1 + 4 + 16; common scalar preserved.',20,ink,'middle',700)
save('projective_01_walsh_filter.svg','Forward–bridge–inverse Walsh filter','Each spectral grade receives its gain once; the inverse tree is not the entire FWHT.',b,490)
# 2
b=''
for g,n,x in [(0,1,70),(1,4,280),(2,16,540)]:
    s=18 if n==16 else 38; sz=n*s; y=160
    b+=txt(x,y-12,f'Level {g+1}: {n} × {n}',19,C[g],weight=700)
    for i in range(n):
        for j in range(n):b+=rect(x+j*s,y+i*s,s-1,s-1,gold if i==j else C[g] if j&i==j else pale,rx=0)
    b+=txt(x,y+sz+25,f'{n} diagonal / {3**(2*g)} filled',16,ink)
    b+=txt(x,y+sz+47,f'{n*n} possible entries',15,muted)
b+=txt(70,395,'Diagonal: 21',25,gold,weight=700)+txt(70,430,'Filled: 91',22,C[0],weight=700)+txt(70,465,'Capacity: 273',22,ink,weight=700)
save('projective_02_sierpinski_blocks.svg','Three Sierpiński blocks','L⊗⁰, L⊗², L⊗⁴; L = [[1,0],[1,1]]. Gold marks the diagonal, blue/green/purple the nonzero support.',b,555)
# 3
b='';
for x,y,X,Y,label in [(500,200,270,260,'degree 2'),(500,200,730,260,'degree 3'),(270,340,500,400,'degree 3'),(730,340,500,400,'degree 2')]:
    b+=line(x,y,X,Y);b+=txt((x+X)/2+(-32 if X<x else 32),(y+Y)/2,label,15,muted,'middle')
for x,y,t,s,c in [(380,125,'F₄₀₉₆','common extension',C[2]),(150,260,'F₆₄','3-dimensional over F₄',C[0]),(610,260,'F₁₆','2-dimensional over F₄',C[1]),(380,400,'F₄','base field',gold)]:b+=box(x,y,240,75,t,s,c)
b+=txt(60,515,'Norm: N(z) = z⁶⁵',19,ink,weight=700)+txt(940,515,'Projective fibres: 273 → 21, size 13',19,ink,'end',700)
save('projective_03_field_tower.svg','Finite-field tower and projective norm','F₆₄ ∩ F₁₆ = F₄; the norm descends to projective multiplicative quotients.',b,560)
# 4
b=txt(75,142,'Norm fibre (projective F₄ representative; encoded integer)',16,muted)
for j,p in enumerate(points):b+=txt(106+j*38,168,p,14,C[grade(p)],'middle',700)
for i,row in enumerate(rows):
    b+=txt(76,191+i*22,'B₀' if i==0 else f'B{i}',14,ink,'end',700 if i==0 else 400)
    for j,(u,w) in enumerate(row):
        b+=rect(89+j*38,177+i*22,34,19,gold if i==0 else ['#d9edf8','#caeee9','#e8dff4'][grade(points[j])],rx=2)
        b+=txt(106+j*38,191+i*22,f'{u}/{w}',9,'white' if i==0 else ink,'middle')
b+=txt(89,490,'Each cell is one actual same-grade matrix-unit pair (u,v).',17,ink)+txt(89,516,'Gold row: the embedded diagonal Baer subplane. Each column has 13 points.',16,muted)
save('projective_04_baer_ledger.svg','The 273-point interaction ledger','13 disjoint Baer subplanes × 21 norm fibres. Labels use the verifier’s finite-field encoding.',b,560)
# 5
b=''; nodes=[(42,'273','Matrix-unit capacity',C[0]),(290,'272','Trace-zero rank',C[1]),(538,'272/13','Compressed trace',C[2]),(786,'17/13','Trace divided by 16',gold)]
for i,(x,t,s,c) in enumerate(nodes):
    b+=box(x,155,172,80,t,s,c)
    if i<3:b+=line(x+172,195,x+242,195,arrow=True)
b+=txt(500,278,'Breg = R P Rᵀ = I − 11ᵀ/273',28,ink,'middle',700)
b+=txt(80,318,'Spectrum of the compressed response',18,muted,weight=700)
for i in range(21):
    x=80+i*40; val=12/13 if i==20 else 1;b+=rect(x,432-95*val,30,95*val,gold if i==20 else C[0],rx=2)
b+=txt(80,458,'20 unit eigenvalues',17,ink)+txt(920,458,'12/13',17,gold,'end',700)
b+=txt(500,498,'det Breg = 12/13; the normalized trace is 17/13 (not its determinant).',17,ink,'middle')
save('projective_05_trace_compression.svg','Trace constraint → registered response','Remove the global identity direction; compress through the 13-point norm fibres.',b,550)
# 6
b='';th=math.pi/3;p=math.tan(th/2);s=math.sin(th)
for i in range(4):
    x=125+i*250;y=270; b+=line(x-95,y,x+95,y,'#d8e1e9')+line(x,y-95,x,y+95,'#d8e1e9'); verts=[]
    for a,d in [(-42,-42),(42,-42),(42,42),(-42,42)]:
        if i>=1:a-=p*d
        if i>=2:d+=s*a
        if i>=3:a-=p*d
        verts.append(f'{x+a},{y-d}')
    b+=f'<polygon points="{" ".join(verts)}" fill="#d9edf8" stroke="{C[0]}" stroke-width="2.5"/>'
    b+=txt(x,390,['Initial','Upper shear','Lower shear','Upper → rotation'][i],18,ink,'middle',700)
    if i<3:b+=line(x+99,y,x+145,y,arrow=True)
b+=txt(500,445,'U(−tan θ/2) L(sin θ) U(−tan θ/2) = R(θ)',23,ink,'middle',700)
b+=txt(500,478,'At θ = 60°: retained amplitude = 1/2, retained probability = 1/4.',17,muted,'middle')
save('projective_06_alternating_shears.svg','Alternating sweeps form a rotation','All three shears have determinant one. Loss appears only after retaining one output port.',b,530)
# HTML is authored separately; replace only the embedded data marker when regenerating.
page=P/'interactive/projective_walsh.html'
if page.exists():
    import re
    page.write_text(re.sub(r'(<script id="enumeration" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps(data,separators=(',',':'))+m[2],page.read_text(),flags=re.S))
print('Generated six diagrams; exact enumeration: 13 × 21 cells, 21 orthogonal plane modes.')
