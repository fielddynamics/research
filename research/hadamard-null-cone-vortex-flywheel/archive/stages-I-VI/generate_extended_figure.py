"""Regenerate the dimensionless analytic transfer and measured memory-error figure."""
from pathlib import Path
import re, ast
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).resolve().parent
raw=(base/'extended_verification_output.txt').read_text()
line=re.search(r'Memory integration errors: (.*)',raw).group(1)
errors=ast.literal_eval(re.sub(r'np\.float64\(([^)]+)\)',r'\1',line))
fig,ax=plt.subplots(1,2,figsize=(10,3.4),layout='constrained');t=np.linspace(0,5,400);g=np.hypot(.8,1.3)
for delta in (0,1,3,10):
    w=np.hypot(g,delta/2); ax[0].plot(t,g*g/w**2*np.sin(w*t)**2,label=f'δ = {delta}')
ax[0].set(xlabel='Dimensionless time',ylabel='Core occupation',title='Bright flywheel: reversible transfer',ylim=(0,1.05));ax[0].legend(frameon=False,ncol=2,fontsize=8)
n=np.array([32,64,128,256]); ax[1].loglog(n,errors,'o-',label='Measured residual');ax[1].loglog(n,errors[0]*(n[0]/n)**2,'--',label='Second-order reference'); ax[1].set(xlabel='Quadrature intervals',ylabel='Derivative residual norm',title='Hidden-mode memory reconstruction');ax[1].legend(frameon=False,fontsize=8)
for a in ax:a.grid(alpha=.18);a.spines[['top','right']].set_visible(False)
fig.savefig(base/'figures/06_extended_dynamics.svg',bbox_inches='tight')
