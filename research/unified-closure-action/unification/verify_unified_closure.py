import numpy as np
from itertools import product
from math import log
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
A=list(product(range(4),repeat=3)); w=np.array([1/32 if b==0 else 1/96 for a,b,c in A]); W=np.diag(w); I=np.eye(64); u=np.ones(64)
M=np.zeros((64,64)); cycle=[0,2,3,1]
for j,v in enumerate(A): M[A.index(tuple(cycle[i] for i in v)),j]=1
Q=(I+M+M@M)/3
P=[]
for k in range(4):
    p=np.zeros((64,64))
    for i,v in enumerate(A):
        mask=np.array([z[:k]==v[:k] for z in A]);p[i,mask]=w[mask]/w[mask].sum()
    P.append(p)
D=[P[k+1]-P[k] for k in range(3)]; checks=[]
def ck(s,v):
    assert v,s
    checks.append(s); print('PASS',s)
ck('weights sum to one',np.isclose(w.sum(),1));ck('Q rank 22',np.linalg.matrix_rank(Q)==22)
for k,p in enumerate(P):
    ck(f'P{k} idempotence, weighted adjoint, symmetry',np.allclose(p@p,p) and np.allclose(W@p,p.T@W) and np.allclose(Q@p,p@Q))
for k,d in enumerate(D):
    ck(f'grade {k+1} rank {4**k} on invariant space',np.linalg.matrix_rank(d@Q)==4**k)
    ck(f'grade {k+1} raw rank {3*4**k}',np.linalg.matrix_rank(d)==3*4**k)
    for j,e in enumerate(D): ck(f'grade product {k+1},{j+1}',np.allclose(d@e,d if k==j else 0))
t=np.sqrt(1/137.035999177); J=[I+(t-1)*d for d in D]; C=J[2]@J[1]@J[0]
ck('factorization',np.allclose(C,P[0]+t*(I-P[0])));ck('common state and charge invariant',np.allclose(C@u,u) and np.allclose(w@C,w))
S=np.diag(np.sqrt(w)); Si=np.diag(1/np.sqrt(w)); vals,vec=np.linalg.eigh(Q); V=vec[:,vals>.5]
for k,j in enumerate(J):
    # Q commutes with the quadrature metric. Use weighted-orthonormal coordinates.
    a=S@j@Si; d=S@D[k]@Si; R=np.sqrt(1-t*t)*d
    dil=np.block([[a,R],[R,-a]])
    ck(f'lossless dilation {k+1}',np.allclose(dil.T@dil,np.eye(128)))
    sign,l=np.linalg.slogdet(V.T@a@V);ck(f'grade {k+1} log determinant',sign==1 and np.isclose(l,4**k*log(t)))
sign,l=np.linalg.slogdet(V.T@S@C@Si@V);ck('collective log determinant',sign==1 and np.isclose(2*l,42*log(t)))
# Response and Legendre primitives. Use analytic inverse for numerical stability.
x=np.geomspace(1e-3,1e3,401); r0=x; r1=2*x/(1+np.sqrt(1+4*x)); mu0=r0/(1+r0);mu1=r1/(1+r1)
ck('drained response',np.allclose(mu0,x/(1+x)));ck('bound response',np.allclose(x*(1-mu1)**2,mu1));ck('positive auxiliary curvatures',np.all(1+2*r1>0))
for b,r,mu in [(0,r0,mu0),(1,r1,mu1)]:
    y=x*x; Vb=r-2*np.log1p(r)+mu if b==0 else r**3/3
    F=y*mu-Vb; target=y-2*x+2*np.log1p(x) if b==0 else r**4+2*r**3/3
    ck(f'Legendre primitive b={b}',np.allclose(F,target,rtol=1e-9,atol=1e-12))
    dmu=1/((1+r)**2*(1+2*b*r)); L=mu+x*dmu
    ck(f'positive radial and transverse stiffness b={b}',np.all(mu>0) and np.all(L>0))
    ratio=L/mu;ck(f'spacelike scalar characteristic ratio b={b}',np.allclose(ratio,1+1/(1+r) if b==0 else 1+1/(1+2*r)))
    ck(f'naive scalar cone exceeds c b={b}',np.all(ratio>1))
# Separate weighted flux quadrature from uniform pair weighting.
pair_weights=np.array([w[[i for i,(a,b,c) in enumerate(A) if a==aa and b==bb]].sum() for aa in range(4) for bb in range(4)])
ck('uniform ordered pair diagonal share',np.isclose(np.trace(pair_weights.reshape(4,4)),.25))
# Different identification: central tile is the self-pair for each face.
ck('central-tile total share differs from uniform self-pair share',np.isclose(sum(w[i] for i,(_,b,_) in enumerate(A) if b==0),.5))
# plot as document assets
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,4.4)); ax.semilogx(x,mu0,label='Drained: x = r');ax.semilogx(x,mu1,label='Internal bound: x = r(1+r)');ax.set(xlabel='Normalized input x',ylabel='Response share μ',ylim=(0,1.02),title='One odds coordinate, two response regimes');ax.grid(alpha=.2);ax.legend();fig.tight_layout()
for ext in ['svg','png']:fig.savefig(root/f'10_unified_response.{ext}',dpi=180)
plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.4));ax.semilogx(x,np.sqrt(1+1/(1+x)),label='Drained');ax.semilogx(x,np.sqrt(1+1/(1+2*r1)),label='Internal bound');ax.axhline(1,ls='--',color='gray',label='Metric light cone');ax.set(xlabel='Static spacelike background x',ylabel='Parallel characteristic speed / c',title='Obstruction for a naive Lorentz-scalar completion');ax.grid(alpha=.2);ax.legend();fig.tight_layout()
for ext in ['svg','png']:fig.savefig(root/f'11_scalar_causality.{ext}',dpi=180)
plt.close(fig)
print(f'{len(checks)} checks passed')
