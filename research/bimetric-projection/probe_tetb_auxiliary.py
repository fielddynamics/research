"""Two-sector form of the SST kinetic function with an auxiliary TetB field.
Claim:  a0^2 F(|g|^2/a0^2) = min_B [ |g - B|^2 - a0^2 F_u(-|B|/a0) ],  F_u(u) = u^2 - 2u + 2 ln(1+u)
(F_u is F written in u = sqrt(y)). The minimiser B is parallel to g with |B| = a0 g/(a0+g) = (1-mu) g:
the TetB share of the field, bounded by a0. g - B = mu g is the TetA (source) field."""
import sympy as sp, numpy as np, itertools
g,b,u=sp.symbols('g b u',positive=True)
ok=lambda m,cond: print(("PASS " if cond else "FAIL ")+m)
Fu=lambda w: w**2-2*w+2*sp.log(1+w)
E=(g-b)**2-Fu(-b)                                      # units a0 = 1, 0 <= b < 1
bstar=g/(1+g)
ok("stationarity dE/db = 0 at b* = g/(1+g), i.e. |B| = a0 g/(a0+g) = (1-mu) g, the TetB share of the field", sp.simplify(sp.diff(E,b).subs(b,bstar))==0)
ok("it is a minimum: d2E/db2 = 2 + 2b(2-b)/(1-b)^2 > 0", sp.simplify(sp.diff(E,b,2)-(2+2*b*(2-b)/(1-b)**2))==0)
ok("value: E(b*) = F_u(g) = g^2 - 2g + 2 ln(1+g)  (the SST kinetic function)", sp.simplify(E.subs(b,bstar)-Fu(g))==0)
ok("TetA field g - b* = g^2/(1+g) = mu(g) g, i.e. the spherical law g_s = g_t^2/(a0+g_t)", sp.simplify(g-bstar-g**2/(1+g))==0)
ok("TetB field saturates: b* -> 1 (= a0) as g -> oo and b* ~ g as g -> 0", sp.limit(bstar,g,sp.oo)==1 and sp.limit(bstar/g,g,0)==1)
P=sp.series(-b**2-Fu(-b)+b**2,b,0,7)  # -F_u(-b)
print("   TetB self-energy -F_u(-b) =",sp.series(-Fu(-b),b,0,7),"  (F_u(u) =",sp.series(Fu(u),u,0,7),")")
ok("parity relation: the TetB self-energy is F with its odd (linear) term reflected, u -> -b", sp.simplify(Fu(-b)-(b**2+2*b+2*sp.log(1-b)))==0)
# vector version: minimise |g - B|^2 - F_u(-|B|) over a 3-vector B
rng=np.random.default_rng(3); from scipy.optimize import minimize
Fn=lambda w: w**2-2*w+2*np.log1p(w)
good=True
for _ in range(20):
    gv=rng.normal(size=3)*rng.uniform(0.05,5); G=np.linalg.norm(gv)
    f=lambda B: np.sum((gv-B)**2)-Fn(-min(np.linalg.norm(B),0.999999))
    res=minimize(f,0.3*gv/G,method='Nelder-Mead',options=dict(xatol=1e-12,fatol=1e-14,maxiter=20000))
    Bs=res.x; good&= np.allclose(Bs,gv/(1+G),atol=1e-5) and abs(res.fun-Fn(G))<1e-8
ok("3D: the minimising TetB vector is B = g/(1+|g|) (parallel to g) and the minimum is F_u(|g|) (20 random g)", good)
# Einstein-Cartan: torsion is auxiliary -- the curvature scalar of Gamma = LC + K is R(LC) + divergence + K*K
x=sp.symbols('x0:4'); eta=sp.diag(-1,1,1,1)
Kf=[[[sp.Function(f'K{l}{m}{n}')(*x) for n in range(4)] for m in range(4)] for l in range(4)]
# flat LC: Gamma = K. R = eta^{ns}( d_m K^m_ns - d_n K^m_ms + K^m_ml K^l_ns - K^m_nl K^l_ms )
R=0
for n in range(4):
    sg=eta[n,n]
    for m in range(4):
        R+=sg*(sp.diff(Kf[m][n][n],x[m])-sp.diff(Kf[m][m][n],x[n]))
        for l in range(4): R+=sg*(Kf[m][m][l]*Kf[l][n][n]-Kf[m][n][l]*Kf[l][m][n])
Q=[sum(eta[n,n]*Kf[m][n][n] for n in range(4))-sum(eta[m,m]*Kf[l][l][m] for l in range(4)) for m in range(4)]
deriv_part=sp.expand(R-sum(sp.diff(Q[m],x[m]) for m in range(4)))
ok("Einstein-Cartan (flat LC): derivatives of torsion/contorsion enter R only as a total divergence -> auxiliary",
   not any(isinstance(a,sp.Derivative) for a in sp.preorder_traversal(deriv_part)))
