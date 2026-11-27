#!/usr/bin/env python3
"""Conditional Hill/clock correspondence. Symbolic and numerical checks, not observational tests."""
import math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import brentq
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,ok,kind='exact'):
    assert bool(ok),name
    checks.append((kind,name));print(f'PASS [{kind}] {name}')

def eq(name,l,r):check(name,s.simplify(l-r)==0)

# Dimensionless Hill potential, lengths in r_J, energies GM/r_J.
x,y,z=s.symbols('X Y Z',real=True)
b=s.symbols('beta', nonnegative=True)
V=-1/s.sqrt(x*x+y*y+z*z)-x*x/2+b*z*z/2
q=s.Matrix([x,y,z]);grad=s.Matrix([s.diff(V,t) for t in q]);H=s.hessian(V,q)
for sign in [-1,1]:
    at={x:sign,y:0,z:0}
    check(f'stationary saddle {sign:+}',grad.subs(at)==s.zeros(3,1))
    eq(f'critical potential {sign:+}',V.subs(at),-s.Rational(3,2))
    check(f'saddle Hessian {sign:+}',H.subs(at)==s.diag(-3,1,1+b))
eq('tangential intercept',V.subs({x:0,y:s.Rational(2,3),z:0}),-s.Rational(3,2))
eq('vertical intercept beta=4',V.subs({x:0,y:0,z:s.Rational(1,2),b:4}),-s.Rational(3,2))
eq('trace of potential Hessian away from source',s.trace(H),b-1)
# At radial saddle, transverse expansion and neck flux.
d=s.symbols('delta',positive=True)
D,nu2=s.symbols('D nu2',positive=True)
# x fixed at saddle, transverse quadratic available area.
eq('two-axis neck area',s.pi*s.sqrt(2*d/D)*s.sqrt(2*d/(D+nu2)),2*s.pi*d/s.sqrt(D*(D+nu2)))
# Integrate unit-circle transverse configuration, available velocity disk.
r=s.symbols('rho',nonnegative=True)
I=s.integrate(2*s.pi*r*2*s.pi*d*(1-r*r),(r,0,1))*2*d/s.sqrt(D*(D+nu2))
eq('local microcanonical one-way flux',I,2*s.pi**2*d*d/s.sqrt(D*(D+nu2)))
# Host tidal Hessian radial derivative for an axisymmetric circular orbit.
Om2,k2=s.symbols('Omega2 kappa2', positive=True)
Hhost=s.diag(k2-3*Om2,Om2,nu2)
check('rotation contribution converts host Hessian to Hill', Hhost-s.diag(Om2,Om2,0)==s.diag(k2-4*Om2,0,nu2))
# Exact lapse distinction in ADM decomposition.
N,beta2,c=s.symbols('N beta2 c',positive=True)
eq('norm of stationary coordinate vector squared',-(-c*c*N*N+beta2)/c**2,N*N-beta2/c**2)
# Constant effective potential trace does not make its interior harmonic.
W=(x*x+y*y+z*z-1)/6
Harm=-s.Rational(3,2)+x*x/2-b*z*z/2-(1-b)*W
check('unit spherical torsion function Delta W=1',s.simplify(s.trace(s.hessian(W,q)))==1)
eq('harmonic continuation of quadratic boundary trace',s.trace(s.hessian(Harm,q)),0)
eq('clock deficit minus ownership residual is trace correction', (V+s.Rational(3,2)+(1-b)*W)-(-1/s.sqrt(x*x+y*y+z*z)-Harm),0)
# Sign of radial derivative on the interior and exterior sides of saddle.
R=s.symbols('R',positive=True)
vr=-1/R-R*R/2
eq('radial potential derivative factorization',s.diff(vr,R),(1-R**3)/R**2)

# Numerical geometry: inner root along each unit ray, tangent double root on radial axis.
def radius(nx,nz,beta):
    k=beta*nz*nz-nx*nx
    if abs(k+1)<1e-12:return 1.
    return brentq(lambda t:k*t**3+3*t-2,1e-10,1.,xtol=1e-14)
angles=np.linspace(0,2*np.pi,721)
for beta in [0,1,4,9]:
    for plane in ['xy','xz']:
        v=np.array([radius(np.cos(t),np.sin(t) if plane=='xz' else 0,beta) for t in angles])
        nx=np.cos(angles);nz=np.sin(angles) if plane=='xz' else np.zeros_like(angles)
        check(f'{plane} boundary beta={beta} satisfies critical level', np.max(np.abs(-1/v+0.5*(beta*nz**2-nx**2)*v**2+1.5))<1e-10,'numeric')
        check(f'{plane} inner branch beta={beta} enclosed by r_J',v.max()<=1+1e-12,'numeric')
# volume from angular radius integration, use Gauss-Legendre quadrature in cos polar angle
nodes,weights=np.polynomial.legendre.leggauss(80)
phis=(np.arange(240)+0.5)*2*np.pi/240
vol=0
for zz,ww in zip(nodes,weights):
    rr=np.array([radius(np.sqrt(1-zz*zz)*np.cos(p),zz,4.) for p in phis])
    vol+=ww*np.sum(rr**3)*(2*np.pi/len(phis))/3
req=(3*vol/(4*np.pi))**(1/3)
check('volume-equivalent radius beta=4 between 0.60 and 0.70 r_J',.60<req<.70,'numeric')
# Neck flux: integrate the transverse position disk analytically in velocity, numerically in radius.
for beta in [0.,4.,9.]:
    for eps in [1e-4,.01,.1]:
        val=quad(lambda u:2*np.pi*u*2*np.pi*eps*(1-u*u),0,1)[0]*2*eps/np.sqrt(1+beta)
        check(f'quadratic neck flux beta={beta}, excess={eps}',np.isclose(val,2*np.pi**2*eps**2/np.sqrt(1+beta),rtol=1e-12),'numeric')
# Numerical scale (illustrative parameters from repository)
GM=1.3271244e20;c0=299792458.;pc=3.085677581491367e16;au=149597870700.;year=31557600.;a0=1.225e-10
rj=1.44*pc;D0=GM/rj**3;V0=GM/rj;deficit=1.5*V0/c0**2
check('reference Jacobi radius reconstruction',np.isclose((GM/D0)**(1/3),rj,rtol=1e-12),'numeric')
check('clock deficit around 5e-14',4.9e-14<deficit<5.1e-14,'numeric')
check('radial tidal/solar acceleration at Earth below 4e-17',(au/rj)**3<4e-17,'numeric')
check('radial tidal/solar acceleration at Neptune below 1.1e-12',(30*au/rj)**3<1.1e-12,'numeric')
check('boundary not a horizon',deficit<1e-12,'numeric')
# Nonzero normal acceleration on closure away from saddles: at y=2/3 r_J.
py=9*GM/(4*rj*rj);mu=py/(a0+py)
check('tangential-side boundary gradient nonzero',py>0,'numeric')
check('fully open settlement q nonzero at nonsaddle boundary',a0*mu>0,'numeric')
# Total geometric potential flux with trace not generally zero. point source + uniform trace.
flux=4*np.pi*GM+(4-1)*D0*vol*rj**3
check('constant clock surface does not force zero potential flux',flux>4*np.pi*GM,'numeric')
print(f'NUMBERS rJ_pc={rj/pc:.6g}, rJ_AU={rj/au:.9g}, D={D0:.9g} s^-2, GM/rJ={V0:.9g} m^2/s^2')
print(f'critical clock deficit={deficit:.9g}; microseconds/year={deficit*year*1e6:.9g}; equivalent radius={req:.9g} rJ')
print(f'tangent-side p={py:.9g} m/s^2; full-open mu={mu:.9g}; gradient flux / GM={flux/GM:.9g}')
# Figure, dimensionless sections and saddle profile.
fig,axes=plt.subplots(1,3,figsize=(13,4.6),layout='constrained')
for ax,plane in zip(axes[:2],['xy','xz']):
    t=np.linspace(0,2*np.pi,721);nx=np.cos(t);ny=np.sin(t)
    rr=np.array([radius(a,bz if plane=='xz' else 0,4) for a,bz in zip(nx,ny)])
    ax.fill(rr*nx,rr*ny,alpha=.2);ax.plot(rr*nx,rr*ny,lw=2,label='critical clock surface');ax.scatter([-1,1],[0,0],marker='x',s=50,label='saddles')
    ax.scatter([0],[0],s=20,label='Sun');ax.set(xlabel='Galactic radial X / rJ',ylabel=('Along orbit Y' if plane=='xy' else 'Vertical Z')+' / rJ',title=plane.upper()+' section',xlim=(-1.15,1.15),ylim=(-1.05,1.05),aspect='equal');ax.grid(alpha=.2)
axes[0].legend(loc='upper center',fontsize=8)
r=np.linspace(.18,1.7,500);axes[2].plot(r,-1/r-r*r/2,label='corotating clock potential');axes[2].axhline(-1.5,ls='--',label='critical level');axes[2].axvline(1,ls=':',label='saddle');axes[2].set(xlabel='Radial distance / rJ',ylabel='Clock potential / (GM/rJ)',title='Radial clock-rate maximum',ylim=(-5,-1.1));axes[2].grid(alpha=.2);axes[2].legend(fontsize=8)
fig.suptitle('Solar closure: a critical co-rotating clock-rate surface (Hill model)')
fig.savefig(ROOT/'figures/clock_closure.png',dpi=180);plt.close(fig)
print(f'{len(checks)} passed: {sum(k=="exact" for k,_ in checks)} exact + {sum(k=="numeric" for k,_ in checks)} numerical.')
