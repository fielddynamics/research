"""Face-first Triforce flywheel: exact incidence, winding and model dynamics.
No fitted physical parameters. Run python verify_triforce_flywheel.py.
"""
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()):
    import verify_current_closure as c
p=c.p
import numpy as np
import sympy as sp
from scipy.linalg import expm, eigh
from itertools import product
checks=[]
def ck(name,ok):
    assert bool(ok),name
    checks.append(name); print(f'PASS {len(checks):03d} {name}',flush=True)
def near(a,b,tol=2e-9):return np.allclose(a,b,atol=tol,rtol=tol)
S=p.S; om=np.exp(2j*np.pi/3); rng=np.random.default_rng(20261125)
# Index each outer tile by apex s and omitted vertex t on its ORIGINAL tetrahedron.
idx={}; base=[]
for f,s in enumerate(S):
    bt=frozenset(tuple(p.V[i]) for i in np.flatnonzero(p.B[:,f]));base.append(next(i for i in p.inner if p.tiles[i][1]==bt))
for f,s in enumerate(S):
    for tile in p.ringids[f]:
        vs=p.tiles[tile][1]; same=range(0,4) if f<4 else range(4,8)
        missing=[g for g in same if g!=f and tuple((s+S[g])//2) not in vs]
        assert len(missing)==1;idx[f,missing[0]]=tile
        ck('tile (apex, omitted vertex) belongs to its original Triforce and stellation',len(vs)==3 and len(vs&p.tiles[base[missing[0]^4]][1])==2)
ck('24 ordered pairs exhaust outer tiles exactly',set(idx.values())==set(p.outer))
# Row sum over local ring, column sum over original Triforce face.
# Use one chamber; same geometry on other chamber.
pairs=[(i,j) for i in range(4) for j in range(4) if i!=j]
R=sp.Matrix(4,12,lambda i,k:int(pairs[k][0]==i)); Q=sp.Matrix(4,12,lambda j,k:int(pairs[k][1]==j)); P=sp.eye(12)-R.T*R/3
ck('row and column maps each have three tiles per entry',R*R.T==3*sp.eye(4) and Q*Q.T==3*sp.eye(4))
ck('local winding projector exact rank eight',P*P==P and P.rank()==8 and R*P==sp.zeros(4,12))
ck('column registration on pure winding has exact singular spectrum',Q*P*Q.T==sp.Rational(8,3)*sp.eye(4)-sp.Rational(2,3)*sp.ones(4))
ck('bright dimension three, dark dimension five per chamber', (Q*P).rank()==3 and 8-(Q*P).rank()==5)
# The two sorts of physical central coupling: base of same stellation (row),
# or central triangle of original face (column); the former vanishes on local winding.
edge=set(map(frozenset,p.tedges));
for f,g in idx:
    actual={i for i in p.inner if frozenset((i,idx[f,g])) in edge}
    ck('exact inner neighbors: opposite chamber base and own original central tile',actual=={base[f],base[g^4]})
# local Fourier columns oriented around each outward normal.
U=np.zeros((33,16),complex); orders=[]
for f,ids in enumerate(p.ringids):
    a,b,d=ids
    if np.cross(p.Tpos[a],p.Tpos[b])@S[f]<0:b,d=d,b
    order=[a,b,d];orders.append(order)
    ck('outward ring order is a positive three-cycle',all(np.cross(p.Tpos[i],p.Tpos[j])@S[f]>0 for i,j in zip(order,order[1:]+order[:1])))
    U[order,2*f]=np.array([1,om,om**2])/np.sqrt(3); U[order,2*f+1]=U[order,2*f].conj()
ck('16 local winding modes orthonormal',near(U.conj().T@U,np.eye(16)))
Pwind=U@U.conj().T
ck('local winding projector real',near(Pwind.imag,0))
# Proper tetrahedral subgroup Klein four: translate the same local circulation to all four A rings.
flips=[PP for A,PP in zip(p.Td,p.Tperms) if near(A,np.diag(np.diag(A)))]; assert len(flips)==4
A=sum(F@U[:,0] for F in flips)/2
# Inversion reverses outward sense and swaps chambers. It is a site permutation, not assumed a symmetry of H.
lookup={vs:i for i,(_,vs) in enumerate(p.tiles)}
inv=np.eye(33)[:,[lookup[frozenset(tuple(-np.array(v)) for v in vs)] for _,vs in p.tiles]]
B=inv@A; E=np.column_stack((A,B));
ck('two chamber winding columns are orthonormal',near(E.conj().T@E,np.eye(2)))
ck('all eight rings have pure winding, opposite outward senses across chambers',near(U.conj().T@A,np.array([.5 if i%2==0 and i<8 else 0 for i in range(16)])*np.exp(1j*np.angle(U.conj().T@A))) and near(abs(U.conj().T@B),[.5 if i%2==1 and i>=8 else 0 for i in range(16)]))
# Actual E isotypic space is 2 copies of the real E doublet.
ck('E and conjugate columns span the full four-dimensional E isotypic space',near(E@E.conj().T+E.conj()@E.T,c.EP))
# model parameter tests, including actual original graph and inner response.
C=np.array(c.C1,float); ring=np.array(c.ringmat,float); Ppar=c.Pv[2]; inner=[0]+list(p.inner); outer=list(p.outer)
minring=1.; minpar=1.; maxpred=0.; bright=[]; snapshots=[]
for trial in range(12):
    H=c.randomH(); M=E.conj().T@H@E
    ck('phase-locked eight-ring sector invariant for generic Td Hamiltonian',near(H@E,E@M))
    ee,vec=eigh(M)
    for b in range(2):
        psi=E@vec[:,b]; F=c.flow(H,psi); j=ring.T@F/3; J=C@F
        ck('exact stationary eight pure local rings; all central amplitudes zero',near(H@psi,ee[b]*psi) and near(psi[inner],0) and min(abs(j))>1e-8)
        ck('registered core circulation is purely parity and conserved',near(Ppar@J,J) and near(p.L@J,0))
        ck('ring currents constant per chamber',np.ptp(j[:4])<1e-9 and np.ptp(j[4:])<1e-9)
        ck('opposite outward ring senses for negative hopping',j[0]*j[4]<0)
        minring=min(minring,min(abs(j)));minpar=min(minpar,np.linalg.norm(J))
        if trial==0: print('locked branch',b,'ring currents',j,'core norm',np.linalg.norm(J))
    # Full 16-dimensional local winding sector: dark/bright map to inner tiles.
    G=H[np.ix_(inner,range(33))]@U
    ck('inner excitation rank six (three per chamber)',np.linalg.matrix_rank(G,tol=1e-9)==6)
    # Start all eight local vortex rings in the SAME phase-sign pattern as E but independent phases.
    phases=rng.uniform(0,2*np.pi,8); amp=np.zeros(16,complex)
    amp[0:8:2]=np.exp(1j*phases[:4])/np.sqrt(8);amp[9:16:2]=np.exp(1j*phases[4:])/np.sqrt(8)
    psi=U@amp; f=c.flow(H,psi); j=ring.T@f/3
    ck('initial condition has all eight nonzero local circulating rings and empty inner tiles',min(abs(j))>1e-8 and near(psi[inner],0))
    predicted=np.zeros(33,complex)
    for f in range(8):
        for g in range(8):
            if (f,g) in idx:
                a=idx[f,g]; predicted[base[g^4]]+=H[base[g^4],a]*psi[a]
    ck('actual inner derivative equals original Triforce column sum, row term cancels',near((H@psi)[inner],predicted[inner]))
    rate=np.linalg.norm((H@psi)[inner])**2
    ck('eight local rings excite inner tiles without imposed axis',rate>1e-5)
    t=1e-5; y=expm(-1j*H*t)@psi
    ck('inner occupation has predicted quadratic onset',abs(np.linalg.norm(y[inner])**2/t**2-rate)<1e-4)
    # exact norm and fine/coarse continuity at finite time
    y=expm(-1j*H*.25)@psi; ff=c.flow(H,y); J=C@ff
    ck('finite-time evolution preserves norm and registered continuity',near(np.linalg.norm(y),1) and near(p.L@J,np.array(c.C0,float)@(2*np.real(y.conj()*(-1j*H@y)))))
    cc=[(i,j) for i,j in p.tedges if i in p.inner and j in p.inner]; innerflows=np.array([p.J(H,y)[i,j] for i,j in cc])
    ck('excited central triangles carry actual shared-edge currents',np.linalg.norm(innerflows)>1e-8)
    ck('centre remains dark under invariant linear dynamics (no A1 component)',abs(y[0])<1e-9)
    bright.append(rate)
    if trial==0:
        for t in np.linspace(0,4,201):
            y=expm(-1j*H*t)@psi; ff=c.flow(H,y); j=ring.T@ff/3; J=C@ff
            snapshots.append([t,np.linalg.norm(y[inner])**2,*j,np.linalg.norm(c.Pv[0]@J),np.linalg.norm(c.Pv[1]@J),np.linalg.norm(Ppar@J)])
ck('tested E states have nonzero parity core registration',minpar>1e-8)
print('Minimum stationary ring magnitude:',minring,'minimum stationary registered parity norm:',minpar)
print('Initial inner growth coefficient range:',min(bright),max(bright))
np.savetxt('triforce_dynamics.csv',snapshots,delimiter=',',header='time,inner_occupation,'+','.join(f'j{i}' for i in range(8))+',principal_cycle,complementary_cycle,parity_cycle',comments='')
print(f'{len(checks)}/{len(checks)} new checks passed; {len(p.checks)+len(c.checks)} inherited checks rerun.')
