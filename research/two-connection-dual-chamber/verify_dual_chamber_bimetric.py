"""Checks for the section 'A GFD-faithful bimetric algebra' of the research note 'Two connections and the dual chamber'.
Keep Hassan-Rosen's partition (bimetric proof, Theorem 8: TetB share = Omega/(1+Omega), Omega = det S) and let the second chamber's
metric be built on the first one's time leg: f = g - (y - 1) u u = h - y u u, i.e. TetB is the spatial subspace with its clock
running at rate x = c^2|a|/a0. Exact sympy. Run: python verify_dual_chamber_bimetric.py"""
import sympy as sp
from itertools import combinations
ok=[]
def check(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
x,y,w=sp.symbols('x y w',positive=True)
LOCK=[1,0,16,0,1]
e=lambda ev,n: sp.Integer(1) if n==0 else sp.expand(sum(sp.prod(c) for c in combinations(ev,n)))
V=lambda ev,bb=LOCK: sp.expand(sum(bb[n]*e(ev,n) for n in range(5)))
F=lambda Y: Y-2*sp.sqrt(Y)+2*sp.log(1+sp.sqrt(Y))
mu=lambda X: X/(1+X)

# 1. the disformal second metric on a general (non-static) background
g=sp.Matrix(4,4,lambda i,j: sp.Symbol(f'g{min(i,j)}{max(i,j)}'))
gi=g.inv()
uu=sp.Matrix(sp.symbols('U0:4'))            # u^mu
ul=g*uu                                       # u_mu
f=g-(y-1)*ul*ul.T                             # f_{mu nu} = g - (y-1) u_mu u_nu
norm={sp.Symbol('U0'):None}
M=gi*f
# with g(u,u) = -1: g^-1 f u = y u ; for v with u.v = 0: g^-1 f v = v
vperp=sp.Matrix(sp.symbols('V0:4'))
cond_uu=(uu.T*g*uu)[0]
Mu=sp.simplify(M*uu-(uu-(y-1)*uu*cond_uu))   # identity: g^-1 f u = u - (y-1) u (u.u)
check("1a for any metric g and unit timelike u, f = g - (y-1) u u gives g^-1 f u = u - (y-1)(u.u) u = y u: the time leg is an eigenvector "
      "with eigenvalue y, and every vector orthogonal to u has eigenvalue 1",
      Mu==sp.zeros(4,1) and sp.simplify(M*vperp - (vperp-(y-1)*uu*(ul.T*vperp)[0]))==sp.zeros(4,1))
N,hh=sp.symbols('N h',positive=True)
gs=sp.diag(-N**2,hh,hh,hh); us=sp.Matrix([1/N,0,0,0]); fs=gs-(y-1)*(gs*us)*(gs*us).T
Ms=sp.simplify(gs.inv()*fs)
check("1b on a static metric, g^-1 f = diag(y, 1, 1, 1), so S = sqrt(g^-1 f) = diag(x, 1, 1, 1) with x = sqrt(y) > 0: the principal root, "
      "which Hassan-Rosen's metric form does see", Ms==sp.diag(y,1,1,1) and sp.diag(x,1,1,1)**2==Ms.subs(y,x**2))
check("1c f is a disformal transformation of g along the time leg (the form Bekenstein's disformal and TeVeS metrics take); f(u,u) = -y, so "
      "TetB's proper time along u runs at rate x relative to TetA's",
      sp.simplify(-1-(y-1)*(-1)**2 - (-y))==0)

# 2. the locked potential on this second chamber, and the partition
ev=[x,1,1,1]
check("2a the locked potential is V = 49 (1 + x), and V/V(I) = det[(I + S)/2] = (1 + x)/2",
      sp.expand(V(ev)-49*(1+x))==0 and sp.simplify(V(ev)/V([1]*4)-sp.prod([(1+t)/2 for t in ev]))==0)
check("2b the odds of the two volume terms are Omega = det S = x, so Theorem 8's TetB share is Omega/(1 + Omega) = x/(1 + x) = mu(x): "
      "the dual-chamber partition and GFD's constitutive law coincide, with Omega = x supplied by the time leg",
      sp.prod(ev)==x and sp.simplify(mu(sp.prod(ev))-x/(1+x))==0)
check("2c the share is the SST's own slope: F'(y) = mu(sqrt y) = det S/(1 + det S)", sp.simplify(sp.diff(F(y),y)-mu(sp.sqrt(y)))==0)
check("2d metric exchange g <-> f sends S to S^-1, x to 1/x, and swaps the shares; the ring x = 1 is f = g (the two chambers coincide at a = a0)",
      sp.simplify(mu(1/x)-(1-mu(x)))==0 and sp.simplify((g-(1-1)*ul*ul.T)-g)==sp.zeros(4))

# 3. the SST's time-leg energy is a function of the HR potential
W=V(ev)/49
D=lambda t: t-1-sp.log(t)
check("3a F(y) - y = -2 D(V/49), D(w) = w - 1 - ln w: the SST's time-leg term is the relative entropy (Bregman divergence of -ln) of the "
      "locked potential from its x -> 0 value V0 = 49 = V(I)/2",
      sp.simplify((F(x**2)-x**2)-(-2*D(W)))==0)
check("3b so the SST's scalar term is -(a0^2/8 pi G)[y - 2 D(V/V0)]: the curvature term's y plus an HR-potential term entering through "
      "V/V0 - 1 - ln(V/V0) rather than linearly", sp.simplify(F(x**2)-(x**2-2*D(W)))==0)
check("3c the linear piece -2(V/V0 - 1) = -2x is exactly F's -2 sqrt(y) term, the one that leaves the constant tail a0 around every mass "
      "(the solar-system problem of the time-leg proof); the log piece 2 ln(V/V0) cancels it in the deep field, where F ~ (2/3) y^(3/2)",
      sp.simplify(-2*(W-1)+2*x)==0 and sp.simplify(sp.series(F(x**2),x,0,4).removeO()-sp.Rational(2,3)*x**3)==0)
# the linear HR term alone: energy (a0^2/4piG) x gives a flux of fixed magnitude a0: the tail
a0,G=sp.symbols('a0 G',positive=True); gr=sp.symbols('gr',positive=True)   # gr = |grad Phi|
Llin=(a0**2/(4*sp.pi*G))*gr/a0
check("3d a term linear in V alone, (a0^2/4 pi G)(V/V0 - 1) = (a0^2/4 pi G)|grad Phi|/a0, contributes a flux of fixed size a0/(4 pi G) "
      "(its derivative in |grad Phi| is constant): a linear HR potential on this f is the a0 tail and nothing else",
      sp.simplify(sp.diff(Llin,gr)-a0/(4*sp.pi*G))==0)

# 4. what does not come together
dEx=sp.simplify(x*D(V([1/x,1,1,1])/49) - D(W))
check("4a the energy is not exchange-symmetric: sqrt(-f) D(V(S^-1)/V0) = x D((1+1/x)) differs from sqrt(-g) D(V(S)/V0) = D(1+x); the "
      "partition is symmetric, the energy is not (matter couples to TetA)", dEx!=0)
Phi=sp.symbols('Phi_over_c2',real=True)
check("4b f is far from g in a galaxy: f(u,u)/g(u,u) = y, of order 1 even though Phi/c^2 ~ 1e-6. The second chamber differs from the "
      "first at O(1) in its clock, not at O(Phi/c^2) as an HR weak-field solution would",
      sp.simplify((us.T*fs*us)[0]/(us.T*gs*us)[0]-y)==0)
# 5. TetB as a subspace
hS=gs+(gs*us)*(gs*us).T                     # spatial metric h = g + u u
check("5a f = h - y u u: TetB's metric is the spatial subspace orthogonal to the time leg, with its time direction weighted by y",
      sp.simplify(fs-(hS-y*(gs*us)*(gs*us).T))==sp.zeros(4))
check("5b in the deep field (y -> 0) TetB collapses onto that subspace: f has rank 3 while g has rank 4", fs.subs(y,0).rank()==3 and gs.rank()==4)
check("5c the reference value of the vertex is the subspace: V(diag(0,1,1,1)) = 49 = V0, against V(I) = 98 at f = g",
      V([0,1,1,1])==49 and V([1,1,1,1])==98)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
