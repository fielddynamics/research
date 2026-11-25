from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from itertools import combinations
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
V=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)
W=np.concatenate((V,-V))
a=np.linspace(0,2*np.pi,100); b=np.linspace(0,np.pi,55)
X=np.outer(np.cos(a),np.sin(b)); Y=np.outer(np.sin(a),np.sin(b)); Z=np.outer(np.ones_like(a),np.cos(b))
fig=plt.figure(figsize=(12,5.8),layout="constrained")
for i in [1,2]:
 ax=fig.add_subplot(1,2,i,projection='3d'); ax.set_box_aspect((1,1,1)); ax.view_init(19,28); ax.set_axis_off()
 ax.plot_surface(X,Y,Z,color='#b9c4cf',alpha=.13,linewidth=0,shade=False)
 for p,q in combinations(W,2):
  if np.isclose(p@q,1/3): ax.plot(*np.stack([p,q]).T,color='#778695',alpha=.65,lw=.9)
 for k,p in enumerate(W):
  color='#137c71' if k<4 else '#cc792e'
  ax.scatter(*p,color=color,s=45,depthshade=False)
  if i==1:
   ax.plot(*np.stack([p,2*p]).T,color=color,lw=2)
   ax.plot_surface(X+2*p[0],Y+2*p[1],Z+2*p[2],color=color,alpha=.12,linewidth=0,shade=False)
  else:
   if k>=4:
    theta=np.arccos((1+np.sqrt(2/3))/2); e=np.cross(p,[0,0,1]);e/=np.linalg.norm(e); f=np.cross(p,e)
    t=np.linspace(0,theta,25); aa,tt=np.meshgrid(a,t); cap=np.cos(tt)[...,None]*p+np.sin(tt)[...,None]*(np.cos(aa)[...,None]*e+np.sin(aa)[...,None]*f)
    ax.plot_surface(*cap.transpose(2,0,1),color=color,alpha=.65,shade=False,linewidth=0)
    ax.plot(*cap[-1].T,color=color,lw=1.5)
   else: ax.plot(*np.stack([np.zeros(3),p]).T,color=color,lw=2)
 lim=3 if i==1 else 1.1
 for fn in [ax.set_xlim,ax.set_ylim,ax.set_zlim]:fn(-lim,lim)
 ax.set_title('Eight equal touching neighbours' if i==1 else 'Four allowed caps for extra contacts',fontsize=14,pad=5)
fig.suptitle('Corner-first Hadamard packing: exact maximum of eight',fontsize=18,fontweight='bold')
fig.legend(handles=[Line2D([0],[0],color='#137c71',marker='o',label='4 fixed active contacts'),Patch(color='#cc792e',alpha=.6,label='4 possible additional contacts / caps'),Line2D([0],[0],color='#778695',label='Hadamard cube')],loc='lower center',ncol=3,frameon=False)
fig.savefig(Path(__file__).parent/'figures/23_corner_first_packing.svg',bbox_inches='tight'); plt.close(fig)
