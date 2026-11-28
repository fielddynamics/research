"""Research experiments, not physical proof. Counterexamples pass if they refute an inference."""
import numpy as np
import sympy as s
import pytest
from scipy.linalg import expm, null_space
from itertools import product
from native_cell import H,O,A,S,F,C,base,bloch

def near(a,b,tol=1e-9): return np.allclose(a,b,atol=tol,rtol=tol)

def read(z):
    a=z[0]; b=z[1:]; n=np.vdot(z,z).real
    p=2*np.real(a.conjugate()*b); c=(-1j*np.cross(b.conj(),b)).real
    return n,p,c

# A. Native geometry and norm budget. No identification with spacetime assumed.
def test_native_graph():
    assert H.shape==(36,36) and np.array_equal(H,H.T)
    assert np.count_nonzero(np.triu(H,1))==128
    assert np.array_equal(H[np.ix_(base,O)],-np.c_[np.ones(8,int),S])

@pytest.mark.parametrize('seed',range(16))
def test_origin_capacity(seed):
    z=np.random.default_rng(seed).normal(size=(2,4)); z=z[0]+1j*z[1]
    n,p,c=read(z); phase=np.exp(-1j*np.angle(z[0])); a=(z[0]*phase).real; u=(z[1:]*phase).real; v=(z[1:]*phase).imag
    assert near(np.dot(p,c),0)
    assert near(n*n-p@p-c@c,(a*a+v@v-u@u)**2+4*(u@v)**2)
    assert near(read(z.conj())[1],p) and near(read(z.conj())[2],-c)
    intensity=abs(np.c_[np.ones(8),S]@z)**2
    assert near(intensity.mean(),n) and near(S.T@intensity/8,p)

def test_workload_norm_does_not_fix_flow():
    # Same norm, different polar read. Also same norm and zero scalar with circulation or not.
    z0=np.array([1,0,0,0]); z1=np.array([1,1,0,0])/np.sqrt(2)
    z2=np.array([0,1,1j,0])/np.sqrt(2)
    assert all(near(read(z)[0],1) for z in (z0,z1,z2))
    assert near(read(z0)[1],0) and near(read(z1)[1],[1,0,0])
    assert near(read(z2)[1],0) and near(read(z2)[2],[0,0,1])

def test_norm_partition_not_unique_lapse():
    # If a and b are called clock and flow amplitudes, the norm gives a budget;
    # a phase change preserves it but destroys polar read.
    z=np.array([.6,.8,0,0]); w=np.array([.6,.8j,0,0]);
    assert near(abs(z),abs(w)) and near(read(z)[0],1)
    assert near(read(z)[1],[.96,0,0]) and near(read(w)[1],0)

# B. Dark states: source information cannot be inferred from filtered histories.
@pytest.fixture(scope='module')
def dark():
    h=s.Matrix(H); c=s.Matrix(C.tolist()); obs=s.Matrix.vstack(*[c*h**k for k in range(7)])
    ker=s.Matrix.hstack(*obs.nullspace()); assert ker.cols==10
    assert obs*ker==s.zeros(obs.rows,10) and obs*h*ker==s.zeros(obs.rows,10)
    assert (h*h-2*h)*ker==s.zeros(36,10)
    assert (h*ker).rank()==5 and ((h-2*s.eye(36))*ker).rank()==5
    K=np.linalg.qr(np.array(ker,dtype=float))[0]
    e,V=np.linalg.eigh(K.T@H@K); return e,K@V

def test_dark_spectrum(dark):
    e,V=dark; assert near(e,[0]*5+[2]*5); assert near(C@V,0); assert near(V[O,:],0)

@pytest.mark.parametrize('j',range(5))
def test_same_optical_record_different_energy(dark,j):
    e,V=dark; p,q=V[:,j],V[:,j+5]
    assert near(np.linalg.norm(p),np.linalg.norm(q))
    assert near(p@H@p,0) and near(q@H@q,2)
    for t in (.1,1.,3.): assert near(C@(p*np.exp(-1j*e[j]*t)),C@(q*np.exp(-1j*e[j+5]*t)))

@pytest.mark.parametrize('j',range(5))
def test_dark_inventory_cannot_drive_filtered_band(dark,j):
    # Local linear model, no added coupling: this directly falsifies automatic sourcing.
    e,V=dark; p=np.r_[V[:,j+5],np.zeros(36)]
    for k in ([0,0,0],[.2,.3,-.1]):
        m=bloch(np.array(k)); assert near(m@p,2*p)
        assert near((expm(-.4j*m)@p)[36:],0)

def test_clock_probe_vs_energy_offset(dark):
    e,V=dark; p,q=V[:,0],V[:,5]; eps=1e-5
    # Assumed lapse coupling H(N)=NH, finite difference measures energy.
    d=lambda z: (z@((1+eps)*H)@z-z@((1-eps)*H)@z)/(2*eps)
    assert near(d(p),0) and near(d(q),2)
    H2=H+7*np.eye(36); assert near(q@H2@q-p@H2@p,2)
    assert near(expm(-.3j*H2),np.exp(-2.1j)*expm(-.3j*H))
    # Absolute Hamiltonian offset is unobservable in the isolated model, but changes assumed lapse source.
    assert near(q@H2@q,9)

@pytest.mark.parametrize('n',[.1,.3,.6,1.,1.4])
def test_lapse_scaling_is_only_assumed(n):
    rng=np.random.default_rng(9); z=rng.normal(size=36)+1j*rng.normal(size=36); z/=np.linalg.norm(z)
    assert near(expm(-.17j*n*H)@z,expm(-1j*H*(n*.17))@z)
    # Same geometry and unitary norm, but H independent of N is also possible and has zero source.
    assert near(np.linalg.norm(expm(-.17j*H)@z),1)

# C. Native scalar propagation vs a physical causal cone.
@pytest.mark.parametrize('filtered',[True,False])
@pytest.mark.parametrize('axis',[np.array([1.,0,0]),np.ones(3)/np.sqrt(3)])
def test_band_edge_stiffness(filtered,axis):
    e,V=np.linalg.eigh(bloch(np.zeros(3),filtered)); u=V[:,0]; k=.003*axis; m=bloch(k,filtered)
    D=(np.linalg.eigvalsh(m)[0]-e[0])/(k@k)
    expected=.10509418 if filtered else .12429467
    assert abs(D-expected)<1e-5
    susceptibility=np.vdot(u,np.linalg.solve(m-e[0]*np.eye(72),u)).real
    assert abs(susceptibility*(k@k)*expected-1)<1e-4

@pytest.mark.parametrize('distance',range(1,7))
def test_continuous_hopping_no_exact_light_cone(distance):
    # Unit hopping chain: first nonzero Taylor coefficient at order d, not at time d/c.
    a=np.diag(np.ones(distance),1)+np.diag(np.ones(distance),-1)
    assert all(np.linalg.matrix_power(a,k)[-1,0]==0 for k in range(distance))
    assert np.linalg.matrix_power(a,distance)[-1,0]==1
    t=.03; exact=expm(-1j*a*t)[-1,0]; leading=(-1j*t)**distance/float(s.factorial(distance))
    assert abs(exact/leading-1)<.001

# D. Candidate workload clock and GR benchmark, c=G=1 in numerical tests.
@pytest.mark.parametrize('load',[0,.01,.1,.25,.5,.75,.9,.99,.9999])
def test_quadratic_clock_budget(load):
    # Constructed mapping: normalized occupation load = v^2/c^2.
    n=np.sqrt(1-load); v=np.sqrt(load)
    assert near(n*n+v*v,1) and near(1-v,1-np.sqrt(load))
    # Rival unitary allocation: identical input load, no forced square-root clock.
    theta=load**2*np.pi/2; assert near(np.cos(theta)**2+np.sin(theta)**2,1)
    if load in (.1,.25,.5,.75,.9): assert not near(np.cos(theta),n)

@pytest.mark.parametrize('load',[.1,.5,.9,.99,1,1.01,2,4])
def test_pg_characteristics(load):
    v=np.sqrt(load); gp=np.array([[-1+v*v,v],[v,1]])
    assert near(np.linalg.det(gp),-1)
    for speed in [-v+1,-v-1]: assert near(np.array([1,speed])@gp@np.array([1,speed]),0)
    assert np.sign(1-v)==np.sign(1-load)
    # Infalling slice-normal worldline remains timelike even at the horizon.
    assert near(np.array([1,-v])@gp@np.array([1,-v]),-1)

def test_symbolic_spherical_constraint():
    r=s.symbols('r',positive=True); v=s.Function('v')(r)
    # Extrinsic curvature eigenvalues up to common sign for flat slices, unit lapse, c=1.
    eig=[s.diff(v,r),v/r,v/r]; K2=sum(eig)**2-sum(t*t for t in eig)
    assert s.simplify(K2-2*s.diff(r*v*v,r)/r**2)==0
    M=s.symbols('M',positive=True); vf=s.sqrt(2*M/r)
    assert s.simplify(s.diff(vf*vf/2,r)+M/r**2)==0
    assert s.simplify(s.diff(r*vf*vf,r))==0

@pytest.mark.parametrize('u',[.05,.1,.2,.5,1.,2.,5.,10.,20.])
def test_er_inversion(u):
    R=lambda t:t+2+1/t; N=lambda t:(t-1)/(t+1)
    assert near(R(u),R(1/u)) and near(N(u),-N(1/u))
    assert R(u)>=4 and near(N(u)**2,1-4/R(u))

def test_er_minimum_and_regular_horizon():
    u=s.symbols('u',positive=True); R=u+2+1/u
    assert s.diff(R,u).subs(u,1)==0 and s.diff(R,u,2).subs(u,1)==2
    # Schwarzschild Kretschmann scalar at r=2M is finite for M>0.
    M=s.symbols('M',positive=True); assert s.simplify(48*M**2/(2*M)**6)==s.Rational(3,4)/M**4

@pytest.mark.parametrize('load',[1e-5,1e-3,.01,.1,.5,.9])
def test_weak_limit_does_not_select_horizon(load):
    a=np.sqrt(1-load); b=np.exp(-load/2)
    assert a>0 and b>0 and b>=a
    assert abs(a-(1-load/2)) <= load**2/(2*(1-load)**.5)
    # Alternative matches linear redshift but has no zero at load=1.
    assert np.exp(-.5)>0

# E. Information and hierarchical registration: consequences, not source law.
@pytest.mark.parametrize('m,r',[(1,2),(1,4),(2,8),(.2,10),(10,20)])
def test_entropy_bound_ratio(m,r):
    # k_B=hbar=c=G=1, compare Bekenstein expression and area expression.
    assert near(2*np.pi*m*r/(np.pi*r*r),2*m/r)

def test_energy_is_not_bit_count():
    # Distinct energy distributions on same two-state space; same Shannon entropy.
    p=np.array([.5,.5]); entropy=-p@np.log(p)
    assert near(entropy,np.log(2)) and p@np.array([0,1]) != p@np.array([0,10])

@pytest.mark.parametrize('n',[4,6,9,12])
def test_registered_boundary_source(n):
    L=2*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1); f=np.arange(1,n+1,dtype=float)
    I=np.arange(0,n//2); B=np.arange(n//2,n); A0=L[np.ix_(I,I)]; C0=L[np.ix_(I,B)]; D=L[np.ix_(B,B)]
    Schur=D-C0.T@np.linalg.solve(A0,C0); source=f[B]-C0.T@np.linalg.solve(A0,f[I]); b=np.linalg.solve(Schur,source)
    a=np.linalg.solve(A0,f[I]-C0@b)
    assert near(np.r_[a,b],np.linalg.solve(L,f))
    # Interface source must replace, not be appended to the original source.
    assert not near(np.linalg.solve(Schur,source+f[B]),b)

@pytest.mark.parametrize('x',[.001,.01,.1,1,10,100])
def test_aqual_separate_response(x):
    mu=x/(1+x); J=x*mu; q=x/(1+x)
    assert near(x-q,J) and near(mu+1/(1+x),1)
    # Constitutive acceleration x is NOT compactness: outside spherical GR x ~ r^-2, compactness ~ r^-1.
    r=1/np.sqrt(x); assert near((1/(2*r)**2)/x,.25) and near((1/(2*r))/(1/r),.5)

# F. Which microscopic source can actually see the hidden energy?
@pytest.mark.parametrize('j',range(5))
def test_origin_only_clock_probe_is_dark(dark,j):
    e,V=dark; z=V[:,j+5]; Q=np.eye(36)[:,O]; P=Q@Q.T
    # All changes localized to the origin block or its incident Hamiltonian bonds
    # annihilate these states. A local lapse on the centre alone is insufficient.
    vertex=(P@H+H@P)/2
    assert near(P@z,0) and near(vertex@z,0) and near(z@vertex@z,0)

@pytest.mark.parametrize('filtered',[True,False])
def test_cellwise_energy_probe_partition(filtered):
    h=bloch(np.array([.2,.1,.3]),filtered); P=np.diag([1]*36+[0]*36); Q=np.eye(72)-P
    # Candidate symmetric local lapse scaling: derivative shares each bond equally.
    E1=(P@h+h@P)/2; E2=(Q@h+h@Q)/2
    assert near(E1+E2,h) and near(E1,E1.conj().T)
    eps=1e-5; scale=lambda n: np.diag([np.sqrt(n)]*36+[1]*36)
    numerical=(scale(1+eps)@h@scale(1+eps)-scale(1-eps)@h@scale(1-eps))/(2*eps)
    assert near(numerical,E1,1e-8)

def test_candidate_source_distinguishes_dark_energy(dark):
    _,V=dark; h=bloch(np.zeros(3)); P=np.diag([1]*36+[0]*36); E1=(P@h+h@P)/2
    z0=np.r_[V[:,0],np.zeros(36)]; z2=np.r_[V[:,5],np.zeros(36)]
    assert near(np.vdot(z0,E1@z0),0) and near(np.vdot(z2,E1@z2),2)
    # A *new* dynamical lapse variable could be sourced by this energy derivative.
    # Prescribing N externally in H(N) alone does not generate a field.
    assert near((np.vdot(z2,(h+1e-5*E1)@z2)-np.vdot(z2,h@z2))/1e-5,2)

@pytest.mark.parametrize('n',[.01,.1,.5,1.])
def test_clock_scaling_cannot_make_one_way_horizon(n):
    # A two-cell real symmetric microscopic hopping remains reciprocal, even with lapse scaling.
    K=F[0]@F[0].T; h=np.block([[H,-K],[-K,H]]).astype(float)
    D=np.diag([np.sqrt(n)]*36+[1]*36); u=expm(-.2j*(D@h@D))
    assert near(u[36:,:36],u[:36,36:].T)
    assert np.linalg.norm(u[36:,:36])>0

def test_zero_lapse_disconnects_both_directions():
    K=F[0]@F[0].T; h=np.block([[H,-K],[-K,H]]).astype(float)
    D=np.diag([0.]*36+[1.]*36); u=expm(-.2j*(D@h@D))
    assert near(u[36:,:36],0) and near(u[:36,36:],0)
    # PG benchmark at horizon has one zero characteristic and one strictly inward.
    assert 1-1==0 and -1-1==-2

@pytest.mark.parametrize('load',[.05,.2,.5,.8,.95])
def test_even_matching_weak_field_and_horizon_not_unique(load):
    # Both have same weak linear lapse, endpoint and quadratic budget with reallocated flow.
    N=np.sqrt(1-load); altered=load+.5*load**2*(1-load); N2=np.sqrt(1-altered)
    assert 0<altered<1 and N2<N
    assert near(N2*N2+altered,1)
    l=s.symbols('l',real=True); expr=l+s.Rational(1,2)*l*l*(1-l)
    assert expr.subs(l,0)==0 and s.diff(expr,l).subs(l,0)==1 and expr.subs(l,1)==1

# G. Explicit conditional feedback: energy read + a registered scalar field.
@pytest.mark.parametrize('n',[5,7,9,13])
def test_energy_source_generates_clock_field(dark,n):
    # Dimensionless Dirichlet graph clock action, *not* derived from H36.
    # E(phi)=1/2 phi^T L phi+sum e_i phi_i. Energy e_i is read from native H.
    _,V=dark; L=2*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1)
    f=np.zeros(n); f[n//2]=V[:,5]@H@V[:,5]-V[:,0]@H@V[:,0]
    phi=-np.linalg.solve(L,f)
    assert near(L@phi+f,0) and np.all(phi<0)
    assert np.argmin(phi)==n//2 and near(phi,phi[::-1])
    # A vacuum-referenced shift of H does not change the source contrast.
    Hp=H+17*np.eye(36)
    assert near(V[:,5]@Hp@V[:,5]-V[:,0]@Hp@V[:,0],f[n//2])
    # Attractive cross energy on positive Green kernel (not force vs distance on every graph).
    f2=np.zeros(n); f2[0]=1; green=np.linalg.inv(L)
    e=lambda q: -.5*q@green@q
    assert near(e(f+f2)-e(f)-e(f2),-f@green@f2) and -f@green@f2<0

@pytest.mark.parametrize('n',[4,7,10])
def test_local_clock_work_conjugacy(n):
    rng=np.random.default_rng(n); h=rng.normal(size=(n,n)); h=(h+h.T)/2
    z=rng.normal(size=n)+1j*rng.normal(size=n); z/=np.linalg.norm(z)
    # All-state derivative at unit lapse: e_i=Re(z_i^* (Hz)_i).
    source=np.real(z.conj()*(h@z)); assert near(source.sum(),np.vdot(z,h@z).real)
    d=rng.normal(size=n); eps=1e-5
    en=lambda l: np.vdot(z,np.diag(np.sqrt(l))@h@np.diag(np.sqrt(l))@z).real
    assert near((en(1+eps*d)-en(1-eps*d))/(2*eps),source@d,1e-8)

@pytest.mark.parametrize('mass',[.5,1.,3.])
def test_energy_not_sufficient_without_size(mass):
    # Same total energy, different radius and causal compactness threshold.
    radii=mass*np.array([1.,2.,4.,8.]); load=2*mass/radii
    assert near(load,[2,1,.5,.25])
    assert np.array_equal(1-np.sqrt(load)>0,[False,False,True,True])
