"""Exact face-first sustained circulation on the published 33-tile graph.
All parameters in the explicit witness are dimensionless model choices, not physical constants.
Run with numpy scipy sympy; reruns 984 inherited assertions on import.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "archive" / "stages-I-VI"))
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()):
    import verify_current_closure as c
p=c.p
import numpy as np
import sympy as sp
from scipy.linalg import expm, eigh
from itertools import combinations
from pathlib import Path
checks=[]
def ck(label,ok):
    assert bool(ok),label
    checks.append(label);print(f'PASS {len(checks):03d} {label}',flush=True)
def near(x,y,tol=2e-9):return np.allclose(x,y,atol=tol,rtol=tol)
A=sp.Matrix(p.S[:4]); Z=sp.eye(4)-sp.ones(4)/4
S=sp.Matrix(p.S); base=[]; idx={}
for f,s in enumerate(p.S):
    verts=frozenset(tuple(p.V[i]) for i in np.flatnonzero(p.B[:,f]))
    base.append(next(i for i in p.inner if p.tiles[i][1]==verts))
    for tile in p.ringids[f]:
        vs=p.tiles[tile][1]; same=range(0,4) if f<4 else range(4,8)
        missing=[g for g in same if g!=f and tuple((s+p.S[g])//2) not in vs]
        assert len(missing)==1;idx[f,missing[0]]=tile
edge=set(map(frozenset,p.tedges)); H=sp.zeros(33); bond_classes={k:0 for k in ['ring','transpose','base','column','central','origin']}
r,d,b,a,k,o,e,ec,e0=map(sp.sympify,[-1,sp.Rational(-1,2),-2,-1,-1,-1,0,sp.Rational(-99,10),0])
for i in p.outer:H[i,i]=e
for i in p.inner:H[i,i]=ec
H[0,0]=e0
def bond(i,j,h,kind):
    assert H[i,j]==0 and frozenset((i,j)) in edge
    H[i,j]=H[j,i]=h;bond_classes[kind]+=1
for f in range(8):
    for i,j in combinations(p.ringids[f],2):bond(i,j,r,'ring')
for (f,t),i in idx.items():
    if f<4:bond(i,idx[t^4,f^4],d,'transpose')
    bond(i,base[f],b,'base');bond(i,base[t^4],a,'column')
for i in range(4):
    for j in range(4):
        if i!=j:bond(base[i],base[j^4],k,'central')
for i in base:bond(0,i,o,'origin')
ck('all 104 graph bonds present and nonzero',sum(bond_classes.values())==104 and {frozenset((i,j)) for i,j in combinations(range(33),2) if H[i,j]}==edge)
print('Bond classes:',bond_classes)
for P in p.Tperms:
    PP=sp.Matrix(P.astype(int));ck('exact Td invariance',PP*H*PP.T==H)
# For inversion-even field, X_B(i,j)=X_A(i,j), y_B(i)=y_A(i).
# q=A z, q sum zero. Embed X_st=u q_s+v q_t, y_s=w q_s.
U,V,Y=[sp.zeros(33,3) for _ in range(3)]
for (f,t),i in idx.items():U[i,:]=A[f%4,:];V[i,:]=A[t%4,:]
for f,i in enumerate(base):Y[i,:]=A[f%4,:]
B=U.row_join(V).row_join(Y)
M=sp.Matrix([[e+2*r,-r+d,b],[d,e-r,a],[3*b-a,-b+3*a,ec-k]])
ck('exact graph restriction for every complex q: H B = B (M tensor I3)',H*B==B*sp.kronecker_product(M,sp.eye(3)))
G=sp.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
ck('metric of reduced coordinates and self-adjointness',B.T*B==8*sp.kronecker_product(G,sp.eye(3)) and G*M==M.T*G)
ck('column amplitudes recover q from pure row-winding input',A.T*A==4*sp.eye(3) and Z*A==A)
X0=sp.Matrix([sp.Rational(1,3),1,0]); Xstar=sp.Matrix([sp.Rational(1,3),1,-sp.Rational(4,15)]); lam=sp.Rational(11,10); Lm=-sp.Rational(11,2)-sp.sqrt(22);Lp=-sp.Rational(11,2)+sp.sqrt(22)
ck('stationary eight-ring and inner-occupied eigenvector exact',M*Xstar==lam*Xstar)
ck('eigenvalue is an isolated triplet on entire graph', (10*(H-lam*sp.eye(33))).to_DM().rank()==30)
xx=M.charpoly().gen;ck('exact three eigenfrequencies',sp.expand(M.charpoly(xx).as_expr()-(xx-lam)*(xx-Lm)*(xx-Lp))==0)
coeff=[]
for l in [lam,Lm,Lp]:
    P=sp.eye(3)
    for m in [lam,Lm,Lp]:
        if l!=m:P=P*(M-m*sp.eye(3))/(l-m)
    P=sp.simplify(P);x=sp.simplify(P*X0);coeff.append(x)
    ck('exact spectral projection',sp.simplify(P*P-P)==sp.zeros(3) and sp.simplify(M*x-l*x)==sp.zeros(3,1))
ck('initial coefficients reconstructed',sp.simplify(sum(coeff,sp.zeros(3,1))-X0)==sp.zeros(3,1))
expected=[sp.Matrix([sp.Rational(25,77),sp.Rational(75,77),-sp.Rational(20,77)]),sp.Matrix([1/sp.Integer(231)+5*sp.sqrt(22)/462,1/sp.Integer(77)+sp.sqrt(22)/462,10/sp.Integer(77)+5*sp.sqrt(22)/231]),sp.Matrix([1/sp.Integer(231)-5*sp.sqrt(22)/462,1/sp.Integer(77)-sp.sqrt(22)/462,10/sp.Integer(77)-5*sp.sqrt(22)/231])]
ck('closed-form coefficients',all(sp.simplify(x-y)==sp.zeros(3,1) for x,y in zip(coeff,expected)))
ck('v coefficients positive and dominant coefficient gives uniform lower bound',all(v[1]>0 for v in coeff) and coeff[0][1]-coeff[1][1]-coeff[2][1]==sp.Rational(73,77))
ck('w coefficients positive except first and sum zero',coeff[0][2]<0 and coeff[1][2]>0 and coeff[2][2]>0 and sp.simplify(sum(v[2] for v in coeff))==0)
ck('frequency gap ratio has nonzero irrational coefficient',sp.expand(sp.radsimp((lam-Lm)/(lam-Lp))).coeff(sp.sqrt(22))!=0)
ck('row mean deviation bound exact',coeff[0][0]-coeff[0][1]/3==0 and sp.simplify(coeff[1][0]-coeff[1][1]/3-sp.sqrt(22)/99)==0 and sp.simplify(coeff[2][0]-coeff[2][1]/3+sp.sqrt(22)/99)==0)
vm=sp.simplify(sum(x[1]**2 for x in coeff));wm=sp.simplify(sum(x[2]**2 for x in coeff));ck('positive exact infinite-time intensity means',vm==sp.Rational(50654,53361) and wm==sp.Rational(6500,53361))
threshold=sp.simplify(sp.Rational(3,2)*sp.sqrt(24)*(2*sp.sqrt(22)/99)/(sp.Rational(73,77)))
print('Sufficient all-bond winding threshold min |s.C| >',threshold, '=',float(threshold))
# Exact orientation of local triangle sums and inner angular moment.
orders=[]
for f,ids in enumerate(p.ringids):
    i,j,l=ids
    if np.cross(p.Tpos[i],p.Tpos[j])@p.S[f]<0:j,l=l,j
    orders.append([i,j,l]); tlist=[next(t for (s,t),v in idx.items() if s==f and v==x) for x in [i,j,l]]
    v=[sp.Matrix(p.S[t]) for t in tlist]; ax=sum((v[n].cross(v[(n+1)%3]) for n in range(3)),sp.zeros(3,1))
    ck('three outward edges sum to 4 face normals',ax==4*sp.Matrix(p.S[f]))
cc=[(base[i],base[j^4],i,j) for i in range(4) for j in range(4) if i!=j]
AX=[A[i,:].T.cross(A[j,:].T) for _,_,i,j in cc]
ck('central shared-edge angular Gram equals 32I',sum((v*v.T for v in AX),sp.zeros(3))==32*sp.eye(3))
for i in range(4):ck('central current separately divergence-free for every q',sum((A[i,:].T.cross(A[j,:].T) for j in range(4) if i!=j),sp.zeros(3,1))==sp.zeros(3,1))
# Exact normalization of a unit z and x0, rho=sqrt(3)/8.
rho=sp.sqrt(3)/8;ck('initial normalization exact',8*rho**2*(X0.T*G*X0)[0]==1)
BN=np.array(B,float);HN=np.array(H,float);CN=np.array(c.C1,float);lamN=np.array([lam,Lm,Lp],float);coeffN=np.array(sp.Matrix.hstack(*coeff),float);rhoN=float(rho)
def state(z,xyz):return rhoN*BN@np.kron(xyz,z)
def xoft(t):return coeffN@np.exp(-1j*lamN*t)
def metrics(psi):
    F=p.J(HN,psi)
    jb=np.array([[F[i,j] for i,j in zip(v,v[1:]+v[:1])] for v in orders])
    inner=np.array([F[i,j] for i,j,_,_ in cc]); moment=sum((F[i,j]*np.cross(p.Tpos[i],p.Tpos[j]) for i,j,_,_ in cc),np.zeros(3))
    return jb,inner,moment
# No preferred central axis: derive C from the input q; test generic, non-axis circular inputs.
def circ(n):
    n=np.asarray(n,float);n/=np.linalg.norm(n);e=np.eye(3)[np.argmin(abs(n))];u=e-n*(n@e);u/=np.linalg.norm(u);return (u+1j*np.cross(n,u))/np.sqrt(2)
rs=np.random.default_rng(2113); orientations=[np.array([.05,.08,1.]),np.array([.98,.07,-.08]),np.array([-.04,1.,.06]),np.array([.03,-.07,-1.])]
for _ in range(8):
    n=rs.uniform(-.07,.07,3);n[rs.integers(3)]=rs.choice([-1.,1.]);orientations.append(n)
minbond=1.; mincore=1.; maxerr=0.; series=[]
for ni,n in enumerate(orientations):
    z=circ(n); C=p.chi(z); normal=p.S@C; ck('generic face phases meet sufficient all-ring bound',min(abs(normal))>float(threshold))
    psi0=state(z,np.array(X0,float).ravel()); q=np.array(A,float)@z
    jb,inner,moment=metrics(psi0)
    ck('eight input rings have zero row sum and nonzero equally directed bond currents',near([sum(psi0[i] for i in ring) for ring in orders],0) and near(jb,np.broadcast_to(normal[:,None]/16,(8,3))) and min(abs(jb.ravel()))>0)
    ck('initial inner region empty and column source nonzero',near(psi0[[0]+base],0) and np.linalg.norm((HN@psi0)[base])>0)
    for t in [.001,.037,.17,.5,1,2,4,10,31,89]:
        x=xoft(t);psi=state(z,x);jb,inner,moment=metrics(psi)
        ck('closed form matches full 33-site unitary evolution',near(psi,expm(-1j*HN*t)@psi0,tol=1e-8))
        ck('all 24 outer ring bonds retain their local circulation signs',np.all(jb*normal[:,None]>0))
        ck('exact face-current means and physical inner moment',near(jb.mean(1),abs(x[1])**2*normal/16) and near(moment,-abs(x[2])**2*C/6))
        ck('physical inner subgraph has zero divergence and nonzero current',np.linalg.norm(inner)>1e-11 and near(inner.reshape(4,3).sum(1),0))
        ck('origin dark and global norm conserved',abs(psi[0])<1e-12 and near(np.vdot(psi,psi),1))
        minbond=min(minbond,min(abs(jb.ravel())));mincore=min(mincore,np.linalg.norm(inner))
        maxerr=max(maxerr,np.linalg.norm(psi-expm(-1j*HN*t)@psi0))
    star=state(z,np.array(Xstar,float).ravel());star/=np.linalg.norm(star);jb,inner,moment=metrics(star)
    ck('same Hamiltonian has stationary simultaneous eight full rings and actual core vortex',near(HN@star,float(lam)*star) and min(abs(jb.ravel()))>0 and np.linalg.norm(inner)>0 and np.all(jb*normal[:,None]>0))
    # Perturb all 33 complex coordinates, not only reduced subspace; unitary orbital bound.
    pert=rs.normal(size=33)+1j*rs.normal(size=33);pert*=1e-5/np.linalg.norm(pert);init=star+pert;init/=np.linalg.norm(init);dist=np.linalg.norm(init-star)
    for t in [0,.7,7,70]:
        evolved=expm(-1j*HN*t)@init;target=np.exp(-1j*float(lam)*t)*star;bj,ij,mj=metrics(evolved)
        ck('unrestricted initial perturbation retains exact orbital distance',near(np.linalg.norm(evolved-target),dist,tol=5e-11))
        ck('perturbed stationary flywheel retains all eight rings and core angular sign',np.all(bj*normal[:,None]>0) and mj@C<0)
    if ni==0:
        for t in np.linspace(0,12,601):
            x=xoft(t);psi=state(z,x);jb,ij,mj=metrics(psi)
            series.append([t,abs(x[1])**2,abs(x[2])**2,3/8*abs(x[2])**2,*jb.mean(1),np.linalg.norm(mj),min(abs(jb.ravel()))])
# Perturb graph coefficients, Td preserved (not necessarily inversion): isolated triplet continues.
for trial in range(10):
    raw=np.diag(rs.normal(size=33))
    for i,j in p.tedges:raw[i,j]=raw[j,i]=rs.normal()
    perturb=sum(P@raw@P.T for P in p.Tperms)/24
    eps=1e-4;HH=HN+eps*perturb
    en,EV=eigh(HH);sel=np.argsort(abs(en-float(lam)))[:3];E=EV[:,sel];pr=E@E.T
    star=state(circ(orientations[0]),np.array(Xstar,float).ravel());star/=np.linalg.norm(star);psi=pr@star;psi/=np.linalg.norm(psi)
    FF=p.J(HH,psi);bb=np.array([[FF[i,j] for i,j in zip(v,v[1:]+v[:1])] for v in orders]);ii=np.array([FF[i,j] for i,j,_,_ in cc])
    ck('isolated triplet and all physical ring/core currents persist under graph coupling perturbation',np.ptp(en[sel])<1e-9 and near(HH@psi,en[sel[0]]*psi) and min(abs(bb.ravel()))>1e-5 and np.linalg.norm(ii)>1e-5)
np.savetxt(Path(__file__).with_name('sustained_dynamics.csv'),series,delimiter=',',header='time,outer_factor,inner_factor,inner_occupation,'+','.join(f'j{i+1}' for i in range(8))+',core_moment_norm,min_outer_bond',comments='')
print('Minimum sampled outer bond magnitude:',minbond,'minimum sampled inner current norm:',mincore,'max full trajectory residual:',maxerr)
print('Exact time means |v|², |w|²:',vm,wm)
print(f'{len(checks)}/{len(checks)} new checks passed; {len(p.checks)+len(c.checks)} inherited checks rerun.')
