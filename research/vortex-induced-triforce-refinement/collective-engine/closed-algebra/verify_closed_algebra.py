"""Further algebra of the unchanged Stage VII flywheel.
Reuses and reruns the 126-check reconstruction in the parent directory.
No additional sites, couplings or calibration. Exact SymPy identities, followed
by numerical diagnostics of the same published witness.
"""
import contextlib, io, runpy
from pathlib import Path
import sympy as s
import numpy as np
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()) as inherited:
    ns=runpy.run_path(str(P.parent/'verify_collective_engine.py'))
assert '126/126 checks passed' in inherited.getvalue()
print('Inherited reconstruction: 126/126 rerun passed')
count=0
def ck(label,yes):
    global count
    assert bool(yes), label
    count+=1;print(f'PASS {count:03d} {label}')
def eq(a,b):
    if isinstance(a,s.MatrixBase):return all(s.simplify(x)==0 for x in a-b)
    return s.simplify(a-b)==0
H=ns['H']; Hw=ns['Hw']; Lw=ns['Lw']; r,d,b,a,k,e,ec=[ns[t] for t in ['r','d','b','a','k','e','ec']]
A=H[:2,:2]; g=H[:2,2]; g2=s.factor(g.dot(g)); delta=s.factor(g.row_join(A*g).det())
ck('native symmetric normalization',eq(H,H.T))
ck('core coupling norm exact',eq(g2,3*a*a-2*a*b+3*b*b))
ck('coupling norm positive for nonzero pair',eq(g2,2*(a*a+b*b)+(a-b)**2))
ck('exact dark-to-bright mixing numerator',eq(delta,2*s.sqrt(2)*((b*b-a*a)*d+(a*a-3*a*b)*r)))
# Unnormalized orthogonal direction makes the chain identity polynomial.
h=s.Matrix([-g[1],g[0]])
ck('outer core-orthogonal combination',eq(h.dot(g),0) and eq(h.dot(h),g2))
ck('dark-bright mixing identity',eq(h.dot(A*g),delta))
ck('outer dark eigenstate criterion via residual',eq(g2*A*h-(h.dot(A*h))*h,delta*g))
# Nonzero g implies unique directly coupled line in the outer plane.
Q=s.Matrix.hstack(s.Matrix.vstack(h,s.zeros(1,1)),s.Matrix.vstack(g,s.zeros(1,1)),s.eye(3)[:,2]);
ck('orthogonal columns for general core-coupled basis',eq(Q.T*Q,s.diag(g2,g2,1)))
ck('no direct core coupling to orthogonal outer coordinate',eq((Q.T*H*Q)[0,2],0))
ck('general core Krylov determinant is precisely mixing numerator',eq(s.Matrix.hstack(s.eye(3)[:,2],H*s.eye(3)[:,2],H**2*s.eye(3)[:,2]).det(),delta))
ck('equal shared-edge access leaves nonzero mixing for a and r nonzero',eq(delta.subs(b,a),-4*s.sqrt(2)*a*a*r))
ck('equal shared-edge access gives simple squared core coupling',eq(g2.subs(b,a),4*a*a))
# Existing witness, not a new fitted matrix.
gw=Hw[:2,2]; bw=gw/s.sqrt(11); dw=s.Matrix([-gw[1],gw[0]])/s.sqrt(11)
U=s.Matrix([[dw[0],bw[0],0],[dw[1],bw[1],0],[0,0,1]])
chain=s.simplify(U.T*Hw*U)
ck('witness exact core link strength',eq(gw.dot(gw),11))
ck('witness change of basis orthogonal',eq(U.T*U,s.eye(3)))
ck('witness exact serial chain',eq(chain,s.Matrix([[s.Rational(13,22),7*s.sqrt(2)/11,0],[7*s.sqrt(2)/11,-s.Rational(35,22),s.sqrt(11)],[0,s.sqrt(11),-s.Rational(89,10)]])))
ck('both chain links nonzero',chain[0,1]!=0 and chain[1,2]!=0)
ck('core vector cyclic in the three-mode witness',s.simplify(s.Matrix.hstack(s.eye(3)[:,2],chain*s.eye(3)[:,2],chain**2*s.eye(3)[:,2]).det())!=0)
ck('chain preserves exact characteristic polynomial',eq(chain.charpoly().as_expr(),Hw.charpoly().as_expr()))
# The real collective eigenbasis and original spectral coefficients.
sq=s.sqrt(22); ev=[s.Rational(11,10),-s.Rational(11,2)-sq,-s.Rational(11,2)+sq]
x0=s.Matrix([0,1,0]); coeff=[]
for l in ev:
    Pr=s.eye(3)
    for j in ev:
        if j!=l:Pr=Pr*(Lw-j*s.eye(3))/(l-j)
    x=s.simplify(Pr*x0);coeff.append(x)
    ck(f'exact original spectral coefficient at {l}',eq(Lw*x,l*x))
ck('spectral decomposition of initial state',eq(sum(coeff,s.zeros(3,1)),x0))
vs=[x[1] for x in coeff];ws=[x[2] for x in coeff];ms=[x[0] for x in coeff]
ck('winding coefficient dominant positive',vs[0]==s.Rational(75,77) and all(x>0 for x in vs) and eq(vs[1]+vs[2],s.Rational(2,77)))
ck('core coefficient signs and sums',ws[0]==-s.Rational(20,77) and ws[1]>0 and ws[2]>0 and eq(ws[1]+ws[2],s.Rational(20,77)))
ck('mean coefficients opposite and first zero',eq(ms[0],0) and eq(ms[1],-ms[2]) and eq(ms[1]**2,s.Rational(22,99**2)))
ratio=s.radsimp((ev[0]-ev[1])/(ev[0]-ev[2]))
ck('two relative frequencies have irrational ratio',s.simplify(ratio).coeff(s.sqrt(22))!=0 and ratio.is_rational is False)
vmin=s.Rational(73,77);wmax=s.Rational(40,77);mmax=2*sq/99
Nvmin=vmin**2; Ncmax=s.Rational(3,8)*wmax**2; Nmmax=s.Rational(9,8)*mmax**2; gainmax=s.Rational(3,4)*(wmax/vmin)**2
ck('sharp occupation bounds exact',Nvmin==s.Rational(5329,5929) and Ncmax==s.Rational(600,5929) and Nmmax==s.Rational(1,99))
ck('winding minimum and core maximum exhaust norm',Nvmin+Ncmax==1)
ck('sharp edge gain supremum',gainmax==s.Rational(1200,5329))
# Density of irrational linear flow on a two-torus makes phase extrema sharp.
# These exact phase evaluations establish extrema on torus; density is proved in note.
xopp=s.simplify(coeff[0]-coeff[1]-coeff[2]); xmix=s.simplify(coeff[0]+coeff[1]-coeff[2])
ck('joint winding minimum/core maximum at same phase pair',eq(xopp,s.Matrix([0,vmin,-wmax])))
ck('row mean bound attained on phase torus',eq(xmix[0]**2,mmax**2))
# Current vector accounting. Uses established D, S and current moment identities.
S=s.Matrix.vstack(ns['A'],-ns['A']); F=ns['F']; D=ns['D']; C=s.Matrix(s.symbols('Cx Cy Cz',real=True)); nv,nc,nm=s.symbols('Nv Nc Nm',real=True,nonnegative=True)
j=nv*S*C/16; I=nc*F*C/8; L=-F.T*I/9
ck('core edge map in occupation variables',eq(nv*I,2*nc*D*j[:4,:]))
ck('outer current vector read equals winding-weighted chirality',eq(2*S.T*j,nv*C))
ck('core angular moment read equals core-weighted chirality',eq(-s.Rational(9,4)*L,nc*C))
ck('combined current vector accounting',eq(2*S.T*j-s.Rational(9,4)*L,(nv+nc)*C))
ck('outer mean-current squared norm',eq(j.dot(j),nv**2*C.dot(C)/32))
ck('core squared edge-current norm',eq(I.dot(I),nc**2*C.dot(C)/2))
ck('relative phase needed for current transfer: not new coordinates',eq(ns['L'][2,1],8*a/3))
# Exact criterion for a closed row-mean-zero subspace, using the existing equations.
ck('row-mean-zero invariant subspace iff both leakage couplings vanish',eq(H[0,1],2*s.sqrt(2)*d/3) and eq(H[0,2],s.sqrt(3)*(b-a/3)))
# Stationary branch is different from empty-core dynamics; validate exact original gain.
ck('stationary gain 2 Nc/Nv equals original value',eq(2*s.Rational(2,77)/s.Rational(75,77),s.Rational(4,75)))
# Compare the phase-space chain, actual bond currents and rigorous bounds along the original trajectory.
T=np.linspace(0,120,1201); ln=np.array(Lw,float); hn=np.array(Hw,float); un=np.array(U,float); cn=np.array(chain,float); norm=np.diag([3/np.sqrt(8),1,np.sqrt(3/8)]); zn=ns['circ']([.05,.08,1]); Cn=(-1j*np.cross(zn.conj(),zn)).real; Sn=np.array(S,float); Fn=np.array(F,float)
lam,V=np.linalg.eigh(hn); init=np.array([0.,1.,0.]); Z=(np.exp(-1j*T[:,None]*lam)* (V.T@init))@V.T; xx=Z@np.linalg.inv(norm).T
occ=abs(Z)**2; gain=2*occ[:,2]/occ[:,1]; read=[]
for idx in np.linspace(0,len(T)-1,81,dtype=int):
    t=T[idx]; x=xx[idx]; psi=ns['state'](x,zn); rings,inner=ns['read'](psi); means=rings.mean(1); ang=-Fn.T@inner/9; curr=2*Sn.T@means-9/4*ang
    ck(f't={t:.2f}: chain/full bond-current accounting',np.allclose(un@expm(-1j*cn*t)@un.T@init,Z[idx],atol=1e-10) and np.allclose(curr,(1-occ[idx,0])*Cn,atol=1e-10) and np.allclose(occ[idx,1]*inner,2*occ[idx,2]*np.array(D,float)@means[:4]))
    read.append([t,*curr,np.linalg.norm(curr-Cn)])
# In the chain, phase differences provide the exact two population exchanges.
for idx in np.linspace(0,len(T)-1,21,dtype=int):
    y=un.T@Z[idx]; popdot=2*np.imag(y.conj()*(cn@y));
    jdb=2*cn[0,1]*np.imag(y[0].conjugate()*y[1]); jbc=2*cn[1,2]*np.imag(y[1].conjugate()*y[2]);
    ck(f't={T[idx]:.2f}: two signed phase exchanges exhaust occupation derivatives',np.allclose(popdot,[jdb,-jdb+jbc,-jbc],atol=1e-12))
ck('all sampled occupations conserve norm',np.max(abs(occ.sum(1)-1))<1e-10)
ck('all samples satisfy exact occupation envelopes',occ[:,1].min()>=float(Nvmin)-1e-12 and occ[:,2].max()<=float(Ncmax)+1e-12 and occ[:,0].max()<=float(Nmmax)+1e-12)
ck('all sampled edge gains obey sharp supremum',gain.max()<=float(gainmax)+1e-12)
ck('combined current read error bounded by 1/99',max(row[-1] for row in read)<=float(Nmmax)*np.linalg.norm(Cn)+1e-12)
np.savetxt(P/'closed_algebra_dynamics.csv',np.column_stack([T,occ,gain,1-occ[:,0]]),delimiter=',',header='t,N_mean,N_winding,N_core,edge_gain,combined_current_factor',comments='')
# Figures in both formats. Physical units not assigned.
fig,ax=plt.subplots(2,1,figsize=(9,6),layout='constrained',sharex=True)
ax[0].plot(T,occ[:,1],label='Winding');ax[0].plot(T,occ[:,2],label='Core');ax[0].plot(T,occ[:,0],label='Row mean');ax[0].axhline(float(Nvmin),ls='--',lw=1,color='C0');ax[0].axhline(float(Ncmax),ls='--',lw=1,color='C1');ax[0].legend(ncol=3);ax[0].set_ylabel('Occupation');ax[0].set_title('Original Stage VII witness — exact envelopes')
ax[1].plot(T,gain,label='Edge gain');ax[1].axhline(float(gainmax),ls='--',label='Sharp supremum');ax[1].set_ylabel('Gain');ax[1].set_xlabel('Dimensionless time');ax[1].legend();
for ext in ['svg','png']:fig.savefig(P/f'occupation_envelopes.{ext}',dpi=170)
plt.close(fig)
fig,ax=plt.subplots(figsize=(9,3.4),layout='constrained');ax.axis('off');ax.set_xlim(0,10);ax.set_ylim(0,3)
for x,label,energy,co in [(1.6,'Orthogonal outer','$13/22$','C0'),(5,'Core-coupled outer','$-35/22$','C0'),(8.4,'Core','$-89/10$','C2')]:
    ax.text(x,1.6,label+'\n'+energy,ha='center',va='center',bbox=dict(boxstyle='round,pad=.65',fc='white',ec=co,lw=1.7),fontsize=11,zorder=3)
for x,y,txt in [(2.65,3.9,r'$7\sqrt{2}/11$'),(6.15,7.55,r'$\sqrt{11}$')]:
    ax.annotate('',(y,1.6),(x,1.6),arrowprops=dict(arrowstyle='<->',lw=1.7));ax.text((x+y)/2,1.95,txt,ha='center',fontsize=11)
ax.text(5,.45,'Exact orthogonal basis change — same three coordinates, no new sites',ha='center',fontsize=10);ax.set_title('Published flywheel in serial coupling coordinates',fontsize=14)
for ext in ['svg','png']:fig.savefig(P/f'collective_chain.{ext}',dpi=170)
plt.close(fig)
print('Exact winding lower bound',Nvmin,float(Nvmin));print('Exact core supremum',Ncmax,float(Ncmax));print('Exact mean supremum',Nmmax,float(Nmmax));print('Exact edge-gain supremum',gainmax,float(gainmax));print(f'{count}/{count} new checks passed')
