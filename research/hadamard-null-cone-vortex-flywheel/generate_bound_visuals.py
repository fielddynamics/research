"""Regenerate static Markdown companions to the recent chat diagrams.
All arrows in the conceptual schematics are illustrative, not particle paths.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT=Path(__file__).resolve().parent/'figures'; OUT.mkdir(exist_ok=True)
A='#2676b9'; B='#bd692c'; G='#14867a'; INK='#203347'; GRAY='#62748a'; PURPLE='#7552ae'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':INK,'text.color':INK,'axes.edgecolor':'#9daab8','xtick.color':INK,'ytick.color':INK,'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',pad_inches=.18); plt.close(fig)
def canvas(size=(10,5),x=(0,10),y=(0,5)):
    fig,ax=plt.subplots(figsize=size); ax.set(xlim=x,ylim=y,aspect='equal'); ax.axis('off'); return fig,ax
def arrow(ax,a,b,color=G,lw=2,rad=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=15,color=color,lw=lw,connectionstyle=f'arc3,rad={rad}'))
def label(ax,x,y,s,**kw): ax.text(x,y,s,ha=kw.pop('ha','center'),va=kw.pop('va','center'),**kw)
def box(ax,x,y,w,h,txt,color=G):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=.08',fc='white',ec=color,lw=1.5));label(ax,x,y,txt,fontsize=10)
def ring(ax,c,ang,r,color,reverse=False):
    d=np.array([np.cos(ang),np.sin(ang)]); p=np.array([-d[1],d[0]]); t=np.linspace(0,1,100)
    for k in range(3):
        xy=np.array(c)[:,None]+d[:,None]*(r*(.22+.78*t))+p[:,None]*(r*(.025+.135*t)*np.sin((-1 if reverse else 1)*t*12+2*np.pi*k/3)); ax.plot(*xy,color=color,lw=1.35)
    arrow(ax,np.array(c)+d*r*.83,np.array(c)+d*r*.48,color,1.3)
def flywheel(ax,c,r,core=True):
    for i,ang in enumerate(np.arange(8)*np.pi/4+np.pi/8):ring(ax,c,ang,r,A if i%2==0 else B)
    ax.add_patch(Circle(c,r*.13,fc='white',ec=G,lw=1.8)); label(ax,*c,'O',fontsize=9,fontweight='bold')
# Capture schematic
fig,ax=canvas((9.5,5.4),(0,10),(0,5.7));label(ax,5,5.45,'Stellar-forge capture: proposed transition',fontsize=17,fontweight='bold')
flywheel(ax,(2.2,3.05),1.35);label(ax,2.2,1.42,'Incoming complete cell',fontweight='bold');arrow(ax,(3.62,3.05),(5.4,3.05),GRAY,2.6);label(ax,4.52,3.55,'External\ncompression',fontsize=10)
flywheel(ax,(7.6,3.05),1.85);ax.add_patch(Circle((7.6,3.05),.5,fc='#fff1df',ec=B,ls='--',lw=1.8));
for k in range(8):
    th=k*np.pi/4;ax.plot([7.6+.15*np.cos(th),7.6+.38*np.cos(th+.35)],[3.05+.15*np.sin(th),3.05+.38*np.sin(th+.35)],color=B,lw=1.8)
arrow(ax,(7.6,3.59),(8.55,4.05),B,2,rad=-.2);arrow(ax,(7.6,2.51),(6.65,2.05),B,2,rad=-.2)
label(ax,7.6,.95,'Receiver with occupied TetB',fontweight='bold');label(ax,7.6,.55,'Return pressure / outward response',fontsize=10);label(ax,5,.1,'[E] Schematic only: whole-cell capture and retention have not been demonstrated.',fontsize=10,color=GRAY);save(fig,'13_stellar_forge_capture')
# two regimes
fig,ax=canvas((10,5.2),(0,10),(0,5.1));label(ax,5,4.88,'Two regimes of the same eight-vortex geometry',fontsize=16,fontweight='bold')
for x,bound in [(2.5,False),(7.5,True)]:
    flywheel(ax,(x,2.65),1.45)
    if bound:
        ax.add_patch(Circle((x,2.65),.4,fc='#fff2e2',ec=B,ls='--',lw=1.8));label(ax,x,2.65,'TetB',fontsize=9,fontweight='bold');arrow(ax,(x+.43,2.65),(x+1.35,2.65),B,2.5);arrow(ax,(x-.43,2.65),(x-1.35,2.65),B,2.5)
    else: arrow(ax,(x,2.46),(x,1.04),G,2.5)
    label(ax,x,.73,'Bound configuration' if bound else 'Propagating configuration',fontweight='bold',fontsize=13);label(ax,x,.35,'Retained occupation + return response' if bound else 'Exchange through the directional throat',fontsize=10)
ax.plot([5,5],[.3,4.4],color='#dce3eb');save(fig,'14_propagating_vs_bound')
# comparison chart, including residual capacity with visible scale
fig,axs=plt.subplots(1,2,figsize=(11,4.1)); a=np.geomspace(1,256,512); rem1=1/(1+a*a); rem2=2/(1+np.sqrt(1+4*a*a));
for ax in axs:
    ax.set_xscale('log');ax.set_xticks([1,4,16,64,256],labels=['1','4','16','64','256']);ax.set_xlabel('Mass number A (assume x = A²)');ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
axs[0].plot(a,1-rem1,color=A,lw=2.5,label='One-directional μ');axs[0].plot(a,1-rem2,color=B,lw=2.5,label='Bound μᵦ');axs[0].set(ylabel='Active fraction',ylim=(.32,1.02));axs[0].legend(loc='lower right',frameon=False,fontsize=9)
axs[1].loglog(a,rem1,color=A,lw=2.5,label='~ A⁻²');axs[1].loglog(a,rem2,color=B,lw=2.5,label='~ A⁻¹');axs[1].set_ylabel('Remaining fraction');axs[1].legend(frameon=False,fontsize=10)
fig.suptitle('Same capacity, different saturation under the nuclear compression premise',fontsize=15,fontweight='bold');fig.tight_layout();save(fig,'15_bound_law_comparison')
# nesting hierarchy, 4 groups of 16, 4 subgroups of 4
fig,ax=canvas((10,8),(0,10),(0,8));label(ax,5,7.72,'Fourfold nesting: 4 × 4 × 4 = 64 field addresses',fontsize=16,fontweight='bold');
for g in range(4):
    gx=.55+(g%2)*4.65;gy=1.0+(1-g//2)*3.05
    ax.add_patch(FancyBboxPatch((gx,gy),4.2,2.75,boxstyle='round,pad=.07',fc='#f3f8fb',ec=GRAY,lw=1.2));label(ax,gx+2.1,gy+2.52,f'Group {g+1} · 16 fields',fontsize=11,fontweight='bold')
    for h in range(4):
        hx=gx+.25+(h%2)*1.92;hy=gy+.18+(1-h//2)*1.05
        ax.add_patch(FancyBboxPatch((hx,hy),1.77,.93,boxstyle='round,pad=.02',fc='white',ec=G,lw=1));
        for q in range(4):
            cx=hx+.25+q*.42;cy=hy+.47;r=.145
            for flip,col in [(1,A),(-1,B)]:
                v=np.array([[0,flip*r],[-.866*r,-flip*r/2],[.866*r,-flip*r/2]])+[cx,cy];ax.add_patch(Polygon(v,closed=True,fc='none',ec=col,lw=1.1))
            ax.add_patch(Circle((cx,cy),.025,fc=G,ec='none'))
label(ax,5,.63,'16 groups of four  •  Four groups of sixteen  •  One complete sector of 64',fontsize=11);label(ax,5,.24,'[E] Hierarchical addresses, not a proved spatial packing or capture trajectory.',fontsize=10,color=GRAY);save(fig,'16_recursive_nesting')
# actual directional tetrahedral ports and local face matching (exact geometry)
s=np.array([1,1,1]); v=np.array([[1,1,-1],[1,-1,1],[-1,1,1]],float); m=(v+np.roll(v,-1,axis=0))/2; tiles=[np.array([v[i],m[i],m[(i-1)%3]]) for i in range(3)]+[m]; R=np.eye(3)-2*np.outer(s,s)/3; o2=2*s/3
fig=plt.figure(figsize=(10,5.5)); ax=fig.add_subplot(111,projection='3d');ax.set_proj_type('ortho');ax.view_init(elev=12,azim=5)
for i,t in enumerate(tiles):ax.add_collection3d(Poly3DCollection([t],facecolor=G if i==3 else A,edgecolor='white',alpha=.7,linewidth=2))
for o,col,n in [(np.zeros(3),A,'O₁'),(o2,B,'O₂')]:
    ax.scatter(*o,color=col,s=90,depthshade=False);ax.text(*(o+np.array([0,0,.12])),n,fontsize=14,color=col,fontweight='bold')
    for p in v:ax.plot(*np.stack([o,p]).T,color=col,alpha=.5,lw=1.5)
    ax.plot(*np.stack([o,m.mean(axis=0)]).T,color=G,lw=3,ls='--')
for p in v:ax.scatter(*p,color=INK,s=18)
ax.set(xlim=(-1.03,1.03),ylim=(-1.03,1.03),zlim=(-1.03,1.03));ax.set_box_aspect([1,1,1]);ax.set_axis_off();fig.suptitle('Matched Triforce interface: four triangles fixed by reflection',fontsize=16,fontweight='bold');fig.text(.5,.08,'O₁ → central tile₁ → central tile₂ → O₂  |  Lateral tiles provide additional paths.',ha='center',fontsize=11);fig.text(.5,.035,'Coincident face geometry; the two cells retain distinct tile amplitudes. Not a global tessellation proof.',ha='center',fontsize=9,color=GRAY);save(fig,'17_matched_triforce_interface')
# port read diagram
fig,ax=canvas((9,5),(0,10),(0,5));label(ax,5,4.72,'Eight central triangle records, one directional Field Origin',fontsize=15,fontweight='bold')
for i,sg in enumerate([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1),(-1,-1,-1),(-1,1,1),(1,-1,1),(1,1,-1)]):
    side=i//4; j=i%4;x=1.35+7.3*side;y=3.9-.86*j;col=A if side==0 else B;box(ax,x,y,1.8,.47,'(1, '+', '.join('+' if t>0 else '−' for t in sg)+')',col);arrow(ax,(x+(.97 if side==0 else -.97),y),(4.0 if side==0 else 6.0,2.62),col,1.1)
box(ax,5,2.62,1.9,1.1,'O: (a, bₓ, bᵧ, b_z)\nscalar + polar triplet',G);label(ax,5,.64,'TᵀT = 8I₄   |   Four independent records per chamber',fontsize=13,fontweight='bold');label(ax,5,.25,'Exact read identity; dynamical centre and normalization are model premises.',fontsize=10,color=GRAY);save(fig,'18_directional_origin_read')
# stage VIII flux
fig,ax=plt.subplots(figsize=(9,4.3));x=np.arange(8);ax.bar(x-.18,[.15]*8,.36,color=A,label='Uniform hopping');ax.bar(x+.18,[-.08066]*4+[.20728]*4,.36,color=B,label='Capacity-weight hypothesis');ax.axhline(0,color=GRAY,lw=1);ax.set_xticks(x,[f'{c}{i}' for c in 'AB' for i in range(1,5)]);ax.set_ylabel('Net inward occupation flux (model units)');ax.set_title('All eight rings feed inward with uniform hopping',fontweight='bold',fontsize=15);ax.legend(frameon=False);ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False);fig.tight_layout();save(fig,'19_chamber_flux_comparison')
# axial receiver chart
fig,ax=plt.subplots(figsize=(9,4.0)); t=np.linspace(0,10,500);g=.7;om=1.3;ax.plot(t,g*(1-np.cos(om*t)),color=G,lw=2,label='Axial momentum along C');ax.plot(t,-g/om*np.sin(om*t),color=A,lw=2,label='Receiver coordinate along C');ax.axhline(0,color=GRAY,lw=.8);ax.set(xlabel='Dimensionless model time',ylabel='Component along unit chirality',title='Closed axial receiver: conservative oscillation, not drainage');ax.legend(frameon=False);ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False);fig.tight_layout();save(fig,'20_axial_receiver')
# exact row/column labels as static counterpart
fig,ax=canvas((9,4.9),(0,10),(0,5.2));label(ax,5,4.92,'The same twelve tiles: two complementary readings',fontsize=15,fontweight='bold');colors=[A,G,B,PURPLE]
for side in [0,1]:
    x0=.9+side*5.0;y0=3.85;label(ax,x0+1.5,4.46,'Rows: local vortex rings' if side==0 else 'Columns: original Triforce faces',fontsize=12,fontweight='bold')
    for i in range(4):
        for j in range(4):
            x=x0+j*.95;y=y0-i*.77;col=colors[i if side==0 else j];ax.add_patch(FancyBboxPatch((x-.39,y-.29),.78,.58,boxstyle='round,pad=.03',fc='white' if i==j else col,alpha=.15 if i!=j else .5,ec=GRAY if i==j else col,lw=1.5));label(ax,x,y,'—' if i==j else f'X{i+1}{j+1}',fontsize=11)
    if side==0:
        for i in range(4):arrow(ax,(x0+3.33,y0-i*.77),(x0+3.65,y0-i*.77),colors[i],1);label(ax,x0+3.87,y0-i*.77,'0',fontsize=10)
    else:
        for j in range(4):arrow(ax,(x0+j*.95,1.18),(x0+j*.95,.82),colors[j],1);label(ax,x0+j*.95,.60,f'y{j+1}',fontsize=10)
label(ax,2.35,.6,'Zero row sums',fontsize=10);label(ax,5,.12,'One chamber shown; the two chambers give eight constituent rings.',fontsize=10,color=GRAY);save(fig,'21_row_column_read')
