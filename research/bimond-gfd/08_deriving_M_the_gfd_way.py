"""08. Deriving BIMOND's function M the GFD way, by integration over the two tetrad shares.

Milgrom (0912.0790) calls M "an a priori unspecified function" to be fixed by phenomenology or by a deeper theory;
his papers give only its limits.  The GFD chain:
  Proof C : exchange symmetry + Moebius uniqueness  ->  mu(x) = x/(1+x)
  shares  : TetA field g* = mu g ,  TetB field ghat = (1-mu) g = a0 mu(x)     (x = g/a0, b = 1 - mu = TetB share)
  Proof B : F(x^2) = 2 int_0^x (g*/a0) d(g/a0)       = x^2 - 2x - 2 ln b        (AQUAL / SST side)
  new     : M(u)   = 2 int_0^u (ghat/a0) d(g*/a0)    = 2x - 1 + 2b - b^2 + 2 ln b  (BIMOND side)
So M is the work done by the TetB field along the TetA field, and F is the work done by TetA along the total field.
The TetB logarithm 2 ln(1+x) appears with opposite signs in F and M and cancels in the Legendre sum F + u^2 + M = 2xu.
"""
import sympy as sp
P=F_=0
def ok(m,c):
    global P,F_
    print(("PASS " if c else "FAIL ")+m); P+=bool(c); F_+=(not c)
x,s=sp.symbols('x s',positive=True)
mu=lambda t: t/(1+t)
b=1-mu(x)
gstar=mu(x)*x; ghat=(1-mu(x))*x                    # units of a0
ok("TetB field = a0 mu(x):  ghat/a0 = (1-mu) x = mu(x)", sp.simplify(ghat-mu(x))==0)
ok("total = TetA + TetB:  x = u + mu(x)", sp.simplify(x-(gstar+mu(x)))==0)
Fx=2*sp.integrate(mu(s)*s,(s,0,x))
ok("Proof B:  F = 2 int (g*/a0) dx = x^2 - 2x - 2 ln b", sp.simplify(Fx-(x**2-2*x-2*sp.log(b)))==0)
u=gstar; du=sp.diff(u,x)
Mx=sp.simplify(2*sp.integrate(sp.simplify(mu(s)*sp.diff(s**2/(1+s),s)),(s,0,x)))
target=2*x-1+2*b-b**2+2*sp.log(b)
ok("M = 2 int (ghat/a0) du = 2x - 1 + 2b - b^2 + 2 ln b", sp.simplify(Mx-target)==0)
# agrees with the closed form of 02 (written in u)
U=sp.symbols('U',positive=True)
Mclosed=sp.sqrt(U)*(U+2)*sp.sqrt(U+4)/2-U**2/2-4*sp.asinh(sp.sqrt(U)/2)
ok("agrees with 02's closed form in u (numerically at x = 0.01, 0.5, 1, 3, 100)",
   all(abs(sp.N(target.subs(x,xv)-Mclosed.subs(U,(xv**2/(1+xv))),30))<1e-25 for xv in map(sp.Rational,['1/100','1/2','1','3','100'])))
ok("M(0) = 0 and M'(z) = (dM/du)/(2u) = 1/x = a0/|grad phi| (the inverse odds ratio)",
   sp.simplify(target.subs(x,0))==0 and sp.simplify(sp.diff(target,x)/du/(2*u)-1/x)==0)
ok("log terms: F carries -2 ln b = +2 ln(1+x), M carries +2 ln b; they cancel in F + M", not sp.simplify(sp.expand_log(Fx+target,force=True)).has(sp.log))
ok("Legendre: F + u^2 + M = 2 x u (exact, symbolic)", sp.simplify(Fx+u**2+target-2*x*u)==0)
ok("dF/dx = 2u (TetA field) and d(u^2 + M)/du = 2x (total field)", sp.simplify(Fx.diff(x)-2*u)==0 and sp.simplify((u**2+target).diff(x)/du-2*x)==0)
print("checks: %d passed, %d failed"%(P,F_))
