"""Reproduce the hardening summary; visualizes exact spectra and candidate energy."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,3,figsize=(13.8,4.0),layout='constrained')
A=ax[0];vals=[-np.sqrt(6),-2,-np.sqrt(2),0,np.sqrt(2),2,np.sqrt(6)];A.bar(vals,[3,6,3,2,3,6,3],width=.24,color='#137f86');A.set(xticks=vals,xticklabels=['−√6','−2','−√2','0','√2','2','√6'],ylabel='Multiplicity',title='A · Exact Hodge–Dirac spectrum');A.set_ylim(0,7)
A=ax[1];xx=np.arange(5);A.bar(xx-.18,[1,1,2,3,3],.34,label='Torsion (regular)',color='#cf793c');A.bar(xx+.18,[0,2,2,4,2],.34,label='Nonzero Dirac',color='#137f86');A.set(xticks=xx,xticklabels=['A₁','A₂','E','T₁','T₂'],title='B · Equal dimensions, different symmetry',ylabel='Irrep multiplicity');A.legend(frameon=False,fontsize=8)
A=ax[2];t=np.linspace(0,2*np.pi,73);b=np.linspace(0,np.pi,37);T,B=np.meshgrid(t,b);x=np.sin(B)*np.cos(T);y=np.sin(B)*np.sin(T);z=np.cos(B);q=1+x*x*y*y+y*y*z*z+z*z*x*x;im=A.pcolormesh(t*180/np.pi,b*180/np.pi,q,cmap='viridis',shading='auto',vmin=1,vmax=4/3);A.set(title='C · Circular-state quartic invariant',xlabel='Azimuth (degrees)',ylabel='Polar angle (degrees)',xticks=[0,90,180,270,360],yticks=[0,45,90,135,180]);fig.colorbar(im,ax=A,label='V₄')
fig.suptitle('Hadamard null cone · exact spectral structure and conditional vortex energy',fontsize=13,fontweight='bold');fig.savefig(Path(__file__).parent/'figures/07_core_hardening.svg',bbox_inches='tight');plt.close(fig)
