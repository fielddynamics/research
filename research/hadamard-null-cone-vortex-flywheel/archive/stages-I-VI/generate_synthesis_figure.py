"""Draw the exact Triforce tile regrouping, using a schematic perspective for the stellation."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
p=Path(__file__).parent
fig,axs=plt.subplots(1,3,figsize=(13.8,4.8),layout='constrained',gridspec_kw={'width_ratios':[1,1.05,1.1]})
fig.patch.set_facecolor('white'); fig.suptitle('From original tetrahedron faces to one vortex stellation',fontsize=18,fontweight='bold',color='#172b3e')
colors=['#2563a6','#bf662d','#7656a5']; teal='#078579'; grey='#e8edf2'; edge='#536579'
def poly(ax,pts,c,alpha=1,lw=1.25):
 ax.add_patch(Polygon(pts,closed=True,facecolor=c,edgecolor=edge,linewidth=lw,alpha=alpha))
def trif(ax,cx,cy,sz,col,sel=True):
 a=np.array([cx,cy+sz*np.sqrt(3)/2]); b=np.array([cx-sz/2,cy]); c=np.array([cx+sz/2,cy]); ab=(a+b)/2; ac=(a+c)/2; bc=(b+c)/2
 for k,v in enumerate([[a,ab,ac],[b,ab,bc],[c,ac,bc],[ab,ac,bc]]): poly(ax,v,col if k==0 and sel else (teal if k==3 and not sel else grey))
 return a,ab,ac,bc
ax=axs[0]
for i,(x,y) in enumerate([(0,1.9),(-.75,.4),(.75,.4)]):
 a,*_=trif(ax,x,y,1.35,colors[i]); ax.text(x,y-.12,f'Face {i+1}',ha='center',va='top',fontsize=11); ax.text(a[0],a[1]+.07,'s',ha='center',fontsize=11,fontweight='bold',color=colors[i])
ax.set(xlim=(-1.55,1.55),ylim=(0,3.33));ax.set_title('1  Select the three outer tiles',fontsize=13,fontweight='bold',pad=10)
ax=axs[1]; a,ab,ac,bc=trif(ax,0,.72,2.45,teal,False); ax.text(0,1.32,'central\ntriangle',color='white',ha='center',va='center',fontsize=12,fontweight='bold');ax.text(0,.50,'Opposite chamber',ha='center',fontsize=11);ax.set(xlim=(-1.55,1.55),ylim=(0,3.33));ax.set_title('2  Select the shared base',fontsize=13,fontweight='bold',pad=10)
ax=axs[2]; # pyramid with apex s and base three signed coordinate vectors
# 2D oblique projection of actual vertices (1,1,1), (1,0,0),(0,1,0),(0,0,1)
# basis chosen so base shows its three vertices; apex projects above base
s=np.array([1.,1.,1.]); base=np.eye(3); normal=s/np.sqrt(3); ex=np.array([1.,-1.,0.])/np.sqrt(2); ev=np.cross(normal,ex); eye=.36*normal+.933*ev; ey=np.cross(eye,ex); ey*=np.sign(ey@normal)
def pr(v):return np.array([v@ex,v@ey])*1.54+np.array([0,1.22])
B=np.array([pr(v) for v in base]); A=pr(s); center=pr(s/3); 
# base and side triangles, draw in approximate depth order with translucency
poly(ax,B,teal,.50,1.8)
for i in sorted(range(3),key=lambda j:eye@(s+base[j]+base[(j+1)%3])): poly(ax,[A,B[i],B[(i+1)%3]],colors[i],.37,2)
for i in range(3): ax.plot([A[0],B[i,0]],[A[1],B[i,1]],color=edge,lw=1.1)
ax.plot([pr(np.zeros(3))[0],A[0]],[pr(np.zeros(3))[1],A[1]],'--',color='#465468',lw=1.1); ax.scatter(*center,s=25,c=teal,zorder=8);ax.text(A[0],A[1]+.08,'apex s',ha='center',fontsize=11,fontweight='bold')
# actual ring through lateral face centroids
ring=np.array([pr((s+base[j]+base[(j+1)%3])/3) for j in range(3)])
for i in range(3):ax.add_patch(FancyArrowPatch(ring[i],ring[(i+1)%3],arrowstyle='-|>',mutation_scale=13,color='#172b3e',lw=2,zorder=9,shrinkA=1,shrinkB=1))
ax.text(0,.52,'One triangular pyramid;\nthree lateral tiles + shared base',ha='center',fontsize=11);ax.set(xlim=(-1.55,1.55),ylim=(0,3.85));ax.set_title('3  Regroup into one stellation',fontsize=13,fontweight='bold',pad=10)
for ax in axs:ax.set_aspect('equal');ax.axis('off')
fig.savefig(p/'figures/00_triforce_regrouping.svg',bbox_inches='tight'); fig.savefig(p/'figures/00_triforce_regrouping.png',dpi=140,bbox_inches='tight');plt.close(fig)
