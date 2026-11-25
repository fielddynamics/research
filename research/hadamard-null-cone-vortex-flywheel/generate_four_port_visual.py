from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from verify_four_port_packing import D,S,base,edges,REM,ADD,neighbors
out=Path(__file__).parent/'figures';out.mkdir(exist_ok=True)
fig=plt.figure(figsize=(12,6),facecolor='white');a=fig.add_subplot(121,projection='3d');b=fig.add_subplot(122,projection='3d')
A=set(base((0,0,0)));corners=[np.array(s) for s in S]+[-np.array(s) for s in S]
def star(ax,c,k,alpha):
    for side,clr in [(corners[:4],'#2476bd'),(corners[4:],'#cc7038')]:
        from itertools import combinations
        ts=[[np.array(c)+k*v for v in t] for t in combinations(side,3)]
        ax.add_collection3d(Poly3DCollection(ts,facecolors=clr,edgecolors=clr,alpha=alpha,linewidths=.65))
for d in D:
    active=d in A;col='#087e75' if active else '#a0a7b0';a.plot(*np.array([(0,0,0),d]).T,color=col,lw=2.3 if active else .9,ls='-' if active else ':',alpha=.9)
    star(a,d,.27,.22 if active else .12)
    a.scatter(*d,color=col,s=17 if active else 9)
star(a,(0,0,0),.27,.32);a.scatter(0,0,0,color='#202e3b',s=23)
a.set_title('One complete field + 12 complete neighbours',fontweight='bold',fontsize=11)
a.text2D(.05,.06,'Green: 4 transmitting links\nGrey: 8 geometric contacts only',transform=a.transAxes,fontsize=10)
for d in D:b.scatter(*d,color='#087e75' if d in A else '#a0a7b0',s=58 if d in A else 24)
for s in S:
    s=np.array(s)/np.sqrt(3)*np.sqrt(2);b.plot(*np.array([np.zeros(3),s]).T,color='#285bb2',ls='--',lw=1.7);b.scatter(*s,color='#285bb2',marker='^',s=45)
    d=next(d for d in A if np.dot(d,s)>1.5);b.plot(*np.array([np.zeros(3),d]).T,color='#087e75',lw=2.4);b.plot(*np.array([s,d]).T,color='#d97736',ls=':',lw=1.7)
b.set_title('Four ports are not collinear with FCC contacts',fontweight='bold',fontsize=11)
b.text2D(.05,.06,'Blue: regular Hadamard directions\nGreen: selected contact directions\nOrange: geometric offset (35.26°)',transform=b.transAxes,fontsize=10)
for ax in (a,b):
    ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5),zlim=(-1.5,1.5));ax.set_box_aspect((1,1,1));ax.view_init(20,32);ax.set_axis_off()
fig.suptitle('FCC four-port packing model · the field object is the entire stellated octahedron',fontsize=15,fontweight='bold',y=.96);fig.subplots_adjust(wspace=.02,top=.88,bottom=.03,left=.02,right=.98)
fig.savefig(out/'22_four_port_packing.svg',bbox_inches='tight');fig.savefig(out/'22_four_port_packing.png',dpi=180,bbox_inches='tight');plt.close(fig)
