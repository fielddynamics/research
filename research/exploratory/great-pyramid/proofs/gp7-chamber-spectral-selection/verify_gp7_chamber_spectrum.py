#!/usr/bin/env python3
"""
GP-7  Chamber spectral selection and symmetry

Exact integer degeneracy arithmetic, the complete rigid-wall spectrum below
120 Hz, parity characters, frequency sensitivity and interval bounds.
Prints PASS/FAIL per check and exits non-zero on any failure.

Run from this folder:  python verify_gp7_chamber_spectrum.py
"""
import sys
RESULTS = []


def check(name, ok):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")

from itertools import product
import numpy as np
from fractions import Fraction

q=lambda n:5*n[0]**2+20*n[1]**2+16*n[2]**2
pairs=[((2,2,1),(4,1,1)),((2,2,2),(4,1,2)),((3,1,3),(5,1,2))]
check('three integer degeneracies',all(q(a)==q(b) for a,b in pairs))
check('entire equal-height floor pair family (integer polynomial)',all(q((2,2,k))==q((4,1,k)) for k in range(100)))
groups={}
for n in product(range(12),repeat=3):groups.setdefault(q(n),[]).append(n)
check('modular necessities across enumerated degeneracies',all((a[0]-b[0])%2==0 and ((a[2]-b[2])%5==0 or (a[2]+b[2])%5==0) for g in groups.values() for a in g for b in g))
check('reflection characters separate stated pairs',all(tuple(i%2 for i in a)!=tuple(i%2 for i in b) for a,b in pairs))
d=np.array([412.24,206.12,230.09])*.0254;c=343
f=lambda n,d0=d:c/2*np.linalg.norm(np.array(n)/d0)
check('nominal floor degeneracies',all(abs(f(a)-f(b))<1e-12 for a,b in pairs[:2]))
split=abs(f(pairs[2][0])-f(pairs[2][1]));check('height-sensitive split',abs(split-.0632718907993)<1e-10);print('split',split,'Hz; beat period',1/split,'s')
limits=np.floor(2*d*120/c).astype(int)
ns=[n for n in product(*(range(k+1) for k in limits)) if any(n) and f(n)<=120]
check('complete illustrative 120 Hz band',len(ns)==89 and [sum(sum(v>0 for v in n)==k for n in ns) for k in (1,2,3)]==[14,43,32])
rng=np.random.default_rng(7)
ok_s = True
for n in ns:
 v=(np.array(n)/d)**2;weights=v/v.sum();direction=rng.normal(size=3);dt=1e-6
 pred=-weights@direction;meas=(np.log(f(n,d*np.exp(dt*direction)))-np.log(f(n,d*np.exp(-dt*direction))))/(2*dt)
 ok_s = ok_s and abs(pred-meas)<1e-8
check('89 frequency sensitivity checks',ok_s)
ok_b = True
for n in ns:
 delta=np.array([.12,.12,.15])*.0254;lo=f(n,d+delta);hi=f(n,d-delta)
 for _ in range(10):ok_b = ok_b and (lo-1e-10<=f(n,d+rng.uniform(-1,1,3)*delta)<=hi+1e-10)
check('890 bounded dimension samples',ok_b)
print("\n" + "=" * 78)
print(f"GP-7: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
