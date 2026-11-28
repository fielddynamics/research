import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hydrogen import *
from pathlib import Path
root=Path(__file__).resolve().parent
hs=[.65,.5,.35,.25];ds=[ground(h) for h in hs]
with open(root/'hydrogen_convergence.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['h_bohr','sites','energy_cell_average_Hartree','energy_graph_point_Hartree','mean_r_cell_average_bohr','mean_r_graph_point_bohr','residual_cell_average','residual_graph_point'])
 for d in ds:w.writerow([d['h'],len(d['r']),d['E'],d['Eg'],d['mean'],d['mg'],d['res'],d['rg']])
fig,ax=plt.subplots(figsize=(7,4.3));ax.plot(hs,[-d['E'] for d in ds],'o-',label='Cell-average Coulomb');ax.plot(hs,[-d['Eg'] for d in ds],'s-',label='Graph point-source Coulomb');ax.axhline(0.5,ls='--',color='gray',label='Hydrogen reference (reduced-mass atomic units)');ax.set(xlabel='Lattice coordinate scale h / Bohr radius',ylabel='Binding energy (reduced-mass Hartree)',title='Fixed-lattice hydrogen: refinement, not a fit');ax.legend(fontsize=8);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'figures/convergence.png',dpi=180);plt.close(fig)
d=ds[-1];r=d['r'];p=d['p'];mask=abs(p[:,2])<.26
fig,ax=plt.subplots(figsize=(6,5.4));q=ax.scatter(p[mask,0],p[mask,1],c=d['psi'][mask]**2/d['vol'],s=10,cmap='viridis');ax.scatter([0],[0],marker='+',s=60,c='red',label='Proton source');ax.set(xlim=(-4,4),ylim=(-4,4),aspect='equal',xlabel='x / Bohr radius',ylabel='y / Bohr radius',title='Recruited electron envelope on unchanged diamond sites');ax.legend();fig.colorbar(q,ax=ax,label='Probability density / Bohr radius³');fig.tight_layout();fig.savefig(root/'figures/recruitment.png',dpi=180);plt.close(fig)
r=np.linspace(.05,8,400);fig,ax=plt.subplots(figsize=(7,4.4));ax.plot(r,q_enc(r),label='Net enclosed electric charge / e');ax.plot(r,mass_fraction(r),label='Enclosed rest-mass fraction (binding omitted)');ax.plot(r,4*r*r*np.exp(-2*r),label='1s radial probability density',ls='--');ax.set(xlabel='Radius / reduced-mass Bohr radius',ylabel='Dimensionless read',title='One extended state, two different source reads');ax.legend(fontsize=8);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'figures/charge_mass.png',dpi=180);plt.close(fig)
with open(root/'radial_reads.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['r_bohr','net_charge_e','rest_mass_fraction_no_binding','neutral_potential_atomic_units','radial_probability']);w.writerows(zip(r,q_enc(r),mass_fraction(r),phi_neutral(r),4*r*r*np.exp(-2*r)))
