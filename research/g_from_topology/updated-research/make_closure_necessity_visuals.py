from pathlib import Path
from html import escape
P=Path(__file__).parent/'figures'; P.mkdir(exist_ok=True)
BLUE='#2563eb'; TEAL='#0f766e'; ORANGE='#b45309'; INK='#142b45'; MUTED='#52647a'
def text(x,y,t,size=18,color=INK,weight=400,anchor='middle'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(t)}</text>'
def rect(x,y,w,h,c='#fff',stroke='#cbd5e1',r=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{stroke}"/>'
def line(x,y,X,Y,color=MUTED,arrow=False):return f'<path d="M{x} {y} L{X} {Y}" stroke="{color}" stroke-width="2" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def save(name,title,subtitle,body):
    s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" font-family="Arial, sans-serif">'
    s+='<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#52647a"/></marker></defs>'
    s+=rect(0,0,960,520,'#f7fafc','#f7fafc',0)+text(32,30,'GFD  /  CLOSURE NECESSITY',12,TEAL,700,'start')+text(32,68,title,28,INK,700,'start')+text(32,98,subtitle,15,MUTED,400,'start')+body+'</svg>'
    (P/name).write_text(s,encoding='utf8')
body=rect(32,126,438,332)+rect(490,126,438,332)
body+=text(251,162,'Blind selection',22,ORANGE,700)+text(709,162,'Sufficient registered read',22,TEAL,700)
for yy,label in [(208,'Neighbor y₁'),(306,'Neighbor y₂')]:
    body+=rect(52,yy,142,50,'#fff7ed','#fdba74')+text(123,yy+30,label,16)+line(194,yy+25,240,275,arrow=True)
body+=rect(242,244,200,62,'#fff7ed','#fdba74')+text(342,269,'Same state x₀',18,ORANGE,700)+text(342,291,'cannot satisfy both',15)
body+=text(251,406,'Impossible if C₁ ∩ C₂ = ∅',18,ORANGE,700)
for yy,label,out in [(208,'Neighbor y₁','S(y₁)'),(306,'Neighbor y₂','S(y₂)')]:
    body+=rect(508,yy,116,50,'#ecfeff','#99d8d1')+text(566,yy+30,label,14)+line(624,yy+25,650,yy+25,arrow=True)+rect(655,yy,99,50,'#eef2ff','#a5b4fc')+text(705,yy+30,'R(y)',16,BLUE,700)+line(754,yy+25,782,yy+25,arrow=True)+rect(786,yy,122,50,'#ecfdf5','#86efac')+text(847,yy+30,out,17,TEAL,700)
body+=text(709,406,'Same read ⇒ same required settlement',17,TEAL,700)+text(480,490,'Compatibility requires access to relevant information, not necessarily every raw variable.',16,MUTED)
save('necessity_01_read.svg','Closure cannot be blind to relevant information','The feasibility criterion and the exact factorization test',body)
body='<ellipse cx="480" cy="280" rx="427" ry="150" fill="#f0fdfa" stroke="#0f766e" stroke-width="2" stroke-dasharray="7 5"/>'
body+='<circle cx="360" cy="267" r="116" fill="#dbeafe" fill-opacity=".8" stroke="#2563eb" stroke-width="2"/><circle cx="600" cy="267" r="116" fill="#fef3c7" fill-opacity=".8" stroke="#b45309" stroke-width="2"/>'
body+=text(360,221,'Child A',22,BLUE,700)+text(600,221,'Child B',22,ORANGE,700)+text(360,250,'W_A(g)',22)+text(600,250,'W_B(g)',22)
body+=line(377,281,455,281,arrow=True)+line(583,302,505,302,arrow=True)+rect(455,261,50,60,'#fff','#0f766e')+text(480,296,'g*',20,TEAL,700)
body+=text(480,367,'∂W_A/∂g + ∂W_B/∂g = 0',21,TEAL,700)+text(480,410,'Parent registers the reduced boundary action',18,TEAL,700)+text(480,475,'Influences may overlap; owned source inventory is counted only once.',17,MUTED)
save('necessity_02_registration.svg','Mutual inclusion and shared settlement','Schematic fixed-domain interface; not a spatial TetA–TetB tunnel',body)
body=rect(32,130,270,294)+rect(345,130,270,294)+rect(658,130,270,294)
for x,tt,lines,c in [(167,'READ',['Neighbor data a, b','Coupling c(r)','Shared constraint'],BLUE),(480,'SETTLE',['∂E/∂x = 0','x* = (ka+cb)/(k+c)','E* = kc(a−b)²/2(k+c)'],TEAL),(793,'RESPOND',['Change separation r','F = −dE*/dr','Sign depends on c′(r)'],ORANGE)]:
    body+=text(x,177,tt,20,c,700)
    for i,l in enumerate(lines):body+=text(x,240+i*48,l,16,INK)
body+=line(302,277,345,277,arrow=True)+line(615,277,658,277,arrow=True)+text(480,470,'Counterexample: E = (x−r)²/2 settles at x=r, but E*=0 and F=0.',17,MUTED)
save('necessity_03_force.svg','Force from the variation of closure','The envelope identity connects settlement to conservative mechanical response',body)
