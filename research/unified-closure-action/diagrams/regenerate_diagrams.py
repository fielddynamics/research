from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg, math
out=Path(__file__).resolve().parent
blue='#3182ce'; teal='#0d9488'; gold='#d97706'; purple='#8b5cf6'; ink='#17283d'; gray='#64748b'; pale='#f1f5f9'
class SVG:
 def __init__(self,w,h,title):
  self.w=w;self.h=h;self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{escape(title)}</title><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="{gray}"/></marker></defs><rect width="100%" height="100%" fill="white"/>'];self.text(w/2,30,title,19,bold=True)
 def text(self,x,y,t,s=14,c=ink,bold=False,anchor='middle'):
  self.a.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{s}" fill="{c}" font-weight="{600 if bold else 400}" text-anchor="{anchor}">{escape(str(t))}</text>')
 def line(self,x,y,X,Y,c=gray,sw=1.4,arrow=False,op=1):self.a.append(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{c}" stroke-width="{sw}" opacity="{op}"'+(' marker-end="url(#arr)"' if arrow else '')+'/>')
 def rect(self,x,y,w,h,c=gray,fill=None,op=.10,r=7):self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" stroke="{c}" fill="{fill or c}" fill-opacity="{op}"/>')
 def circle(self,x,y,r,c=ink,op=1):self.a.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" fill-opacity="{op}"/>')
 def path(self,d,c,op=.08):self.a.append(f'<path d="{d}" stroke="{c}" stroke-width="2" stroke-linejoin="round" fill="{c}" fill-opacity="{op}"/>')
 def box(self,x,y,w,h,title,sub='',c=gray):
  self.rect(x,y,w,h,c); self.text(x+w/2,y+(h/2 if sub else h/2+5),title,16,bold=True); 
  if sub:self.text(x+w/2,y+h/2+21,sub,12,c=gray)
 def save(self,name):
  p=out/(name+'.svg');p.write_text(''.join(self.a)+'</svg>');cairosvg.svg2png(url=str(p),write_to=str(p.with_suffix('.png')),scale=2)
def tetra(s,cx,y,scale=1):
 def P(x,Y):return f'{cx+x*scale} {y+Y*scale}'
 for pts,c in [([(0,0),(-85,107),(85,107),(0,0),(0,75),(-85,107),(0,75),(85,107)],blue), ([(0,130),(-85,23),(85,23),(0,130),(0,55),(-85,23),(0,55),(85,23)],gold)]:s.path('M'+' L'.join(P(*p) for p in pts),c)
 s.circle(cx,y+65*scale,4)
# 1 butterflies
s=SVG(720,390,'Eight-channel FWHT — three subcycles')
for j,c in enumerate([teal,blue,purple]):
 x=40+j*235;s.rect(x,58,170,280,c,op=.05);s.text(x+85,82,f'Cycle {j+1}',15,bold=True)
 for i in range(8):
  y=105+i*29;s.line(x+20,y,x+150,y,gray,1,op=.4)
  if not i&(1<<j):
   k=i^(1<<j);Y=105+k*29;s.line(x+20,y,x+150,Y,c,1.8);s.line(x+20,Y,x+150,y,c,1.8)
  s.circle(x+20,y,3);s.circle(x+150,y,3)
  if j<2:s.line(x+150,y,x+255,y,gray,1,op=.35)
 s.text(x+85,326,'4 pairings',12)
s.text(360,367,'8 = 2³ channels · 12 butterfly pairings in total',14);s.save('01_eight_channel_fwht')
# 2 initial engine
s=SVG(660,570,'Dual-tetrad phase read and settlement');tetra(s,330,50,.85);s.text(330,180,'Eight outer vertex channels (schematic)',13,c=gray)
s.line(330,190,330,211,arrow=True);s.box(120,220,420,64,'π phase walk','Geometric read and sign inversion');s.line(330,284,330,314,arrow=True)
for i,(n,c) in enumerate(zip(['Faces','Subfaces','Subchannels'],[blue,teal,gold])):s.box(30+i*205,324,190,76,f'{i+1} · {n}','4 pairings',c)
s.line(330,400,330,446,arrow=True);s.box(120,454,420,76,'Field registration and settlement','Completed candidate closure cycle');s.save('02_dual_tetrad_phase_engine')
# 3 tree
s=SVG(960,420,'Three-level face / subface / subchannel hierarchy');s.box(410,50,140,36,'Origin');
for a in range(4):
 x=120+240*a;s.line(480,86,x,122);s.box(x-34,122,68,32,f'{a+1}',c=blue)
 for b in range(4):
  X=30+240*a+60*b;s.line(x,154,X,206,op=.7);s.rect(X-13,206,26,24,teal,op=.25)
  for c in range(4):
   xx=9+240*a+60*b+14*c;s.line(X,230,xx,281,op=.55);s.circle(xx,284,3,gold)
s.text(480,315,'64 terminal records',15,bold=True);s.text(480,345,'1 + 4 + 16 = 21 internal readers',18,bold=True)
for x,n,l,c in [(160,'4','Primary faces',blue),(480,'16','Subfaces',teal),(800,'64','Subchannels',gold)]:s.text(x,380,n,20,c,True);s.text(x,400,l,13)
s.save('03_recursive_address_tree')
# 4 attenuation
s=SVG(700,430,'Candidate collective closure transmission')
for i,(n,l,p,c) in enumerate([(16,'Subchannel settlement','α¹⁶',gold),(4,'Subface settlement','α⁴',teal),(1,'Primary face settlement','α',blue)]):
 y=66+i*92;s.text(30,y,l,16,bold=True,anchor='start');s.text(655,y+30,p,26,bold=True,anchor='end')
 for j in range(n):s.rect(30+j*25,y+12,19,26,c,op=.7,r=2)
 s.text(30,y+57,f'{n} invariant channel'+('s' if n!=1 else ''),12,gray,anchor='start')
 if i<2:s.line(350,y+43,350,y+83,arrow=True)
s.line(25,338,675,338);s.text(350,370,'α¹⁶ × α⁴ × α = α²¹',24,bold=True);s.text(350,401,'1.33804868 × 10⁻⁴⁵  ·  conditional collective power',15);s.save('04_collective_attenuation')
# 5 triangle
s=SVG(650,405,'Solid-angle registration on a tetrahedral face');s.path('M190 57 L32 331 L348 331 Z',blue,.12);s.path('M111 194 L269 194 L190 331 Z',gold,.27)
for x,y in [(190,150),(110,288),(269,288)]:s.text(x,y,'π/6',24)
s.text(190,245,'π/2',26,bold=True);s.text(492,105,'One face',16);s.text(492,141,'π sr',32,bold=True);s.rect(410,182,18,18,gold,op=.4);s.text(441,196,'Central tile',15,anchor='start');s.rect(410,219,18,18,blue,op=.3);s.text(441,233,'Lateral tiles',15,anchor='start');s.text(325,373,'Equal Euclidean areas do not imply equal radial flux.',14,c=gray);s.save('05_triforce_solid_angles')
# 6 weighted engine
s=SVG(760,815,'Unified three-subcycle settlement engine');tetra(s,380,48,.8);s.text(380,177,'Eight vortices · 64 relational coordinates',14,c=gray)
for y,t,sub in [(206,'π-addressed phase read','Candidate addressing and phase schedule'),(305,'Three recursive subcycles','4 × 4 × 4 = 64')]:s.line(380,y-25,380,y-4,arrow=True);s.box(135,y,490,70,t,sub)
s.line(380,375,380,405,arrow=True);s.box(35,414,330,84,'1 common mode','Conserved registration',blue);s.box(395,414,330,84,'21 contrast modes','Collective attenuation',gold);s.line(200,498,380,535,arrow=True);s.line(560,498,380,535,arrow=True);s.box(130,546,500,74,'Settlement action','G = c⁴ λ² / (4πκ)');s.line(380,620,380,654,arrow=True)
for i,(n,l) in enumerate([('G','Gravity'),('mₑ','Matter'),('a₀','Closure threshold')]):s.box(25+i*240,665,230,80,n,l)
s.text(380,785,'Physical selection of the read remains an open requirement.',13,c=gray);s.save('06_weighted_unified_engine')
# 7 face pairs
s=SVG(640,445,'Four-face relational settlement — TetB diagonal read')
for i in range(4):
 s.text(170+i*65,68,f'F{i+1}',15);s.text(105,115+i*65,f'F{i+1}',15)
 for j in range(4):
  c=gray if i==j else teal;s.rect(141+j*65,83+i*65,58,58,c,op=.15 if i==j else .25);s.text(170+j*65,119+i*65,0 if i==j else 1,22,bold=True)
s.circle(170,365,15,blue,.25);s.text(170,370,'1',16,bold=True);s.text(195,370,'Independent Field Origin',15,anchor='start');s.text(320,410,'(12 + 1) / (16 + 1) = 13/17',24,bold=True);s.save('07_face_pair_exchange')
# 8 static balance graph
s=SVG(690,400,'Closure balance — origin weighting fixed at 1/17');left=80;top=75;w=540;h=250
for y in [0,.25,.5,.75,1]:
 Y=top+h*(1-y);s.line(left,Y,left+w,Y,gray,1,op=.25);s.text(left-12,Y+4,f'{y:.2f}',12,anchor='end')
for p in [0,25,50,75,100]:
 X=left+w*p/100;s.text(X,top+h+23,f'{p}%',12)
s.line(left,top,left+w,top+h*16/17,blue,3);x=left+w*.25;y=top+h*(1-13/17);s.line(x,y,x,top+h,gray,1,op=.6);s.circle(x,y,6,teal);s.text(x+20,y-12,'Balanced: 13/17',14,teal,True,anchor='start');s.text(350,380,'Self-pair share p · stiffness ratio = 1 − (16/17)p',14);s.save('08_closure_balance')
# 9 final engine
s=SVG(780,730,'Microscopic stiffness and complete mathematical architecture')
s.box(125,56,530,68,'Field Origin and dual-tetrad geometry','Original 36-coordinate Hamiltonian');s.line(390,124,390,153,arrow=True);s.box(125,163,530,65,'π-walk and FWHT','Candidate balanced geometric read');s.line(390,228,390,259,arrow=True)
s.box(25,270,355,100,'Collective transmission','α^(1 + 4 + 16)  ·  21 contrast factors',gold);s.box(400,270,355,100,'Structural stiffness','(1 + 16 − 4)/(1 + 16) = 13/17',teal);s.line(202,370,390,412,arrow=True);s.line(577,370,390,412,arrow=True);s.box(110,424,560,85,'Gravitational settlement','G = (17/13) α²¹ ℏc / mₑ²');s.line(390,509,390,546,arrow=True);s.box(110,558,560,98,'Electron closure','a₀ = 16Gmₑ/Rₑ²  ·  mₑc² = αℏc/Rₑ');s.text(390,695,'Conditional architecture, not an independent physical derivation.',14,c=gray);s.save('09_microscopic_stiffness_engine')
