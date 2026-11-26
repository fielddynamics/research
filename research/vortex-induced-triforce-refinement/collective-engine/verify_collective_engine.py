"""Exact identities and numerical checks of the published Stage VII flywheel.
No new Hamiltonian, no fitted coupling. Run with numpy, scipy, sympy, matplotlib.
"""
from itertools import permutations, combinations
from pathlib import Path
import sympy as s
import numpy as np
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
ncheck=0
def check(msg, yes):
    global ncheck
    assert bool(yes),msg
    ncheck+=1; print(f'PASS {ncheck:03d} {msg}')
A=s.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
S=[A[i,:].T for i in range(4)]
pairs=[(i,j) for i in range(4) for j in range(4) if i!=j]
check('tetrahedral tight frame',A.T*A==4*s.eye(3) and A.T*s.ones(4,1)==s.zeros(3,1))
# Complementary edge identity; epsilon sign fixed by the actual vectors.
D=s.zeros(12,4); F=s.zeros(12,3); B=s.zeros(8,12)
for p,(i,j) in enumerate(pairs):
    k,l=[a for a in range(4) if a not in (i,j)]
    cross=S[i].cross(S[j]); sig=(cross.dot(S[k]-S[l]))/8
    check(f'actual complementary difference {i},{j}',sig in [-1,1] and cross==sig*(S[k]-S[l]))
    D[p,k]=sig;D[p,l]=-sig;F[p,:]=cross.T
    B[i,p]=1;B[4+j,p]=-1
check('edge operator factors through four face currents',D*A==F)
check('edge current is divergence free on all eight bases',B*D==s.zeros(8,4))
check('edge map has rank three and constant kernel',D.rank()==3 and D*s.ones(4,1)==s.zeros(12,1))
check('edge map tight frame identity',D.T*D==8*s.eye(4)-2*s.ones(4))
check('core vector tight frame',F.T*F==32*s.eye(3))
check('edge angular moment operator',-F.T*F/9==-s.Rational(32,9)*s.eye(3))
# One chamber, row-closed outer amplitudes and column read.
R=s.zeros(4,12); Q=s.zeros(4,12)
for p,(i,j) in enumerate(pairs):R[i,p]=1;Q[j,p]=1
Pr=s.eye(12)-R.T*R/3
K=Q*Pr*Q.T
check('row zero projection',Pr**2==Pr and R*Pr==s.zeros(4,12))
check('column read exact tight frame',K==s.Rational(8,3)*s.eye(4)-s.Rational(2,3)*s.ones(4))
check('row closed eight dimensions split into three column-active and five dark',Pr.rank()==8 and (Q*Pr).rank()==3 and 8-(Q*Pr).rank()==5)
U=s.Rational(3,8)*Pr*Q.T
check('unique least-norm column lift',Q*U==s.eye(4)-s.ones(4)/4 and R*U==s.zeros(4,4))
check('column lift orthogonal to row-column nullspace',all(U.T*x==s.zeros(4,1) for x in R.col_join(Q).nullspace()))
check('original row closed flywheel is exactly this lift',U*A==s.Matrix.vstack(*[(S[j]+S[i]/3).T for i,j in pairs])*s.Rational(3,8))
# Exact general Stage VII reduction and a change of coordinates, no new state.
r,d,b,a,k,e,ec=s.symbols('r d b a k e ec', real=True)
M=s.Matrix([[e+2*r,-r+d,b],[d,e-r,a],[3*b-a,-b+3*a,ec-k]])
T=s.Matrix([[1,-s.Rational(1,3),0],[0,1,0],[0,0,1]])
L=s.simplify(T*M*T.inv()); G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
check('exact row mean, winding and core reduction',L==s.Matrix([[e+2*r-d/3,8*d/9,b-a/3],[d,e-r+d/3,a],[3*b-a,8*a/3,ec-k]]))
check('occupation diagonal in three existing coordinates',T.inv().T*G*T.inv()==s.diag(3,s.Rational(8,3),1))
N=s.diag(3/s.sqrt(8),1,s.sqrt(s.Rational(3,8))); H=s.simplify(N*L*N.inv())
check('normalized three-coordinate Hamiltonian real symmetric',s.simplify(H-H.T)==s.zeros(3))
check('empty-core activation independent of base coupling b',L[2,1]==8*a/3)
# Existing Stage VII witness.
subs={r:-1,d:-s.Rational(1,2),b:-2,a:-1,k:-1,e:0,ec:-s.Rational(99,10)}
Mw=M.subs(subs); Lw=L.subs(subs); Hw=H.subs(subs)
xstar=s.Matrix([0,1,-s.Rational(4,15)])
check('existing stationary branch unchanged',Lw*xstar==s.Rational(11,10)*xstar)
check('stationary core-to-ring edge multiplier',s.Rational(3,4)*xstar[2]**2==s.Rational(4,75))
check('stationary normalized central occupation',s.Rational(3,8)*xstar[2]**2/(1+s.Rational(3,8)*xstar[2]**2)==s.Rational(2,77))
check('early core occupation second derivative',s.Rational(3,8)*Lw[2,1]**2==s.Rational(8,3))
# Reconstruct actual 33-site graph, not a new fine model.
An=np.array(A,int); normals=np.vstack([An,-An]); tiles=[frozenset([(0,0,0)])]; tags=['O']
for sg in [1,-1]:
    for f in combinations(range(4),3):
        tri=sg*An[list(f)];mid=lambda x,y:tuple((x+y)//2)
        tiles.append(frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2)));tags.append('C')
        for i in range(3):
            tiles.append(frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i]));tags.append('L')
pos=np.array([np.mean(list(t),axis=0) for t in tiles]);outer=[i for i,t in enumerate(tags) if t=='L']; inner=[i for i,t in enumerate(tags) if t=='C']; edges=[(i,j) for i,j in combinations(range(1,33),2) if len(tiles[i]&tiles[j])==2]+[(0,i) for i in inner]; rings=[]; base=[]; idx={}
for i,sv in enumerate(normals):
    ids=[j for j in outer if tuple(sv) in tiles[j]]
    if np.cross(pos[ids[0]],pos[ids[1]])@sv<0:ids[1],ids[2]=ids[2],ids[1]
    rings.append(ids);base.append(next(j for j in inner if np.allclose(pos[j],sv/3)))
    for j in ids:
        t=next(g for g in range(4*(i//4),4*(i//4)+4) if g!=i and tuple((sv+normals[g])//2) not in tiles[j]);idx[i,t]=j
W=s.zeros(33)
def bond(i,j,v):
    assert W[i,j]==0 and tuple(sorted((i,j))) in edges;W[i,j]=W[j,i]=v
for i in inner:W[i,i]=subs[ec]
for ids in rings:
    for i,j in combinations(ids,2):bond(i,j,subs[r])
for (i,j),p in idx.items():
    if i<4:bond(p,idx[j^4,i^4],subs[d])
    bond(p,base[i],subs[b]);bond(p,base[j^4],subs[a])
for i,j in pairs:bond(base[i],base[j+4],subs[k])
for i in base:bond(0,i,-1)
check('all original 104 graph bonds',len(edges)==104 and sum(W[i,j]!=0 for i,j in combinations(range(33),2))==104)
Emb=s.zeros(33,9)
for (i,j),p in idx.items():Emb[p,:3]=A[i%4,:];Emb[p,3:6]=A[j%4,:]
for i,p in enumerate(base):Emb[p,6:9]=A[i%4,:]
check('full graph reduction exact',W*Emb==Emb*s.kronecker_product(Mw,s.eye(3)))
check('full embedding norm exact',Emb.T*Emb==8*s.kronecker_product(G,s.eye(3)))
# Actual oriented bond-current checks, including full trajectories.
Wn=np.array(W,float); En=np.array(Emb,float); Dn=np.array(D,float); Fn=np.array(F,float); Ln=np.array(Lw,float); rho=np.sqrt(3)/8
rng=np.random.default_rng(20261126)
core_edges=[(base[i],base[j+4]) for i,j in pairs]
def state(x,z):return rho*En@np.kron(np.array(T.inv(),float)@x,z)
def read(psi):
    J=2*np.imag(psi[:,None]*Wn.T*psi.conj()[None,:]); rr=np.array([[J[i,j] for i,j in zip(ids,ids[1:]+ids[:1])] for ids in rings]);return rr,np.array([J[i,j] for i,j in core_edges])
def circ(n):
    n=np.array(n,float);n/=np.linalg.norm(n);u=np.eye(3)[np.argmin(abs(n))];u-=n*np.dot(n,u);u/=np.linalg.norm(u);return (u+1j*np.cross(n,u))/np.sqrt(2)
for i in range(24):
    z=rng.normal(size=3)+1j*rng.normal(size=3);z/=np.linalg.norm(z);x=rng.normal(size=3)+1j*rng.normal(size=3);C=(-1j*np.cross(z.conj(),z)).real;rr,I=read(state(x,z));j=rr.mean(1); av=abs(x[1])**2/16; bv=3*abs(x[2])**2/64
    check('actual bond currents agree with face-edge law',np.allclose(j,av*normals@C) and np.allclose(I,bv*Fn@C) and np.allclose(av*I,bv*Dn@j[:4]))
    check('actual edge and face current norm relation',np.isclose(av**2*np.dot(I,I),4*bv**2*np.dot(j,j)))
    check('three-coordinate occupation equals full norm',np.isclose(np.vdot(state(x,z),state(x,z)).real,9/8*abs(x[0])**2+abs(x[1])**2+3/8*abs(x[2])**2))
# Same instantaneous mean and core currents but opposite transfer, even with norm fixed.
z=circ([.05,.08,1]);x=np.array([0,1,1j]);x=x/np.sqrt(1+3/8);y=x.conj(); rr,I=read(state(x,z));rr2,I2=read(state(y,z))
check('identical full ring and core currents for opposite relative core phase',np.allclose(rr,rr2) and np.allclose(I,I2))
transfer=lambda x: .75*np.imag(x[2].conjugate()*(Ln@x)[2])
check('same currents opposite occupation transfer',np.isclose(transfer(x),-transfer(y)) and abs(transfer(x))>.1)
# Exact already-published model, no modified parameters; plot amplitudes/occupation.
x0=np.array([0.,1.,0.]);ts=np.linspace(0,12,241); rows=[]
for t in ts:
    x=expm(-1j*Ln*t)@x0; rows.append([t,9/8*abs(x[0])**2,abs(x[1])**2,3/8*abs(x[2])**2, .75*abs(x[2])**2/abs(x[1])**2]);
for t in [0,.01,.1,.5,1,2,4,12]:
    x=expm(-1j*Ln*t)@x0;psi=state(x,z);rr,I=read(psi);j=rr.mean(1)
    check('reduced trajectory equals full graph',np.allclose(psi,expm(-1j*Wn*t)@state(x0,z)))
    check('full trajectory face-edge current law',np.allclose(I,(.75*abs(x[2])**2/abs(x[1])**2)*Dn@j[:4]))
arr=np.array(rows);np.savetxt(P/'flywheel_dynamics.csv',arr,delimiter=',',header='t,row_mean_occupation,ring_coordinate_occupation,core_occupation,edge_gain',comments='')
fig,ax=plt.subplots(2,1,figsize=(9,6),sharex=True,layout='constrained');ax[0].plot(ts,arr[:,1:4]);ax[0].legend(['Row mean','Ring winding','Core']);ax[0].set_ylabel('Normalized occupation');ax[0].set_title('Published Stage VII flywheel: one coupled evolution');ax[1].plot(ts,arr[:,4]);ax[1].set_ylabel('Core edge / face difference gain');ax[1].set_xlabel('Dimensionless time');ax[1].axhline(4/75,ls='--',label='Stationary witness gain 4/75');ax[1].legend();fig.savefig(P/'flywheel_dynamics.svg');fig.savefig(P/'flywheel_dynamics.png',dpi=160);plt.close(fig)
print(f'{ncheck}/{ncheck} checks passed')
