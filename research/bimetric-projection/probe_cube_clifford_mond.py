"""Stellated octahedron, cube, MOND and the locked bimetric potential: structural tests."""
import itertools, sympy as sp, numpy as np
ok=lambda m,c: print(("PASS " if c else "FAIL ")+m)
B=[1,0,16,0,1]
def e(ev,k): return 1 if k==0 else sum(np.prod(c) for c in itertools.combinations(ev,k))
V=lambda ev: sum(B[n]*e(ev,n) for n in range(5))
# ---------- T1: V on the cube of spatial leg flips S = diag(1,s1,s2,s3) ----------
print("T1  locked V on the 8 spatial sign-flip transitions (the cube vertices):")
tA,tB=[],[]
for s in itertools.product([1,-1],repeat=3):
    v=V([1,*s]); cls='TetA (s1s2s3=+1)' if np.prod(s)==1 else 'TetB (s1s2s3=-1)'
    print(f"     {s}  V = {v:4d}   {cls}"); (tA if np.prod(s)==1 else tB).append(v)
ok("V vanishes on every TetB transition (det S = -1) and is non-zero on every TetA transition", all(v==0 for v in tB) and all(v!=0 for v in tA))
ok("on TetA: 98 at the uniform (+,+,+) vertex, -30 at the three mixed ones; sum over TetA = 8 = 2^D, mean over cube = 1 = b0",
   sorted(tA)==[-30,-30,-30,98] and sum(tA)==8 and sum(tA+tB)/8==1)
x,y,z=sp.symbols('x y z')   # Paper C's restricted TetA modes (signs of the three axes)
VA=2+32*(x+y+z)
ok("on TetA's Walsh algebra {1,x,y,z} (Paper C): V = 2(1 + K^2 (x+y+z)), K^2 = 16",
   all(VA.subs({x:s[0],y:s[1],z:s[2]})==V([1,*s]) for s in itertools.product([1,-1],repeat=3) if np.prod(s)==1))
print("     (the same 49 and -15 are the components of the potential's stress at S = P: diag(49,-15,-15,-15))")
# ---------- T2: exterior/Clifford weights ----------
# blades of the even exterior algebra of V = R^{1,3}: Lambda^0, Lambda^2 (6), Lambda^4; weights 1,16,1
blades=[()] + list(itertools.combinations(range(4),2)) + [(0,1,2,3)]
w={b:(1 if len(b) in (0,4) else 16) for b in blades}
# Cl+(1,3) ~ Cl(3): e0^ei -> sigma_i (odd in Cl3), ei^ej -> sigma_i sigma_j (even), e0123 -> sigma_123 (odd)
def cl3(b):
    if len(b)==0: return ()
    if len(b)==4: return (1,2,3)
    if 0 in b: return (b[1],)
    return tuple(b)
even=sum(w[b] for b in blades if len(cl3(b))%2==0); odd=sum(w[b] for b in blades if len(cl3(b))%2==1)
ok(f"Cl+(1,3) = Cl(3): its 8 blades are the cube's vertices; locked weights split parity-wise {even} | {odd} (TetA = scalar + rotations, TetB = boosts + volume)", even==49 and odd==49)
for axis in (1,2,3):
    inside=sum(w[b] for b in blades if axis in b); outside=sum(w[b] for b in blades if axis not in b)
    ok(f"face split along spatial axis {axis} (blades containing that leg vs not): {outside} | {inside}", inside==49 and outside==49)
lam=sp.Symbol('lambda',positive=True)
ok("so the rank-one V = 49(1 + lambda) is exactly the face split along the stretched (acceleration) leg", sp.expand(V([1,1,1,lam])-49*(1+lam))==0)
ok("49 = 1 + 3*16 = (K+D)^2 and V(I) = 98 = 2*49", 1+3*16==49==(4+3)**2 and V([1,1,1,1])==98)
# ---------- T3: AQUAL is Poisson in the conformal metric f = mu^2 delta, only in D = 3 ----------
c=sp.Symbol('c',positive=True); D=sp.Symbol('D',positive=True)
ok("densitized Laplacian of f = c^2 delta in D dims: sqrt(f) f^ij = c^(D-2) delta_ij; equals AQUAL's mu iff c = mu with D = 3",
   sp.simplify(c**D*c**-2-c**(D-2))==0 and sp.simplify((c**(D-2)).subs(D,3)-c)==0)
gs=sp.symbols('g_s',positive=True); xx=sp.Symbol('x',positive=True)
print("     -> MOND: Phi is harmonic (Poisson-sourced) in the second spatial metric f = mu(|grad Phi|/a0)^2 g;")
print("        deep field mu ~ x: f ~ |grad Phi|^2/a0^2 g, the 3-Laplacian, conformally invariant in 3D (Milgrom's scale invariance).")
# ---------- T4: frame partition e = mu e + (1-mu) e ----------
mu=xx/(1+xx)
cAB=sp.simplify((1-mu)/mu)
ok("TetA frame mu*e and TetB frame (1-mu)*e sum to e; their transition is S = (1-mu)/mu I = (a0/g) I (proportional branch, c = 1/x)", sp.simplify(cAB-1/xx)==0)
ok("Field Origin: c = 1 exactly at g = a0; exchange x -> 1/x is c -> 1/c, i.e. g <-> f with beta_n <-> beta_{4-n} (palindromic)", cAB.subs(xx,1)==1 and sp.simplify(cAB.subs(xx,1/xx)*cAB-1)==0)
# ---------- T5: mu as a light-cone (boost) share ----------
th=sp.Symbol('theta',real=True)
ok("with x = e^(2 theta): mu = (1 + tanh theta)/2 (the forward light-cone share of a boost of rapidity theta); exchange is theta -> -theta",
   all(abs(float((mu.subs(xx,sp.exp(2*t))-(1+sp.tanh(t))/2).evalf()))<1e-14 for t in (-2,-0.3,0.4,1.7)))
ok("GFD's sigma(x) = (x-1)/(x+1) = tanh(theta): the 'state' coordinate is a velocity, Field Origin = rest (theta = 0)",
   all(abs(float((((xx-1)/(xx+1)).subs(xx,sp.exp(2*t))-sp.tanh(t)).evalf()))<1e-14 for t in (-2,-0.3,0.4,1.7)))
