from core_model import *
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import csv
P=Path(__file__).parent; (P/'figures').mkdir(exist_ok=True)
gf=brentq(lambda g:branch(g)['real_max'],.75,1)
gs=np.linspace(.36,1.95,500);ds=[branch(g) for g in gs]
with (P/'branch_scan.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['gain','occupation','frequency','core_fraction','angular_moment','energy','growth_squared']);w.writerows([[d['g'],d['n'],d['omega'],d['core'],np.linalg.norm(core_moment(d['p'],d['g'])),d['energy'],d['growth_sq']] for d in ds])
for filename,key,ylabel in [('frequency','omega','Intrinsic phase frequency'),('core_fraction','core','Core occupation / total occupation'),('stability','growth_sq','Largest squared tangent growth rate')]:
 fig,ax=plt.subplots(figsize=(7,4.1));
 for mask,label in [(gs<gf,'Unstable fixed-orientation branch'),(gs>=gf,'Stable fixed-orientation branch')]:
  ax.plot([d['n'] for d,m in zip(ds,mask) if m],[d[key] for d,m in zip(ds,mask) if m],label=label)
 d=branch(gf);ax.scatter([d['n']],[d[key]],marker='o',label='Fold / soft mode');ax.set(xlabel='Total occupation (dimensionless)',ylabel=ylabel,xlim=(.90,5));
 if key=='growth_sq': ax.set_ylim(-10,100);ax.axhline(0,linestyle='--',linewidth=.8)
 ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(P/'figures'/f'{filename}.svg');plt.close(fig)
