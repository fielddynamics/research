import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle,Polygon
from itertools import product,combinations
from pathlib import Path
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
out=Path(__file__).parent/'figures';out.mkdir(exist_ok=True)
A=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]]); C=np.array(list(product([-1,1],repeat=3)));E=np.r_[np.eye(3),-np.eye(3)]; D=np.array([a-b for a in A for b in A if not np.array_equal(a,b)])
U=np.array([[1,-1,0],[1,1,-2]],float)/np.sqrt([[2],[6]])
proj=lambda p:np.array(p)@U.T
blue='#2563a6';orange='#c56b22';green='#087e79';gray='#a1a8b3'
fig,ax=plt.subplots(figsize=(7,7)); p,q=proj(E[0])/2,proj(E[1])/2; pitch=np.linalg.norm(p)
for i,j in product(range(-6,7),repeat=2):
    pos=i*p+j*q
    if np.linalg.norm(pos)<=4.3*pitch:ax.add_patch(Circle(pos,pitch,fill=False,edgecolor='#b8c4d0',lw=.55,alpha=.65))
for T,col in [(A,blue),(-A,orange)]:
    for i,j in combinations(range(4),2):ax.plot(*proj(T[[i,j]]).T,c=col,lw=2)
    ax.scatter(*proj(T).T,c=col,s=30,zorder=5)
for i,j in combinations(range(6),2):
    if E[i]@E[j]==0:ax.plot(*proj(E[[i,j]]).T,c=green,lw=1.6)
ax.scatter(*proj(E).T,c=green,s=27,zorder=6);ax.scatter(0,0,c='black',s=36,zorder=7)
ax.set_aspect('equal');ax.set_xlim(-2,2);ax.set_ylim(-2,2);ax.axis('off');ax.set_title('Hadamard → Flower of Life\nExact body-diagonal projection',fontsize=15,pad=14)
fig.text(.5,.035,'Six outer + six inner + one projected centre • radius ratio 2:1\nThree separate axial points coincide; circles are a planar construction.',ha='center',fontsize=10);fig.savefig(out/'24_hadamard_flower.svg',bbox_inches='tight');plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(11,5));T=np.array([[1,.25,.25],[.25,1,.25],[.25,.25,1]]); B=1-T
for tri,col in [(T,blue),(B,orange)]:
    t=proj(tri);mid=(t+np.roll(t,1,axis=0))/2
    axs[0].add_patch(Polygon(t,closed=True,facecolor=col,alpha=.09,edgecolor=col));axs[0].plot(*np.r_[t,t[:1]].T,c=col,lw=2);axs[0].plot(*np.r_[mid,mid[:1]].T,c=col,lw=1.5,ls='--')
    for i,x in enumerate(t):axs[0].text(*(x*1.13),str(i+1),color=col,ha='center',va='center',fontsize=12)
hexp=proj(np.array(list(__import__('itertools').permutations([.25,.5,.75]))));hexp=hexp[np.argsort(np.arctan2(hexp[:,1],hexp[:,0]))];axs[0].add_patch(Polygon(hexp,closed=True,facecolor=green,alpha=.22,edgecolor=green,lw=2));axs[0].set_aspect('equal');axs[0].autoscale();axs[0].axis('off');axs[0].set_title('Actual midplane overlap\nTwo facing tetrahedral sections')
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])
axs[1].imshow(W/9,cmap='Blues',vmin=0,vmax=2/3);labels=['Outer 1','Outer 2','Outer 3','Centre'];axs[1].set_xticks(range(4),labels,rotation=30);axs[1].set_yticks(range(4),labels);axs[1].set_title('Exact area / one tile area');axs[1].set_xlabel('Neighbour tiles');axs[1].set_ylabel('Central field tiles')
for i,j in product(range(4),repeat=2):axs[1].text(j,i,['0','1/9','2/9','3/9','4/9','5/9','2/3'][W[i,j]],ha='center',va='center',color='white' if W[i,j]>=4 else 'black')
fig.suptitle('Overlapping fields create a four-channel geometric kernel',fontsize=15);fig.tight_layout();fig.savefig(out/'25_flower_triforce_overlap.svg',bbox_inches='tight');plt.close(fig)
fig=plt.figure(figsize=(10,6));ax=fig.add_subplot(111,projection='3d');
for d in D:ax.plot(*np.array([[0,0,0],d]).T,c=gray,lw=.7,ls=':')
for d in A:ax.plot(*np.array([[0,0,0],d]).T,c=green,lw=3)
for d in A:
    for s in A:
        if np.array_equal(d,s):continue
        ax.plot(*np.array([d,d-s]).T,c=green,alpha=.45,lw=1.1)
for t,col in [(A,blue),(-A,orange)]:
    for i,j in combinations(range(4),2):ax.plot(*t[[i,j]].T,c=col,lw=1.3)
ax.scatter(*A.T,c=green,s=65,label='4 direct ports (R)');ax.scatter(*D.T,c=gray,s=40,label='12 second origins (√(8/3) R)');ax.scatter(0,0,0,c='black',s=60,label='Central Field Origin');ax.set_box_aspect((1,1,1));ax.set_axis_off();ax.view_init(22,28);ax.legend(loc='upper left',frameon=False);ax.set_title('Recursive Hadamard–Flower diamond lattice\nEvery green edge is a reciprocal direct port',fontsize=15);fig.savefig(out/'26_flower_diamond_network.svg',bbox_inches='tight');plt.close(fig)
