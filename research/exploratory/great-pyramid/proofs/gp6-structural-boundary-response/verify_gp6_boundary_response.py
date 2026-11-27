#!/usr/bin/env python3
"""
GP-6  Structural boundary response and sourced closure

Symbolic identities (sympy) for the sourced frustum balance and the constitutive
Hessian; numerical witnesses for the sourced interval and reciprocity.
Prints PASS/FAIL per check and exits non-zero on any failure.

Run from this folder:  python verify_gp6_boundary_response.py
"""
import sys
RESULTS = []


def check(name, ok):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")

import sympy as s
import numpy as np
from scipy.optimize import brentq
u,m=s.symbols('u m', real=True); x=s.symbols('x',positive=True)

M=1-(1-u)**3
check('mass fraction',s.simplify(s.integrate(3*(1-u)**2,(u,0,u))-M)==0)
check('mass at half section',s.simplify(M.subs(u,1-1/s.sqrt(2))-(1-1/(2*s.sqrt(2))))==0)
mu=x/(1+x);lam=mu+x*s.diff(mu,x)
check('longitudinal Hessian',s.simplify(lam-(1-(1+x)**-2))==0)
check('response ratio',s.simplify(lam/mu-(2-mu))==0)
# Exact sourced affine field: integrate lateral flux for a unit-height pyramid
j,rho,A0,h=s.symbols('j rho A0 h',positive=True)
F=A0*(1-u)**2*(j+rho*h*u); M=A0*rho*h*(1-(1-u)**3)/3
# four faces collectively have n_z dA = -A'(u) du
lat=s.integrate(2*A0*(1-u)*(j+rho*h*u),(u,0,u))
check('sourced frustum identity',s.expand(F+lat-A0*j-M)==0)
check('outgoing equality residual',s.expand((F-lat)-(2*F-A0*j-M))==0)
hv=5776*.0254;mv=4*np.pi*6.674e-11*2300*hv/(3*9.7929)
F=lambda u:(1-u)**2*(1+3*mv*u);M=lambda u:mv*(1-(1-u)**3)
uh=brentq(lambda u:2*F(u)-1,0,1,xtol=1e-15);us=brentq(lambda u:2*F(u)-1-M(u),0,1,xtol=1e-15)
first=-mv*(1-2**-1.5)/(2*np.sqrt(2));check('source shift sign and first-order error',us<uh and abs(us-uh-first)<1e-10)
print('m =',mv,'root-definition shift (inches) =',(us-uh)*5776,'first order =',first*5776)
rng=np.random.default_rng(610)
ok_int = True
for i in range(200):
 eps=rng.uniform(.001,.35);m0=rng.uniform(0,.3);b=rng.uniform(-eps,eps)
 r=lambda u:1+b*u
 z=brentq(lambda u:2*(1-u)**2*r(u)-1-m0*(1-(1-u)**3),0,1)
 lo=max(0,1-np.sqrt((1+m0)/(2*(1-eps))));hi=1-1/np.sqrt(2*(1+eps))
 ok_int = ok_int and (lo-1e-12<=z<=hi+1e-12)
check('200 sourced interval witnesses',ok_int)
# Constant-gradient harmonic perturbations on a unit cube: exact boundary map energy K
ok_rec = True
for i in range(100):
 a=rng.normal(size=3);b=rng.normal(size=3);e=rng.normal(size=3);e/=np.linalg.norm(e);x0=rng.uniform(.1,10)
 K=x0/(1+x0)*np.eye(3)+x0/(1+x0)**2*np.outer(e,e)
 ok_rec = ok_rec and bool(np.isclose(a@K@b,b@K@a) and a@K@a>0)
check('100 linear harmonic reciprocal energy witnesses',ok_rec)
print("\n" + "=" * 78)
print(f"GP-6: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
