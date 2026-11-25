from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
p=Path(__file__).parent
a=np.genfromtxt(p/'sustained_dynamics.csv',delimiter=',',names=True)
fig,ax=plt.subplots(2,2,figsize=(11,7),layout='constrained');fig.patch.set_facecolor('white')
fig.suptitle('Eight Triforce vortex rings generate and sustain actual inner circulation',fontsize=16,fontweight='bold')
t=a['time'];cols=['#2563a6','#d97729']
ax[0,0].plot(t,a['outer_factor'],color=cols[0],label=r'$|v|^2$');ax[0,0].axhline((73/77)**2,color='#64748b',ls='--',label='Proved lower bound');ax[0,0].set(title='Outer winding factor stays nonzero',xlabel='Model time',ylabel='Normalized factor');ax[0,0].legend(frameon=False,fontsize=9)
ax[0,1].plot(t,a['inner_occupation'],color='#087f75');ax[0,1].set(title='Central triangles start empty and become occupied',xlabel='Model time',ylabel='Fraction of total occupation');ax[0,1].yaxis.set_major_formatter(PercentFormatter(1))
for i in range(8):ax[1,0].plot(t,a[f'j{i+1}'],color=cols[i//4],alpha=.85,lw=1.3,label=['TetA','TetB'][i//4] if i%4==0 else None)
ax[1,0].axhline(0,color='#94a3b8',lw=.8);ax[1,0].set(title='All eight outward-oriented ring means retain sign',xlabel='Model time',ylabel='Signed ring current');ax[1,0].legend(frameon=False,fontsize=9)
ax[1,1].plot(t,a['core_moment_norm'],color='#087f75',label='Actual central-edge angular moment');ax[1,1].axhline(8/693,color='#7c3aed',ls='--',label='Stationary state of same H');ax[1,1].set(title='Generated core circulation (not registered outer current)',xlabel='Model time',ylabel='Angular current magnitude');ax[1,1].legend(frameon=False,fontsize=8)
for x in ax.flat:x.spines[['top','right']].set_visible(False);x.grid(alpha=.15)
fig.savefig(p/'figures/10_sustained_flywheel.svg',bbox_inches='tight');plt.close(fig)
