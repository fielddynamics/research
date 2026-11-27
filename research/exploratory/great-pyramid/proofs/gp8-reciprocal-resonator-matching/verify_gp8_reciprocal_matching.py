#!/usr/bin/env python3
"""
GP-8  Reciprocal resonator matching and the propagation baseline

Helmholtz Green function (sympy), reciprocity and the finite-aperture bound,
parity cancellation, resolvent Cauchy-Schwarz and the GP-5 peak transfer.
Prints PASS/FAIL per check and exits non-zero on any failure.

Run from this folder:  python verify_gp8_reciprocal_matching.py
"""
import sys
RESULTS = []


def check(name, ok):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")

import numpy as np
import sympy as s
from scipy.linalg import expm

r,k=s.symbols('r k',positive=True);G=s.exp(s.I*k*r)/(4*s.pi*r)
check('radial Helmholtz equation off origin',s.simplify(s.diff(G,r,2)+2*s.diff(G,r)/r+k*k*G)==0)
check('Green source normalization',s.simplify(s.limit(4*s.pi*r*r*s.diff(G,r),r,0,dir='+'))==-1)
rng=np.random.default_rng(8)
ok_ap = True
for j in range(200):
 X=rng.normal(size=(8,3));X*=.8/np.maximum(1,np.linalg.norm(X,axis=1))[:,None];Y=rng.normal(size=(7,3));Y*=.9/np.maximum(1,np.linalg.norm(Y,axis=1))[:,None];Y+=np.array([4,0,0]);qx=rng.normal(size=8);qy=rng.normal(size=7);dist=np.linalg.norm(X[:,None,:]-Y[None,:,:],axis=2);k0=rng.uniform(0,5)+1j*rng.uniform(0,1)
 K=np.exp(1j*k0*dist)/(4*np.pi*dist);a=qx@K@qy;b=qy@K.T@qx;bound=np.linalg.norm(qx,1)*np.linalg.norm(qy,1)*np.exp(-k0.imag*(4-.8-.9))/(4*np.pi*(4-.8-.9))
 ok_ap = ok_ap and abs(a-b)<1e-12 and abs(a)<=bound+1e-12
check('200 reciprocal discrete aperture bounds',ok_ap)
# parity cancellation under common reflection (point-quadrature witness)
X=np.array([[-1,0,0],[1,0,0]]);Y=np.array([[-1,4,0],[1,4,0]]);d=np.linalg.norm(X[:,None,:]-Y[None,:,:],axis=2);K=np.exp(2j*d)/(4*np.pi*d)
check('opposite parity cancels despite identical support shape',abs(np.array([1,1])@K@np.array([1,-1]))<1e-12)
ok_cs = True
for j in range(200):
 B=rng.normal(size=(5,5));A=np.linalg.inv(B.T@B+np.eye(5));a=rng.normal(size=5)+1j*rng.normal(size=5);b=rng.normal(size=5)+1j*rng.normal(size=5)
 ok_cs = ok_cs and abs(a.conj()@A@b)**2 <= ((a.conj()@A@a)*(b.conj()@A@b)).real+1e-10
check('200 positive resolvent overlap bounds',ok_cs)
ok_pk = True
for j in range(100):
 D=rng.uniform(-10,10);kap=rng.uniform(.1,5);H=np.array([[D/2,kap],[kap,-D/2]]);Om=np.sqrt(D*D+4*kap*kap);t=np.pi/Om;P=abs(expm(-1j*H*t)[1,0])**2
 ok_pk = ok_pk and abs(P-4*kap*kap/(D*D+4*kap*kap))<1e-12
check('100 exact GP-5 peak transfer comparisons',ok_pk)
print("\n" + "=" * 78)
print(f"GP-8: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
