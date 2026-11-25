"""Exact native coherent-history decoder, symmetry obstruction and controlled FWHT.
No modification of the inherited 36-coordinate Hamiltonian for the history read.
"""
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import expm
from itertools import product
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
ns={};exec((P/'verify_coupled_origins.py').read_text().split("ck('33 original geometric positions;")[0],ns)
H,d,S,base,idx,O=[ns[k] for k in ('H','d','S','base','idx','O')]
h=sp.Matrix(H); E=sp.eye(d)[:,base]; p=np.prod(S,axis=1)
C=sp.Matrix(np.array([np.eye(d,dtype=int)[:,[idx[i,j] for j in range(4) if j!=i]+[base[i]]]@np.array([1,1,1,6]) for i in range(4)]))
T=sp.Matrix(np.column_stack([np.ones(4,int),S[:4]])); R=T.T*C/4
checks=0
def ck(label,ok):
 global checks
 assert bool(ok),label
 checks+=1; print('PASS',label)
def near(a,b,tol=1e-9):return np.allclose(a,b,atol=tol,rtol=tol)
chars=np.column_stack([np.ones(8,int),S,p[:,None]*S,p]); W=sp.Matrix(chars.T); target=W*E.T/8
ck('complete eight Walsh characters in geometry order',W*W.T==8*sp.eye(8))
ck('four optical port Hadamard combinations',T.T*T==4*sp.eye(4))
M=sp.Matrix.vstack(*[C*h**k for k in range(7)])
ck('native filtered history rank 26',M.rank()==26)
K=sp.Matrix.hstack(*M.nullspace());ck('all ten hidden coordinates have zero central component',E.T*K==sp.zeros(8,10))
ck('hidden space invariant',M*h*K==sp.zeros(M.rows,10))
ranks=[]
for k in range(7):
 m=M[:4*(k+1),:]; hidden=sp.Matrix.hstack(*m.nullspace()); ranks.append(8-(E.T*hidden).rank())
ck('central recovery rank by derivative order',ranks==[0,0,0,1,2,5,8])
print('Central recoverable dimensions at order 0..6:',ranks)
# q0 and q7 use uniform port combination; vector pairs use each signed combination.
coeff={}; polys={}; greens={}; z=sp.symbols('z'); powers=[h**k for k in range(9)]
for i in range(8):
 g=0 if i==0 else 1 if i<4 else 2 if i<7 else 3
 a=0 if g in (0,3) else (i if g==1 else i-3)
 B=sp.Matrix.vstack(*[R[a,:]*powers[k] for k in range(7)])
 sol,params=B.T.gauss_jordan_solve(target[i,:].T); sol=sol.subs({v:0 for v in params});
 ck(f'exact native decoder for Walsh coordinate {i}',sol.T*B==target[i,:]);
 if g in coeff:ck(f'grade {g} identical polynomial for all axes',sol==coeff[g])
 else:coeff[g]=sol
 v=E*W[i,:].T; kry=sp.Matrix.hstack(*[P0*v for P0 in powers]); n=kry.rank(); Q=kry[:,:n]; rec=Q.gauss_jordan_solve(kry[:,n])[0]; poly=sp.factor(z**n-sum(rec[k]*z**k for k in range(n)))
 ck(f'Krylov minimal polynomial annihilates core mode {i}',powers[n]*v==sum((rec[k]*powers[k]*v for k in range(n)),sp.zeros(d,1)))
 A=sp.zeros(n); A[:,n-1]=rec
 for k in range(n-1):A[k+1,k]=1
 green=sp.factor((v.T*Q*(z*sp.eye(n)-A).inv()*sp.eye(n)[:,0])[0]/8)
 if g in polys:ck(f'grade {g} exact same resolvent',green==greens[g] and poly==polys[g])
 else:polys[g]=poly;greens[g]=green
for g in range(4):
 print('grade',g,'decoder',list(coeff[g]),'polynomial',polys[g],'core Green',greens[g])
# Core compression of every power is Walsh diagonal, scalar by grade.
for k in range(9):
 Z=W*E.T*powers[k]*E*W.T/8
 ck(f'core response moment {k} Walsh diagonal and grade-degenerate',Z==sp.diag(*Z.diagonal()) and Z[1,1]==Z[2,2]==Z[3,3] and Z[4,4]==Z[5,5]==Z[6,6])
# Actual time samples, not numerical derivatives. Pseudoinverse recovers core for arbitrary unknown cell.
N=np.array(C,float); Ef=np.array(E,float); Wf=np.array(W,float); rng=np.random.default_rng(2026)
results=[]
for delta in np.linspace(.1,1.4,27):
 A=np.vstack([N@expm(-1j*H*k*delta) for k in range(7)]); singular=np.linalg.svd(A,compute_uv=False); rank=(singular>1e-9).sum(); decoder=Ef.T@np.linalg.pinv(A,rcond=1e-10); err=np.linalg.norm(decoder@A-Ef.T,2);results.append((delta,rank,singular[0]/singular[25],err,np.linalg.norm(decoder,2)))
best=min((r for r in results if r[1]==26 and r[3]<1e-7),key=lambda r:r[4]); dt=best[0]; A=np.vstack([N@expm(-1j*H*k*dt) for k in range(7)]); decoder=Ef.T@np.linalg.pinv(A,rcond=1e-10)
print('Example seven sample spacing, rank, condition, core residual, noise gain:',best)
ck('seven coherent samples recover all central records',best[3]<1e-9)
for k in range(12):
 psi=rng.normal(size=d)+1j*rng.normal(size=d); ck(f'arbitrary full-cell initial state Walsh read {k}',near(Wf@decoder@A@psi/8,Wf@Ef.T@psi/8))
# Autonomous U(t) commutes with inversion, hence no raw FWHT on core for arbitrary input.
# Construct inversion on all 36 coords geometrically.
tiles=ns['tiles']; lookup={v:i for i,(_,v) in enumerate(tiles)}; perm=[lookup[frozenset(tuple(-np.array(v)) for v in vs)] for _,vs in tiles]; Inv=np.zeros((d,d),int);Inv[perm,np.arange(33)]=1;Inv[33:,33:]=-np.eye(3,dtype=int)
ck('native Hamiltonian inversion symmetric',np.array_equal(Inv@H,H@Inv))
# standard bit ordering and transform matrix
order=[next(i for i,s in enumerate(S) if tuple(s)==tuple(1-2*((j>>np.arange(3))&1))) for j in range(8)]
Emb=Ef[:,order]; H8=np.array([[(-1)**((i&j).bit_count()) for j in range(8)] for i in range(8)])/np.sqrt(8); I8=Emb.T@Inv@Emb
ck('target butterfly not inversion equivariant',not near(I8@H8,H8@I8))
ck('native inversion-even uniform input cannot map to a single core corner',near(I8@np.ones(8),np.ones(8)) and not near(I8@H8@np.ones(8),H8@np.ones(8)))
# New controls, not a native dynamical derivation. Use only actual cube bonds for hopping.
U=np.eye(d,dtype=complex); steps=[]
for k in range(3):
 X=np.zeros((8,8)); Z=np.diag([(-1)**((i>>k)&1) for i in range(8)])
 for i in range(8):X[i,i^(1<<k)]=1
 ck(f'axis {k} four disjoint actual central bonds',np.count_nonzero(X)==8 and np.all((Emb.T@H@Emb)[X!=0]==-1))
 gate=Emb@(-X-Z)@Emb.T; pulse=expm(-1j*np.pi/(2*np.sqrt(2))*gate); U=pulse@U
 ck(f'axis {k} controlled pulse unitary',near(pulse.conj().T@pulse,np.eye(d)))
 ck(f'axis {k} no leakage with isolated controls',near((np.eye(d)-Emb@Emb.T)@pulse@Emb,0))
 steps.append(gate)
ck('three controlled pulses implement normalized H8 up to global phase',near(Emb.T@U@Emb,(-1j)*H8))
for k in range(8):
 v=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8)); u=Emb.T@U@Emb;ck(f'two-pass normalized H64 arbitrary table {k}',near(u@v@u.T,-H8@v@H8))
# Native H core cannot itself execute butterfly; unitarity of driven pulses != energy conservation.
ck('controlled pulse Hamiltonian differs from original',all(not near(G,H) for G in steps))
print(f'{checks}/{checks} new assertions passed. 5304 previous recorded assertions not rerun.')
np.savetxt(P/'native_walsh_sampling.csv',results,delimiter=',',header='sample_spacing,rank,condition_nonzero,core_reconstruction_residual,noise_gain',comments='')
fig,ax=plt.subplots(1,3,figsize=(13,4),layout='constrained')
ax[0].step(range(7),ranks,where='mid',marker='o');ax[0].set(xlabel='Highest coherent derivative order',ylabel='Exactly recoverable core dimensions',ylim=(-.3,8.4),title='Native core observability');ax[0].set_xticks(range(7));
for g in range(4):
 ev=np.roots([float(v) for v in sp.Poly(polys[g],z).all_coeffs()]); ax[1].scatter(ev.real,[g]*len(ev),s=45,label=f'Grade {g}')
ax[1].set(xlabel='Dimensionless eigenfrequency',ylabel='Walsh grade',yticks=range(4),title='Exact core spectral poles');ax[1].grid(alpha=.2)
a=np.array(results);ax[2].semilogy(a[:,0],a[:,4]);ax[2].scatter([best[0]],[best[4]],marker='o');ax[2].set(xlabel='Coherent sampling interval',ylabel='Core decoder noise gain (2-norm)',title='Seven sampled port histories');ax[2].grid(alpha=.2)
fig.suptitle('Existing vortex engine: read the eight core Walsh modes through four ports')
for ext in ('png','svg'):fig.savefig(P/'figures'/f'42_native_walsh_read.{ext}',dpi=160)
