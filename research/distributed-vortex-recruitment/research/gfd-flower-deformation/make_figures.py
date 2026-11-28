from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from deformation import *
root=Path(__file__).parent; out=root/'figures';out.mkdir(exist_ok=True)
p,e,b,o,L,s,q,i=dimple();r=np.linalg.norm(p,axis=1); mask=(p[:,2]==0)&(r>2)
fig,ax=plt.subplots(figsize=(7,6)); sc=ax.scatter(p[mask,0],p[mask,1],c=q[mask],s=42,cmap='viridis');ax.set(aspect='equal',xlabel='Lattice x',ylabel='Lattice y',title='Conditional scalar dimple on the diamond mesh (z=0)');fig.colorbar(sc,ax=ax,label='q = conformal scalar perturbation');fig.tight_layout();fig.savefig(out/'diamond_dimple.svg');plt.close(fig)
rows=[]
for R in range(4,13):
 m=abs(r-R)<.5;rows.append([R,m.sum(),np.mean(q[m]*r[m]),np.std(q[m]*r[m])])
np.savetxt(root/'radial_benchmark.csv',rows,delimiter=',',header='radius,node_count,mean_q_times_r,std_q_times_r',comments='')
fig,ax=plt.subplots(figsize=(7,4)); rr=np.geomspace(1.001,100,300); N,B,_=fields(rr);ax.semilogx(rr,N,label='Static lapse N');ax.semilogx(rr,B,label='Spatial scale B');ax.set(xlabel='Isotropic radius / a',ylabel='Dimensionless response',title='GR benchmark: temporal and spatial response');ax.legend();fig.tight_layout();fig.savefig(out/'metric_response.svg');plt.close(fig)
bs=np.geomspace(30,16000,25); vals=np.array([[b,*[bending(b,kind=k) for k in ('full','time','space')]] for b in bs]);np.savetxt(root/'deflection.csv',vals,delimiter=',',header='impact_parameter,full_radians,time_only_radians,space_only_radians',comments='')
fig,ax=plt.subplots(figsize=(7,4));
for j,label in enumerate(['Full metric','Time only','Space only'],1):ax.semilogx(vals[:,0],vals[:,j]*vals[:,0],label=label)
ax.set(xlabel='Impact parameter / a',ylabel='Deflection × b/a',title='Light deflection: time and space both matter');ax.legend();fig.tight_layout();fig.savefig(out/'deflection.svg');plt.close(fig)
sh=np.linspace(0,.5,26);over=[]
for d in sh:
 K,M=overlap_kernel((d,0));over.append([d,K.sum()/4,np.linalg.norm(K-W)])
np.savetxt(root/'overlap_scan.csv',over,delimiter=',',header='in_plane_shift,overlap_fraction,kernel_difference_norm',comments='')
fig,ax=plt.subplots(figsize=(7,4));ov=np.array(over);ax.plot(ov[:,0],ov[:,1],label='Overlap fraction');ax.plot(ov[:,0],ov[:,2],label='Kernel change (Frobenius norm)');ax.set(xlabel='Relative in-plane displacement',title='Unequal local deformation modifies the interface');ax.legend();fig.tight_layout();fig.savefig(out/'interface_shift.svg');plt.close(fig)
