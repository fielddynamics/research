from pathlib import Path
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, FancyArrowPatch, Wedge, Ellipse
from itertools import combinations,product
root=Path(__file__).resolve().parent.parent; out=root/'additional_visuals';out.mkdir(exist_ok=True)
blue='#2563a6'; teal='#087e83'; gold='#bd741b'; purple='#8058a3'; ink='#23364b'; pale='#edf3f8'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':ink,'axes.labelcolor':ink,'svg.fonttype':'none','font.size':12})
def canvas(title,subtitle='',size=(10,6)):
 f,a=plt.subplots(figsize=size); f.patch.set_facecolor('white');a.set(xlim=(0,10),ylim=(0,6));a.axis('off');f.text(.06,.95,title,fontsize=19,weight='bold',color=ink);f.text(.06,.895,subtitle,fontsize=10.5,color='#52667a');return f,a
def save(f,name):
 for ext in ['svg','png']:f.savefig(out/(name+'.'+ext),dpi=200,bbox_inches='tight',pad_inches=.25,facecolor='white')
 plt.close(f)
def box(a,x,y,w,h,t,sub='',c=blue):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04,rounding_size=.12',fc=pale,ec=c,lw=1.5));a.text(x+w/2,y+h*(.62 if sub else .5),t,ha='center',va='center',weight='bold',fontsize=12,color=c)
 if sub:a.text(x+w/2,y+h*.27,sub,ha='center',va='center',fontsize=10)
def arrow(a,x,y,X,Y):a.add_patch(FancyArrowPatch((x,y),(X,Y),arrowstyle='-|>',mutation_scale=13,color='#7b8b9c',lw=1.4))
def trigram(a,n,x,y,w=.65,h=.13,gap=.09,nbits=3):
 for j in range(nbits):
  yy=y-j*(h+gap); bit=(n>>j)&1
  if bit:a.add_patch(Rectangle((x-w/2,yy),w,h,fc=ink,ec='none'))
  else:
   for xx in (x-w/2,x+.08*w):a.add_patch(Rectangle((xx,yy),.42*w,h,fc=ink,ec='none'))
# 18 cube
f,a=canvas('Trigrams and the stellated octahedron','Octal address = three binary coordinates; complementary addresses sum to seven.')
coords=np.array([[2.0+2.9*((n>>2)&1)+1.25*((n>>1)&1),.85+2.55*(n&1)+1.0*((n>>1)&1)] for n in range(8)])
for i,j in combinations(range(8),2):
 if (i^j).bit_count()==1:a.plot(*coords[[i,j]].T,color='#a8b7c5',lw=1,zorder=0)
for parity,c in [(1,blue),(0,gold)]:
 ids=[n for n in range(8) if n.bit_count()%2==parity]
 for i,j in combinations(ids,2):a.plot(*coords[[i,j]].T,color=c,lw=1.8,alpha=.7)
names=['Earth','Mountain','Water','Wind','Thunder','Fire','Lake','Heaven']
for n,(x,y) in enumerate(coords):
 a.scatter(x,y,s=105,color=blue if n.bit_count()%2 else gold,zorder=4);a.text(x,y+.23,f'{n} · {names[n]}',ha='center',fontsize=10,weight='bold')
for i,n in enumerate([0,1,2,3,4,5,6,7]):
 y=4.85-i*.55;trigram(a,n,7.0,y,w=.48,h=.08,gap=.06);a.text(7.43,y-.10,f'{n:03b}  {names[n]}',fontsize=10,va='center')
a.text(3.95,.22,'TetA: odd parity     TetB: even parity',ha='center',color=ink)
save(f,'18_iching_trigram_cube')
# 19 hexagram wheel
f,a=canvas('Circular I Ching address space','Illustrative binary ordering of all 64 hexagrams; not a claim about the historic ordering.',(9,7));a.set_aspect('equal');a.set(xlim=(0,10),ylim=(0,7.5));cx,cy=5,3.75
for r in (2.35,3.25):a.add_patch(Circle((cx,cy),r,fill=False,ec='#a5b2bf',lw=.8))
for n in range(64):
 theta=np.pi/2-n*2*np.pi/64; radial=np.array([np.cos(theta),np.sin(theta)]);tan=np.array([-radial[1],radial[0]])
 for j in range(6):
  p=np.array([cx,cy])+(3.05-j*.095)*radial
  spans=[(-.105,.105)] if (n>>j)&1 else [(-.105,-.023),(.023,.105)]
  for l,r in spans:
   xy=np.array([p+l*tan,p+r*tan]);a.plot(*xy.T,color=ink,lw=1.15,solid_capstyle='butt')
for tri,c in [([(5,5.5),(3.5,2.8),(6.5,2.8)],blue),([(5,2),(3.5,4.7),(6.5,4.7)],gold)]:
 p=np.array(tri+[tri[0]]);a.plot(*p.T,color=c,lw=2);a.fill(*p.T,color=c,alpha=.07)
a.scatter(cx,cy,s=42,c=ink);a.text(cx,.15,'8 × 8 ordered pairs = 64 hexagrams',ha='center',weight='bold');save(f,'19_iching_hexagram_wheel')
# 20 three pairs
f,a=canvas('Three paired binary reads','Reorder two trigrams into three coordinate pairs: (aₓ,bₓ), (aᵧ,bᵧ), (a_z,b_z).')
for i,axis in enumerate(['X axis','Y axis','Z axis']):
 x=1.8+3.2*i;box(a,x-1.35,1.1,2.7,3.9,'','', [blue,teal,gold][i]);a.text(x,4.2,axis,ha='center',weight='bold',color=[blue,teal,gold][i]);
 for j,n in enumerate(range(4)):
  y=3.7-.67*j;trigram(a,n,x-.3,y,w=.7,h=.13,gap=.08,nbits=2);a.text(x+.35,y-.05,f'{n:02b}',va='center')
a.text(5,.45,'4 × 4 × 4 = 64 terminal addresses',ha='center',fontsize=16,weight='bold');save(f,'20_paired_binary_reads')
# 21 wedges
f,a=canvas('Three angular axis sweeps','Each read vector has four increments totaling eight sectors; one sector = π/4.')
a.set_aspect('equal');a.set(xlim=(0,10),ylim=(0,6))
for i,v in enumerate([[3,3,1,1],[3,1,3,1],[3,1,1,3]]):
 x=1.75+i*3.25;y=3.2;start=90
 for j,d in enumerate(v):
  end=start-45*d;c=[blue,teal,gold,purple][j];a.add_patch(Wedge((x,y),1.30,end,start,fc=c,alpha=.24,ec=c,lw=1.5));ang=np.deg2rad((start+end)/2);a.text(x+.83*np.cos(ang),y+.83*np.sin(ang),str(d),ha='center',va='center',weight='bold');start=end
 a.add_patch(Circle((x,y),.09,fc=ink));a.text(x,1.58,['X read','Y read','Z read'][i],ha='center',weight='bold');a.text(x,1.22,str(v),ha='center',fontsize=11)
a.text(5,.53,'Each full sweep = 2π',ha='center',fontsize=15,weight='bold');save(f,'21_three_axis_sector_sweeps')
# 22 carry circuit, order high to low
f,a=canvas('Circular increment as a binary carry circuit','Toffoli → controlled NOT → NOT. Exact increment modulo eight; not a Hadamard transform.')
ys=[4.6,3.1,1.6]
for i,y in enumerate(ys):a.plot([1.2,9], [y,y],color=ink,lw=1.5);a.text(.7,y,f'b{2-i}',va='center',ha='center');a.text(9.4,y,f'b{2-i}′',va='center')
for x,control,target,c in [(3,[1,2],0,gold),(5.5,[2],1,teal),(8,[],2,blue)]:
 if control:a.plot([x,x],[ys[target],ys[max(control)]],color=c,lw=2)
 for i in control:a.add_patch(Circle((x,ys[i]),.085,fc=c,ec=c))
 a.add_patch(Circle((x,ys[target]),.20,fc='white',ec=c,lw=2));a.plot([x-.16,x+.16],[ys[target]]*2,c=c,lw=2);a.plot([x,x],[ys[target]-.16,ys[target]+.16],c=c,lw=2)
for x,t in [(3,'Double carry'),(5.5,'Single carry'),(8,'Inversion')]:a.text(x,.65,t,ha='center',fontsize=12,weight='bold')
save(f,'22_binary_carry_circuit')
# 23 physical sweep visual
f,a=canvas('Three circular averages around the field','Averaging over each full rotation suppresses angular structure; endpoint rotation alone does not.')
for i in range(3):
 x=1.7+3.3*i;y=3.5;a.add_patch(Circle((x,y),1.15,fc=pale,ec='#a8b7c5'));p=np.array([(x,y+.85),(x-.78,y-.55),(x+.78,y-.55),(x,y+.85)]);a.plot(*p.T,c=blue,lw=1.5);p[:,1]=2*y-p[:,1];a.plot(*p.T,c=gold,lw=1.5);a.add_patch(Ellipse((x,y),2.45,.8,angle=[0,60,120][i],fill=False,ec=[blue,teal,gold][i],lw=2.2,ls='--'));a.scatter(x,y,s=24,c=ink);a.text(x,2.08,['X average','Y average','Z average'][i],ha='center',weight='bold');arrow(a,x,1.85,5,.95)
a.text(5,.58,'Monopole preserved · anisotropic harmonics contracted',ha='center',fontsize=13,weight='bold');save(f,'23_perpendicular_angular_averages')
# 24 rotation quotient
f,a=canvas('TIME-axis quotient and the 21-mode target','A physical 120° cube rotation gives 24 orbits. Two extra axial identifications are hypothetical.')
box(a,3.4,4.75,3.2,.75,'64 ordered records');arrow(a,5,4.75,5,4.28);box(a,.7,3.35,4.0,.85,'20 three-element orbits','60 original records',teal);box(a,5.3,3.35,4.0,.85,'4 fixed axial records','00, 07, 70, 77',gold);arrow(a,5,4.28,2.7,4.2);arrow(a,5,4.28,7.3,4.2);arrow(a,7.3,3.35,7.3,2.8);box(a,5.3,1.9,4.0,.85,'2 axial identifications','00 = 77; 07 = 70',gold);arrow(a,2.7,3.35,2.7,1.9);arrow(a,7.3,1.9,5.2,1.45);arrow(a,2.7,1.9,4.8,1.45);box(a,2.5,.35,5,1.0,'22 invariant coordinates','1 common scalar + 21 contrasts',blue);save(f,'24_time_axis_quotient')
# 25 recursive registration
f,a=canvas('Recursive field registration','Static domain decomposition with disjoint owned interiors and common interface traces.')
for i in range(4):
 x=1.25+2.5*i;y=4.65
 for r in [.52,.33,.10]:a.add_patch(Circle((x,y),r,fill=r==.10,ec=blue,fc=blue if r==.10 else 'none',lw=1.3))
 arrow(a,x,4.1,2.5 if i<2 else 7.5,3.3)
for x in [2.5,7.5]:
 for r in [.65,.40,.13]:a.add_patch(Circle((x,2.65),r,fill=r==.13,ec=teal,fc=teal if r==.13 else 'none',lw=1.4))
 arrow(a,x,1.95,5,1.35)
for r in [.7,.45,.14]:a.add_patch(Circle((5,.75),r,fill=r==.14,ec=gold,fc=gold if r==.14 else 'none',lw=1.4))
a.text(5,3.9,'Boundary response records',ha='center',fontsize=11);a.text(5,1.85,'Compose and match flux',ha='center',fontsize=11);save(f,'25_recursive_boundary_registration')
# 26 feedback
f,a=canvas('Proposed π–Walsh settlement feedback','Separate exact mathematical operations from the open physical identification.')
items=[('Stellated geometry','Three axis vectors'),('BBP resonator','Octal π output'),('I Ching traversal','64 ordered addresses'),('Walsh phase read','Three paired coordinates'),('Boundary settlement','Common charge + contrast read')]
for i,(t,s) in enumerate(items):
 y=5.05-i*1.06;box(a,2.1,y,5.8,.78,t,s,[blue,teal,gold,purple,blue][i]);
 if i:arrow(a,5,y+1.06,5,y+.78)
a.add_patch(FancyArrowPatch((7.95,1.23),(7.95,5.45),connectionstyle='arc3,rad=-.6',arrowstyle='-|>',mutation_scale=13,color='#8999a9',lw=1.5,ls='--'));a.text(9.0,3.4,'Candidate\nfeedback',ha='center',fontsize=10);save(f,'26_pi_walsh_feedback')
# 27 phase sweep and gravity diagram
f,a=canvas('Internal phase sweep and external gravitational read','Conditional mechanism: angular averaging + independently established Gauss flux law.')
a.set_aspect('equal');a.set(xlim=(0,10),ylim=(0,6))
x,y=3,3.25
for r in [2.05,1.75,1.45]:a.add_patch(Circle((x,y),r,fill=False,ec=blue,alpha=.32))
for angle,c in [(-28,teal),(32,gold),(90,purple)]:a.add_patch(Ellipse((x,y),3.85,1.3,angle=angle,fill=False,ec=c,lw=2,ls='--'))
for sign,c in [(1,blue),(-1,gold)]:
 p=np.array([(x,y+sign*.98),(x-.9,y-sign*.63),(x+.9,y-sign*.63),(x,y+sign*.98)]);a.plot(*p.T,c=c,lw=1.7)
a.scatter(x,y,c=ink,s=30);a.text(3,.65,'Internal angular read',ha='center',weight='bold');arrow(a,5.2,3.25,6.15,3.25)
for r in [.55,1,1.42]:a.add_patch(Circle((7.95,3.25),r,fill=False,ec=blue,alpha=.55))
for th in np.linspace(0,2*np.pi,12,endpoint=False):
 u=np.array([np.cos(th),np.sin(th)]);p=np.array([7.95,3.25]);arrow(a,*(p+1.42*u),*(p+.32*u))
a.scatter(7.95,3.25,c=ink,s=38);a.text(7.95,.65,'External monopole',ha='center',weight='bold');save(f,'27_phase_sweep_external_field')
