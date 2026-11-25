import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
base=Path(__file__).parent
x=np.genfromtxt(base/'triforce_dynamics.csv',delimiter=',',names=True)
fig=plt.figure(figsize=(12,6.3),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1,1.35]);ax=fig.add_subplot(gs[:,0]);ax.set(xlim=(-.8,4.25),ylim=(-1.15,4.7),aspect='equal');ax.axis('off');ax.set_title('One chamber: same twelve lateral tiles',fontweight='bold',loc='left',pad=14)
for i in range(4):
 for j in range(4):
  if i==j:
   ax.add_patch(Rectangle((j,3-i),.85,.85,fc='#eef1f4',ec='none'));ax.text(j+.425,3-i+.425,'—',ha='center',va='center',color='#81909e')
  else:
   ax.add_patch(Rectangle((j,3-i),.85,.85,fc='#d9e9fb',ec='#3574b7',lw=1.2));ax.text(j+.425,3-i+.425,rf'$X_{{{i+1}{j+1}}}$',ha='center',va='center',fontsize=13)
for i in range(4):
 ax.text(-.14,3-i+.425,f'Ring {i+1}',ha='right',va='center',fontsize=10,color='#245d96');ax.text(i+.425,4.05,f'Face {i+1}',ha='center',fontsize=10)
 ax.annotate('',(i+.425,-.62),(i+.425,-.08),arrowprops={'arrowstyle':'->','color':'#087d72','lw':1.5});ax.text(i+.425,-.84,rf'$y_{{-{i+1}}}$',ha='center',color='#087d72',fontsize=13)
ax.text(1.9,4.48,'Each row winds around a stellation',ha='center',fontsize=10);ax.text(1.9,-1.08,'Each column reads into a central Triforce tile',ha='center',fontsize=10)
a=fig.add_subplot(gs[0,1]);a.plot(x['time'],x['inner_occupation'],color='#087d72',lw=2);a.set(title='Core excitation from eight initially pure rings',ylabel='Inner occupation',xlabel='Dimensionless time',ylim=(0,1));a.grid(alpha=.18)
b=fig.add_subplot(gs[1,1]);
for i in range(8):b.plot(x['time'],x[f'j{i}'],color='#3574b7' if i<4 else '#ce7434',alpha=.75,label=('TetA rings' if i==0 else 'TetB rings' if i==4 else None))
b.axhline(0,color='#888',lw=.6);b.set(title='Actual local ring currents (not constrained to stay pure)',ylabel='Signed current',xlabel='Dimensionless time');b.legend(frameon=False,loc='upper right');b.grid(alpha=.18)
fig.savefig(base/'figures/09_triforce_face_first.svg',bbox_inches='tight');plt.close(fig)
