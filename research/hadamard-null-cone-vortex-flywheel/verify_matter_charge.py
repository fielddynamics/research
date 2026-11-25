"""Conditional matter/charge extension of SFM. All units dimensionless.
Exact algebra, a reduced conservative nonlinear model, and static diamond Gauss law.
Not a derivation of electron mass, elementary charge, spin, physical binding or Maxwell dynamics.
"""
from pathlib import Path
from itertools import product
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import pinvh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
# Reuse the actual previously specified 36-coordinate tile Hamiltonian (not historical tests).
ns={'__file__':str(root/'verify_coupled_origins.py')}
exec((root/'verify_coupled_origins.py').read_text().split("ck('33 original geometric positions;")[0],ns)
A,S,H,tiles,dim=[ns[k] for k in ['A','S','H','tiles','d']]
checks=[]
def ck(name,test):
    assert bool(test),name
    checks.append(name);print(f'PASS {len(checks):03d} {name}',flush=True)
def near(x,y,tol=1e-9):return np.allclose(x,y,atol=tol,rtol=tol)
rng=np.random.default_rng(20261124)
T=np.c_[np.ones(8,dtype=int),S];par=np.prod(S,axis=1);U=np.c_[T,par[:,None]*T]
ck('full eight-register Walsh transform is exactly orthogonal up to 8',np.array_equal(U.T@U,8*np.eye(8,dtype=int)))
ck('four records in each chamber resolve all four chamber coordinates',all(np.array_equal(t.T@t,4*np.eye(4,dtype=int)) for t in (T[:4],T[4:])))
for _ in range(16):
    c=rng.normal(size=8)+1j*rng.normal(size=8);r=U@c;plus=c[:4]+c[4:];minus=c[:4]-c[4:]
    nA,nB=[np.vdot(x,x).real for x in (plus,minus)]
    ck('complete dual-chamber read, inverse, independent intensities and parity difference',near(U.T@r/8,c) and near(abs(r[:4])@abs(r[:4])/4,nA) and near(abs(r[4:])@abs(r[4:])/4,nB) and near(nB-nA,-4*np.real(np.vdot(c[:4],c[4:]))))
    def P(x):return 2*np.real(x[0].conj()*x[1:])
    def Q(x):b=x[1:];return 2*np.real(b[[1,2,0]].conj()*b[[2,0,1]])
    ck('separate chamber polar read and quadrupole alias removal identity',near(A.T@abs(r[:4])**2/4,P(plus)+Q(plus)) and near((-A).T@abs(r[4:])**2/4,P(minus)-Q(minus)))
    # energy and charge-like scalar transform differently under chamber exchange
    ck('interchanging chambers preserves total occupation and reverses signed read',near(nA+nB,2*np.vdot(c,c).real) and near(4*np.real(np.vdot(c[:4],-c[4:])),nB-nA))
# Original Hamiltonian: occupation parity is not a conserved charge.
qdiag=np.zeros(dim,dtype=int)
for i,(tag,_) in enumerate(tiles):
    if tag!='O':qdiag[i]=1 if tag[-1]=='B' else -1
Qmat=np.diag(qdiag);comm=H@Qmat-Qmat@H
cross=[(i,j) for i in range(33) for j in range(i+1,33) if qdiag[i]*qdiag[j]==-1 and H[i,j]!=0]
ck('old Hamiltonian has explicit cross-chamber bonds',len(cross)>0)
i,j=cross[0];x=np.zeros(dim,complex);x[i]=1/np.sqrt(2);x[j]=1j/np.sqrt(2)
qdot=(1j*np.vdot(x,comm@x)).real
ck('explicit old-state counterexample to chamber occupation charge conservation',abs(qdot)>1 and near(qdot,2*np.real(np.vdot(Qmat@x,-1j*H@x))))
print('old cross-chamber bond count',len(cross),'counterexample indices',i,j,'qdot',qdot)
# Conditional reduced local Hamiltonian. x_A,x_B are excess retained-mode registers,
# not the baseline eight geometric vortices or literal tile occupations.
# Both minima have circular directional winding; outward/inward read is elastic response,
# NOT persistent material or probability flux. Sign of q is a modelling premise.
eps=.2;lam=1.;gamma=.7;xi=.8;delta=.5
nstar=(2+np.sqrt(1-3*eps/lam))/3;nbar=(2-np.sqrt(1-3*eps/lam))/3
V=lambda n:eps*n+lam*n*(n-1)**2
Vp=lambda n:eps+lam*(3*n*n-4*n+1)
Vpp=lambda n:lam*(6*n-4)
sign=np.array([-1.,1.]);circ=np.array([0,1,1j,0])/np.sqrt(2)
def density(z):return np.sum(abs(z)**2,axis=1)
def charge(z):return sign@density(z)
def local_energy(z,u,p):
    n=density(z);q=sign@n;b=z[:,1:]
    return np.sum(V(n))+gamma*n[0]*n[1]+delta*np.sum(abs(z[:,0])**2)+xi*np.sum(abs(np.sum(b*b,axis=1))**2)+.5*(p@p+(u-q/4)@(u-q/4))
def gradient(z,u):
    n=density(z);q=sign@n;g=(Vp(n)+gamma*n[::-1]-sign*np.sum(u-q/4)/4)[:,None]*z
    g[:,0]+=delta*z[:,0];b=z[:,1:];g[:,1:]+=2*xi*np.sum(b*b,axis=1)[:,None]*b.conj();return g
def pack(z,u,p):return np.r_[z.real.ravel(),z.imag.ravel(),u,p]
def unpack(y):return (y[:8]+1j*y[8:16]).reshape(2,4),y[16:20],y[20:24]
def rhs(t,y):
    z,u,p=unpack(y);return pack(-1j*gradient(z,u),p,-(u-charge(z)/4))
ck('positive-energy vortex well and intervening barrier are exact stationary roots',near(Vp(nstar),0) and near(Vp(nbar),0) and Vpp(nstar)>0 and Vpp(nbar)<0 and V(nstar)>0 and V(nbar)>V(nstar))
branches=[]
for name,k in [('neutral',None),('inward A',0),('outward B',1)]:
    z=np.zeros((2,4),complex)
    if k is not None:z[k]=np.sqrt(nstar)*circ
    q=charge(z);u=np.full(4,q/4);p=np.zeros(4);y=pack(z,u,p)
    ck(name+' exact static solution and correct radial sign',near(rhs(0,y),0) and near(u.sum(),q) and (q==0 if k is None else q*sign[k]>0))
    C=(-1j*np.cross(z[:,1:].conj(),z[:,1:])).real
    ck(name+' circular vortex read and empty/occupied excess sector',near(np.linalg.norm(C,axis=1),density(z)))
    ck(name+' local-minimum normal directions have positive curvature',Vp(0)>0 and (k is None or Vpp(nstar)>0 and Vp(0)+gamma*nstar>0))
    E0=local_energy(z,u,p);branches.append((name,z.copy(),u.copy(),p.copy(),E0))
    # Random perturbations test local minimum, not a global stability proof.
    diffs=[]
    for _ in range(100):
        y1=y+.005*rng.normal(size=len(y));diffs.append(local_energy(*unpack(y1))-E0)
    ck(name+' 100 local energy perturbations nonnegative',min(diffs)>0)
    # Perturb and evolve the closed conservative reduced Hamiltonian.
    y1=y+.02*rng.normal(size=len(y));sol=solve_ivp(rhs,(0,60),y1,t_eval=np.linspace(0,60,601),rtol=2e-10,atol=2e-12,method='DOP853')
    ck(name+' conservative perturbation integration successful',sol.success)
    E=np.array([local_energy(*unpack(v)) for v in sol.y.T]);densities=np.array([density(unpack(v)[0]) for v in sol.y.T]);n0=densities[0]
    ck(name+' energy conserved',np.max(abs(E-E[0]))<1e-7)
    ck(name+' both excess-mode charges conserved separately',np.max(abs(densities-n0))<1e-7)
    print(name,'n=',density(z),'q=',q,'energy=',E0,'perturbed max drift',np.max(abs(E-E[0])),np.max(abs(densities-n0)))
    # Finite difference for energy gradient.
    zp,up,pp=unpack(y1);dz=rng.normal(size=(2,4))+1j*rng.normal(size=(2,4));h=1e-6
    fd=(local_energy(zp+h*dz,up,pp)-local_energy(zp-h*dz,up,pp))/(2*h)
    ck(name+' exact complex Hamiltonian gradient verified by finite difference',near(fd,2*np.real(np.vdot(gradient(zp,up),dz)),2e-7))
ck('charge conjugate example energies equal and signs reverse',near(branches[1][-1],branches[2][-1]) and near(branches[1][2],-branches[2][2]))
# Optional neutral TetA response rings: actual four geometric lateral triplets.
# Independent neutral w variables do not carry Q. Positive symmetric-read stiffness
# h|sum w|^2 has an effective +h ring hopping (not the old -1 Hamiltonian).
# This separate nonnegative energy supplies static circulation, not spontaneous
# creation of a charged/neutral amplitude from exactly zero.
from itertools import permutations
ordered=[]
for i in range(4):
    ordered.append([next(j for j in range(4) if j!=i and ns['idx'][i,j]==site) for site in ns['rings'][i]])
M=np.array([A[js]+A[i]/3 for i,js in enumerate(ordered)])
ck('four real geometric row projections annihilate symmetric sum',near(M.sum(1),0))
hw=.4;nu=.5;align=.9
def response_matrices(z):
    v=np.einsum('ijk,xk->xij',M,z[:,1:]);return np.einsum('xij,xik->ijk',v,v.conj())
def response_energy(z,w):
    S= response_matrices(z);t=np.trace(S,axis1=1,axis2=2).real;n=np.sum(abs(w)**2,axis=1)
    return hw*np.sum(abs(w.sum(1))**2)+.5*np.sum((n-nu*t)**2)+align*np.sum(t*n-np.einsum('ij,ijk,ik->i',w.conj(),S,w).real)
resp=[]
for name,z,u,p,e in branches:
    b=z[:,1:].sum(0);w=np.sqrt(nu)*np.einsum('ijk,k->ij',M,b);S=response_matrices(z);t=np.trace(S,axis1=1,axis2=2).real
    ck(name+' exact zero of nonnegative neutral-ring response energy',near(response_energy(z,w),0) and near(np.sum(abs(w)**2,axis=1),nu*t))
    # Symmetric-read hopping plus alignment term. On-site shifts carry no edge current.
    Hring=hw*np.ones((4,3,3))-align*S
    cur=np.array([[2*np.imag(w[i,j].conj()*Hring[i,j,(j+1)%3]*w[i,(j+1)%3]) for j in range(3)] for i in range(4)])
    ck(name+' every neutral response ring has conserved circulating edge current',near(cur,cur[:,[0]]) and (np.max(abs(cur))<1e-10 if name=='neutral' else np.min(abs(cur))>1e-3))
    ck(name+' independent response phases and charge-conserving matter phases leave energy unchanged',near(response_energy(z*np.exp(1j*np.array([.4,-.7]))[:,None],w*np.exp(1j*np.arange(4))[:,None]),response_energy(z,w)))
    # Each squared term is nonnegative; check nearby arbitrary states.
    ck(name+' positive response energy for 20 random perturbations',all(response_energy(z+.02*(rng.normal(size=z.shape)+1j*rng.normal(size=z.shape)),w+.02*(rng.normal(size=w.shape)+1j*rng.normal(size=w.shape)))>=-1e-10 for _ in range(20)))
    resp.append([name,*u,*cur[:,0]])
    print(name,'TetA response ring currents',cur[:,0])
# Rotation/permutation covariance of the row projections, including order reversal.
for R in [np.diag(sig)@np.eye(3,dtype=int)[list(p)] for p in permutations(range(3)) for sig in product([-1,1],repeat=3) if np.prod(sig)==1]:
    perm=[next(j for j,t in enumerate(A) if np.array_equal(t,R@s)) for s in A]
    ck('neutral response geometry covariant under all 24 tetrahedral symmetries',all(near(M[perm[i],ordered[perm[i]].index(perm[j])],R@M[i,k]) for i in range(4) for k,j in enumerate(ordered[i])))
import csv
with (root/'matter_charge_rings.csv').open('w') as f:
    wr=csv.writer(f);wr.writerow(['branch','u1','u2','u3','u4','J1','J2','J3','J4']);wr.writerows(resp)
fig,ax=plt.subplots(1,2,figsize=(9,3.6));xx=np.arange(4);labels=['neutral','inward A','outward B']
for k,row in enumerate(resp):
    ax[0].bar(xx+(k-1)*.24,row[1:5],width=.22,label=labels[k]);ax[1].bar(xx+(k-1)*.24,row[5:9],width=.22,label=labels[k])
for a,title,ylabel in zip(ax,['Signed radial read','Neutral TetA ring circulation'],['Response per port','Current per ring edge']):
    a.set(xticks=xx,xticklabels=['1','2','3','4'],xlabel='Hadamard port / ring',ylabel=ylabel,title=title);a.axhline(0,color='.6',lw=.7);a.legend(fontsize=8)
fig.tight_layout();fig.savefig(root/'figures/35_matter_response_rings.svg');fig.savefig(root/'figures/35_matter_response_rings.png',dpi=180);plt.close(fig)

# Charge-preserving dressed interchamber transfer. Separate optional rotor completion;
# it is not included in the pure-sector minima above. q_total=q+2p_theta.
hop=.31;inertia=1.4
# x_A and x_B scalar modes suffice for the symmetry witness (same for vector dot product).
def rotor_pack(z,theta,p):return np.r_[z.real,z.imag,theta,p]
def rotor_unpack(y):return y[:2]+1j*y[2:4],y[4],y[5]
def rotor_energy(z,theta,p):return 2*hop*np.real(np.exp(1j*theta)*z[0].conj()*z[1])+p*p/(2*inertia)
def rotor_rhs(t,y):
    z,theta,p=rotor_unpack(y);v=np.exp(1j*theta);g=hop*np.array([v*z[1],v.conj()*z[0]]);pd=2*hop*np.imag(v*z[0].conj()*z[1]);return rotor_pack(-1j*g,p/inertia,pd)
def rotor_charge(z,theta,p):return sign@abs(z)**2+2*p
for _ in range(12):
    z=rng.normal(size=2)+1j*rng.normal(size=2);theta,p,ang=rng.normal(size=3)
    zp=z*np.exp(-1j*ang*sign)
    ck('dressed exchange invariant under relative chamber phase plus compensating rotor',near(rotor_energy(z,theta,p),rotor_energy(zp,theta+2*ang,p)))
y=rotor_pack(np.array([1.,.15j]),.2,.1);sol=solve_ivp(rotor_rhs,(0,40),y,t_eval=np.linspace(0,40,401),rtol=2e-11,atol=2e-13,method='DOP853')
ck('dressed exchange integrated successfully',sol.success)
rz=[rotor_unpack(v) for v in sol.y.T];qbare=np.array([sign@abs(z)**2 for z,t,p in rz]);qc=np.array([rotor_charge(*v) for v in rz]);ee=np.array([rotor_energy(*v) for v in rz]);nn=np.array([np.vdot(z,z).real for z,t,p in rz])
ck('bare chamber difference actually changes during dressed transfer',np.ptp(qbare)>.1)
ck('dressed total charge, energy and norm conserved',max(np.ptp(qc),np.ptp(ee),np.ptp(nn))<1e-8)
ck('undressed or dressed nonzero linear hopping does not preserve exactly empty B',abs(rotor_rhs(0,rotor_pack(np.array([1.,0.]),0.,0.))[3])>.1)
# Static candidate electric read on same diamond graph. Add Gauss constraint as premise;
# minimum squared edge read gives unique curl-free edge response.
source=(root/'verify_field_read.py').read_text();local={'A':A,'np':np,'product':product};exec(source[source.index('def lattice('):source.index('xyz,NB,dirs,Bmat=lattice(4)')],local)
xyz,NB,dirs,Bmat=local['lattice'](6);N=len(NB);edges=[(i,int(j)) for i in range(0,N,2) for j in NB[i]]
D=np.zeros((N,len(edges)));ii,jj=np.array(edges).T;D[ii,np.arange(len(edges))]=1;D[jj,np.arange(len(edges))]=-1
L=D@D.T;G=pinvh(L,rtol=1e-12);P=np.eye(N)-np.ones((N,N))/N
ck('same diamond graph has four ports and one gauge zero mode',near(np.diag(L),4) and near(L@G,P,2e-8))
for _ in range(8):
    q=rng.normal(size=N);q-=q.mean();phi=G@q;E=D.T@phi;trial=rng.normal(size=len(edges));cycle=trial-D.T@(G@(D@trial))
    ck('discrete Gauss law, orthogonality to divergence-free perturbations and minimal energy',near(D@E,q,2e-8) and near(D@cycle,0,2e-8) and abs(E@cycle)<1e-7 and near(.5*E@E,.5*q@phi,2e-8))
    cut=rng.random(N)>.5;ck('regional electric flux equals enclosed signed charge',near(q[cut].sum(),((cut.astype(int)@D)@E),2e-8))
# Pair interaction energies, with uniform compensating background per source.
# Use exact graph distances via shortest path. Sample along FCC primitive vector.
from scipy.sparse.csgraph import shortest_path
dist=shortest_path(L<0,directed=False,unweighted=True,indices=0)
rows=[]
for r in sorted(set(dist[1:])):
    inds=np.where(dist==r)[0];rows.append([r,np.mean(G[0,inds]),np.min(G[0,inds]),np.max(G[0,inds])])
rows=np.array(rows);ck('near-source Green function exceeds distant shell (sampled finite periodic graph)',rows[0,1]>rows[-1,1])
for j in [1,NB[0,1],2,20]:
    q1=P[:,0];q2=P[:,j];U=lambda q:.5*q@G@q
    ck('pair cross energy is signed Green interaction for opposite charges',near(U(q1+q2)-U(q1)-U(q2),G[0,j]) and near(U(q1-q2)-U(q1)-U(q2),-G[0,j]))
    ck('conditional positive-energy gravitational source has charge-even attractive kernel',near(-U(q1+q2)+U(q1)+U(q2),-G[0,j]))
np.savetxt(root/'matter_charge_green.csv',rows,delimiter=',',header='graph_distance,mean_G,min_G,max_G',comments='')
np.savetxt(root/'matter_charge_rotor.csv',np.c_[sol.t,qbare,qc,ee,nn],delimiter=',',header='t,bare_chamber_difference,total_dressed_charge,energy,norm',comments='')
fig,ax=plt.subplots(1,3,figsize=(13,4))
n=np.linspace(0,1.35,300);ax[0].plot(n,V(n));ax[0].scatter([0,nbar,nstar],V(np.array([0,nbar,nstar])),zorder=3);ax[0].set(xlabel='Excess occupation n',ylabel='Energy (model units)',title='Neutral and vortex wells');ax[0].annotate('barrier',(nbar,V(nbar)),xytext=(-14,18),textcoords='offset points');ax[0].annotate('vortex well',(nstar,V(nstar)),xytext=(-6,-25),textcoords='offset points')
ax[1].plot(sol.t,qbare,label='Bare chamber difference');ax[1].plot(sol.t,qc,'--',label='Total dressed charge');ax[1].set(xlabel='Model time',ylabel='Signed read',title='Exchange requires compensation');ax[1].legend(fontsize=8)
ax[2].plot(rows[:,0],rows[:,1],'.-',label='Like charge');ax[2].plot(rows[:,0],-rows[:,1],'.-',label='Opposite charge / gravity kernel');ax[2].set(xlabel='Diamond graph distance',ylabel='Pair cross energy',title='Conditional static interaction');ax[2].legend(fontsize=8);ax[2].axhline(0,color='.6',lw=.7)
for a in ax:a.grid(alpha=.2)
fig.tight_layout();fig.savefig(root/'figures/34_matter_charge.svg');fig.savefig(root/'figures/34_matter_charge.png',dpi=180);plt.close(fig)
print(f'{len(checks)}/{len(checks)} matter-charge checks passed.')
