import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research import *
from core_model import rhs,core_moment,gain
from scipy.integrate import solve_ivp
out=Path('figures');out.mkdir(exist_ok=True)
k=np.arange(1,5);be=[alpha_binding(i) for i in k];details=[4*i-i*i for i in k]
fig,ax=plt.subplots(figsize=(7,4));ax.plot(k,be,'o-',label='Atomic mass defect (MeV)');ax.plot(k,details,'s--',label='Walsh detail power (dimensionless)');ax.axhline(0,lw=.6);ax.set_xticks(k,['He-4','Be-8','C-12','O-16']);ax.set_ylabel('Distinct quantities, not a fit');ax.legend();fig.tight_layout();fig.savefig(out/'packing_binding.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4));ns=np.arange(1,101);cl=[np.exp(shell_log_clock(*hierarchy(int(n)))) for n in ns];ax.semilogy(ns,cl);ax.set(xlabel='Number of nested static shells',ylabel='Central lapse relative to infinity',title='Every shell has compactness 0.4');fig.tight_layout();fig.savefig(out/'nested_clock.svg');plt.close(fig)
rows=benchmarks();fig,ax=plt.subplots(figsize=(9,5));ax.barh([x[0] for x in rows],[compactness(x[1],x[2]) for x in rows]);ax.set_xscale('log');ax.set_xlabel('GR compactness (log scale)');ax.invert_yaxis();fig.tight_layout();fig.savefig(out/'scale_compactness.svg');plt.close(fig)
with open('scale_benchmarks.csv','w') as f:
 w=csv.writer(f);w.writerow(['object','mass_kg','radius_m','compactness']);w.writerows([(*row,compactness(row[1],row[2])) for row in rows])
with open('packing_benchmarks.csv','w') as f:
 w=csv.writer(f);w.writerow(['alpha_count','neutral_atomic_mass_u','additional_binding_MeV','normalized_Walsh_detail_power_for_16_address_block']);w.writerows([(k,v,alpha_binding(k),4*k-k*k if k<=4 else '') for k,v in MASSES.items()])
with open('loaded_vortex_scan.csv','w') as f:
 w=csv.writer(f);w.writerow(['complete_child_count','phase_step','norm','energy','overlap','initial_core_moment','minimum_core_moment','maximum_core_moment']);
 for k in range(5):
  for phase in np.linspace(0,2*np.pi,13):
   p=branch(1)['p']+.13*load_tetb(k,phase);sol=solve_ivp(lambda t,y:rhs(y),[0,2],p,t_eval=np.linspace(0,2,101),rtol=2e-9,atol=2e-11,method='DOP853');mom=[np.linalg.norm(core_moment(y,gain(overlap(y)))) for y in sol.y.T];w.writerow([k,phase,np.vdot(p,p).real,energy(p),overlap(p),mom[0],min(mom),max(mom)])
