from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
p=Path(__file__).resolve().parent
fig,axs=plt.subplots(1,3,figsize=(13,4.7),gridspec_kw={'width_ratios':[1,1,1.18]}); fig.patch.set_facecolor('#f8fafc')
for ax in axs: ax.set_facecolor('#f8fafc');ax.axis('off')
a=axs[0];a.set(xlim=(0,4),ylim=(-1,5));a.set_aspect('equal');a.set_title('16 actual Triforce tiles',weight='bold',pad=12)
for i in range(4):
 for j in range(4):
  a.add_patch(Rectangle((j,3-i),.95,.95,facecolor='#b8e4dc' if i==j else '#dbeafe',edgecolor='white'))
  a.text(j+.475,3-i+.475,f'C{i+1}' if i==j else f'L{i+1}{j+1}',ha='center',va='center',fontsize=11,color='#134e4a' if i==j else '#1e3a8a')
a.text(2,-.3,'4 central + 12 lateral',ha='center',fontsize=11)
a.text(2,-.72,'Face index × vertex index',ha='center',fontsize=10,color='#475569')
a=axs[1];a.set(xlim=(0,4),ylim=(-1,5));a.set_aspect('equal');a.set_title('Hadamard change of basis',weight='bold',pad=12)
for i in range(4):
 for j in range(4):
  a.add_patch(Rectangle((j,3-i),.95,.95,facecolor='#dbeafe' if i<=j else '#fee2c7',edgecolor='white'))
  a.text(j+.475,3-i+.475,f'{i}{j}',ha='center',va='center',fontsize=10)
a.text(2,-.3,'10 metric + 6 Lorentz gauge*',ha='center',fontsize=11)
a.text(2,-.72,'*Linearized, lowered-index split',ha='center',fontsize=9.5,color='#475569')
a=axs[2];a.set(xlim=(0,4.5),ylim=(-1,5));a.set_aspect('equal');a.set_title('Equal weak-field potentials',weight='bold',pad=12)
for i in range(4):
 for j in range(4):
  a.add_patch(Rectangle((j+.25,3-i),.95,.95,facecolor='#0f766e' if i==j else '#e2e8f0',edgecolor='white'))
  a.text(j+.725,3-i+.475,'−φ' if i==j else '0',ha='center',va='center',color='white' if i==j else '#64748b',fontsize=13)
a.text(2.25,-.3,'δX = −φ I₄',ha='center',fontsize=13)
a.text(2.25,-.72,'Basis-specific candidate read',ha='center',fontsize=10,color='#475569')
fig.suptitle('Triforce channels → coframe → weak-field metric',fontsize=17,weight='bold',y=.98);fig.subplots_adjust(top=.83,bottom=.04,wspace=.27)
for ext in ('svg','png'):fig.savefig(p/'figures'/f'37_triforce_tetrad_read.{ext}',dpi=150,bbox_inches='tight',facecolor=fig.get_facecolor())
