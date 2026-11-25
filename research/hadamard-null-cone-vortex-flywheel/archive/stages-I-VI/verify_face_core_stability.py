"""Complementary minima and simultaneous eight-ring currents in the Triforce model."""
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()):
    import verify_current_closure as c
p=c.p
import numpy as np
import sympy as s
from itertools import combinations
checks=[]
def ck(msg,ok):
    assert bool(ok),msg
    checks.append(msg);print(f'PASS {len(checks):03d} {msg}',flush=True)
def near(a,b):return np.allclose(a,b,rtol=1e-9,atol=1e-9)
a=s.symbols('a0:6',real=True);z=s.Matrix([a[i]+s.I*a[i+3] for i in range(3)])
m=[a[i]**2+a[i+3]**2 for i in range(3)];N=sum(m);q=sum(t*t for t in z);Q=s.expand(q*s.conjugate(q));beta=s.symbols('beta',real=True)
V4=sum((sum(int(v[i])*a[i] for i in range(3))**2+sum(int(v[i])*a[i+3] for i in range(3))**2)**2 for v in p.S)/8
F=2*sum((t-N/3)**2 for t in m)+(beta-1)*Q
ck('complementary quartic homogeneous identity',s.expand(F-(s.Rational(4,3)*N*N-V4+beta*Q))==0)
w=(-1+s.I*s.sqrt(3))/2;z0=s.Matrix([1,w,w**2])/s.sqrt(3);u=s.ones(3,1)/s.sqrt(3)
def re(x):return s.simplify(s.Matrix([s.re(t).expand(complex=True) for t in x]+[s.im(t).expand(complex=True) for t in x]))
T=s.Matrix.hstack(re(s.conjugate(z0)),re(u),re(s.I*s.conjugate(z0)),re(s.I*u));H=s.simplify(T.T*s.hessian(F,a).subs(dict(zip(a,re(z0))))*T)
B=s.Matrix([[8*(beta-1)+s.Rational(8,3),s.Rational(8,3)],[s.Rational(8,3),s.Rational(8,3)]])
ck('orthonormal tangent chart',s.simplify(T.T*T)==s.eye(4));ck('exact face Hessian',H==s.diag(B,s.diag(1,-1)*B*s.diag(1,-1)));ck('positive determinant for beta > 1',s.expand(B.det()-s.Rational(64,3)*(beta-1))==0)
def circ(n):
    n=np.array(n,float);n/=np.linalg.norm(n);e=np.eye(3)[np.argmin(abs(n))];u=e-n*(e@n);u/=np.linalg.norm(u);return (u+1j*np.cross(n,u))/np.sqrt(2)
for n in p.S:
    z=circ(n);ck('face-normal circular minimum',near(abs(z)**2,[1/3]*3) and near(z@z,0) and near(p.chi(z),n/np.sqrt(3)))
for n in p.V:
    z=circ(n);ck('axial circular minimum',near(z@z,0) and near(p.chi(z),n) and near(sum(np.real(z[i].conjugate()*z[j])**2 for i,j in combinations(range(3),2)),0))
C=np.array(c.C1,float);K=p.K;minring=1.;mincore=1.;maxerr=0.
for k in range(6):
    branch=p.T2B@p.tv[:,3*k:3*k+3];read=max(p.reads,key=lambda R:np.linalg.norm(R@branch));l,sv,rh=np.linalg.svd(read@branch);branch=branch@rh.T@l.T
    ca,cb=p.ks[k];ck(f'branch {k+1} both ring coefficients nonzero',min(abs(ca),abs(cb))>1e-8)
    for n in p.V:
        z=circ(n);psi=branch@z;j=p.ringcurr(psi);target=(p.S@n)*np.array([ca]*4+[cb]*4);flow=p.J(p.TH,psi);Jcore=C@np.array([flow[i,jj] for i,jj in p.tedges]);principal=K.T@Jcore/4
        ck('all eight physical ring currents simultaneous in one stationary state',near(j,target) and min(abs(j))>1e-8 and near(p.TH@psi,p.te[3*k]*psi))
        ck('registered core conserved and nonzero axial projection',near(p.L@Jcore,0) and np.linalg.norm(principal)>1e-8 and near(np.cross(principal,n),0))
        ck('ring aggregation gives common axial contribution',near(K.T@p.D@j/4,(ca+cb)*n))
        minring=min(minring,min(abs(j)));mincore=min(mincore,np.linalg.norm(principal));maxerr=max(maxerr,np.max(abs(j-target)))
        if k==0 and np.array_equal(n,[0,0,1]):print('Example +z, branch 1: face currents',j,'registered principal',principal)
print('Minimum |physical ring current|:',minring,'Minimum |registered principal coefficient|:',mincore,'Maximum ring error:',maxerr)
print(f'{len(checks)}/{len(checks)} new checks passed; {len(p.checks)+len(c.checks)} earlier checks rerun on import.')
