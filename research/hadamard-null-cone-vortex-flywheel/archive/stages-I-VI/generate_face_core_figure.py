"""Illustrate the measured ring currents in branch 1, +z, in normalized model units."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from itertools import combinations
S=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1),(-1,-1,-1),(-1,1,1),(1,-1,1),(1,1,-1)])
V=np.vstack([np.eye(3),-np.eye(3)])
# Values from the actual verification log, rounded for display.
j=S[:,2]*np.repeat([.006833633888511937,.0037427367139764808],4)
colors=['#2563b0']*4+['#c76b24']*4
# Orthographic view (avoid projected vertex overlaps).
yaw=.58; pitch=.38
P=np.array([[np.cos(yaw),-np.sin(yaw),0],[-np.sin(pitch)*np.sin(yaw),-np.sin(pitch)*np.cos(yaw),np.cos(pitch)]])
pr=lambda x:np.asarray(x)@P.T
fig,(ax,b)=plt.subplots(1,2,figsize=(11,5),gridspec_kw={'width_ratios':[1.15,1]},layout='constrained')
for k,s in enumerate(S):
    base=V[V@s==1]
    for x in base:
        q=pr([x,s]);ax.plot(*q.T,color=colors[k],alpha=.20,lw=1)
    # Lateral face centroids form the actual three-site ring.
    tri=np.array([(s+base[i]+base[(i+1)%3])/3 for i in range(3)])
    if np.cross(tri[1]-tri[0],tri[2]-tri[1])@s<0:tri=tri[::-1]
    if j[k]<0:tri=tri[::-1]
    q=pr(tri)
    for i in range(3):
        a,c=q[i],q[(i+1)%3];ax.add_patch(FancyArrowPatch(a,c,arrowstyle='-|>',mutation_scale=9,linewidth=1.7,color=colors[k],shrinkA=0,shrinkB=0))
    pos=pr(s*1.16);ax.text(*pos,('A' if k<4 else 'B')+str(k%4+1),color=colors[k],fontsize=9,ha='center',va='center',fontweight='bold')
for i,k in combinations(range(6),2):
    if V[i]@V[k]==0:ax.plot(*pr([V[i],V[k]]).T,color='#718494',alpha=.6,lw=1)
q=pr([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]])
for i in range(4):ax.add_patch(FancyArrowPatch(q[i],q[(i+1)%4],arrowstyle='-|>',mutation_scale=13,linewidth=2.8,color='#078477',shrinkA=0,shrinkB=0))
ax.set(aspect='equal',xlim=(-1.85,1.85),ylim=(-1.85,1.85),title='A · Eight outer rings + one principal core square');ax.axis('off')
b.barh(np.arange(8),j,color=colors);b.axvline(0,color='#526476',lw=1);b.set(yticks=np.arange(8),yticklabels=[('A' if k<4 else 'B')+str(k%4+1) for k in range(8)],xlabel='Outward-signed ring current (model units)',title='B · Actual simultaneous ring-current read');b.invert_yaxis();b.spines[['top','right']].set_visible(False);b.grid(axis='x',alpha=.18);b.set_axisbelow(True);b.text(.02,-.22,'All eight rings are nonzero in the same state.\nRegistered principal component: +0.125987 along z.',transform=b.transAxes,fontsize=10,color='#078477')
fig.suptitle('One Hadamard null cone · one collective flywheel',fontweight='bold',fontsize=15);fig.savefig(Path(__file__).parent/'figures/08_eight_faces_one_core.svg',bbox_inches='tight');plt.close(fig)
