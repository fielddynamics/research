import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bridge import *
root=Path(__file__).resolve().parent
r=np.linspace(.001,16,600)
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
for nn,ll,label in [(1,0,'1s'),(2,0,'2s'),(2,1,'2p')]:ax.plot(r,r*r*radial(nn,ll,r)**2,label=label)
ax.set(xlabel='Radius (Bohr units)',ylabel='Radial probability per unit radius',title='Different recruitment profiles on the same processor geometry');ax.legend();ax.grid(alpha=.2)
fig.savefig(root/'figures/radial_profiles.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
r=np.linspace(0,16,300);a=np.array([integrated_energy(2,0,R) for R in r]);b=np.array([integrated_energy(2,1,R) for R in r]);ax.plot(r,a,label='2s');ax.plot(r,b,label='2p');ax.axhline(-.125,color='gray',ls='--',label='Common total energy');ax.set(xlabel='Radius (Bohr units)',ylabel='Enclosed model energy (Hartree)',title='Different local energy distributions, same total energy');ax.legend();ax.grid(alpha=.2);fig.savefig(root/'figures/enclosed_energy.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained');q=np.linspace(0,.3,100)
ax.plot(q,27.211386*quartic_energy(3,2,5/7)*q*q,label='3d E doublet');ax.plot(q,27.211386*quartic_energy(3,2,11/21)*q*q,label='3d T2 triplet');ax.set(xlabel='Lattice coordinate scale / Bohr radius',ylabel='Leading kinetic correction (eV, approximate)',title='Finite lattice anisotropy: a falsifiable diagnostic');ax.legend();ax.grid(alpha=.2);fig.savefig(root/'figures/lattice_splitting.svg');plt.close(fig)
with open(root/'orbital_benchmarks.csv','w') as f:
    w=csv.writer(f);w.writerow(['n','l','m','energy_Hartree','mean_radius_Bohr','integral_density_squared','energy_integral_Hartree']);
    for nn in range(1,5):
        for ll in range(nn):
            for mm in range(-ll,ll+1):w.writerow([nn,ll,mm,energy(nn),radial_moment(nn,ll,1),ipr(nn,ll,mm),integrated_energy(nn,ll)])
