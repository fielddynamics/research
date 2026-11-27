#!/usr/bin/env python3
"""Clock trace, harmonic projection and nested clock capacitance. Conditional models only."""
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,ok,kind='exact'):
    assert bool(ok),name
    checks.append((kind,name)); print(f'PASS [{kind}] {name}')
def eq(name,a,b):check(name,s.simplify(a-b)==0)
r,R,a,b,K,a0=s.symbols('r R a b K a0',positive=True)
l=s.symbols('l',integer=True,nonnegative=True)
U,V=s.symbols('U V',real=True)
x,y,z=s.symbols('x y z',real=True)
# Mode radial equation and interior/exterior DtN (outward from each domain).
for name,f,sign in [('interior',(r/R)**l,1),('exterior',(R/r)**(l+1),-1)]:
    eq(name+' spherical harmonic radial equation',s.diff(r*r*s.diff(f,r),r)-l*(l+1)*f,0)
    eq(name+' unit boundary trace',f.subs(r,R),1)
    eq(name+' normal eigenvalue',sign*s.diff(f,r).subs(r,R),(l if sign==1 else l+1)/R)
# Smooth density gives nontrivial interior field with constant trace.
phi=U+K*(r*r-R*R)/(2*R**3)
eq('uniform sphere boundary clock',phi.subs(r,R),U)
eq('uniform sphere Poisson source',s.diff(r*r*s.diff(phi,r),r)/r**2,3*K/R**3)
eq('uniform sphere flux',4*s.pi*R**2*s.diff(phi,r).subs(r,R),4*s.pi*K)
eq('boundary-normal drive',s.diff(phi,r).subs(r,R),K/R**2)
eq('point-mass exterior clock has nonzero flux',4*s.pi*R**2*s.diff(-K/r,r).subs(r,R),4*s.pi*K)
# Annulus: inner/outer constant traces need not match.
f=U+(V-U)*(1/a-1/r)/(1/a-1/b)
eq('annulus inner trace',f.subs(r,a),U)
eq('annulus outer trace',f.subs(r,b),V)
eq('annulus harmonic equation',s.diff(r*r*s.diff(f,r),r),0)
eq('annulus conserved radial current',r*r*s.diff(f,r),a*b*(V-U)/(b-a))
eq('annulus energy',2*s.pi*(a*b*(V-U)/(b-a))**2*(1/a-1/b),2*s.pi*a*b*(V-U)**2/(b-a))
# Full AQUAL radial law and its primitive. sqrt form is positive root.
g=(K+s.sqrt(K*K+4*a0*K*r*r))/(2*r*r)
eq('AQUAL spherical conserved current',s.factor(r*r*g*g/(g+a0)),K)
F=(-K-s.sqrt(K*K+4*a0*K*r*r))/(2*r)+s.sqrt(a0*K)*s.asinh(2*r*s.sqrt(a0/K))
eq('AQUAL clock gap primitive',s.diff(F,r),g)
eq('deep-field coefficient',s.limit(r*g,r,s.oo),s.sqrt(a0*K))
eq('Newtonian short-radius coefficient',s.limit(r*r*g,r,0,dir='+'),K)
# Analytic projection of zero-trace residual on harmonic gradient.
H=2+x+x*y+z*z-x*x
w=(x*x+y*y+z*z-1)*(1+x+2*y*z)
q=s.Matrix([x,y,z]);grad=lambda f:s.Matrix([s.diff(f,t) for t in q]);lap=lambda f:sum(s.diff(f,t,2) for t in q)
eq('harmonic boundary lift',lap(H),0)
eq('integration-by-parts divergence identity',sum(s.diff(w*grad(H)[i],q[i]) for i in range(3)),grad(w).dot(grad(H)))
# Discrete Dirichlet-to-Neumann and projection, actual 3D grid.
for n in [4,6,9]:
    pts=list(np.ndindex(n,n,n)); ix={p:i for i,p in enumerate(pts)}
    edges=[]
    for p in pts:
        for d in range(3):
            if p[d]+1<n:
                q0=list(p);q0[d]+=1;edges.append((ix[p],ix[tuple(q0)]))
    m=len(edges);i,j=np.array(edges).T
    B=csr_matrix((np.r_[-np.ones(m),np.ones(m)],(np.r_[np.arange(m),np.arange(m)],np.r_[i,j])),shape=(m,n**3)); L=B.T@B
    bd=np.array([k for k,p in enumerate(pts) if any(t in (0,n-1) for t in p)]); ii=np.setdiff1d(np.arange(n**3),bd)
    Lii=L[ii][:,ii]; Lib=L[ii][:,bd];Lbi=L[bd][:,ii];Lbb=L[bd][:,bd]
    lift=-spsolve(Lii,Lib.toarray()); S=Lbb.toarray()+Lbi@lift
    check(f'grid {n}: DtN symmetric',np.max(np.abs(S-S.T))<1e-11,'numeric')
    check(f'grid {n}: DtN constants kernel',np.max(np.abs(S@np.ones(len(bd))))<1e-11,'numeric')
    ev=np.linalg.eigvalsh(S);check(f'grid {n}: DtN PSD, exactly one zero',ev[0]>-1e-10 and ev[1]>1e-8,'numeric')
    rng=np.random.default_rng(n)
    for rep in range(4):
        p=rng.normal(size=n**3);h=p.copy();h[ii]=lift@p[bd];w=p-h
        Bh=B@h; Bw=B@w
        check(f'grid {n} trial {rep}: harmonic lift residual',np.max(np.abs((L@h)[ii]))<1e-10,'numeric')
        check(f'grid {n} trial {rep}: orthogonal energy split',abs(Bh@Bw)<1e-9 and abs(np.dot(B@p,B@p)-Bh@Bh-Bw@Bw)<1e-9,'numeric')
        check(f'grid {n} trial {rep}: projected correction invisible to interior',np.max(np.abs((L@h)[ii]))<1e-10,'numeric')
        # nonlinear energy of lift, finite-difference directional test on zero-trace variations
        def correction(v):
            h2=v.copy();h2[ii]=lift@v[bd];t=np.abs(B@h2);return np.sum(t-np.log1p(t))
        check(f'grid {n} trial {rep}: nonlinear trace correction invariant under interior variation',abs(correction(p+w)-correction(p))<1e-10,'numeric')
    const=np.ones(n**3);const[ii]=rng.normal(size=len(ii));check(f'grid {n}: arbitrary internal field with constant trace has zero boundary correction',correction(const)<1e-20,'numeric')
# Nonlinear annular clock difference tests in units a0=1, K=1.
def newton(r,K=1):return K/r**2
def mond(r,K=1):return .5*(K/r**2+np.sqrt((K/r**2)**2+4*K/r**2))
def prim(r,K=1):return (-K-np.sqrt(K*K+4*K*r*r))/(2*r)+np.sqrt(K)*np.arcsinh(2*r/np.sqrt(K))
for K0 in [.01,1,100]:
    for a1,b1 in [(.1,1),(1,3),(1,30),(10,100)]:
        drop=prim(b1,K0)-prim(a1,K0);num=quad(lambda t:mond(t,K0),a1,b1,epsabs=1e-11)[0]
        check(f'annulus K={K0:g}, [{a1},{b1}]: exact primitive',np.isclose(drop,num,rtol=1e-10),'numeric')
        check(f'annulus K={K0:g}, [{a1},{b1}]: drained clock difference exceeds Newton',drop>K0*(1/a1-1/b1),'numeric')
# Same prescribed clock gap, different fluxes under alternative constitutive laws.
for gap in [.01,.1,1,10]:
    K_N=gap/(1-1/10)
    K_M=brentq(lambda kk:prim(10,kk)-prim(1,kk)-gap,1e-14,K_N,xtol=1e-16)
    check(f'fixed clock difference {gap}: both laws admissible with different source flux',0<K_M<K_N and abs(prim(10,K_M)-prim(1,K_M)-gap)<1e-10,'numeric')
    print(f'CLOCK GAP {gap:g}: Newton K={K_N:.9g}, drained K={K_M:.9g}')
# 16-address detail projection, constant input vs same trace arbitrary normal derivative.
P=s.eye(16)-s.ones(16)/16
check('16-address detail projector rank 15',P*P==P and P.rank()==15)
check('16-address uniform trace annihilated',P*s.ones(16,1)==s.zeros(16,1))
# Visual summary: sphere with fixed trace, nested contrast, and law comparison.
fig,ax=plt.subplots(1,3,figsize=(13.6,4.4),layout='constrained')
t=np.linspace(0,1,301)
for k in [.5,1,2]:ax[0].plot(t,k*(t*t-1)/2,label=f'K={k:g}')
ax[0].axhline(0,color='gray',ls='--',label='constant clock trace');ax[0].set(xlabel='r / R',ylabel='Clock potential (normalized)',title='Same boundary, different interiors');ax[0].legend(fontsize=8)
t=np.geomspace(1,10,300);ax[1].plot(t,(1-1/t)/.9,label='Harmonic lift (Newtonian)');ax[1].plot(t,(prim(t)-prim(1))/(prim(10)-prim(1)),label='Drained law, same end clocks');ax[1].set(xlabel='r / inner radius',ylabel='Normalized clock difference',title='Two registered clock surfaces');ax[1].legend(fontsize=8)
t=np.geomspace(.1,100,400);ax[2].loglog(t,newton(t),label='Newtonian');ax[2].loglog(t,mond(t),label='Fully open AQUAL');ax[2].set(xlabel='r / √(K/a₀)',ylabel='g / a₀',title='Same source flux, different clock slopes');ax[2].legend(fontsize=8)
for a1 in ax:a1.grid(alpha=.2)
fig.suptitle('Clock registration: boundary data, interior field and nested response');fig.savefig(ROOT/'figures/clock_registration.png',dpi=180);plt.close(fig)
print(f'{len(checks)} passed: {sum(k=="exact" for k,_ in checks)} exact + {sum(k=="numeric" for k,_ in checks)} numerical.')
