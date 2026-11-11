"""07. Where the GFD algebra (research/gfd_algebra.py) and BIMOND's algebra intersect.

A. Odds ratio Omega(x) = x  <=>  |grad phihat| * |grad phi| = a0 * |grad phi*|   (twin field x total field = a0 x Newtonian field)
B. Exchange mu(1/x) = 1 - mu(x)  <=>  the TetA and TetB shares of the BIMOND total field swap under x -> 1/x
C. Legendre duality: GFD's SST kinetic function F and BIMOND's M are exact Legendre duals
       F(x^2) + u^2 + M(u) = 2 x u ,   u = x^2/(1+x)      (AQUAL <-> QUMOND, in closed form)
D. Logistic identity x mu' = mu(1-mu) <=>  g* ghat / g^2  (product of the two shares)
E. Component count: BIMOND's C = Gamma - Gammahat (two Levi-Civita connections) has 4 x 10 = 40 components = GFD's retained 40.
   The tetrad (Weitzenboeck) difference of the two frames has 4^3 = 64 = 40 + 24; the 24 is the torsion difference.
F. Spin is invisible to metric BIMOND: two tetrads differing by a local rotation R(theta(x)) have the same metric, so C = 0,
   but their Weitzenboeck difference has axial torsion whose sign follows the sense of rotation (brake vs drive).
"""
import numpy as np, sympy as sp
P=F=0
def ok(m,c):
    global P,F
    print(("PASS " if c else "FAIL ")+m); P+=bool(c); F+=(not c)

mu=lambda x: x/(1+x)
x=np.logspace(-4,4,401)
g=x; gs=mu(x)*x; gh=(1-mu(x))*x          # units of a0: total, TetA (phi*), TetB (phihat)

# A
ok("A  Omega(x)=x  <=>  |grad phihat| |grad phi| = a0 |grad phi*|   (max rel err %.1e)"%np.max(abs(gh*g-gs)/gs), np.allclose(gh*g,gs,rtol=1e-12))
ok("A' equivalently |grad phi*| / |grad phihat| = |grad phi| / a0", np.allclose(gs/gh, g, rtol=1e-12))
# B
xi=1/x
ok("B  TetB share at 1/x = TetA share at x   (mu(1/x) = 1 - mu(x))", np.allclose((1-mu(xi)), mu(x)))
# C  Legendre duality
def Mclosed(u): return 0.5*np.sqrt(u)*(u+2)*np.sqrt(u+4)-u**2/2-4*np.arcsinh(np.sqrt(u)/2)
def Fgfd(y): return y-2*np.sqrt(y)+2*np.log1p(np.sqrt(y))
u=x**2/(1+x)
lhs=Fgfd(x**2)+u**2+Mclosed(u); rhs=2*x*u
ok("C  F(x^2) + u^2 + M(u) = 2 x u  for u = x^2/(1+x), x in [1e-4,1e4]  (max rel err %.1e)"%np.max(abs(lhs-rhs)/rhs), np.allclose(lhs,rhs,rtol=1e-8))
import mpmath as mp; mp.mp.dps=50
mpM=lambda u:mp.sqrt(u)*(u+2)*mp.sqrt(u+4)/2-u**2/2-4*mp.asinh(mp.sqrt(u)/2)
mpF=lambda y:y-2*mp.sqrt(y)+2*mp.log(1+mp.sqrt(y))
err=max(abs((mpF(xx**2)+(xx**2/(1+xx))**2+mpM(xx**2/(1+xx))-2*xx*xx**2/(1+xx))/(2*xx*xx**2/(1+xx))) for xx in map(mp.mpf,['1e-4','0.3','1','7','1e4']))
ok("C  same identity at 50 digits (max rel err %s): exact"%mp.nstr(err,3), err<mp.mpf('1e-35'))
# derivative check of the duality: d/dx of AQUAL density = g*, d/du of QUMOND density = g
X=sp.symbols('x',positive=True); U=X**2/(1+X)
A=(X**2-2*X+2*sp.log(1+X))/2               # (1/2)F(x^2) = int_0^x mu(s) s ds
ok("C' dA/dx = mu(x) x = g*/a0  (AQUAL side)", sp.simplify(sp.diff(A,X)-X**2/(1+X))==0)
# D
ok("D  x mu'(x) = mu(1-mu) = g* ghat / g^2", np.allclose(x/(1+x)**2, gs*gh/g**2))
# E
ok("E  symmetric connection difference: 4 x 10 = 40 = GFD retained; tetrad difference 4^3 = 64 = 40 + 24", 4*10==40 and 4**3==40+24)
# F  relative rotation of the two frames
t,X1,X2,X3,w,k=sp.symbols('t x y z omega k',real=True)
co=[t,X1,X2,X3]
def tetrad(th):
    R=sp.eye(4); R[1,1]=sp.cos(th); R[1,2]=-sp.sin(th); R[2,1]=sp.sin(th); R[2,2]=sp.cos(th); return R
eta=sp.diag(-1,1,1,1)
def weitz(E):                              # Gamma^l_{m n} = E_a^l d_m E^a_n
    Ei=E.inv()
    return [[[sp.simplify(sum(Ei[l,a]*sp.diff(E[a,n],co[m]) for a in range(4))) for n in range(4)] for m in range(4)] for l in range(4)]
def axial(E):
    G=weitz(E); g=E.T*eta*E; gi=g.inv()
    T=[[[G[l][n][m]-G[l][m][n] for n in range(4)] for m in range(4)] for l in range(4)]   # T^l_{mn}
    Tl=[[[sum(g[l,q]*T[q][m][n] for q in range(4)) for n in range(4)] for m in range(4)] for l in range(4)]
    return [sp.simplify(sum(sp.LeviCivita(mm,a,b,c)*Tl[a][b][c] for a in range(4) for b in range(4) for c in range(4))) for mm in range(4)]
for name,th in [("twist about z, theta = k z",k*X3),("spin in time, theta = omega t",w*t)]:
    E=tetrad(th); metric=sp.simplify(E.T*eta*E)
    a=axial(E); am=axial(tetrad(-th))
    same=sp.simplify(metric-eta)==sp.zeros(4,4)
    print("   %s: metric = eta? %s ; axial torsion (lower index) = %s ; reversed sense = %s"%(name,same,a,am))
    ok("F  %s: same metric (BIMOND C = 0) but nonzero axial torsion that flips sign with the rotation sense"%name,
       same and any(c!=0 for c in a) and all(sp.simplify(a[i]+am[i])==0 for i in range(4)))
E=sp.diag(1,-1,1,1)
ok("F' constant parity P (TetA -> TetB): Weitzenboeck difference = 0, like C = 0 and V(P) = 0 in 06",
   all(weitz(E)[l][m][n]==0 for l in range(4) for m in range(4) for n in range(4)))
print("checks: %d passed, %d failed"%(P,F))
