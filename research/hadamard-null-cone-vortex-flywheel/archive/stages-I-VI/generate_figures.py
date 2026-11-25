"""Regenerate static SVG figures. Uses the integer octahedral boundary construction.
Requires numpy and matplotlib. Figures are explanatory, not new physical tests.
"""
from pathlib import Path
from itertools import combinations
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT=Path(__file__).parent/'figures'; OUT.mkdir(exist_ok=True)
S=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1],[-1,-1,-1],[-1,1,1],[1,-1,1],[1,1,-1]])
V=np.vstack((np.eye(3,dtype=int),-np.eye(3,dtype=int))); E=[(i,j) for i,j in combinations(range(6),2) if V[i]@V[j]==0]
p=np.prod(S,axis=1); W=np.column_stack((np.ones(8),S,p[:,None]*S,p)); D=np.array([[np.cross(V[i],V[j])@s if V[i]@s==V[j]@s==1 else 0 for s in S] for i,j in E]); L=np.zeros((6,12))
for e,(i,j) in enumerate(E): L[i,e]=-1;L[j,e]=1
assert np.array_equal(D.T@D@W,W@np.diag([0,2,2,2,4,4,4,6])) and np.all(L@D==0)
BLUE='#2563b0'; ORANGE='#c76b24'; TEAL='#078477'; PURPLE='#7854b4'; INK='#142536'; GREY='#718096'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.labelcolor':INK,'axes.edgecolor':'#d1d9e0','xtick.color':INK,'ytick.color':INK,'svg.fonttype':'none'})
def save(fig,name): fig.savefig(OUT/name,bbox_inches='tight',pad_inches=.22,facecolor='white');plt.close(fig)
def style(ax,lim=1.25):
 ax.set_box_aspect((1,1,1));ax.set(xlim=(-lim,lim),ylim=(-lim,lim),zlim=(-lim,lim));ax.view_init(21,34);ax.set_axis_off()
def octa(ax):
 for i,j in E: ax.plot(*V[[i,j]].T,color=TEAL,lw=1.4,alpha=.8)
def faceids(s):return np.flatnonzero(V@s==1)
fig=plt.figure(figsize=(12,6));ax=fig.add_subplot(121,projection='3d');style(ax);octa(ax)
for i,s in enumerate(S):
 col=BLUE if p[i]==1 else ORANGE; ids=faceids(s)
 for u,v in combinations(V[ids],2):ax.add_collection3d(Poly3DCollection([[s,u,v]],facecolors=col,edgecolors=col,linewidths=.65,alpha=.105))
 ax.plot(*np.array([[0,0,0],s]).T,color=col,ls=':',alpha=.6);ax.scatter(*s,color=col,s=27)
ax.set_title('Eight stellations of the Hadamard cube',fontweight='bold',pad=0)
ax=fig.add_subplot(122,projection='3d');style(ax);octa(ax)
for i,s in enumerate(S):
 ids=faceids(s);col=BLUE if p[i]==1 else ORANGE;ax.add_collection3d(Poly3DCollection([V[ids]],facecolors=col,edgecolors=col,alpha=.25));ax.scatter(*(s/3),color=col,s=13)
ax.scatter(*V.T,color=TEAL,s=30);ax.set_title('Their common octahedral core',fontweight='bold',pad=0)
fig.suptitle('One geometry: 8 triangular bases · 12 edges · 6 vertices',fontsize=17,fontweight='bold');fig.text(.5,.04,'Blue: TetA apex parity    •    Orange: TetB apex parity    •    Teal: core edges',ha='center',color=GREY);save(fig,'01_geometry.svg')
fig,axs=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={'width_ratios':[1.1,1]});ax=axs[0];im=ax.imshow(D,cmap=matplotlib.colors.ListedColormap([ORANGE,'#f2f5f8',BLUE]),vmin=-1,vmax=1,aspect='auto');ax.set_title('Oriented boundary matrix D');ax.set_xticks(range(8),['A1','A2','A3','A4','B1','B2','B3','B4']);ax.set_yticks(range(12),[f'e{i+1}' for i in range(12)]);ax.set_xlabel('Stellation base');ax.set_ylabel('Oriented core edge')
for i,j in np.ndindex(D.shape):ax.text(j,i,str(D[i,j]),ha='center',va='center',fontsize=9,color='white' if D[i,j] else GREY)
ax=axs[1];ax.bar(range(8),[0,2,2,2,4,4,4,6],color=[GREY]+[BLUE]*3+[ORANGE]*3+[PURPLE]);ax.set_xticks(range(8),['1','x','y','z','yz','xz','xy','xyz']);ax.set_ylabel('Eigenvalue of $D^T D$');ax.set_ylim(0,6.6);ax.grid(axis='y',alpha=.2);ax.set_title('Exact Walsh spectrum: 0, 2, 4, 6');fig.suptitle('The oriented core boundary is the cube Laplacian',fontsize=16,fontweight='bold');fig.tight_layout();save(fig,'02_boundary_spectrum.svg')
fig=plt.figure(figsize=(12,4.6));modes=[(3,'Principal ring: z',BLUE),(6,'Complementary cycle: xy',ORANGE),(7,'Parity cycle: xyz',PURPLE)]
for j,(k,title,col) in enumerate(modes):
 ax=fig.add_subplot(1,3,j+1,projection='3d');style(ax);ax.set_title(title,fontweight='bold');J=D@W[:,k]
 for l,(a,b) in enumerate(E):
  u,v=V[a],V[b];ax.plot(*np.array([u,v]).T,color='#b6c1cd',lw=.8)
  if J[l]:
   if J[l]<0:u,v=v,u
   ax.quiver(*(u+.15*(v-u)),*((v-u)*.7),color=col,lw=2.6,arrow_length_ratio=.23)
 ax.scatter(*V.T,color=TEAL,s=25)
fig.suptitle('Three representatives of the 3 + 3 + 1 core cycle space',fontsize=16,fontweight='bold');fig.text(.5,.03,'Arrows = exact signs of D times the selected Walsh mode; not particle trajectories.',ha='center',color=GREY);save(fig,'03_cycle_sectors.svg')
fig,ax=plt.subplots(figsize=(10,3.6));ax.axis('off');ax.set_xlim(0,10);ax.set_ylim(0,4)
for x,y,w,h,title,sub,c in [(0.4,2.5,3.1,1,'33 fine sites','occupation',BLUE),(6.5,2.5,3.1,1,'6 core vertices','registered occupation',TEAL),(0.4,.4,3.1,1,'104 fine bonds','current',BLUE),(6.5,.4,3.1,1,'12 core edges','registered current',TEAL)]:
 ax.add_patch(plt.Rectangle((x,y),w,h,fc=c+'12',ec=c,lw=1.5));ax.text(x+w/2,y+.64,title,ha='center',weight='bold');ax.text(x+w/2,y+.26,sub,ha='center',color=GREY,fontsize=10)
for a,b,lab in [((3.5,3),(6.5,3),'C₀'),((3.5,.9),(6.5,.9),'C₁'),((1.95,1.4),(1.95,2.5),'L₃₃'),((8.05,1.4),(8.05,2.5),'L')]:
 ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':INK,'lw':1.5});ax.text((a[0]+b[0])/2+.12,(a[1]+b[1])/2+.15,lab,ha='center')
ax.text(5,1.95,'LC₁ = C₀L₃₃',ha='center',color=TEAL,fontsize=16,fontweight='bold');fig.suptitle('Current-preserving registration',fontsize=16,fontweight='bold');save(fig,'04_registration.svg')
fig,axs=plt.subplots(1,2,figsize=(11,4));t=np.linspace(0,6,300);eta=1/np.sqrt(3);charge=1/np.cosh(np.sqrt(2)*eta*t)**2;ax=axs[0];ax.plot(t,charge,color=BLUE,lw=2.4,label='Flywheel charge');ax.plot(t,1-charge,color=PURPLE,lw=2.4,label='E harmonic charge');ax.set(xlabel='Dimensionless time (λ=1)',ylabel='Weighted occupation',ylim=(0,1.03));ax.legend(frameon=False);ax.set_title('Exact resonant conversion');ax.grid(alpha=.2)
ax=axs[1];delta=np.linspace(0,10,300);b=4*eta/(np.sqrt(delta**2+32*eta**2)+delta);ax.plot(delta,b*b,color=PURPLE,lw=2.5);ax.set(xlabel='Absolute detuning (λ=1)',ylabel='Maximum E occupation bound',ylim=(0,.52));ax.set_title('Off-resonance suppression');ax.grid(alpha=.2);fig.suptitle('Conservative candidate harmonic interaction',fontsize=16,fontweight='bold');fig.tight_layout();save(fig,'05_harmonic_conversion.svg')
print('5 SVG figures generated; exact D/W and LD identities checked.')
