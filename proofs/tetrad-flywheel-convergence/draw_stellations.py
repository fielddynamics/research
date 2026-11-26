"""Coordinate-derived illustration; no fitted streamlines or physical flow envelope."""
from itertools import combinations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
out=Path(__file__).parent/'figures';out.mkdir(exist_ok=True)
s=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)
spikes=[(eps,np.array([eps*s[i]]+[eps*(s[i]+s[j])/2 for j in range(4) if j!=i])) for eps in [1,-1] for i in range(4)]
v=np.vstack((np.eye(3),-np.eye(3)))
faces=[v[list(t)] for t in combinations(range(6),3) if all(v[i]@v[j]==0 for i,j in combinations(t,2))]
fig=plt.figure(figsize=(12,4.1),facecolor='white')
colors={1:'#2879c9',-1:'#dc752d'}
for k,title in enumerate(['1  Two parity-related tetrahedra','2  Eight stellations around one core','3  The shared octahedron']):
    ax=fig.add_subplot(1,3,k+1,projection='3d',computed_zorder=False);ax.set_proj_type('ortho');ax.view_init(elev=54,azim=54);ax.set_box_aspect((1,1,1));ax.set_axis_off();ax.set_title(title,fontsize=12,pad=2,fontweight='bold',color='#17263c')
    if k==0:
        for eps in [1,-1]:
            a=eps*s;ax.add_collection3d(Line3DCollection([a[list(e)] for e in combinations(range(4),2)],colors=colors[eps],linewidths=2));ax.scatter(*a.T,c=colors[eps],s=24,depthshade=False)
    if k==1:
        for eps,a in spikes:
            ax.add_collection3d(Poly3DCollection([a[list(t)] for t in combinations(range(4),3)],facecolors=colors[eps],edgecolors=colors[eps],alpha=.16,linewidths=1.0));ax.scatter(*a[0],c=colors[eps],s=20,depthshade=False)
    if k>=1:
        ax.add_collection3d(Poly3DCollection(faces,facecolors='#18a69b',edgecolors='#087f75',alpha=.25 if k==1 else .43,linewidths=1.5));ax.scatter(*v.T,c='#087f75',s=20,depthshade=False)
    if k==2:
        # The exact core face-dual currents for C=(0.2,0.35,1); arrow direction only.
        C=np.array([.2,.35,1.]);
        for i in range(4):
            for j in range(4):
                if i==j:continue
                a=s[i]/3;b=-s[j]/3;I=np.cross(s[i],s[j])@C
                if I<0:a,b=b,a
                d=b-a;start=a+.17*d;end=a+.83*d
                ax.quiver(*start,*(end-start),color='#055e58',linewidth=1.35,arrow_length_ratio=.21)
    lim=1.15 if k<2 else .85
    ax.set(xlim=(-lim,lim),ylim=(-lim,lim),zlim=(-lim,lim))
fig.text(.5,.04,'Blue / orange: four stellations in each chamber. Teal: six core vertices and eight faces. Dark arrows: example oriented core currents.',ha='center',fontsize=10,color='#475569');fig.subplots_adjust(left=.015,right=.985,top=.89,bottom=.10,wspace=.015)
for ext in ['png','svg','pdf']:fig.savefig(out/f'stellations_and_core.{ext}',dpi=190,bbox_inches='tight',pad_inches=.12)
