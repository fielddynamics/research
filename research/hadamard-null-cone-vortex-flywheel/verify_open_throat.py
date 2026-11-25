"""Stage VIII: source, outlet and axial observable on the 33-tile Triforce graph.
All rates and frequency are dimensionless witness choices, not GFD constants.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)])
S=np.vstack((A,-A)); tiles=[('O',frozenset([(0,0,0)]))]
for tag,T in [('A',A),('B',-A)]:
    for f in combinations(range(4),3):
        tri=T[list(f)]; mid=lambda a,b:tuple((a+b)//2)
        tiles.append(('C'+tag,frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2))))
        for i in range(3): tiles.append(('E'+tag,frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i])))
pos=np.array([np.mean(list(v),axis=0) for _,v in tiles]); lookup={v:i for i,v in enumerate(tiles)}
outer=[i for i,(k,_) in enumerate(tiles) if k[0]=='E']; inner=[i for i,(k,_) in enumerate(tiles) if k[0]=='C']
edges=[(i,j) for i,j in combinations(range(1,33),2) if len(tiles[i][1]&tiles[j][1])==2]+[(0,i) for i in inner]
rings=[]; idx={}; base=[]
for f,s in enumerate(S):
    ids=[i for i in outer if tuple(s) in tiles[i][1]]
    if np.cross(pos[ids[0]],pos[ids[1]])@s<0: ids[1],ids[2]=ids[2],ids[1]
    rings.append(ids)
    base.append(next(i for i in inner if np.allclose(pos[i],s/3)))
    for i in ids:
        t=next(g for g in range(4*(f//4),4*(f//4)+4) if g!=f and tuple((s+S[g])//2) not in tiles[i][1]);idx[f,t]=i
# Six collective spatial triplets (row, column, central for each chamber).
B=np.zeros((33,18)); Y=np.zeros((33,6))
for (f,t),i in idx.items():
    b=9*(f//4); B[i,b:b+3]=A[f%4];B[i,b+3:b+6]=A[t%4]
for f,i in enumerate(base):
    b=9*(f//4); B[i,b+6:b+9]=A[f%4];Y[i,3*(f//4):3*(f//4)+3]=A[f%4]/2
Q=np.linalg.qr(B)[0]; P=Y@Y.T
checks=[]
def ck(n,v):
    assert bool(v),n;checks.append(n);print(f'PASS {len(checks):03d} {n}')
def near(a,b,tol=1e-9):return np.allclose(a,b,atol=tol,rtol=tol)
def chi(z):return (-1j*np.cross(z.conj(),z)).real
def J(H,psi):return 2*np.imag(psi[:,None]*H.T*psi.conj()[None,:])
def ringcurr(H,x):
    j=J(H,x);return np.array([[j[a,b] for a,b in zip(r,r[1:]+r[:1])] for r in rings])
def inner_moment(H,x):
    j=J(H,x);return sum((j[a,b]*np.cross(pos[a],pos[b]) for a,b in edges if a in inner and b in inner),np.zeros(3))
def matrix(kind):
    H=np.zeros((33,33))
    for a,b in edges:
        ta,tb=tiles[a][0],tiles[b][0]
        # Exploratory capacity-weight mapping: same-chamber edges 21 or 13; cross-chamber / centre 17.
        h=-1 if kind=='uniform' else -(21 if ta[-1]==tb[-1]=='A' else 13 if ta[-1]==tb[-1]=='B' else 17)/17
        H[a,b]=H[b,a]=h
    return H
z=np.array([1,1j,0],complex)/np.sqrt(2);C=chi(z)
def source(z):
    x=np.zeros(33,complex);q=A@z
    for (f,t),i in idx.items():x[i]=q[f%4]/3+q[t%4]
    return x/np.linalg.norm(x)
f=source(z); gamma=.5
ck('33 sites, 104 actual edges, 8 disjoint three-tile rings',len(tiles)==33 and len(edges)==104 and len(set(sum(rings,[])))==24)
ck('six orthonormal directional output modes, no scalar outlet',near(Y.T@Y,np.eye(6)) and near(Y.T@np.ones(33),0))
ck('pure row-winding source with no initial core',all(abs(sum(f[r]))<1e-12 for r in rings) and near(f[inner],0))
for R in [np.diag(sig)@np.eye(3,dtype=int)[list(p)] for p in permutations(range(3)) for sig in product([-1,1],repeat=3) if np.prod(sig)==1]:
    U=np.eye(33)[:,[lookup[k,frozenset(tuple(R@np.array(a)) for a in vs)] for k,vs in tiles]]
    ck('directional port projector respects Td',near(U@P@U.T,P))
    ck('chirality transforms axially',near(chi(R@z),np.linalg.det(R)*R@C))
    ck('uniform and capacity-assigned graph respect Td',all(near(U@matrix(k)@U.T,matrix(k)) for k in ['uniform','capacity']))
# Scan frequency; choose a shared witness before testing steady and transient flux.
for kind in ['uniform','capacity']:
    H=matrix(kind); h=Q.T@H@Q; p=Q.T@P@Q
    ck(kind+' collective sector exactly invariant',near(H@Q,Q@h))
    ck(kind+' closed scalar centre is dark',near(H[0]@Q,0))
    print(kind,'candidate frequencies:')
    for nu in [-10,-6,-4,-3,-2,-1,0,1,2,3,4,6,10]:
        try: x=Q@np.linalg.solve(nu*np.eye(18)-h+1j*gamma*p,Q.T@f)
        except np.linalg.LinAlgError:continue
        j=ringcurr(H,x); signs=np.sign(S@C)
        print(nu, np.min(j*signs[:,None]),np.linalg.norm(inner_moment(H,x)),2*gamma*np.linalg.norm(Y.T@x)**2)
# Common drive frequency chosen from scan above, not a physical prediction.
nu=2.; records=[]; summaries=[]
for kind in ['uniform','capacity']:
    H=matrix(kind); h=Q.T@H@Q; p=Q.T@P@Q
    K=nu*np.eye(18)-h+1j*gamma*p
    x=Q@np.linalg.solve(K,Q.T@f)
    j=J(H,x); b=ringcurr(H,x); L=inner_moment(H,x)
    port=Y.T@x; flux=2*gamma*np.vdot(port,port).real
    injection=2*np.imag(np.vdot(x,f)); cut=j[np.ix_(outer,inner)].sum()
    ck(kind+' full forced equation',near((nu*np.eye(33)-H+1j*gamma*P)@x,f))
    ck(kind+' all 24 ring directions preserved in driven state',np.min(b*np.sign(S@C)[:,None])>0)
    ck(kind+' actual central angular current nonzero',np.linalg.norm(L)>1e-5)
    ck(kind+' physical inward cut flux = outlet = source',flux>0 and near([injection,cut],[flux,flux]))
    cuts=np.array([j[np.ix_(r,inner)].sum() for r in rings])
    ck(kind+' ring-resolved flux balances total cut',near(cuts.sum(),flux))
    if kind=='uniform': ck('all eight rings feed inner region with equal positive net cut',near(cuts,np.full(8,3/20)))
    else: ck('asymmetry permits one chamber to feed and other to receive net inner flow',np.all(cuts[:4]<0) and np.all(cuts[4:]>0))
    print(kind,'ring-resolved net inward cut:',cuts.tolist())
    ck(kind+' scalar O still dark',abs(x[0])<1e-12)
    ck(kind+' local steady continuity including directional sink',near(-j.sum(1)+2*np.imag(x.conj()*f)-2*gamma*np.real(x.conj()*(P@x)),0))
    # In this sector P acts as identity on inner amplitudes, so local loss nonnegative.
    ck(kind+' local outlet loss nonnegative',near((P@x)[inner],x[inner]))
    # Chirality of outgoing polar triplet amplitudes, not polar flow velocity.
    axial=sum((chi(v) for v in port.reshape(2,3)),np.zeros(3))*2*gamma
    xr=Q@np.linalg.solve(K,Q.T@source(z.conj())); pr=Y.T@xr
    ar=sum((chi(v) for v in pr.reshape(2,3)),np.zeros(3))*2*gamma
    ck(kind+' axial output parallel to chirality',near(axial,flux*C))
    ck(kind+' reversing input swirl reverses axial output but not mass/occupation flux',near(ar,-axial) and near(2*gamma*np.linalg.norm(pr)**2,flux))
    ck(kind+' all eight ring means reverse under conjugate input polarization',near(ringcurr(H,xr).mean(1),-b.mean(1)))
    # Finite unpumped packet: exact open linear evolution and integrated flux.
    G=-1j*h-gamma*p; initial=Q.T@f
    def rhs(t,X):
        a=X[:18];return np.r_[G@a,2*gamma*np.vdot(Y.T@Q@a,Y.T@Q@a).real]
    sol=solve_ivp(rhs,[0,30],np.r_[initial,0j],rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,30,301))
    norm=np.sum(abs(sol.y[:18])**2,axis=0);out=sol.y[-1].real
    ck(kind+' integrated packet occupation conservation',near(norm+out,1,tol=1e-7))
    ck(kind+' unpumped packet drains and cannot supply indefinite throughput',out[-1]>.01 and np.min(np.diff(out))>=-1e-9 and out[-1]<=1+1e-8)
    ck(kind+' closed packet conserves occupation',near(np.linalg.norm(expm(-1j*h*30)@initial),1))
    for t,N,D in zip(sol.t,norm,out):records.append([kind,t,N,D])
    summaries.append((kind,flux,np.min(b*np.sign(S@C)[:,None]),np.linalg.norm(L),out[-1],np.linalg.norm(port[:3])**2,np.linalg.norm(port[3:])**2))
# Neutral receiver: canonical axial position a and momentum p; time-reversal even Hamiltonian.
# H_r=(p^2+Omega^2 a^2)/2-g p.C. Constant C for collinear backreaction.
g=.7;Omega=1.3
for t in np.linspace(0,10,31):
    a=-g*C*np.sin(Omega*t)/Omega; mom=g*C*(1-np.cos(Omega*t)); vel=mom-g*C
    ck('neutral axial receiver exact energy and collinearity',near((mom@mom+Omega**2*(a@a))/2-g*mom@C,0) and near(np.cross(mom,C),0) and near(vel,-g*C*np.cos(Omega*t)))
# U(1) no-go for phase-neutral quadratic forcing of phase-charged complex vector.
for phase in np.linspace(0,2*np.pi,13):ck('chirality invariant under global phase',near(chi(np.exp(1j*phase)*z),C))
# Nonlinear, phase-neutral read cannot by itself transfer occupation; real Hamiltonian preserves U(1).
# Exact reduced rational certificate at nu=2 for both weight choices.
import sympy as sp
B1=sp.Matrix(B[:,::3].astype(int)); dual=(B1.T*B1).inv()*B1.T
for kind in ['uniform','capacity']:
    HH=sp.Matrix(matrix(kind)).applyfunc(lambda v:sp.Rational(float(v)).limit_denominator(17)); PP=sp.Matrix(P).applyfunc(lambda v:sp.Rational(float(v)).limit_denominator(4)); M=dual*HH*B1; D=dual*PP*B1
    ck(kind+' exact reduced graph and port intertwining',HH*B1==B1*M and PP*B1==B1*D)
    X=sp.Matrix([sp.Rational(1,3),1,0,sp.Rational(1,3),1,0]); T=2*sp.eye(6)-M+sp.I*D/2; sol=T.inv()*X
    ck(kind+' exact nonzero central coefficients for forced response',all(sp.simplify(sol[i]*sp.conjugate(sol[i]))>0 for i in [2,5]))
    print(kind,'exact reduced coefficients:',list(map(sp.simplify,sol)))
    if kind=='uniform':
        zz=sp.Matrix([1,sp.I,0]); bb=sp.Matrix(B.astype(int))
        raw=bb*sp.kronecker_product(X,zz); scale2=1/(sp.conjugate(raw).T*raw)[0]; xx=bb*sp.kronecker_product(sol,zz)*sp.sqrt(scale2)
        def jj(a,b): return sp.simplify(2*sp.im(xx[a]*HH[b,a]*sp.conjugate(xx[b])))
        ck('uniform exact positive inward flux per ring',all(sum(jj(a,b) for a in r for b in inner)==sp.Rational(3,20) for r in rings))
        ck('uniform exact all 24 ring bond signs',all(jj(a,b)*int(S[i,2])>0 for i,r in enumerate(rings) for a,b in zip(r,r[1:]+r[:1])))
        ck('uniform exact total outlet occupation flux 6/5',sp.simplify((sp.conjugate(xx).T*PP*xx)[0])==sp.Rational(6,5))
root=Path(__file__).parent
import csv
with (root/'open_throat_dynamics.csv').open('w') as ff:
    w=csv.writer(ff);w.writerow(['model','time','remaining_occupation','cumulative_outlet']);w.writerows(records)
fig,axes=plt.subplots(1,2,figsize=(10,4))
for kind in ['uniform','capacity']:
    d=np.array([r[1:] for r in records if r[0]==kind]);axes[0].plot(d[:,0],d[:,2],label=kind)
axes[0].set(xlabel='Dimensionless time',ylabel='Cumulative outlet occupation',title='Unpumped packet: finite drainage');axes[0].legend();axes[0].grid(alpha=.2)
axes[1].bar([0,1],[r[1] for r in summaries]);axes[1].set(xticks=[0,1],xticklabels=['Uniform','Capacity mapping'],ylabel='Occupation per model time',title='Driven state: source = cut = outlet');axes[1].grid(axis='y',alpha=.2)
fig.tight_layout();fig.savefig(root/'figures/11_open_throat.svg');plt.close(fig)
for r in summaries:print('model, steady flux, min directed ring bond, inner moment norm, packet outlet at t=30, port A, port B:',r)
print(f'{len(checks)}/{len(checks)} new checks passed.')
